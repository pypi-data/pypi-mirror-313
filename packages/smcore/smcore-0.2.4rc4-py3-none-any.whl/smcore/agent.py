from .blackboard_http_client import BlackboardHTTPClient
from threading import Lock
from . import types_pb2 as pb2
from .filter_chain import FilterChain
from .tag_set import TagSet
from .post import Post
from .time_sync import SyncTime
import asyncio
import sys
import time

from typing import Iterable

# An observation (10/25/2024)
# This agent implementation is fundamnetally flipped from how I've done it in
# the latest Go implementation. In that version, an agent "is a" spec and "has
# a" blackboard trasporter.  In this implementation, I've made an agent "be a"
# blackboard transporter type (network client) and it "has a" spec.  I wonder
# what the implications of that are and how much of a difference it would make
# to change to to be the other way around. I think that the current Go approach
# makes more sense.  An agent is (ideally ) inseparably defined from its
# specification, whereas it could talk to the blackboard ina number of different
# ways (http, grpc, both?)
#
# nvm, I do a "has a" for both the transporter and the spec.  We change  to do both here too.
# NOTE: This could add some semi-weird and undesirable pb message functionality to Agent. Will need
# to keep an eye on  this.
#
# NOTE: nvm again. We're back to where we started b/c we can't actually inherit from a pb2.AgentSpec type
CLIENT_TYPE = BlackboardHTTPClient


def get_default_agent(addr: str):
    return Agent(addr)


