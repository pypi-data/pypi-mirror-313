from typing import Any, Literal, Mapping, TypedDict, overload

from pydantic import BaseModel
from typing_extensions import NotRequired, Unpack

from toloka.a9s.client.models.generated.ai.toloka.experts.portal.money.repository.config import (
    MoneyConfigCommonSettings,
    MoneyConfigSnippetSettings,
    MoneyConfigStatusWorkflowSettingsStatusWorkflowMutableTransition,
    MoneyConfigStatusWorkflowSettingsStatusWorkflowPaidTransition,
)
from toloka.a9s.client.models.money_config import (
    MoneyConfigAnnotationSettingsStrict,
    MoneyConfigFormStrict,
    MoneyConfigStatusWorkflowSettingsStrict,
)


class StatusTransitionPayment(BaseModel):
    price: float
    portal_review_result: Literal['ACCEPTED', 'REJECTED']


StatusTransitionPayments = Mapping[str, StatusTransitionPayment]


class StatusTransitionMutablePayment(BaseModel):
    price: float


StatusTransitionMutablePayments = Mapping[str, StatusTransitionMutablePayment]


class BaseBuildStatusWorkflowMoneyConfigFormParams(TypedDict):
    snippet_price: float
    currency: Literal['BU', 'USD']
    mutable_transitions: StatusTransitionMutablePayments
    paid_transitions: StatusTransitionPayments
    tenant_id: NotRequired[str | None]
    skip_pending_balance: NotRequired[bool]


class BuildStatusWorkflowMoneyConfigFormParams(BaseBuildStatusWorkflowMoneyConfigFormParams):
    requester_id: str
    name: str


class BuildStatusWorkflowMoneyConfigFormParamsWithDefaults(TypedDict):
    requester_id: str
    name: str
    snippet_price: float
    currency: Literal['BU', 'USD']
    mutable_transitions: StatusTransitionMutablePayments
    paid_transitions: StatusTransitionPayments
    tenant_id: str | None
    skip_pending_balance: bool


def apply_build_status_workflow_money_config_form_defaults(
    params: BuildStatusWorkflowMoneyConfigFormParams,
) -> BuildStatusWorkflowMoneyConfigFormParamsWithDefaults:
    return {
        'tenant_id': None,
        'skip_pending_balance': False,
        **params,
    }


def build_status_workflow_money_config_form(
    **kwargs: Unpack[BuildStatusWorkflowMoneyConfigFormParams],
) -> MoneyConfigFormStrict:
    with_defaults = apply_build_status_workflow_money_config_form_defaults(kwargs)

    return MoneyConfigFormStrict(
        name=with_defaults['name'],
        currency=with_defaults['currency'],
        requester_id=with_defaults['requester_id'],
        snippet_settings=MoneyConfigSnippetSettings(price=with_defaults['snippet_price']),
        common_settings=MoneyConfigCommonSettings(skip_pending_balance=with_defaults['skip_pending_balance']),
        specific_settings=MoneyConfigStatusWorkflowSettingsStrict(
            mutable_transitions=[
                MoneyConfigStatusWorkflowSettingsStatusWorkflowMutableTransition(
                    to_status=status,
                    price=transition.price,
                )
                for status, transition in with_defaults['mutable_transitions'].items()
            ],
            paid_transitions=[
                MoneyConfigStatusWorkflowSettingsStatusWorkflowPaidTransition(
                    to_status=status,
                    price=transition.price,
                    portal_review_result=transition.portal_review_result,
                )
                for status, transition in with_defaults['paid_transitions'].items()
            ],
        ),
        tenant_id=with_defaults['tenant_id'],
    )


class BaseAnnotationMoneyConfigFormParams(TypedDict):
    price: float
    currency: Literal['BU', 'USD']
    tenant_id: NotRequired[str | None]
    skip_pending_balance: NotRequired[bool]


class AnnotationMoneyConfigFormParams(BaseAnnotationMoneyConfigFormParams):
    requester_id: str
    name: str


class AnnotationMoneyConfigFormParamsWithDefaults(TypedDict):
    requester_id: str
    name: str
    price: float
    currency: Literal['BU', 'USD']
    tenant_id: str | None
    skip_pending_balance: bool


def apply_annotation_money_config_form_defaults(
    params: AnnotationMoneyConfigFormParams,
) -> AnnotationMoneyConfigFormParamsWithDefaults:
    return {
        'tenant_id': None,
        'skip_pending_balance': False,
        **params,
    }


def build_annotation_money_config_form(
    **kwargs: Unpack[AnnotationMoneyConfigFormParams],
) -> MoneyConfigFormStrict:
    with_defaults = apply_annotation_money_config_form_defaults(kwargs)

    return MoneyConfigFormStrict(
        name=with_defaults['name'],
        currency=with_defaults['currency'],
        requester_id=with_defaults['requester_id'],
        snippet_settings=MoneyConfigSnippetSettings(price=with_defaults['price']),
        common_settings=MoneyConfigCommonSettings(skip_pending_balance=with_defaults['skip_pending_balance']),
        specific_settings=MoneyConfigAnnotationSettingsStrict(price=with_defaults['price']),
        tenant_id=with_defaults['tenant_id'],
    )


@overload
def build_form_from_base_parameters(
    name: str,
    requester_id: str,
    **kwargs: Unpack[BaseBuildStatusWorkflowMoneyConfigFormParams],
) -> MoneyConfigFormStrict: ...


@overload
def build_form_from_base_parameters(
    name: str,
    requester_id: str,
    **kwargs: Unpack[BaseAnnotationMoneyConfigFormParams],
) -> MoneyConfigFormStrict: ...


def build_form_from_base_parameters(
    name: str,
    requester_id: str,
    **kwargs: Any,
) -> MoneyConfigFormStrict:
    if 'mutable_transitions' in kwargs:
        return build_status_workflow_money_config_form(
            name=name,
            requester_id=requester_id,
            **kwargs,
        )
    return build_annotation_money_config_form(
        name=name,
        requester_id=requester_id,
        **kwargs,
    )
