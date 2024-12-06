from abc import ABC, abstractmethod
from typing import Any, Callable


class BaseQueue(ABC):
  @abstractmethod
  async def add(self, name: str, data: Any):
    pass

  @abstractmethod
  def run(self, callback: Callable | None = None):
    pass
