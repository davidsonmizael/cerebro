import requests, csv

from core.task_interface import TaskInterface
from core.sqlite_database import SQLiteDatabase
from core.event_logger import EventLogger
from core.decorators import monitor_task, get_task_config

class UpdateASNTask(TaskInterface):

    def __init__(self) -> None:
        super().__init__()

    @monitor_task
    def run(self) -> None:
        EventLogger.log_info("Downloading ASN data from GITHUB")
        data = self.get_asn_data()
        
        EventLogger.log_info("Populating database")
        with SQLiteDatabase() as db:
            self.insert_data(db, data)

        EventLogger.log_info("Data update completed")

    def get_asn_data(self) -> csv.DictReader:
        url = get_task_config(self.task_name, 'data_url')
        EventLogger.log_debug("Running GET Request to url " + url)
        response = requests.get(url)
        csv_text = response.text
        return csv.DictReader(csv_text.split('\n'), fieldnames=['ip_range_start', 'ip_range_end', 'country_code'])

    def insert_data(self, db: SQLiteDatabase, data: csv.DictReader) -> None:
        select_query = "SELECT id FROM asn_data WHERE country_code = ? AND ip_range_start = ? AND ip_range_end = ?"
        insert_query = "INSERT INTO asn_data(ip_range_start, ip_range_end, country_code, create_date, last_seen_date) VALUES (?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'));"
        update_query = "UPDATE asn_data SET last_seen_date = datetime('now', 'localtime') WHERE id = ?"
        
        for row in data:
            select_params = [row['country_code'], row['ip_range_start'], row['ip_range_end']]
            result = db.execute_fetchone(select_query, select_params)
            if result:
                existing_id = result[0]
                EventLogger.log_debug("Updating row: %s: %s - %s" % (row['country_code'], row['ip_range_start'], row['ip_range_end']))
                db.execute(update_query, [existing_id])
            
            else:
                EventLogger.log_debug("Inserting row: %s: %s - %s" % (row['country_code'], row['ip_range_start'], row['ip_range_end']))
                params = [row['ip_range_start'], row['ip_range_end'], row['country_code']]
                db.execute(insert_query, params)
