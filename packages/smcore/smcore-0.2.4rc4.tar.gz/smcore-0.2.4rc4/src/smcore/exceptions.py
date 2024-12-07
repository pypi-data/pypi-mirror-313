# Define as *few* exception types as possible.

# This exception should be raised whenever communication between the server and client fails.
# At present, we do no exception handling.
class BlackboardCommunicationError(Exception):
    pass
