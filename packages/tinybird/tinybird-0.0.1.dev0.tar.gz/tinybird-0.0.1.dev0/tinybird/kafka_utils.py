import asyncio
import functools
import json
import logging
import multiprocessing.dummy
import random
import re
import struct
import time
import traceback
import urllib.parse
from datetime import datetime, timedelta
from functools import reduce
from typing import List, Optional

import orjson
from confluent_kafka import OFFSET_BEGINNING, DeserializingConsumer, KafkaError, KafkaException, TopicPartition
from confluent_kafka.admin import AdminClient
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import Deserializer, StringDeserializer
from tornado.httpclient import AsyncHTTPClient, HTTPResponse

from tinybird.data_connector import DataConnector, KafkaSettings
from tinybird.guess_analyze import analyze
from tinybird.ingest.json_encoder import ExtendedJsonEncoder
from tinybird.ndjson import extend_json_deserialization
from tinybird.sql import parse_table_structure
from tinybird.syncasync import sync_to_async
from tinybird.user import User
from tinybird.views.api_errors.data_connectors import KafkaPreviewError
from tinybird.views.json_deserialize_utils import json_deserialize_merge_schema_jsonpaths, parse_augmented_schema
from tinybird.views.ndjson_importer import kafka_preview

EARLIEST_POLL_TIMEOUT_SECONDS = 5
PREVIEW_POOL_SIZE = 32


def escape_password_url(url: str) -> str:
    """Escape the user and password only if they are not already escaped for compatibility
    >>> escape_password_url('https://user:password@url.co')
    'https://user:password@url.co'
    >>> escape_password_url('https://us/er:password@url.co')
    'https://us%2Fer:password@url.co'
    >>> escape_password_url('https://user:pass/word@url.co')
    'https://user:pass%2Fword@url.co'
    >>> escape_password_url('https://us%2Fer:password@url.co')
    'https://us%2Fer:password@url.co'
    >>> escape_password_url('https://user:pass%2Fword@url.co')
    'https://user:pass%2Fword@url.co'
    >>> a = 'https://G635IKRM3XQ7KFVW:nOGPY5Y9PU/EJSwabxn10ApYbX5cSOa+T8Nq9YJ3SgwUTdWArnEaJEPsYLsimxcy@psrc-d9vg7.europe-west3.gcp.confluent.co'
    >>> escape_password_url(a)
    'https://G635IKRM3XQ7KFVW:nOGPY5Y9PU%2FEJSwabxn10ApYbX5cSOa%2BT8Nq9YJ3SgwUTdWArnEaJEPsYLsimxcy@psrc-d9vg7.europe-west3.gcp.confluent.co'
    """
    special_char_res = re.compile("[@_!#$%^&*()<>?/\|}{~:]")

    def quote_if_necessary(part: str):
        if urllib.parse.unquote(part) != part or special_char_res.search(part) is None:
            return (False, part)
        return (True, urllib.parse.quote(part, safe=""))

    res = re.match("(https?):\/\/(.*?):(.*)@(.*)", url)
    result = url
    if res:
        url_groups = res.groups()
        user_changed, user = quote_if_necessary(url_groups[1])
        password_changed, password = quote_if_necessary(url_groups[2])
        if password_changed or user_changed:
            result = f"{url_groups[0]}://{user}:{password}@{url_groups[3]}"
    return result


class RawDeserializer(Deserializer):
    def __call__(self, value, ctx):
        return value


class KafkaServerGroupsConfig:
    server_groups: dict[str, list[str]] = {}

    @classmethod
    def config(cls, server_groups: dict[str, list[str]]):
        if isinstance(server_groups, dict) and all(
            isinstance(key, str) and isinstance(value, list) for key, value in server_groups.items()
        ):
            cls.server_groups = server_groups

    @classmethod
    def get_servers(cls, kafka_server_group: str) -> list[str]:
        return cls.server_groups.get(kafka_server_group, [])


