import json
import os
from typing import List, Generic, TypeVar
from typing import Union, Literal, Annotated

from google.protobuf.message import Message
from pydantic import BaseModel, Field

T = TypeVar("T", bound=Message)


class TopicBaseModel(BaseModel):
    topic_name: str
    topic_key: str
    message_type: str


class PUB(TopicBaseModel):
    topic_type: Literal["PUB"]


class SUB(TopicBaseModel):
    topic_type: Literal["SUB"]


class EndpointBaseModel(BaseModel):
    endpoint_name: str
    endpoint_key: str
    requester_message_type: str
    provider_message_type: str


class REQ(EndpointBaseModel):
    endpoint_type: Literal["REQ"]


class PRV(EndpointBaseModel):
    endpoint_type: Literal["PRV"]


Topic = Annotated[Union[PUB, SUB], Field(discriminator="topic_type")]
Endpoint = Annotated[Union[REQ, PRV], Field(discriminator="endpoint_type")]


class Topics(BaseModel):
    topics: List[Topic]


class Endpoints(BaseModel):
    endpoints: List[Endpoint]


def parse_topics() -> Topics:
    try:
        topic_data_env = os.environ["TOPICS"]
        return Topics.model_validate_json(topic_data_env)
    except KeyError:
        raise EnvironmentError("`TOPICS` environment variable not set.")
    except json.JSONDecodeError as e:
        raise ValueError("`TOPICS` environment variable is not valid JSON.") from e


def parse_endpoints() -> Endpoints:
    try:
        endpoints_data_env = os.environ["ENDPOINTS"]
        return Endpoints.model_validate_json(endpoints_data_env)
    except KeyError:
        raise EnvironmentError("`ENDPOINTS` environment variable not set.")
    except json.JSONDecodeError as e:
        raise ValueError("`ENDPOINTS` environment variable is not valid JSON.") from e


class Metadata:
    def __init__(self, topic_name: str, message_type_decoded: str, bytes_transmitted: int):
        self.topic_name: str = topic_name
        self.message_type_decoded: str = message_type_decoded
        self.bytes_transmitted: int = bytes_transmitted

    def __repr__(self):
        return f"Metadata(topic_name={self.topic_name}, message_type_decoded={self.message_type_decoded}, bytes_transmitted={self.bytes_transmitted})"

    def __str__(self):
        return f"Metadata(topic_name={self.topic_name}, message_type_decoded={self.message_type_decoded}, bytes_transmitted={self.bytes_transmitted})"


class MessageWithMetadata(Generic[T]):
    """A message with metadata."""

    def __init__(self, message: T, metadata: Metadata):
        self.message: T = message
        self.metadata: Metadata = metadata
