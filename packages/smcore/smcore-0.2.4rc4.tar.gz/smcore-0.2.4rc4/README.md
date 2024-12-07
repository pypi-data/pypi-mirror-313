# `core` Python API

[TOC]

The Go implementation of the agent API should be considered the "reference"
implementation.  This python implementation seeks to implement the same
user-facing interfaces and pattern with language-specific concessions as
needed.

## Installing the `smcore` package

We're planning to stay with pip the primary distribution method for `smcore`.
We will do our best to keep the PyPi package up to date (it is not currently).

Thus, the other recommended way to install it is to clone this repo, navigate
into the `cmd/client-apis/python/pkg` directory and run `pip install .`.


## A note on concurrency

We have made substantial use of `asyncio` and `aiohttp`.  These unfortunately 
sort of "pollute" source code with a lot of `async` and `await` where it 
may not always feel necessary.  This is one of the language-specific concessions
mentioned above and we are open to other ideas and implementations that 
preserve the spirit but get rid of this.

Although we *use* concurrency, our intention is to shield
you from the worst of the details.   You will need to `await` all
API calls, but in many cases you can otherwise program normally
if you utilize the lifecycle we provide.

For more reading on using python concurrency, please check out the following:

- https://realpython.com/async-io-python/
- https://docs.python.org/3/library/asyncio.html
- https://docs.aiohttp.org/en/stable/index.html

## The Agent API

### Quick Summary

Derive your agent from an `Agent` superclass, and implement a `Setup` and
`Loop` method.

```python
from smcore import Agent, pb2

class MyAgent(Agent):
  async def setup(self): 
    return None # Return non-None "error" value if agent setup should stop

  async def loop():
    return True, None # Return True to continue the loop
    # return False, None # Return False to break the loop
```
```python
# Essential agent API for BB communication (provided by the Agent base class)
def post(self, metadata: bytes, data: bytes, *tags):
def reply(self, posts: list(Post), metadata: bytes, data: bytes, *tags):
def listen_for(*tags) -> asyncio.Queue:
def log(severity: pb2.Log.Severity, msg: str):
```
```python
# Additional API provided by BasicAgent
def trace(self, post: Post):
```

```python
# Run your agent using the our managed lifecycle
async def main():
    # Create your agent
    agt = MyAgent(blackboard_addr)

    # Run the agent lifecycle
    err = await RunUntilComplete(agt)

    # Log any concluding errors from the agent's lifecycle
    if err is not None:
        print(f"Agent completed returning an error: {err}")

asyncio.run(main())
```

### Detailed Explanation

#### Importing the client package

We're planning to make pip the primary distribution method for `smcore`.

The other recommended way to install it is to clone the repo, navigate
into the `cmd/client-apis/python/pkg` directory and run `pip install`.

Once installed, we suggest the following variants for importing the client package:

```python
import smcore
from smcore import Agent, pb2
```

#### The Agent superclass

To make an agent, create a new class that inherits from our agent
base class.  
```python
class MyAgent(Agent):
  ...
```

The `Agent` base class provides all of the essential functionality for agent
blackboard communication including but not limited to posting, replying, and
receiving data from the blackboard.  You are not required to utilize Agent to
communicate with the blackboard however we cannot provide support at this point
for those more advanced use cases.

#### Agent lifecycle

`Agent` actually runs several processes concurrently, which can leave dangling
coroutines and unfreed memory if we're not careful.  As a result, we have implemented
an agent lifecycle that can handle this cleanup for you.

##### Utilize the lifecycle management

To utilize the lifecycle, you must implement two functions.

These allow your agent to fulfill the `ManagedAgent` interface.

```python
class MyAgent(Agent):
  async def setup(self): 
    # This is where you should do agent initialization
    # This also where you should make your calls to listen_for
    return None # Return non-None "error" value if agent setup should stop

  async def loop():
    # This is where your agent should do its processing
    return True, None # Return True to continue the loop
    # return False, None # Return False to break the loop
```

(This pattern is inspired by the Arduino lifecycle)

###### Setup

Setup is executed once, prior to any communication with the blackboard.  **Do
not** call any blackboard communication methods inside of setup.  Although they
will succeed, this interferes with proper message delivery using the
`listen_for` method we provide.

Any agent initialization you'd like to perform prior to communicating with the
blackboard should be performed here.  Additionally, any calls to `listen_for`
should be made in `setup`.

Returning anything non-`None` from `setup` will prevent the agent from starting.
This is to match behavior between the Go and Python APIs.  Return-by-value
errors are kind of a hallmark of Go, but in this case, it works well for
the lifecycle management.  In general, exception handling is the correct
approach to errors in python.

###### Loop

`loop` will be executed infinitely many times until it is told to stop by
returning `False`.  Persistence can be achieved by always returning `True`.
Returning an error in the second return parameter from a `loop` does not itself
cause the agent to stop executing.

Inside of the loop is where your agent should listen for messages, process
data, and communicate with the blackboard.

##### Run your agent using our lifecycle management

An agent that has properly implemented a Setup and Loop method can then be managed
using the `RunUntilComplete` function.

```python
async def main():
    # Create your agent
    agt = MyAgent(blackboard_addr)

    # Run the agent lifecycle
    err = await RunUntilComplete(agt)

    # Log any concluding errors from the agent's lifecycle
    if err is not None:
        print(f"Agent completed returning an error: {err}")


asyncio.run(main())
```

#### Blackboard Communication

The `core` agent API is fundamentally three methods: `post`, `reply`, and `listen_for`.
These three methods provide all key functionality for multiagent systems.

##### Post

Analogous to a real blackboard, `post` just means "put something on the blackboard".

```python
self.post(b'hello', b'world', 'tag1', 'tag2')
```

