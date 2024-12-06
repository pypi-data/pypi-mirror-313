# FastAPI queue tasks

## Introduction

FastAPI Queue helps you add tasks to a queue and run them in parallel, supporting both **asynchronous** and **synchronous** task handlers.

## How to use

### 1. Instantiate the Queue

First, create an instance of the Queue class by providing a Redis instance and configuration options like concurrency and max retry attempts:

```python
# config/queue.py

from fastapi_queue_task import Queue
from redis.asyncio.utils import from_url

queue = Queue('main', redis, {'concurrency': QUEUE_MAX_CONCURRENCY, 'max_attempt': QUEUE_MAX_ATTEMP})

def queue_processing(task: Task):
  print('TASK_DETAIL')
  print('task name', task.get('name'))
  print('task data', task.get('data'))
  print('task attempt', task.get('attempt'))


def init_queue():
  if env.IS_ALLOW_RUN_QUEUE:
    queue.run(queue_processing)

```

```python
# bootstrap/app.py

@asynccontextmanager
async def lifespan(app: FastAPI):
  init_queue()
  yield

app = FastAPI(title='API', lifespan=lifespan)
```

### 2. Add task to queue:

You can add a task to the queue by calling the add_to_queue method, passing the task name and the data to be processed:

```python
# mail_service.py
from config import queue

await queue.add(name="TASK_NAME", data: Any = {})

async def track(channel_id: UUID, dto: TrackHotspotMediaViewDto):
    return await queue.add(
      TrackViewTaskEnum.POST,
      {
        'post_id': dto.post_id
      },
    )
```

### 3. Define a Task Handler

Define the task handler using the @task decorator. The handler will process the task asynchronously or synchronously based on its definition:

```python
# tasks/track_view.py

from fastapi_queue_task import BaseTask, task

@task(TrackViewTaskEnum.POST)
class TrackViewPostTask(BaseTask):
  def __init__(self, track_post_view_service: TrackPostViewService = Depends()):
    self.track_post_view_service = track_post_view_service

  async def handler(self, data: TrackPostViewDataType):
    await self.track_post_view_service.handle_tracking(data)
```

In this example, the task TrackViewPostTask is added to the queue, and the handler method will process the task asynchronously.
