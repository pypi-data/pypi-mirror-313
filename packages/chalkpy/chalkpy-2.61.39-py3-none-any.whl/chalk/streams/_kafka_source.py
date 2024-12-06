from typing import TYPE_CHECKING, Any, List, Literal, Optional, Union

from chalk.integrations.named import load_integration_variable
from chalk.sink._models import SinkIntegrationProtocol
from chalk.streams.base import StreamSource
from chalk.utils.duration import Duration
from chalk.utils.string import comma_whitespace_split

if TYPE_CHECKING:
    import pydantic
    from pydantic import BaseModel
else:
    try:
        import pydantic.v1 as pydantic
        from pydantic.v1 import BaseModel
    except ImportError:
        import pydantic
        from pydantic import BaseModel


class KafkaSource(StreamSource, SinkIntegrationProtocol, BaseModel, frozen=True):
    bootstrap_server: Optional[Union[str, List[str]]] = None
    """The URL of one of your Kafka brokers from which to fetch initial metadata about your Kafka cluster"""

    topic: Optional[str] = None
    """The name of the topic to subscribe to."""

    ssl_keystore_location: Optional[str] = None
    """
    An S3 or GCS URI that points to the keystore file that should be
    used for brokers. You must configure the appropriate AWS or
    GCP integration in order for Chalk to be able to access these
    files.
    """

    ssl_ca_file: Optional[str] = None
    """
    An S3 or GCS URI that points to the certificate authority file that should be
    used to verify broker certificates. You must configure the appropriate AWS or
    GCP integration in order for Chalk to be able to access these files.
    """

    client_id_prefix: str = "chalk/"
    group_id_prefix: str = "chalk/"

    security_protocol: Literal["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"] = "PLAINTEXT"
    """
    Protocol used to communicate with brokers.
    Valid values are `"PLAINTEXT"`, `"SSL"`, `"SASL_PLAINTEXT"`, and `"SASL_SSL"`.
    Defaults to `"PLAINTEXT"`.
    """

    sasl_mechanism: Literal["PLAIN", "GSSAPI", "SCRAM-SHA-256", "SCRAM-SHA-512", "OAUTHBEARER"] = "PLAIN"
    """
    Authentication mechanism when `security_protocol`
    is configured for SASL_PLAINTEXT or SASL_SSL.
    Valid values are `"PLAIN"`, `"GSSAPI"`, `"SCRAM-SHA-256"`, `"SCRAM-SHA-512"`, `"OAUTHBEARER"`.
    Defaults to `"PLAIN"`.
    """

    sasl_username: Optional[str] = None
    """
    Username for SASL PLAIN, SCRAM-SHA-256, or SCRAM-SHA-512 authentication.
    """

    sasl_password: Optional[str] = pydantic.Field(default=None, repr=False)
    """
    Password for SASL PLAIN, SCRAM-SHA-256, or SCRAM-SHA-512 authentication.
    """

    name: Optional[str] = None
    """
    The name of the integration, as configured in your Chalk Dashboard.
    """

    late_arrival_deadline: Duration = "infinity"
    """
    Messages older than this deadline will not be processed.
    """

    dead_letter_queue_topic: Optional[str] = None
    """
    Kafka topic to send messages when message processing fails
    """

    def __init__(
        self,
        *,
        bootstrap_server: Optional[Union[str, List[str]]] = None,
        topic: Optional[str] = None,
        ssl_keystore_location: Optional[str] = None,
        ssl_ca_file: Optional[str] = None,
        client_id_prefix: Optional[str] = None,
        group_id_prefix: Optional[str] = None,
        security_protocol: Optional[str] = None,
        sasl_mechanism: Optional[Literal["PLAIN", "GSSAPI", "SCRAM-SHA-256", "SCRAM-SHA-512", "OAUTHBEARER"]] = None,
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
        name: Optional[str] = None,
        late_arrival_deadline: Duration = "infinity",
        dead_letter_queue_topic: Optional[str] = None,
    ):
        super(KafkaSource, self).__init__(
            bootstrap_server=bootstrap_server
            or load_integration_variable(
                name="KAFKA_BOOTSTRAP_SERVER", integration_name=name, parser=comma_whitespace_split
            ),
            topic=topic or load_integration_variable(name="KAFKA_TOPIC", integration_name=name),
            ssl_keystore_location=ssl_keystore_location
            or load_integration_variable(name="KAFKA_SSL_KEYSTORE_LOCATION", integration_name=name),
            client_id_prefix=client_id_prefix
            or load_integration_variable(name="KAFKA_CLIENT_ID_PREFIX", integration_name=name)
            or KafkaSource.__fields__["client_id_prefix"].default,
            group_id_prefix=group_id_prefix
            or load_integration_variable(name="KAFKA_GROUP_ID_PREFIX", integration_name=name)
            or KafkaSource.__fields__["group_id_prefix"].default,
            security_protocol=security_protocol
            or load_integration_variable(name="KAFKA_SECURITY_PROTOCOL", integration_name=name)
            or KafkaSource.__fields__["security_protocol"].default,
            sasl_mechanism=sasl_mechanism
            or load_integration_variable(name="KAFKA_SASL_MECHANISM", integration_name=name)
            or KafkaSource.__fields__["sasl_mechanism"].default,
            sasl_username=sasl_username or load_integration_variable(name="KAFKA_SASL_USERNAME", integration_name=name),
            sasl_password=sasl_password or load_integration_variable(name="KAFKA_SASL_PASSWORD", integration_name=name),
            name=name,
            late_arrival_deadline=late_arrival_deadline,
            dead_letter_queue_topic=dead_letter_queue_topic,
            ssl_ca_file=ssl_ca_file or load_integration_variable(name="KAFKA_SSL_CA_FILE", integration_name=name),
        )
        self.registry.append(self)

    def config_to_json(self) -> Any:
        return self.json()

    @property
    def streaming_type(self) -> str:
        return "kafka"

    @property
    def dlq_name(self) -> Union[str, None]:
        return self.dead_letter_queue_topic

    @property
    def stream_or_topic_name(self):
        assert self.topic is not None
        return self.topic
