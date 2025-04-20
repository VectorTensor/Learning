import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import activity

# Define the workflow


@workflow.defn
class HelloWorldWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        # Call the activity
        result = await workflow.execute_activity(
            say_hello_activity, name, start_to_close_timeout=timedelta(
                seconds=5)
        )
        return result



# Define the activity
@activity.defn
async def say_hello_activity(name: str) -> str:
    print(f"Hello, {name}")
    return f"Hello, bye {name}!"

# worker.py
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="hello-task-queue",
        workflows=[HelloWorldWorkflow],
        activities=[say_hello_activity],
    )

    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
