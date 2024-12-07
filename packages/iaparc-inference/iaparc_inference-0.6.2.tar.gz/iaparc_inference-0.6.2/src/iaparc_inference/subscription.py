from __future__ import annotations

from ast import Subscript
import asyncio
from typing import (
    TYPE_CHECKING,
    AsyncIterator,
    Awaitable,
    Callable,
    List,
    Optional,
)
from uuid import uuid4

from nats.errors import TimeoutError, ConnectionClosedError
from nats.aio.msg import Msg
from nats.aio.subscription import Subscription

class BatchSubscription:

    def __init__(self, sub: Subscription, batch_size: int):
        self._sub = sub
        self._batch_size = batch_size
        self._dones = {}
        self._pending_tasks = {}
    
    async def get_batch(self, timeout: Optional[float] = 0.005) -> List[Msg]:
        msgs: List[Msg] = []
        task_name = str(uuid4())
        if timeout is None:
            timeout = 0.005
        self._dones[task_name] = False
        try:
            msg = await self._sub.next_msg(timeout=600)
            msgs.append(msg)
            future = asyncio.create_task(
                asyncio.wait_for(self._wait_for_next_batch(task_name, timeout), timeout)
            )
            self._pending_tasks[task_name] = future
            await future
        except asyncio.TimeoutError:
            if self._sub._conn.is_closed:
                raise ConnectionClosedError
            self._dones[task_name] = True
            raise TimeoutError
        except asyncio.CancelledError:
            if self._sub._conn.is_closed:
                raise ConnectionClosedError
            self._dones[task_name] = True
            raise
        else:
            msgs.extend(self._pending_tasks[task_name])
            return msgs
        finally:
            self._pending_tasks.pop(task_name, None)
            self._dones.pop(task_name, None)
        
        return msgs
    
    async def _wait_for_next_batch(self, task_name: str, timeout: float = 0.005) :
        self._pending_tasks[task_name] = []
        limit = self._batch_size - 1
        wait_time = timeout / 5
        if wait_time < 0.005:
            wait_time = 0.001
        while not self._dones[task_name]:
            try:
                #msg = await self._sub._pending_queue.get()
                msg = await self._sub.next_msg(timeout=wait_time)
                self._sub._pending_size -= len(msg.data)
                #self._sub._pending_queue.task_done()
                self._pending_tasks[task_name].append(msg)
                if len(self._pending_tasks[task_name]) >= limit:
                    break
            except asyncio.CancelledError:
                break
            except TimeoutError:
                break
            except Exception as e:
                print("Unknown exception:", e)
                break