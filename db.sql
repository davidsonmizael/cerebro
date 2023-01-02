CREATE TABLE IF NOT EXISTS cerebro.asn_data (id INTEGER PRIMARY KEY, country_code TEXT, ip_range_start TEXT, ip_range_end TEXT, create_date TEXT, last_seen_date TEXT, last_scan_date TEXT);
CREATE TABLE IF NOT EXISTS cerebro.ip (id SERIAL PRIMARY KEY, asn_data_id INT, ipv4 TEXT, ipv6 TEXT, hostname TEXT, status TEXT);
CREATE TABLE IF NOT EXISTS cerebro.task (name TEXT PRIMARY KEY, frequency TEXT, last_run_date TEXT, status TEXT);
CREATE TABLE IF NOT EXISTS cerebro.task_run (id SERIAL PRIMARY KEY, task_name TEXT, start_date TEXT, end_date TEXT, status TEXT, additional_info TEXT);
CREATE TABLE IF NOT EXISTS cerebro.task_config (id SERIAL PRIMARY KEY, task_name TEXT, config_name TEXT, config_value TEXT);
CREATE TABLE IF NOT EXISTS cerebro.event (id SERIAL PRIMARY KEY, event_name TEXT, timestamp TEXT, message TEXT, type TEXT);