class KafkaTbUtils:
    @staticmethod
    async def get_kafka_preview(
        workspace: User,
        data_connector: DataConnector,
        kafka_group_id: Optional[str] = None,
        kafka_topic: Optional[str] = None,
        max_records=KafkaSettings.PREVIEW_MAX_RECORDS,
        preview_activity=True,
        preview_earliest_timestamp=False,
        schema=None,
    ):
        if KafkaTbUtils._is_isolated(workspace) and (client := KafkaTbUtils._get_client(workspace)) is not None:
            return (
                await client.get_preview(
                    data_connector,
                    kafka_group_id,
                    kafka_topic,
                    max_records,
                    preview_activity,
                    preview_earliest_timestamp,
                    schema,
                )
                if client
                else None
            )
        else:
            return await KafkaUtils.get_kafka_preview(
                data_connector=data_connector,
                kafka_group_id=kafka_group_id,
                kafka_topics=(kafka_topic and [kafka_topic]),
                max_records=max_records,
                preview_activity=preview_activity,
                preview_earliest_timestamp=preview_earliest_timestamp,
                schema=schema,
            )

    @staticmethod
    async def get_kafka_topic_group(
        workspace: User, data_connector: DataConnector, kafka_topic: str, kafka_group_id: str
    ):
        if KafkaTbUtils._is_isolated(workspace) and (client := KafkaTbUtils._get_client(workspace)) is not None:
            return await client.get_kafka_topic_group(data_connector, kafka_topic, kafka_group_id)
        else:
            async_get_kafka_topic_group = sync_to_async(KafkaUtils.get_kafka_topic_group)
            return await async_get_kafka_topic_group(
                kafka_topic=kafka_topic, kafka_group_id=kafka_group_id, data_connector=data_connector
            )

    @staticmethod
    def _is_isolated(workspace: User):
        return workspace.kafka_server_group is not None

    @staticmethod
    def _get_client(workspace: User):
        if workspace.kafka_server_group is None:
            return None

        servers = KafkaServerGroupsConfig.get_servers(workspace.kafka_server_group)
        if servers is None or len(servers) == 0:
            return None
        random_server = random.choice(servers)
        return TBAKafkaClient(random_server)


class TBAKafkaClient:
    def __init__(self, url: Optional[str] = None):
        self.http_client = AsyncHTTPClient(defaults=dict(request_timeout=3600.0))
        self.url = url.rstrip("/") if url else "http://localhost:8500"
        self.timeout = 30
        self.default_headers = {"User-Agent": "tb-internal-query", "Content-Type": "application/x-www-form-urlencoded"}

    async def get_preview(
        self,
        data_connector: DataConnector,
        kafka_group_id: Optional[str] = None,
        kafka_topic: Optional[str] = None,
        max_records=KafkaSettings.PREVIEW_MAX_RECORDS,
        preview_activity=True,
        preview_earliest_timestamp=False,
        schema=None,
    ):
        params = {
            "connector_id": data_connector.id,
            "max_records": max_records,
            "preview_activity": preview_activity,
            "preview_earliest_timestamp": preview_earliest_timestamp,
        }
        if kafka_topic:
            params["kafka_topic"] = kafka_topic
        if schema:
            params["schema"] = schema
        if kafka_group_id:
            params["kafka_group_id"] = kafka_group_id

        url = f"{self.url}/preview"
        method = "POST"
        body = urllib.parse.urlencode(params)
        try:
            response: HTTPResponse = await self.http_client.fetch(
                url, method=method, body=body, headers=self.default_headers, request_timeout=self.timeout
            )
            if response.code != 200:
                logging.error(str(response.error))
                return {"error": KafkaPreviewError.connection_error().message}
            return json.loads(response.body)
        except Exception as e:
            logging.error(str(e))
            return {"error": KafkaPreviewError.connection_error().message}

    async def get_kafka_topic_group(self, data_connector: DataConnector, kafka_topic: str, kafka_group_id: str):
        params = {"connector_id": data_connector.id, "kafka_topic": kafka_topic, "kafka_group_id": kafka_group_id}
        url = f"{self.url}/check_group_id"
        method = "POST"
        body = urllib.parse.urlencode(params)
        try:
            response: HTTPResponse = await self.http_client.fetch(
                url, method=method, body=body, headers=self.default_headers, request_timeout=self.timeout
            )
            if response.code != 200:
                return {"error": KafkaPreviewError.connection_error().message}
            return json.loads(response.body)
        except Exception as e:
            logging.error(str(e))
            return {"error": KafkaPreviewError.connection_error().message}


