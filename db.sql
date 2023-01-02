CREATE TABLE IF NOT EXISTS cerebro.asn_data (id SERIAL PRIMARY KEY, country_code TEXT, ip_range_start TEXT, ip_range_end TEXT, create_date timestamp, last_seen_date timestamp, last_scan_date timestamp);
CREATE TABLE IF NOT EXISTS cerebro.ip (id SERIAL PRIMARY KEY, asn_data_id INT, ipv4 TEXT, ipv6 TEXT, hostname TEXT, status TEXT);
CREATE TABLE IF NOT EXISTS cerebro.task (name TEXT PRIMARY KEY, frequency TEXT, last_run_date timestamp, status TEXT);
CREATE TABLE IF NOT EXISTS cerebro.task_run (id SERIAL PRIMARY KEY, task_name TEXT, start_date timestamp, end_date timestamp, status TEXT, additional_info TEXT);
CREATE TABLE IF NOT EXISTS cerebro.task_config (id SERIAL PRIMARY KEY, task_name TEXT, config_name TEXT, config_value TEXT);
CREATE TABLE IF NOT EXISTS cerebro.event (id SERIAL PRIMARY KEY, event_name TEXT, timestamp timestamp, message TEXT, type TEXT);
ALTER TABLE cerebro.ip ADD CONSTRAINT ip_fk FOREIGN KEY (asn_data_id) REFERENCES cerebro.asn_data(id);

INSERT INTO cerebro.task ("name",frequency,last_run_date,status) VALUES
	 ('UpdateASNTask','0 0 * * *','2023-01-02 05:16:31','RUNNING'),
	 ('MapActiveIpsTask','0 * * * *','2023-01-02 05:16:30','RUNNING');
     
INSERT INTO cerebro.task_config (task_name,config_name,config_value) VALUES
	 ('MapActiveIpsTask','hosts_limit','10000'),
	 ('UpdateASNTask','data_url','https://raw.githubusercontent.com/sapics/ip-location-db/master/geo-whois-asn-country/geo-whois-asn-country-ipv4.csv');
