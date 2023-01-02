import requests, csv

from core.task import TaskInterface
from core.db import PostgresConnector
from core.logger import EventLogger
from core.decorator import monitor_task
from core.util.task_util import get_task_config

class UpdateASNTask(TaskInterface):

    def __init__(self) -> None:
        super().__init__()

    @monitor_task
    def run(self) -> None:
        EventLogger.log_info("Downloading ASN data from GITHUB")
        data = self.get_asn_data()
        
        EventLogger.log_info("Populating database")
        with PostgresConnector() as db:
            self.insert_data(db, data)

        EventLogger.log_info("Data update completed")

    def get_asn_data(self) -> csv.DictReader:
        url = get_task_config(self.task_name, 'data_url')
        EventLogger.log_debug("Running GET Request to url " + url)
        response = requests.get(url)
        csv_text = response.text
        return csv.DictReader(csv_text.split('\n'), fieldnames=['ip_range_start', 'ip_range_end', 'country_code'])

    def insert_data(self, db: PostgresConnector, data: csv.DictReader) -> None:
        select_query = "SELECT id FROM asn_data WHERE country_code = %s AND ip_range_start = %s AND ip_range_end = %s"
        insert_query = "INSERT INTO asn_data(ip_range_start, ip_range_end, country_code, create_date, last_seen_date) VALUES (%s, %s, %s, now(), now());"
        update_query = "UPDATE asn_data SET last_seen_date = now() WHERE id = %s"
        
        rows = list(data)
        total_rows = len(rows)

        for i, row in enumerate(rows, start=1):
            select_params = [row['country_code'], row['ip_range_start'], row['ip_range_end']]

            result = db.execute_select(select_query, select_params)
            if result:
                existing_id = result[0]
                EventLogger.log_debug(f"[{i}/{total_rows}] Updating row: {row['country_code']}: {row['ip_range_start']} - {row['ip_range_end']}")
                db.execute_update(update_query, [existing_id])
            
            else:
                EventLogger.log_debug(f"[{i}/{total_rows}] Inserting row: {row['country_code']}: {row['ip_range_start']} - {row['ip_range_end']}")
                params = [row['ip_range_start'], row['ip_range_end'], row['country_code']]
                db.execute_insert(insert_query, params)
