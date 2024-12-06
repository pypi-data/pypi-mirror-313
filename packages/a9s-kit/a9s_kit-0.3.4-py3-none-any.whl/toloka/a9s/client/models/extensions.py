from typing import TypeVar, cast

from toloka.a9s.client.models.batch import (
    BatchCreateFormV1Strict,
    BatchUpdateFormV1ExtensionInstanceConfigV1Strict,
    BatchUpdateFormV1ExtensionsV1Strict,
    BatchUpdateFormV1Strict,
)
from toloka.a9s.client.models.extension_id import (
    GROUND_TRUTH_EXTENSION_ID,
    MONEY_CONFIG_EXTENSION_ID,
    QUALITY_CONFIG_EXTENSION_ID,
    ExtensionId,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.project.web.v1.form import ProjectFormV1
from toloka.a9s.client.models.project import (
    ProjectExtensionInstanceConfigViewFormV1Strict,
    ProjectExtensionsViewFormV1Strict,
    ProjectFormV1Strict,
)
from toloka.a9s.client.models.types import MoneyConfigId


def add_extension_to_project_form(
    project_form: ProjectFormV1, extension_id: ExtensionId, instance_id: str
) -> ProjectFormV1Strict:
    project_form_strict = ProjectFormV1Strict.model_validate(project_form, from_attributes=True).model_copy(deep=True)

    current_instances = list(project_form_strict.extensions.instances)
    current_instances.append(
        ProjectExtensionInstanceConfigViewFormV1Strict(
            extension_id=extension_id,
            instance_id=instance_id,
        )
    )

    project_form_strict.extensions.instances = current_instances
    return project_form_strict


def with_money_config_extension_project(
    project_form: ProjectFormV1,
    money_config_id: MoneyConfigId,
) -> ProjectFormV1Strict:
    return add_extension_to_project_form(
        project_form=project_form,
        extension_id=MONEY_CONFIG_EXTENSION_ID,
        instance_id=str(money_config_id),
    )


def with_ground_truth_extension_project(
    project_form: ProjectFormV1,
    ground_truth_config_id: str,
) -> ProjectFormV1Strict:
    return add_extension_to_project_form(
        project_form=project_form,
        extension_id=GROUND_TRUTH_EXTENSION_ID,
        instance_id=ground_truth_config_id,
    )


def with_quality_config_extension_project(
    project_form: ProjectFormV1,
    quality_config_id: str,
) -> ProjectFormV1Strict:
    return add_extension_to_project_form(
        project_form=project_form,
        extension_id=QUALITY_CONFIG_EXTENSION_ID,
        instance_id=quality_config_id,
    )


BatchFormType = TypeVar('BatchFormType', bound=BatchCreateFormV1Strict | BatchUpdateFormV1Strict)


def add_extension_to_batch_form(
    batch_form: BatchFormType,
    extension_id: ExtensionId,
    instance_id: str,
) -> BatchFormType:
    batch_form_copy: BatchFormType = cast(BatchFormType, batch_form.model_copy())

    current_instances = list(batch_form_copy.extensions.instances)
    current_instances.append(
        BatchUpdateFormV1ExtensionInstanceConfigV1Strict(
            extension_id=extension_id,
            instance_id=instance_id,
        )
    )

    batch_form_copy.extensions.instances = current_instances
    return batch_form_copy


def remove_extension_from_batch_form(
    batch_form: BatchFormType,
    extension_id: ExtensionId,
) -> BatchFormType:
    batch_form_copy: BatchFormType = cast(BatchFormType, batch_form.model_copy())

    current_instances = [
        instance for instance in batch_form_copy.extensions.instances if instance.extension_id != extension_id
    ]

    batch_form_copy.extensions.instances = current_instances
    return batch_form_copy


def with_money_config_extension_batch(
    batch_form: BatchFormType,
    money_config_id: MoneyConfigId,
) -> BatchFormType:
    return add_extension_to_batch_form(
        batch_form=batch_form,
        extension_id=MONEY_CONFIG_EXTENSION_ID,
        instance_id=str(money_config_id),
    )


def with_ground_truth_extension_batch(
    batch_form: BatchFormType,
    ground_truth_config_id: str,
) -> BatchFormType:
    return add_extension_to_batch_form(
        batch_form=batch_form,
        extension_id='ground-truth',
        instance_id=ground_truth_config_id,
    )


def with_quality_config_extension_batch(
    batch_form: BatchFormType,
    quality_config_id: str,
) -> BatchFormType:
    return add_extension_to_batch_form(
        batch_form=batch_form,
        extension_id='quality-management',
        instance_id=quality_config_id,
    )


def find_extension_instance_id(
    project: ProjectExtensionsViewFormV1Strict | BatchUpdateFormV1ExtensionsV1Strict,
    extension_id: ExtensionId,
) -> str | None:
    matched_instances = [instance for instance in project.instances if instance.extension_id == extension_id]
    if len(matched_instances) > 1:
        raise ValueError(f'Multiple instances of extension {extension_id} found in project')
    if matched_instances:
        return matched_instances[0].instance_id
    return None
