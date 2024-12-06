import inspect
from abc import abstractmethod
from contextlib import AsyncExitStack
from typing import Any, Callable

from fastapi import Request
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_dependant, solve_dependencies
from pydantic import ValidationError

from ..loggers.logger import logger


class BaseTask:
  _task_name: str

  @abstractmethod
  def handler(self, data: Any) -> Any | None:
    pass

  async def solve_depends(self, request: Request, dependant: Dependant, stack: AsyncExitStack):
    values, errors, _1, _2, _3 = await solve_dependencies(request=request, dependant=dependant, async_exit_stack=stack)
    if errors:
      raise ValidationError(errors, None)
    if inspect.iscoroutinefunction(dependant.call):
      result = await dependant.call(**values)
    else:
      result = dependant.call(**values)

    return result

  async def init_task(self, handler: Callable, data: Any):
    error = None
    async with AsyncExitStack() as stack:
      request = Request(
        {
          'type': 'http',
          'headers': [],
          'query_string': '',
          'fastapi_astack': stack,
        }
      )

      dependant = get_dependant(path=f'task:{self._task_name}', call=handler)

      await self.solve_depends(request, dependant, stack)

      try:
        if inspect.iscoroutinefunction(self.handler):
          await self.handler(data)
        else:
          self.handler(data)
      except Exception as exception:
        error = exception
        logger.error(f'{self.__class__.__name__} exception: {str(exception)}')
        raise

    if error:
      raise error

  async def run(self, data):
    try:
      await self.init_task(self.__init__, data)
    except Exception:
      raise
