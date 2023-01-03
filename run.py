from core.task import *
from core.logger import EventLogger
from core.controller import TaskController

from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    EventLogger.log_info("Starting cerebro")
    task_controller = TaskController()
    task_controller.start()