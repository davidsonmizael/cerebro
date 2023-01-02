from abc import abstractmethod
from core.util.task_util import get_frequency
from threading import Thread

class TaskInterface(Thread):

    def __init__(self) -> None:
        super().__init__()
        self._task_name = type(self).__name__
        self._frequency = get_frequency(self._task_name)

    @property
    def task_name(self) -> str:
        return self._task_name

    @property
    def frequency(self) -> str:
        return self._frequency

    @abstractmethod
    def run(self): raise NotImplementedError