class KafkaUtils:
    @staticmethod
    async def get_kafka_preview(
        data_connector,
        kafka_group_id=None,
        kafka_topics=None,
        max_records=KafkaSettings.PREVIEW_MAX_RECORDS,
        preview_activity=True,
        preview_earliest_timestamp=False,
        schema=None,
    ):
        jsonpaths = None
        if schema:
            parsed_schema = parse_augmented_schema(schema)
            schema = parsed_schema.schema
            jsonpaths = parsed_schema.jsonpaths

        kafka_bootstrap_servers = data_connector.all_settings["kafka_bootstrap_servers"]
        security_protocol = data_connector.all_settings.get("kafka_security_protocol", "SASL_SSL")
        sasl_mechanism = None
        sasl_plain_username = None
        sasl_plain_password = None
        ssl_ca_pem = None
        if security_protocol == "SASL_SSL":
            sasl_mechanism = data_connector.all_settings.get("kafka_sasl_mechanism", "PLAIN")
            sasl_plain_username = data_connector.all_settings["kafka_sasl_plain_username"]
            sasl_plain_password = data_connector.all_settings["kafka_sasl_plain_password"]
            ssl_ca_pem = data_connector.all_settings.get("kafka_ssl_ca_pem", None)
        kafka_schema_registry_url = data_connector.all_settings.get("kafka_schema_registry_url", None)
        kafka_store_headers = data_connector.all_settings.get("kafka_store_headers", False)
        timeout = KafkaSettings.PREVIEW_POLL_TIMEOUT_MS / 1000

        groupid_check_enable = bool(kafka_group_id)
        kafka_group_id = kafka_group_id or "tinybird_temporal_preview"

        key_deserializer = RawDeserializer()
        value_deserializer = StringDeserializer("utf_8")

        if kafka_schema_registry_url:
            escaped_url = escape_password_url(kafka_schema_registry_url)
            schema_registry_conf = {"url": escaped_url}

            schema_registry_client = SchemaRegistryClient(schema_registry_conf)
            avro = AvroDeserializer(schema_registry_client)

            def deserializer(x, ctx):
                return json.dumps(avro(x, ctx), cls=ExtendedJsonEncoder)

            value_deserializer = deserializer

        created_consumers: List[DeserializingConsumer] = []
        earliest_poll_consumers: List[DeserializingConsumer] = []

        def create_consumer(consumers: List[DeserializingConsumer], auto_offset_reset="latest"):
            settings = {
                "enable.auto.commit": False,
                "key.deserializer": key_deserializer,
                "value.deserializer": value_deserializer,
                "group.id": kafka_group_id,
                "bootstrap.servers": kafka_bootstrap_servers,
                "auto.offset.reset": auto_offset_reset,
                "security.protocol": security_protocol,
            }
            if security_protocol == "SASL_SSL":
                settings.update(
                    {
                        "sasl.mechanism": sasl_mechanism,
                        "sasl.username": sasl_plain_username,
                        "sasl.password": sasl_plain_password,
                    }
                )
                if ssl_ca_pem:
                    settings.update({"ssl.ca.pem": re.sub(r"\\n", r"\n", ssl_ca_pem)})

            consumer = DeserializingConsumer(settings)
            consumers.append(consumer)
            return consumer

        consumers = []

        def blocking_io():
            nonlocal kafka_topics
            consumer = create_consumer(consumers=created_consumers)
            consumers.append(consumer)
            topic = ",".join(kafka_topics) if kafka_topics else None
            kafka_topics = [
                topic_metadata for topic_metadata in consumer.list_topics(topic=topic, timeout=timeout).topics.values()
            ]
            return kafka_topics

        loop = asyncio.get_running_loop()
        try:
            kafka_topics = await loop.run_in_executor(None, blocking_io)
        except Exception as e:
            logging.error(f"Could not list topics: {str(e)}")
            return {"error": True}

        async def pool_map(*args, **kwargs):
            def blocking_map():
                return pool.map(*args, **kwargs)

            return await loop.run_in_executor(None, blocking_map)

        try:
            pool = multiprocessing.dummy.Pool(PREVIEW_POOL_SIZE)

            for w in pool._pool:
                w.name = w.name.replace("Thread", "ThreadPoolPreview")

            topics_for_group_id = []
            if groupid_check_enable:
                try:
                    get_topics_for_group_id = functools.partial(
                        get_kafka_groupid_active_topics,
                        kafka_bootstrap_servers,
                        security_protocol,
                        kafka_group_id,
                        sasl_mechanism,
                        sasl_plain_username,
                        sasl_plain_password,
                        ssl_ca_pem,
                    )
                    topics_for_group_id = await loop.run_in_executor(None, get_topics_for_group_id)
                except AssigmentDecodeException as e:
                    logging.error(f"AssigmentDecodeException: {e}")

            def topic_preview(kafka_topic):
                if kafka_topic.topic in set(topics_for_group_id):
                    return {"error": "group_id_already_active_for_topic"}
                if not preview_activity:
                    return {
                        "topic": kafka_topic.topic,
                    }

                consumer = consumers.pop() if consumers else create_consumer(consumers=created_consumers)

                topic = kafka_topic.topic
                partitions = kafka_topic.partitions

                if not partitions:
                    return {"topic": kafka_topic.topic, "error": "not_exists"}

                topic_partitions = [TopicPartition(topic, partition) for partition in partitions]

                t_cmp = int((datetime.now() - timedelta(minutes=60)).timestamp() * 1000)

                def f(topic_partition):
                    try:
                        return {topic_partition: consumer.get_watermark_offsets(topic_partition, timeout=timeout)}
                    except KafkaException:
                        return {}

                watermarks = reduce(lambda x, y: {**x, **y}, pool.map(f, topic_partitions, 1))
                if len(watermarks) != len(topic_partitions):
                    return {
                        "topic": topic,
                    }

                skip_last_messages = True

                if max_records > 0:
                    topic_partition_offsets = []

                    for topic_partition, watermark in watermarks.items():
                        begin = watermark[0]
                        end = watermark[1]
                        offset = max(begin, end - max_records)
                        topic_partition_offset = TopicPartition(
                            topic_partition.topic, topic_partition.partition, offset
                        )
                        topic_partition_offsets.append(topic_partition_offset)

                        if begin < end:
                            skip_last_messages = False

                    if not skip_last_messages:
                        consumer.assign(topic_partition_offsets)

                messages = []

                if not skip_last_messages:
                    for _i in range(max_records):
                        try:
                            record = consumer.poll(timeout=timeout)
                        except KafkaException as e:
                            logging.error(f"Kafka Preview consumer.poll() exception (code {e.code}): {e}")
                            if e.code == KafkaError.GROUP_AUTHORIZATION_FAILED:
                                return {"topic": kafka_topic.topic, "error": "consume_failed_auth_groupid_failed"}
                            elif e.code == KafkaError._VALUE_DESERIALIZATION:
                                return {
                                    "topic": kafka_topic.topic,
                                    "error": "message_not_produced_with_confluent_schema_registry",
                                }
                            return {"topic": kafka_topic.topic, "error": "consume_failed"}
                        if record is None:
                            break
                        if record.value() is None:
                            continue

                        headers = (
                            orjson.dumps({k: decode_header_value(v) for k, v in record.headers()})
                            if record.headers()
                            else b""
                        )
                        messages.append(
                            {
                                "__timestamp": record.timestamp()[1] // 1000,
                                "__topic": str(record.topic()),
                                "__partition": record.partition(),
                                "__offset": record.offset(),
                                "__key": record.key(),
                                "__value": record.value(),
                                "__headers": headers.decode("utf-8"),
                            }
                        )

                def off(offset, ending):
                    if offset < 0:
                        return ending
                    return offset

                timestamps = [TopicPartition(topic, partition, t_cmp) for partition in partitions]
                try:
                    offsets_for_times = consumer.offsets_for_times(timestamps, timeout)
                    offsets = {x: x.offset for x in offsets_for_times}
                    messages_in_last_hour = sum(
                        [
                            watermark[1] - off(offsets[topic_partition], watermark[1])
                            for topic_partition, watermark in watermarks.items()
                        ]
                    )
                except KafkaException:
                    messages_in_last_hour = -1

                try:
                    committed_partitions = consumer.committed([TopicPartition(topic, p) for p in partitions], timeout)
                    committed = any(map(lambda x: x.offset >= 0, committed_partitions))
                except KafkaException:
                    committed = None

                consumers.append(consumer)

                return {
                    "topic": topic,
                    "partitions": len(partitions),
                    "last_messages": messages,
                    "messages_in_last_hour": messages_in_last_hour,
                    "committed": committed,
                }

            preview = await pool_map(topic_preview, kafka_topics, 1)
            await pool_map(lambda consumer: consumer.close, created_consumers)

            if any(map(lambda x: x.get("error"), preview)):
                return next(x for x in preview if x.get("error"))

            def get_earliest_timestamp(kafka_topic):
                try:
                    consumer = (
                        earliest_poll_consumers.pop()
                        if earliest_poll_consumers
                        else create_consumer(earliest_poll_consumers, "earliest")
                    )
                    topic = kafka_topic.topic
                    partitions = kafka_topic.partitions
                    first_messages_topic_partition = [
                        TopicPartition(topic, partition, OFFSET_BEGINNING) for partition in partitions
                    ]
                    consumer.assign(first_messages_topic_partition)
                    earliest_message = consumer.poll(timeout=EARLIEST_POLL_TIMEOUT_SECONDS)

                    if not earliest_message:
                        return [topic, ""]

                    earliest_message_timestamp = _parse_record_timestamp(earliest_message)
                    return [topic, earliest_message_timestamp]
                except Exception as e:
                    return {"topic": kafka_topic.topic, "error": repr(e)}

            async def deserialize(topic):
                if topic.get("last_messages", None) is None:
                    return topic
                nonlocal jsonpaths, schema
                if not jsonpaths:
                    messages = [msg["__value"] for msg in topic["last_messages"]]
                    rows = []
                    for msg in messages:
                        try:
                            rows.append(orjson.loads(msg))
                        except orjson.JSONDecodeError:
                            pass
                    analysis = await analyze(rows)
                    if not analysis:
                        return topic
                    topic["analysis"] = analysis
                    schema = analysis["schema"]
                    parsed_schema = parse_augmented_schema(schema)
                    schema = parsed_schema.schema
                    jsonpaths = parsed_schema.jsonpaths

                json_conf = json_deserialize_merge_schema_jsonpaths(parse_table_structure(schema), jsonpaths)
                extended_json_deserialization = extend_json_deserialization(json_conf)
                try:
                    topic["deserialized"] = await kafka_preview(
                        extended_json_deserialization, topic["last_messages"], kafka_store_headers
                    )
                    return topic
                except Exception as e:
                    topic["error"] = f"Unexpected error while deserializing: {e}\nTraceback: {traceback.format_exc()}"
                    return topic

            preview = [await deserialize(x) for x in preview]

            response = {"preview": preview}

            if preview_earliest_timestamp:
                earliest_timestamps = await pool_map(get_earliest_timestamp, kafka_topics, 1)
                for x in earliest_timestamps:
                    if type(x) == dict and x.get("error", False):  # noqa: E721
                        return x
                response = {
                    "preview": preview,
                    "earliest": [{"name": x[0], "timestamp": x[1]} for x in earliest_timestamps if x],
                }
            preview_error = next((x for x in preview if x.get("error", None)), None)
            if preview_error:
                response["error"] = preview_error

            for topic in response["preview"]:
                for msg in topic.get("last_messages", []):
                    if isinstance(msg["__key"], bytes):
                        msg["__key"] = msg["__key"].decode("utf-8", "replace")
            return response

        finally:
            if pool:
                await pool_map(lambda consumer: consumer.close, created_consumers)
                await pool_map(lambda consumer: consumer.close, earliest_poll_consumers)
                pool.close()

    @staticmethod
    def get_kafka_topic_group(data_connector, kafka_topic, kafka_group_id):
        sasl_mechanism = None
        sasl_plain_username = None
        sasl_plain_password = None
        ssl_ca_pem = None

        kafka_bootstrap_servers = data_connector.all_settings["kafka_bootstrap_servers"]
        security_protocol = data_connector.all_settings.get("kafka_security_protocol", "SASL_SSL")

        if security_protocol == "SASL_SSL":
            sasl_mechanism = data_connector.all_settings.get("kafka_sasl_mechanism", "PLAIN")
            sasl_plain_username = data_connector.all_settings["kafka_sasl_plain_username"]
            sasl_plain_password = data_connector.all_settings["kafka_sasl_plain_password"]
            ssl_ca_pem = data_connector.all_settings.get("kafka_ssl_ca_pem", None)

        retries = 3
        for retry in range(0, retries):
            try:
                topics_for_group_id = get_kafka_groupid_active_topics(
                    kafka_bootstrap_servers,
                    security_protocol,
                    kafka_group_id,
                    sasl_mechanism,
                    sasl_plain_username,
                    sasl_plain_password,
                    ssl_ca_pem,
                )

                if kafka_topic in set(topics_for_group_id):
                    return {"error": "group_id_already_active_for_topic"}

                return {"response": "ok"}
            except AssigmentDecodeException as e:
                logging.error(f"AssigmentDecodeException: {e}")
                return {"error": "metadata_protocol_error"}
            except Exception as e:
                if retry < retries - 1:
                    time.sleep(0.25)
                    continue
                logging.error(f"Error connecting to Kafka Broker: {e}")
                return {"error": "connection_error"}


