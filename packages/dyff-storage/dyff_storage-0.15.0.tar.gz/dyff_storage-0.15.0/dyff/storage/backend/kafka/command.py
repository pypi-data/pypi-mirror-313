# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

# mypy: disable-error-code="import-untyped"
import json
from typing import Optional, TypeVar

import pydantic
from confluent_kafka import Producer

from dyff.schema import ids
from dyff.schema.platform import (
    Audit,
    Dataset,
    DataSource,
    DyffEntity,
    DyffEntityType,
    EntityStatus,
    EntityStatusReason,
    Evaluation,
    Family,
    FamilyMembers,
    InferenceService,
    InferenceSession,
    Labeled,
    Measurement,
    Method,
    Model,
    Module,
    Report,
    SafetyCase,
)
from dyff.storage import timestamp
from dyff.storage.config import config
from dyff.storage.typing import YAMLObject

from ..base.command import CommandBackend


def serialize_id(id: str) -> bytes:
    return id.encode("utf-8")


def serialize_value(value: YAMLObject) -> bytes:
    return json.dumps(value).encode("utf-8")


def serialize_entity(entity: DyffEntity) -> bytes:
    return entity.json().encode("utf-8")


def deserialize_id(id: bytes) -> str:
    return id.decode("utf-8")


def deserialize_value(value: bytes) -> YAMLObject:
    return json.loads(value.decode("utf-8"))


def deserialize_entity(entity: bytes) -> DyffEntityType:
    s = entity.decode("utf-8")
    # DyffEntityType is a pydantic "discriminated union", so pydantic infers
    # the type from the '.kind' field
    return pydantic.parse_raw_as(DyffEntityType, s)  # type: ignore


EntityT = TypeVar("EntityT", bound=DyffEntity)


