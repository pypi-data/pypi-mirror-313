"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class HelloRequest(google.protobuf.message.Message):
    """The request message containing the user's name and how many greetings
    they want.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    NUM_GREETINGS_FIELD_NUMBER: builtins.int
    name: typing.Text
    num_greetings: typing.Text
    def __init__(
        self,
        *,
        name: typing.Text = ...,
        num_greetings: typing.Text = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "name", b"name", "num_greetings", b"num_greetings"
        ],
    ) -> None: ...

global___HelloRequest = HelloRequest

class HelloReply(google.protobuf.message.Message):
    """A response message containing a greeting"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MESSAGE_FIELD_NUMBER: builtins.int
    message: typing.Text
    def __init__(
        self,
        *,
        message: typing.Text = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["message", b"message"]
    ) -> None: ...

global___HelloReply = HelloReply
