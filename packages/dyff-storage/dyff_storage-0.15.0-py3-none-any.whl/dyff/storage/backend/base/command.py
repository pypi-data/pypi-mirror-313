# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

import abc
from typing import Optional

from dyff.schema.platform import (
    Audit,
    Dataset,
    DataSource,
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


class CommandBackend(abc.ABC):
    @abc.abstractmethod
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

    @abc.abstractmethod
    def update_labels(self, id: str, labels: Labeled) -> None:
        """Updated the labels of a labeled entity.

        :param id: The ID of the entity to update.
        :type id: str
        :param labels: The labels to update.
        :type labels: Labeled
        """

    @abc.abstractmethod
    def update_family_members(self, id: str, members: FamilyMembers) -> None:
        """Updated the members of a Family.

        :param id: The ID of the Family to update.
        :type id: str
        :param members: The members to update.
        :type members: FamilyMembers
        """

    @abc.abstractmethod
    def create_audit(self, spec: Audit) -> Audit:
        """Create a new Audit entity in the system.

        :param spec: Specification of the Audit. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Audit
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Audit
        """

    @abc.abstractmethod
    def create_data_source(self, spec: DataSource) -> DataSource:
        """Create a new DataSource entity in the system.

        :param spec: Specification of the DataSource. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: DataSource
        :return: A copy of ``spec`` with all system fields set.
        :rtype: DataSource
        """

    @abc.abstractmethod
    def create_dataset(self, spec: Dataset) -> Dataset:
        """Create a new Dataset entity in the system.

        :param spec: Specification of the Dataset. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Dataset
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Dataset
        """

    @abc.abstractmethod
    def create_evaluation(self, spec: Evaluation) -> Evaluation:
        """Create a new Evaluation entity in the system.

        :param spec: Specification of the Evaluation. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Evaluation
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Evaluation
        """

    @abc.abstractmethod
    def create_family(self, spec: Family) -> Family:
        """Create a new Family entity in the system.

        :param spec: Specification of the Family. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Family
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Family
        """

    @abc.abstractmethod
    def create_inference_service(self, spec: InferenceService) -> InferenceService:
        """Create a new InferenceService entity in the system.

        :param spec: Specification of the InferenceService. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: InferenceService
        :return: A copy of ``spec`` with all system fields set.
        :rtype: InferenceService
        """

    @abc.abstractmethod
    def create_inference_session(self, spec: InferenceSession) -> InferenceSession:
        """Create a new InferenceSession entity in the system.

        :param spec: Specification of the InferenceSession. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: InferenceSession
        :return: A copy of ``spec`` with all system fields set.
        :rtype: InferenceSession
        """

    @abc.abstractmethod
    def create_measurement(self, spec: Measurement) -> Measurement:
        """Create a new Measurement entity in the system.

        :param spec: Specification of the Measurement. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Measurement
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Measurement
        """

    @abc.abstractmethod
    def create_method(self, spec: Method) -> Method:
        """Create a new Method entity in the system.

        :param spec: Specification of the Method. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Method
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Method
        """

    @abc.abstractmethod
    def create_model(self, spec: Model) -> Model:
        """Create a new Model entity in the system.

        :param spec: Specification of the Model. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Model
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Model
        """

    @abc.abstractmethod
    def create_module(self, spec: Module) -> Module:
        """Create a new Module entity in the system.

        :param spec: Specification of the Module. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Module
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Module
        """

    @abc.abstractmethod
    def create_report(self, spec: Report) -> Report:
        """Create a new Report entity in the system.

        :param spec: Specification of the Report. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: Report
        :return: A copy of ``spec`` with all system fields set.
        :rtype: Report
        """

    @abc.abstractmethod
    def create_safetycase(self, spec: SafetyCase) -> SafetyCase:
        """Create a new SafetyCase entity in the system.

        :param spec: Specification of the SafetyCase. The system fields of the spec
            such as ``.id`` must be **unset**.
        :type spec: SafetyCase
        :return: A copy of ``spec`` with all system fields set.
        :rtype: SafetyCase
        """

    def terminate_workflow(self, id: str) -> None:
        """Terminate a running workflow.

        :param id: The ID of the workflow.
        :type id: str
        """
        self.update_status(
            id,
            status=EntityStatus.terminated,
            reason=EntityStatusReason.terminate_command,
        )

    def delete_entity(self, id: str) -> None:
        """Delete an existing entity.

        :param id: The ID of the entity.
        :type id: str
        """
        self.update_status(
            id,
            status=EntityStatus.deleted,
            reason=EntityStatusReason.delete_command,
        )
