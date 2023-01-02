import ipaddress, nmap

from core.task import TaskInterface
from core.db import PostgresConnector
from core.logger import EventLogger
from core.decorator import monitor_task
from core.util.task_util import get_task_config

class MapActiveIpsTask(TaskInterface):

    def __init__(self) -> None:
        super().__init__()

    @monitor_task
    def run(self) -> None:
        EventLogger.log_info("Retrieving IP subnet masks from ASNs")
        with PostgresConnector() as db:
            data, total_hosts = self.get_ip_masks(db)

        if not data:
            EventLogger.log_error(f"No data found")
            return    
            
        EventLogger.log_info(f"Scanning {total_hosts} IPs from retrieved masks")
        for asn in data:
            self.check_asn_ips(asn)

    def get_ip_masks(self, db: PostgresConnector) -> list:
        hosts_limit = int(get_task_config(self.task_name, 'hosts_limit'))
        total_hosts = 0
        asn_list = []

        while total_hosts < hosts_limit:
            result = db.execute_select("select id, ip_range_start, ip_range_end from asn_data where country_code = 'BR' order by last_scan_date desc", fetch_one=True)

            if not result:
                break

            asn_data_id, ip_range_start, ip_range_end = result
            cidrs = [str(ipaddr) for ipaddr in ipaddress.summarize_address_range(ipaddress.IPv4Address(ip_range_start), ipaddress.IPv4Address(ip_range_end))]
            subnet_total_hosts = 0

            for subnet_mask in cidrs:
                mask = ipaddress.IPv4Network(subnet_mask)
                subnet_total_hosts += mask.num_addresses
                total_hosts += mask.num_addresses
            
            asn_list.append({
                "asn_data_id": asn_data_id,
                "ip_range_start": ip_range_start,
                "ip_range_end": ip_range_end,
                "total_hosts": subnet_total_hosts,
                "subnet_masks": cidrs
            })

        return asn_list, total_hosts

    def check_asn_ips(self, data: dict) -> None:
        arguments = '-sn'
        log_prefix = f"[asn_data_id={data['asn_data_id']}]"
        insert_query = "INSERT INTO ip (asn_data_id, hostname, ipv4, ipv6, state, create_date, last_update) VALUES (%s, %s, %s, %s, %s, now(), now())"

        EventLogger.log_info(f"{log_prefix} Scanning total of {data['total_hosts']} IPs ({data['ip_range_start']} - {data['ip_range_end']})")
        nm = nmap.PortScanner()

        for mask in data['subnet_masks']:
            mask_log_prefix = f"{log_prefix}[subnet_mask={mask}]"
            EventLogger.log_info(f"{mask_log_prefix} Starting NMAP scan with parameters: {arguments}")

            nm.scan(hosts=mask, arguments=arguments)
            scan_stats = nm.scanstats()
            EventLogger.log_info(f"{mask_log_prefix} Finished scan in {scan_stats['elapsed']} seconds. Total of {scan_stats['uphosts']}/{scan_stats['totalhosts']} found.")

            
            for host in nm.all_hosts():  
                host = nm[host]
                hostname = host.hostname()
                ipv4 = host['addresses']['ipv4'] if 'ipv4' in host['addresses'] else None
                ipv6 = host['addresses']['ipv6'] if 'ipv6' in host['addresses'] else None
                state = host.state()
                EventLogger.log_debug(f"{mask_log_prefix}[{ipv4=}][{hostname=}] Saving data into database")
                with PostgresConnector() as db:
                    db.execute_insert(insert_query, [data['asn_data_id'], hostname, ipv4, ipv6, state])

        with PostgresConnector() as db:
            db.execute_update("update asn_data set last_scan_date = now() where id = %s", [data['asn_data_id']])