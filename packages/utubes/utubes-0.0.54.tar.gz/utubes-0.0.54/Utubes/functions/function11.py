import asyncio
from .collections import THREAD
#===============================================================================================

class Cancel:

    async def killtasks():
        tasks = [ task for task in asyncio.all_tasks() if task is not asyncio.current_task() ]
        for task in tasks:
            task.cancel()

        THREAD.shutdown(wait=False) if THREAD else None
        await asyncio.gather(*tasks, return_exceptions=True)

#===============================================================================================
