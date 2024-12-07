import asyncio
import signal

from . import Agent, Runner


# Wrapping each call out to the server in an try/except handler setup
# seems awful and bad for readability.  I've chosen to let the implementer of
# setup() and loop() do any exception handling, and all we care about are the
# "should I continue to execute" return values.  It's not very "pythonic" but
# it does allow for a deeper similarity between the python implementation and
# the go implementation
#
# I would generally discourage people from programming like this, but in the
# case of lifecycle, consistent behavior between the two client api
# implementations is important to me and I'm doing my best to not overthink it.


# SIGTERM trapping here is experimental. Shutdown of agents rn with ctrl-c is
# very ugly because of asyncio.  This is an attempt to remedy and cleanly
# shutdown our agents (and have them finish their lifecycle).
class GracefulExitManager:
    exit_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


async def RunUntilComplete(agent: Agent):
    # Agent Initialization (ours, then users)
    await agent._initialize_session()
    err = await agent.setup()
    if err is not None:
        return err

    # Start the message retrieval loop and send our first communication with the BB
    message_retrieval_task = asyncio.create_task(agent._message_thread())
    filter_chain_task = asyncio.create_task(
        agent.post_filters.listen_and_filter(agent.incoming)
    )
    err = await agent.hello()
    if err is not None:
        return err

    # Main agent loop
    # Loop can be broken by the agent returning false
    # or a ctrl-c on at the user-level.  Either way
    # we'd like to exit cleanly.
    g = GracefulExitManager()
    while not g.exit_now:
        cont, err = await agent.loop()

        # Each time loop returns, we assess whether
        # or not to continue and/or throw an error
        if err is not None:
            print(f"agent loop returned an error: {err}")

        # Only break the loop if agent says to stop
        if not cont:
            break

    await agent.goodbye()
    agent.stop()

    # await asyncio.sleep(10.0)

    # Close down the message retrieval loop
    message_retrieval_task.cancel()
    filter_chain_task.cancel()
    try:
        await message_retrieval_task
    except asyncio.CancelledError:
        print("message fetch loop shut down")

    return err


# Best function signature of all time
async def RunRunner(runner: Runner):
    # Agent Initialization (ours, then users)
    await runner._initialize_session()
    err = await runner.setup()
    if err is not None:
        return err

    # Start the message retrieval loop and send our first communication with the BB
    message_retrieval_task = asyncio.create_task(runner._message_thread())
    err = await runner.hello()
    if err is not None:
        return err

    # Main agent loop
    while True:
        cont, err = await runner.loop()

        # Each time loop returns, we assess whether
        # or not to continue and/or throw an error
        if err is not None:
            print(f"agent loop returned an error: {err}")

        # Only break the loop if agent says to stop
        if not cont:
            break

    await runner.goodbye()

    # await asyncio.sleep(10.0)

    # Close down the message retrieval loop
    message_retrieval_task.cancel()
    try:
        await message_retrieval_task
    except asyncio.CancelledError:
        print("message fetch loop shut down")

    return err
