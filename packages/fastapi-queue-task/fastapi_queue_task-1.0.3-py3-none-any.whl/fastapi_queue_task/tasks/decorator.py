from typing import Callable, Type, TypeVar

from ..tasks.storage import list_tasks

T = TypeVar('T')


def task(name: str, **options) -> Callable[[Type[T]], Type[T]]:
  def decorator(cls: Type[T]) -> Type[T]:
    setattr(cls, '_task_name', name)
    if not hasattr(options, 'ignore_result'):
      options['ignore_result'] = True
    options['name'] = name

    async def task_handler(data):
      instance = cls()
      await instance.run(data)

    list_tasks.append({'name': name, 'handler': task_handler})

    return cls

  return decorator