###### Tagging

This version of `core` changes how messages are exchanged between agents.

We have ultimately done away with attributes and promises in favor of a tagging
system.

Agents post their messages with a set of tags and other agents listen for a set
of tags.  Each matching message will surface into the appropriate `listen_for`
channel. (There are deep and obvious similarities here to traditional pub/sub
architectures)

Messages will match if the incoming message contains *at least* the tags provided
to `listen_for`. E.g., 

```
self.listen_for("test") matches post(md, d, "test")
self.listen_for("test") also matches post(md, d, "test", "tag2")

self.listen_for("test", "tag2") matches post(md, d, "test", "tag2")
self.listen_for("test", "tag2") does **not** match post(md, d, "test")
```

This means that without care in tagging there can easily be agent "cross talk"
particularly with multiple agents performing the same or similar tasks.  This
is intentional and by design and places a great deal of control and flexibility
in the hands of the user although new users may find it challenging. Please
utilize our issues page for feedback and assistance with the new tagging system
if it is unclear, or some additional instruction, guidance, or debugging help
is required.

##### ListenFor

Many agents will want to receive some data from the blackboard to begin 
executing.  `listen_for` will provide you with an `asyncio.Queue`  on which messages with
matching tags will arrive.  These can then be utilized as a normal concurrent queue
on which you can receive data from the blackboard.

>>>
**IMPORTANT**: To ensure proper behavior, listen_for **must** be called in
`setup`, before any messages have been sent to the blackboard.
>>>

Here is an example from our ping pong agents:
```python
class PongAgent(Agent):
    async def setup(self):
        # listen_for returns an asyncio.Queue from which we can receive desired messages
        self.ping_queue = self.listen_for("ping-message")
        return None

    async def loop(self):
        ping_post = await self.ping_queue.get()
        #... do stuff with ping_post
```

`listen_for` returns a `Post` object
([source](cmd/client-apis/python/pkg/src/post.py)).  The post has metadata and
data that can be used as desired, but importantly, the post object can be used
to begin a "chain" of posts using the reply mechanism.  A reply actually just
shows up on the blackboard as a post, but you'll notice that it has one or more
messages listed in the "replying_to" field.  It also creates very logical and
light links between messages on the blackboard that enable techniques such as
tracing.

Here is an example from our Pong agent:

```python
class PongAgent(Agent):
    # ...
    async def loop(self):
        ping_post = await self.ping_queue.get()
        await self.reply([ping_post], None, None, "pong-message")
        return True, None
```

##### Tracing

```python
def trace(self, post *Post) -> list(Post):
```

Tracing in a core blackboard allows an agent to retrieve messages via a chain
of replies; effectively, we walk the "linked list" of messages and give them
back to the tracer.

Here is an example from our [ping-pong example](cmd/client-apis/python/agents/full_example.py), using a "MonitorAgent":

```python
#...
    traced_posts = await self.trace(pong_post)
    
    idxs = [post.replyto_idx for post in traced_posts]
    # labels = [post.labels for post in traced_posts]
    labels = []
    for post in traced_posts:
        labels.append(*post.labels)
    
    print("running trace")
    
    trace_results = {
        "n_post_in_trace": len(traced_posts),
        "post_indices": idxs,
        "msg_labels": labels,
    }
    
    data = json.dumps(trace_results)
    await self.reply(traced_posts, None, data.encode("utf-8"), "trace-results")
#...
```

Tracing is *not* part of the core agent interface, however is a special feature
of the `core` base agent.

> **NOTE:** Tracing is a method that exists slightly outside of the core agent API
> and is a service provided by the `core` blackboard (some of the secret sauce
> of our implementation we hope). In fact, although we have placed it into
> Blackboard interface, certain blackboards implementations may wish to not
> provide or return useful tracing information.

##### Logging

Logging is, strictly speaking, not a necessary part of the `core` protocol,
however logging is so ubiquitously useful during development, execution, and
monitoring that we'd be hard pressed not to include it. Defining this message
type allows us to separate messages meant for agents (posts) which may or may
not be human readable, from posts that should be human-readable (logs).

```python
def log(self, severity: pb2.Log.Severity, message: str):
```

The default severity everyone should use is `pb2.Log.Severity.Info`.  This is a
bread and butter log message.

We encourage the following guidelines for the other severities:

```
pb2.Log.Severity.Debug:    should not appear during normal logging
pb2.Log.Severity.Info:     normal logging
pb2.Log.Severity.Warning:  possible with errors, but can continue
pb2.Log.Severity.Error:    normal operation is not occuring
pb2.Log.Severity.Critical: 🔥🔥🔥 (possibly trigger a halt and catch fire?)
```
##### Hello and Goodbye

If using the managed lifecycle, you don't need to worry about sending `hello`
and `goodbye` messages.  If you're implementing a more "raw" agent, these
messages indicate an agent's first and last connection to the blackboard, and
are one way to trigger the concurrent loops necessary to handle message
delivery.

For now, we only recommend using the managed lifecycle, unless you've got a lot
of time to debug. We won't be able to guarantee any support for non-lifecycle
agents for now, although we'd be interested in hearing about your
implementations.

For feedback on the lifecycle, or to report issues, or request features, please use 
our issues page.

## Examples

For a complete and working example of multiple agents exchanging information
using the `core` python API, please reference our python
[ping-pong](cmd/client-apis/python/full_example.py) example.

These can be executed against a blackboard using 
```
core start server # start the blackboard
micromamba activate smcore-env # set up your environment that has the smcore package installed
python full_example.py localhost:8080
```


Please check out the base class ["agent"](cmd/client-apis/python/pkg/src/agent.go) implementation
if you need manage agent behavior using even lower-level
API elements (out of scope for this documentation).

