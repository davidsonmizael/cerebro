from util.event_logger_util import *
import logging

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    handlers=[
        logging.FileHandler('logs/events.log'),
        logging.StreamHandler()
    ])

class EventLogger:

    @staticmethod
    def log_info(msg) -> None:
        timestamp, log_type, event_name = get_current_time(), get_log_type(), get_caller_class_name()
        logging.info("[%s] - %s" % (event_name, msg))
        save_event_in_db(event_name, timestamp, msg, log_type)

    @staticmethod
    def log_error(msg, stack) -> None:
        timestamp, log_type, event_name = get_current_time(), get_log_type(), get_caller_class_name()
        logging.error("[%s] - %s \nStackTrace: %s" % (event_name, msg, stack))
        save_event_in_db(event_name, timestamp, f"{msg}\n StackTrace: {stack}", log_type)

    @staticmethod
    def log_debug(msg) -> None:
        timestamp, log_type, event_name = get_current_time(), get_log_type(), get_caller_class_name()
        logging.debug("[%s] - %s" % (event_name, msg))
        save_event_in_db(event_name, timestamp, msg, log_type)

    @staticmethod
    def log_warn(msg) -> None:
        timestamp, log_type, event_name = get_current_time(), get_log_type(), get_caller_class_name()
        logging.warn("[%s] - %s" % (event_name, msg))
        save_event_in_db(event_name, timestamp, msg, log_type)