def get_kafka_groupid_active_topics(
    kafka_bootstrap_servers,
    security_protocol,
    kafka_group_id,
    sasl_mechanism=None,
    sasl_plain_username=None,
    sasl_plain_password=None,
    ssl_ca_pem=None,
) -> List[str]:
    settings = {
        "bootstrap.servers": kafka_bootstrap_servers,
        "security.protocol": security_protocol,
    }
    if security_protocol == "SASL_SSL":
        settings.update(
            {
                "sasl.mechanism": sasl_mechanism,
                "sasl.username": sasl_plain_username,
                "sasl.password": sasl_plain_password,
            }
        )
        if ssl_ca_pem:
            settings.update({"ssl.ca.pem": ssl_ca_pem})
    timeout = KafkaSettings.PREVIEW_POLL_TIMEOUT_MS / 1000
    admin = AdminClient(settings)
    admin_groups = admin.list_groups(timeout=timeout)
    group = [x for x in admin_groups if x.id == kafka_group_id]
    if not group:
        return []
    group_metadata = group[0]

    def decode(x):
        # Some Kafka implementations store the assignment in the metadata field
        try:
            return decode_assignment(x.assignment)
        except AssigmentDecodeException:
            try:
                return decode_assignment(x.metadata)
            except Exception:
                pass
            raise

    topics: List[str] = sum(list(map(decode, group_metadata.members)), [])  # noqa: RUF017
    return topics


