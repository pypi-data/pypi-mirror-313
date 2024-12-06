import asyncio
import base64
import pickle
from typing import Any, Callable

import pydash

from ..constants.queue_constant import QUEUE_CONCURRENCY, QUEUE_MAX_ATTEMP
from ..loggers.logger import logger
from ..tasks.storage import list_tasks
from ..type_dicts.queue_option_type import QueueOption
from ..type_dicts.task_type import Task
from .base_queue import BaseQueue


class Queue(BaseQueue):
  running_tasks = set()

  def __init__(self, queue_name: str, redis: Any, options: QueueOption):
    self.redis = redis
    self.queue_name = f'{queue_name}_queue'
    self.concurrency = options.get('concurrency') or QUEUE_CONCURRENCY
    self.max_attempt = options.get('max_attempt') or QUEUE_MAX_ATTEMP

  def __find_task_handler(self, name: str):
    task = pydash.find(list_tasks, lambda t: t['name'] == name)
    if task:
      return task

    logger.info(f'Dont have any handler for task: {task}')

  async def __add_retry_process_task(self, task_data: Task):
    if task_data['attempt'] >= self.max_attempt:
      logger.error(f"Max attempt: {task_data['attempt']}, please recheck the code")
      await self.__add_to_list(f'failed_{self.queue_name}', base64.b64encode(pickle.dumps(task_data)))
    else:
      task_data['attempt'] += 1
      await self.__add_queue(task_data)

  async def __add_queue(self, options):
    await self.__add_to_list(self.queue_name, base64.b64encode(pickle.dumps(options)))

  async def __process_task(self, task, callback: Callable | None = None):
    logger.info('Start processing task')

    task_data: Task = pickle.loads(base64.b64decode(task))

    if callback:
      callback(task_data)

    if task_data['attempt']:
      logger.warning(f"Attempt to processing task: {task_data['attempt']}")
    task_handler = self.__find_task_handler(task_data['name'])

    if not task_handler:
      logger.error('Empty task handler')
      return

    logger.info(f"Run processing task: {task_data['name']}")
    try:
      await task_handler['handler'](task_data['data'])
    except Exception:
      await self.__add_retry_process_task(task_data)

    logger.info(f"End queue: {task_data['name']}")

  async def __add_to_list(self, key: str, value: Any):
    print('Add to list')
    return await self.redis.lpush(key, value)

  async def add(self, name: str, data: Any):
    await self.__add_to_list(
      self.queue_name,
      base64.b64encode(pickle.dumps({'name': name, 'data': data, 'attempt': 0})),
    )

  async def __get_task(self, callback: Callable | None = None):
    if len(self.running_tasks) < self.concurrency:
      task = await self.redis.rpop(self.queue_name)
      if task:
        task = asyncio.create_task(self.__process_task(task, callback))
        self.running_tasks.add(task)
        task.add_done_callback(lambda t: self.running_tasks.discard(t))

    await asyncio.sleep(2)
    asyncio.create_task(self.__get_task(callback))

  def run(self, callback: Callable | None = None):
    asyncio.create_task(self.__get_task(callback))
