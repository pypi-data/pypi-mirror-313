from google.protobuf import json_format
from typing import Iterable
from . import types_pb2 as pb2
import aiohttp
import asyncio
import json

# Based on the exchange between John and Josh, we're opting for essentially
# no fault tolerance to network issues for now.  Instead, we'll fail loudly and
# quickly if there are communication problems.
from .exceptions import BlackboardCommunicationError


def fail_loudly(resp):
    try:
        resp.raise_for_status()
    except aiohttp.ClientResponseError as e:
        raise BlackboardCommunicationError(
            f"server issued error response: {resp.status} {e.Message}"
        )


# Users of core's python agent api should not need to interact
# directly with this class unless deeper customization of the
# networking is required (just leaving this breadcrumb in case you end
# up here and are wondering if it's important).
#
# This is (at present) the primary API client we provide (HTTP).  If
# other protocols are desired, please feel free to contribute
# additional classes (the grpc client can also be used as a blueprint,
# but is not currently up to date).  Please follow this basic approach though.


class BlackboardHTTPClient:
    """
    BlackboardHTTPClient represents the primary API client for core's Blackboard.

    Attributes
    ----------
    - addr (str): address hosting the Blackboard.
    - session (aiohttp.ClientSession): current client session.
    """

    slice_path = "/blackboard?start_idx={0}&end_idx={1}"
    write_path = "/message"
    trace_path = "/trace/{0}"
    length_path = "/blackboard/len"

    def __init__(self, addr: str):
        """
        Constructor for the BlackboardHTTPClient class.

        Parameters
        ----------
        addr (str): address hosting the Blackboard.
        """
        self.addr = addr
        self.session = None

    def __del__(self):
        """
        Destructor for BlackboardHTTPClient class.
        """
        asyncio.create_task(self.session.close())

    async def _initialize_session(self):
        """
        _initialize_session initializes the client session.
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()

    # A little bit of future-proofing to allow for easily changed common url components
    def _get_url(self, path: str):
        return "http://" + self.addr + path

    async def _read(self, msg_idx):
        url = self._get_url(self.slice_path.format(msg_idx, msg_idx + 1))

        async with self.session.get(url) as response:
            fail_loudly(response)
            body = await response.text()
            msgs = json.loads(body)
            msg_stack = json_format.ParseDict(msgs, pb2.MessageStack())
            return msg_stack.messages[0]

    async def _slice(self, start_idx: int, end_idx: int):
        # Form the specific API path e.g. http://myblackboard.com:8080/blackboard?start_idx=1&end_idx=25
        url = self._get_url(self.slice_path.format(start_idx, end_idx))

        async with self.session.get(url) as response:
            # Fail loudly if
            fail_loudly(response)

            body = await response.text()
            msgs = json.loads(body)
            msg_stack = json_format.ParseDict(msgs, pb2.MessageStack())
            return msg_stack.messages

    async def _trace(self, msg_idx: int) -> Iterable[pb2.Message]:
        """
        trace retrieves a container of messages associated with an incoming message.

        Parameters
        ----------
        msg (pb2.Message): message to retrieve the trace of.

        Returns
        -------
        msg_stack.messages (Iterable[pb2.Message]): container of messages in the trace.
        """

        # Form the specific API path e.g. http://myblackboard.com:8080/trace/25
        # url = self._get_url(self.trace_path.format(msg.index))
        url = self._get_url(self.trace_path.format(msg_idx))

        async with self.session.get(url) as response:
            fail_loudly(response)
            body = await response.text()
            msgs = json.loads(body)
            msg_stack = json_format.ParseDict(msgs, pb2.MessageStack())
            return msg_stack.messages

    async def _len(self):
        url = self._get_url(self.length_path)

        async with self.session.get(url) as response:
            fail_loudly(response)
            body = await response.text()
            bb_length = json.loads(body)
            return bb_length

    async def _write(self, msg):
        url = self._get_url(self.write_path)
        msg_json = json_format.MessageToJson(msg)

        async with self.session.post(url, data=msg_json.encode("utf-8")) as response:
            if response.status != 201:  # Would be better to accept any 200 message?
                print("send message error: ", response.status)

            fail_loudly(response)
