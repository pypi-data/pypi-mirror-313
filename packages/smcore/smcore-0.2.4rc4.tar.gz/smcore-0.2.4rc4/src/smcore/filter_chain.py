import asyncio
from . import types_pb2 as pb2
from .tag_set import TagSet
from .post import Post


class TagFilter(TagSet):
    def __init__(self, *tags):
        super(TagFilter, self).__init__(*tags)
        self.ch = asyncio.Queue()

    async def filter(self, msg: pb2.Message) -> bool:
        """
        Filter must return "True" or "False" specifying whether
        the filter chain should continue processing potential
        matches. This is slightly different than the Go implementation
        that returns an error or not an error
        """

        incoming_tags = TagSet(*msg.post.tags)
        matches = self.matches(incoming_tags)

        if matches:
            p = Post()
            await p.from_proto_message(msg)
            await self.ch.put(p)

        return True


# FilterChains are not thread safe, however in our API, all listen_for calls should be made during setup
# so that once this is running, it's the only thing accessing the filters array.


# Filter chain is specific to TagFilters for now.  No immediate use case to make it more
# generalizable.
class FilterChain:
    def __init__(self):
        self.filters = []

    def insert(self, tag_set: TagSet) -> asyncio.Queue:
        filter = TagFilter(*tag_set.tags)
        self.filters.append(filter)
        return filter.ch

    async def listen_and_filter(self, incoming: asyncio.Queue):
        while True:
            msg = await incoming.get()

            # Surface the new message into each of our TagSet-specific queues
            for f in self.filters:
                cont = await f.filter(msg)

                # Stop processing the filter chain
                if not cont:
                    break  # break out to await the arrival of the next message
