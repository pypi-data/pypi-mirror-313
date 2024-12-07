from typing import TYPE_CHECKING, Any, Optional, Union

from chalk.integrations.named import load_integration_variable
from chalk.streams.base import StreamSource
from chalk.utils.duration import Duration

if TYPE_CHECKING:
    from pydantic import BaseModel
else:
    try:
        import pydantic.v1 as pydantic
        from pydantic.v1 import BaseModel
    except ImportError:
        import pydantic
        from pydantic import BaseModel


class PubSubSource(StreamSource, BaseModel, frozen=True):
    project_id: Optional[str] = None
    """The project id of your PubSub source"""

    subscription_id: Optional[str] = None
    """
    The subscription id of your PubSub topic from which you want to consume messages.
    To enable permission for consuming this screen, ensure that the service account has
    the permissions 'pubsub.subscriptions.consume' and 'pubsub.subscriptions.get'.
    """

    name: Optional[str] = None
    """
    The name of the integration, as configured in your Chalk Dashboard.
    """

    late_arrival_deadline: Duration = "infinity"
    """
    Messages older than this deadline will not be processed.
    """

    dead_letter_queue_topic_id: Optional[str] = None
    """
    PubSub topic id to send messages when message processing fails. Add the permission
    'pubsub.topics.publish' if this is set.
    """

    def __init__(
        self,
        *,
        project_id: Optional[str] = None,
        subscription_id: Optional[str] = None,
        name: Optional[str] = None,
        late_arrival_deadline: Duration = "infinity",
        dead_letter_queue_topic_id: Optional[str] = None,
    ):
        super(PubSubSource, self).__init__(
            name=name,
            project_id=project_id
            or load_integration_variable(name="PUBSUB_PROJECT_ID", integration_name=name)
            or PubSubSource.__fields__["project_id"].default,
            subscription_id=subscription_id
            or load_integration_variable(name="PUBSUB_SUBSCRIPTION_ID", integration_name=name)
            or PubSubSource.__fields__["subscription_id"].default,
            late_arrival_deadline=late_arrival_deadline
            or load_integration_variable(name="PUBSUB_LATE_ARRIVAL_DEADLINE", integration_name=name)
            or PubSubSource.__fields__["late_arrival_deadline"].default,
            dead_letter_queue_topic_id=dead_letter_queue_topic_id
            or load_integration_variable(name="PUBSUB_DEAD_LETTER_QUEUE_TOPIC_ID", integration_name=name)
            or PubSubSource.__fields__["dead_letter_queue_topic_id"].default,
        )
        self.registry.append(self)

    def config_to_json(self) -> Any:
        return self.json()

    @property
    def streaming_type(self) -> str:
        return "pubsub"

    @property
    def dlq_name(self) -> Union[str, None]:
        return self.dead_letter_queue_topic_id

    @property
    def stream_or_topic_name(self) -> str:
        assert self.subscription_id is not None
        return self.subscription_id
