from typing import Any, TypedDict


class Task(TypedDict):
  name: str
  data: Any
  attempt: int
