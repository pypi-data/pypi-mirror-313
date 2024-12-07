import os
import sys
import asyncio

sys.path.append(os.path.abspath(".."))

from src.smcore import Agent, Post
from src.smcore.lifecycle import RunUntilComplete


class APITestResult:
    def __init__(self, endpoint, signature):
        self.endpoint = endpoint
        self.signature = signature
        self.passed = False
        self.error_message = ""


# API Pieces being tested
api_components = [
    APITestResult("hello", "hello()"),
    APITestResult("goodbye", "goodbye()"),
    APITestResult("post", "post(b'1234', b'5678', 'post-data')"),
    APITestResult(
        "reply",
        "reply([Post._for_testing(1)], b'life without knowledge', b'is death in disguise', 'reply-data', 'test-test')",
    ),
]


# This agent tests compatibility between the core python API and a core server
# For now, this is a cursory evaluation checking for basic functionality
class APITesterAgent(Agent):
    async def setup(self):
        self.test_data_ch = self.listen_for(
            "reply-data", "test-test"
        )  # reply data will also allow us to test tracing

    async def loop(self):
        test_results = []

        # Run our tests
        for test_data in api_components:
            test_results.append(await self.do_api_test(test_data))

        # Evaluate our tests
        total = len(api_components)
        passed = 0
        for test_result in test_results:
            if test_result.passed:
                passed += 1
            else:
                print(test_result.error_message)

        print(f"{round(100.0*float(passed)/float(total), 0)}% of endpoints passed")

        # Check that our reply surfaced correctly
        # TODO: Verify the received data matches expectation
        reply_data = await self.test_data_ch.get()

        # TODO: Verify the traced data matches expectation (2 msgs, msg idx 1 and 5)
        msgs = await self.trace(reply_data)
        for msg in msgs:
            print(msg)

        # We only run  once
        return False, None

    # Run a single endpoint test
    async def do_api_test(self, test_data):
        method_signature = test_data.signature

        # Attempt to evaluate the provided method
        try:
            await eval(f"self.{method_signature}")
            test_data.passed = True

        except Exception as e:
            test_data.error_message = (
                f"api evaluation failed for endpoint {test_data.endpoint}: {e}"
            )
            test_data.passed = False

        return test_data


async def main():
    # Create your agent
    agt = APITesterAgent(sys.argv[1])

    # Run the agent lifecycle
    err = await RunUntilComplete(agt)

    # Log any concluding errors from the agent's lifecycle
    if err is not None:
        print(f"Agent completed returning an error: {err}")


asyncio.run(main())
