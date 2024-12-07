import sys
from . import types_pb2 as pb2
import aiohttp


# Fetch data from remote resource as required
async def ResolveCoreData(core_data: pb2.CoreData):
    field = core_data.WhichOneof("contents")

    if field == "data":
        return core_data.data
    elif field == "link":
        # this is a definite inefficiency, although I'm going to
        # advise not troubleshooting until there's a demonstrable
        # cost or problem.  Attaching it to the transporter seems like
        # an obvious solution, but it doesn't really make any more
        # sense there.  Also consider that the the object store host is not
        # necessarily the blackboard host, so the benefit of reusing the same http
        # connection is a little less obviously clear.
        async with aiohttp.ClientSession() as session:
            async with session.get(core_data.link) as response:
                return await response.read()


class Post:
    @classmethod
    def _for_testing(cls, reply_idx):
        p = Post()
        p.replyto_idx = reply_idx
        return p

    async def from_proto_message(self, pb2_message):
        pb2_post = pb2_message.post
        self.data = await ResolveCoreData(pb2_post.data)
        self.metadata = await ResolveCoreData(pb2_post.metadata)
        self.labels = pb2_post.tags
        self.replyto_idx = pb2_message.index

    def tags(self):
        return self.labels

    def __str__(self):
        return (
            f"post idx {self.replyto_idx} metadata: {self.metadata} data: {self.data}"
        )
