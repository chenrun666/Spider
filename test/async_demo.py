# 绑定回调函数

import time
import asyncio

now = lambda: time.time()


async def do_some_work(x):
    print("waiting", x)
    return "Done after {}s".format(x)


def callback(future):
    print("callback", future.result())


start = now()

corotuine = do_some_work(2)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(corotuine)
print(task)
task.add_done_callback(callback)
print(task)
loop.run_until_complete(task)

print("Time: ", now() - start)