class Agent(CLIENT_TYPE):
    """
    Agent is the primary agent base class. Inheritors must implement self.run().
    It is a subclass of a client class (default BlackboardHTTPClient).

    Attributes
    ----------
    - start_time (float): launch time of the Agent.
    - last_msg_index (int): index of the last received message.
    - spec (AgentSpec): AgentSpec of the Agent.
    - blackboard_remote_addr (str): address of the Blackboard the Agent communicates with.
    - attributes (Attributes): Attributes of the Agent.
    - dump_startup (bool): whether to ignore previous Blackboard messages.
    - mutex (threading.Lock): mutex for thread-safety.
    - is_fulfilled (asyncio.Event): an empty event to mark whether a promise is fulfilled.
    - stopped (bool): whether the Agent's process has been stopped.
    """

    def __init__(self, addr: str):
        # def __init__(self, spec: pb2.AgentSpec, bb_addr: str, dump_startup: bool = True):
        """
        Constructor for Agent class.

        Parameters
        ----------
        - spec (AgentSpec): initialized AgentSpec for the current Agent.
        - bb_addr (str): address of the Blackboard to interface with.
        - dump_startup (bool): whether to ignore previous Blackboard messages (optional, default True).
        """
        super(Agent, self).__init__(addr)
        self.name = "basic-agent"
        self.start_time = time.monotonic()
        self.last_msg_idx = 0
        self.blackboard_remote_addr = addr
        self.dump_startup = False  # TODO: is there a better name for this?
        self.mutex = Lock()
        self.stopped = False
        self.post_filters = FilterChain()
        self.incoming = asyncio.Queue()
        self.time = SyncTime()
        self.poll_interval_ms = 100

    async def setup(self):
        raise NotImplementedError()

    async def loop():
        raise NotImplementedError()

    def dump_startup(self):
        """
        dump_startup sets self.dump_started to True.
        """
        self.dump_startup = True

    ####################################################################
    # Primary AgentHTTP interface that users should employ when writing
    # their own agents
    ####################################################################

    async def log(self, severity: str, message: str, stdout: bool = True):
        """
        log sends a Log message to the Blackboard.

        Parameters
        ----------
        - severity (str): severity of the logged message.
        - message (str): message string.
        - stdout (bool): whether to write the message to stdout (optional, default True).
        """
        log_message = pb2.Message(log=pb2.Log(severity=severity, message=message))
        await self.send_message(log_message)
        if stdout:
            monotonic_time = time.monotonic() - self.start_time
            monotonic_time = int(round(monotonic_time, 0))  # make it nicer to print
            print(
                "%05d %-10s %s"
                % (monotonic_time, str(severity).removeprefix("Log."), message),
                flush=True,
            )

    def set_name(self, name):
        self.name = name

    def listen_for(self, *tags) -> asyncio.Queue:
        ts = TagSet(*tags)
        return self.post_filters.insert(ts)

    async def post(self, metadata, data, *args):
        labels = []
        for a in args:
            labels.append(a)

        post_msg = pb2.Post(
            tags=labels,
            data=pb2.CoreData(data=data),
            metadata=pb2.CoreData(data=metadata),
        )

        await self.send_message(pb2.Message(post=post_msg))

    async def trace(self, post):
        msg_idx = post.replyto_idx

        traced_posts = []

        msgs = await self._trace(msg_idx)
        for msg in msgs:
            p = Post()
            await p.from_proto_message(msg)
            traced_posts.append(p)

        return traced_posts

    async def reply(self, posts, metadata, data, *args):
        labels = []
        for a in args:
            labels.append(a)

        post_msg = pb2.Post(
            tags=labels,
            data=pb2.CoreData(data=data),
            metadata=pb2.CoreData(data=metadata),
        )

        replying_to = []
        for p in posts:
            replying_to.append(p.replyto_idx)

        await self.send_message(pb2.Message(replyingTo=replying_to, post=post_msg))

    async def send_ping(self):
        """
        send_ping sends a Ping message to the Blackboard.
        """
        # Although still technically available, ping messages as a
        # fundamental part of our protocol will likely be deprecated
        # await self.send_message(pb2.Message(ping={}))
        await self.post(None, None, "ping")

    async def hello(self):
        """
        hello sends a Hello message to the Blackboard.
        """
        await self.send_message(pb2.Message(hello={}))

    async def goodbye(self):
        """
        goodbye sends a Goodbye message to the Blackboard.
        """
        await self.send_message(pb2.Message(goodbye={}))

    # NOTE: This is really the only function call in the Agent API (for now) that we could
    # reasonably "expect" to encounter an error state (i.e. unable to communicate with the bb
    # or otherwise getting bad error codes).  Error handling in the python api can't probably
    # shouldn't look like the go library. I think that'll make everyone unhappy.
    #
    # Some options:
    # - Each send_message can raise an exception that must be handled by the user.  This would be something like
    #   BlackboardCommunicationException so that we don't force the user to handle like 30 different exception
    #   types if playing that game is something they want to do.
    #   This means that if they don't want their agent to crash, then any call to the API MUST be wrapped in the
    #   following:
    #
    #   try:
    #       agt.hello()
    #   except BlackboardCommunicationException as bb_err:
    #       # handle or raise the exception
    #
    #   Regardless of how anyone else feels, I think I hate this. the "send_message" exception
    #   kind of bubbles out to all the other API calls.  If this is the "most pythonic" way, and peole like it,
    #   then I could support this, but I think it makes our code harder to read and write.
    #
    # - Don't do anything.  Let it fail, let it crash. Our users are developing agents and a stack trace is not
    #   the end of the world.  This essentially is the "must communicate with the blackboard" model and is not
    #   fault tolerant of the network.  This can probably work in certain environments but would likely require
    #   retooling for certain applications and deployment scenarios.
    #
    #   A major pro of this approach is that it requires zero-effort from us, which could be important right now while
    #   we prioritize developing real use cases.  It also kind of puts the onus on the network operator to be responsible
    #   for network quality, although in practice, this is likely to cause some frustration among users since
    #   most people do not have intimate knowledge of networking or run their own network.
    #
    async def send_message(self, msg: pb2.Message):
        """
        send_message sends an incoming message to the Blackboard.

        Parameter
        ---------
        - msg (pb2.Message): message to send.
        """

        msg.source = self.name
        msg.timeSent.FromDatetime(self.time.now())

        await self._write(msg)

    async def _message_thread(self):
        """
        message_thread launches the thread for handling messages from the Blackboard.
        """

        # If ignoring current data on blackboard (i.e. if only
        # interesting in adding data, or dta "going forward", no need
        # to parse existing msgs on bb.
        if self.dump_startup:
            bb_length = await self._get_len()
            print(
                f"skipping all messages currently on blackboard ({bb_length} msgs)",
                flush=True,
            )
            self.last_msg_idx = bb_length - 1

        while not self._stopped():
            await asyncio.sleep(self.poll_interval_ms / 1000)
            # msgs = await self._get_messages(self.last_msg_idx + 1)  # list of messages
            msgs = await self._slice(self.last_msg_idx + 1, 0)  # list of messages

            if len(msgs) > 0:
                for msg in msgs:
                    msg_type = msg.WhichOneof("contents")

                    if msg_type == "post":
                        await self.incoming.put(msg)
                    elif msg_type == "halt":
                        return

                    self.last_msg_idx = msg.index

    def stop(self):
        """
        stop sets self.stopped to True, causing the agent's
        concurrent background processes to cleanly exit.
        """

        with self.mutex:
            self.stopped = True

    def _stopped(self) -> bool:
        """
        _stopped checks whether the Agent has stopped.

        Returns true if it has stopped; false otherwise.
        """
        with self.mutex:
            return self.stopped


# This main runs some tests
if __name__ == "__main__":
    bb_addr = sys.argv[1]

    a = Agent(bb_addr)

    a.hello()
    a.send_ping()
    a.log(pb2.Log.Severity.Info, "hello world")
    a.goodbye()

    # asyncio.run(a.start())