class AssigmentDecodeException(Exception):
    pass


def decode_assignment(a: bytes) -> List[str]:
    """ "
    >>> decode_assignment(b'\\x00\\x00\\x00\\x00\\x00\\x01\\x00\\x0fdavid_perf_test\\x00\\x00\\x00\\x06\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x03\\x00\\x00\\x00\\x04\\x00\\x00\\x00\\x05\\x00\\x00\\x00\\x00')
    ['david_perf_test']
    >>> decode_assignment(b'\\x00\\x00\\x00\\x00\\x00\\x01\\x00\\x04t_09\\x00\\x00\\x00\\x06\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x03\\x00\\x00\\x00\\x04\\x00\\x00\\x00\\x05\\x00\\x00\\x00\\x00')
    ['t_09']
    """
    version = struct.unpack("!h", a[:2])[0]
    if version not in {0, 1}:
        raise AssigmentDecodeException(f"Protocol version not supported, supported=0, found={version}")
    a = a[2:]
    num_topics = struct.unpack("!i", a[:4])[0]
    if num_topics != 1:
        raise AssigmentDecodeException(f"Unimplemented: unexpected number of topics, num_topics={num_topics}")
    a = a[4:]
    topics = []
    i = 0
    while i < num_topics:
        topic_len = struct.unpack("!h", a[:2])[0]
        a = a[2:]
        topic = a[:topic_len].decode("utf-8", "replace")
        topics.append(topic)
        a = a[topic_len:]
        i += 1
    return topics


def _parse_record_timestamp(message):
    if not message:
        return ""
    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
    timestamp_in_seconds = message.timestamp()[1] / 1000
    return datetime.utcfromtimestamp(timestamp_in_seconds).strftime(TIMESTAMP_FORMAT)


def decode_header_value(value):
    """
    >>> decode_header_value("")
    ''
    >>> decode_header_value("some text")
    'some text'
    >>> decode_header_value("some text".encode("utf-8"))
    'some text'
    >>> decode_header_value((1234).to_bytes(4, byteorder='big'))
    1234
    >>> decode_header_value("some text".encode("utf-16"))
    ''
    """

    try:
        if len(value) == 0:
            return ""
        elif isinstance(value, bytes):
            try:
                return value.decode("utf-8")
            except UnicodeDecodeError:
                return struct.unpack(">i", value)[0]
        elif isinstance(value, str):
            return value
        else:
            return str(value)
    except Exception as e:
        logging.warning(f"Error decoding Kafka value: {str(value)}. {e}")
        return ""