class KafkaCommandBackend(CommandBackend):
    def __init__(self):
        self.events_topic = config.kafka.topics.workflows_events
        producer_config = config.kafka.config.get_producer_config()
        # FIXME: This should be the global default. It's supposed to be the
        # default in Kafka > 3.0, but the docs of librdkafka suggest that
        # its default is still False.
        # See: https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md
        producer_config["enable.idempotence"] = True
        # FIXME: See comment in alignmentlabs.dyff.web.server
        # Can't get real logging to work when running in uvicorn
        print(
            f"Creating KafkaCommandBackend with config:\n{json.dumps(producer_config, indent=2)}",
            flush=True,
        )
        # logging.info(f"Creating KafkaCommandBackend with config:\n{json.dumps(producer_config, indent=2)}")
        self._kafka_producer = Producer(producer_config)

    def _copy_and_add_system_fields(self, entity: EntityT) -> EntityT:
        entity = entity.copy()
        entity.creationTime = timestamp.now()
        entity.status = EntityStatus.created
        entity.id = ids.generate_entity_id()
        return entity

    def _produce_create_event(self, entity: EntityT) -> EntityT:
        entity = self._copy_and_add_system_fields(entity)
        assert entity.id is not None
        self._kafka_producer.produce(
            topic=self.events_topic,
            value=serialize_entity(entity),
            key=serialize_id(entity.id),
        )
        return entity

    def _produce_terminate_event(self, id: str) -> None:
        update = {
            "status": EntityStatus.terminated,
            "reason": EntityStatusReason.terminate_command,
        }
        self._kafka_producer.produce(
            topic=self.events_topic,
            value=serialize_value(update),
            key=serialize_id(id),
        )

    def update_status(
        self, id: str, *, status: str, reason: Optional[str] = None
    ) -> None:
        """Update the status of an entity.

        :param id: The entity .id
        :type id: str
        :param status: New .status value
        :type status: str
        :param reason: New .reason value
        :type reason: Optional[str]
        """
        update = {
            "status": status,
            "reason": reason,
        }
        self._kafka_producer.produce(
            topic=self.events_topic,
            value=serialize_value(update),
            key=serialize_id(id),
        )

    def update_labels(self, id: str, labels: Labeled) -> None:
        """Updated the labels of a labeled entity.

        :param id: The ID of the entity to update.
        :type id: str
        :param labels: The labels to update.
        :type labels: Labeled
        """
        update = labels.dict()
        self._kafka_producer.produce(
            topic=self.events_topic, value=serialize_value(update), key=serialize_id(id)
        )

    def update_family_members(self, id: str, members: FamilyMembers) -> None:
        """Updated the members of a Family.

        :param id: The ID of the Family to update.
        :type id: str
        :param members: The members to update.
        :type members: FamilyMembers
        """
        update = members.dict()
        self._kafka_producer.produce(
            topic=self.events_topic, value=serialize_value(update), key=serialize_id(id)
        )

    # def update_documentation(self, documentation_id: str, documentation: DocumentationBase):
    #     edit_dict = documentation.dict(exclude_unset=True)
    #     result = collection.find_one_and_update(
    #         {"_id": id},
    #         {"$set": edit_dict},
    #         upsert=True,
    #         return_document=pymongo.ReturnDocument.AFTER,
    #     )
    #     if result is None:
    #         return None
    #     del result["_id"]
    #     return Documentation.parse_obj(result)

    def create_audit(self, spec: Audit) -> Audit:
        """Create a new Audit entity in the system.

        :param spec: Specification of the Audit. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Audit
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Audit
        """
        return self._produce_create_event(spec)

    def create_data_source(self, spec: DataSource) -> DataSource:
        """Create a new DataSource entity in the system.

        :param spec: Specification of the DataSource. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: DataSource
        :return: A copy of ``spec`` with all system fields set.
        :rtype: DataSource
        """
        return self._produce_create_event(spec)

    def create_dataset(self, spec: Dataset) -> Dataset:
        """Create a new Dataset entity in the system.

        :param spec: Specification of the Dataset. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Dataset
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Dataset
        """
        return self._produce_create_event(spec)

    def create_evaluation(self, spec: Evaluation) -> Evaluation:
        """Create a new Evaluation entity in the system.

        :param spec: Specification of the Evaluation. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Evaluation
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Evaluation
        """
        return self._produce_create_event(spec)

    def create_family(self, spec: Family) -> Family:
        """Create a new Family entity in the system.

        :param spec: Specification of the Family. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Family
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Family
        """
        return self._produce_create_event(spec)

    def create_inference_service(self, spec: InferenceService) -> InferenceService:
        """Create a new InferenceService entity in the system.

        :param spec: Specification of the InferenceService. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: InferenceService
        :return: A copy of ``spec`` with all system fields set.
        :rtype: InferenceService
        """
        return self._produce_create_event(spec)

    def create_inference_session(self, spec: InferenceSession) -> InferenceSession:
        """Create a new InferenceSession entity in the system.

        :param spec: Specification of the InferenceSession. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: InferenceSession
        :return: A copy of ``spec`` with all system fields set.
        :rtype: InferenceSession
        """
        return self._produce_create_event(spec)

    def create_measurement(self, spec: Measurement) -> Measurement:
        """Create a new Measurement entity in the system.

        :param spec: Specification of the Measurement. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Measurement
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Measurement
        """
        return self._produce_create_event(spec)

    def create_method(self, spec: Method) -> Method:
        """Create a new Method entity in the system.

        :param spec: Specification of the Method. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Method
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Method
        """
        return self._produce_create_event(spec)

    def create_model(self, spec: Model) -> Model:
        """Create a new Model entity in the system.

        :param spec: Specification of the Model. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Model
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Model
        """
        return self._produce_create_event(spec)

    def create_module(self, spec: Module) -> Module:
        """Create a new Module entity in the system.

        :param spec: Specification of the Module. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Module
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Module
        """
        return self._produce_create_event(spec)

    def create_report(self, spec: Report) -> Report:
        """Create a new Report entity in the system.

        :param spec: Specification of the Report. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Report
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Report
        """
        return self._produce_create_event(spec)

    def create_safetycase(self, spec: SafetyCase) -> SafetyCase:
        """Create a new SafetyCase entity in the system.

        :param spec: Specification of the SafetyCase. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: SafetyCase
        :return: A copy of ``spec`` with all system fields set.
        :rtype: SafetyCase
        """
        return self._produce_create_event(spec)
