from typing import Optional, TypedDict


class QueueOption(TypedDict):
  max_attempt: Optional[int]
  concurrency: Optional[int]
