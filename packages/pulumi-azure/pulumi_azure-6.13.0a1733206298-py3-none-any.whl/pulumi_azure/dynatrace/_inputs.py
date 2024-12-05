# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from .. import _utilities

__all__ = [
    'MonitorIdentityArgs',
    'MonitorIdentityArgsDict',
    'MonitorPlanArgs',
    'MonitorPlanArgsDict',
    'MonitorUserArgs',
    'MonitorUserArgsDict',
]

MYPY = False

if not MYPY:
    class MonitorIdentityArgsDict(TypedDict):
        type: pulumi.Input[str]
        """
        The type of identity used for the resource. Only possible value is `SystemAssigned`.
        """
        principal_id: NotRequired[pulumi.Input[str]]
        tenant_id: NotRequired[pulumi.Input[str]]
elif False:
    MonitorIdentityArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class MonitorIdentityArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 principal_id: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] type: The type of identity used for the resource. Only possible value is `SystemAssigned`.
        """
        pulumi.set(__self__, "type", type)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of identity used for the resource. Only possible value is `SystemAssigned`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)


if not MYPY:
    class MonitorPlanArgsDict(TypedDict):
        plan: pulumi.Input[str]
        """
        Plan id as published by Dynatrace.
        """
        billing_cycle: NotRequired[pulumi.Input[str]]
        """
        Different billing cycles. Possible values are `MONTHLY` and `WEEKLY`.
        """
        effective_date: NotRequired[pulumi.Input[str]]
        """
        Date when plan was applied.
        """
        usage_type: NotRequired[pulumi.Input[str]]
        """
        Different usage type. Possible values are `PAYG` and `COMMITTED`.
        """
elif False:
    MonitorPlanArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class MonitorPlanArgs:
    def __init__(__self__, *,
                 plan: pulumi.Input[str],
                 billing_cycle: Optional[pulumi.Input[str]] = None,
                 effective_date: Optional[pulumi.Input[str]] = None,
                 usage_type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] plan: Plan id as published by Dynatrace.
        :param pulumi.Input[str] billing_cycle: Different billing cycles. Possible values are `MONTHLY` and `WEEKLY`.
        :param pulumi.Input[str] effective_date: Date when plan was applied.
        :param pulumi.Input[str] usage_type: Different usage type. Possible values are `PAYG` and `COMMITTED`.
        """
        pulumi.set(__self__, "plan", plan)
        if billing_cycle is not None:
            pulumi.set(__self__, "billing_cycle", billing_cycle)
        if effective_date is not None:
            pulumi.set(__self__, "effective_date", effective_date)
        if usage_type is not None:
            pulumi.set(__self__, "usage_type", usage_type)

    @property
    @pulumi.getter
    def plan(self) -> pulumi.Input[str]:
        """
        Plan id as published by Dynatrace.
        """
        return pulumi.get(self, "plan")

    @plan.setter
    def plan(self, value: pulumi.Input[str]):
        pulumi.set(self, "plan", value)

    @property
    @pulumi.getter(name="billingCycle")
    def billing_cycle(self) -> Optional[pulumi.Input[str]]:
        """
        Different billing cycles. Possible values are `MONTHLY` and `WEEKLY`.
        """
        return pulumi.get(self, "billing_cycle")

    @billing_cycle.setter
    def billing_cycle(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "billing_cycle", value)

    @property
    @pulumi.getter(name="effectiveDate")
    def effective_date(self) -> Optional[pulumi.Input[str]]:
        """
        Date when plan was applied.
        """
        return pulumi.get(self, "effective_date")

    @effective_date.setter
    def effective_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "effective_date", value)

    @property
    @pulumi.getter(name="usageType")
    def usage_type(self) -> Optional[pulumi.Input[str]]:
        """
        Different usage type. Possible values are `PAYG` and `COMMITTED`.
        """
        return pulumi.get(self, "usage_type")

    @usage_type.setter
    def usage_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "usage_type", value)


if not MYPY:
    class MonitorUserArgsDict(TypedDict):
        country: pulumi.Input[str]
        """
        Country of the user.
        """
        email: pulumi.Input[str]
        """
        Email of the user used by Dynatrace for contacting them if needed.
        """
        first_name: pulumi.Input[str]
        """
        First name of the user.
        """
        last_name: pulumi.Input[str]
        """
        Last name of the user.
        """
        phone_number: pulumi.Input[str]
        """
        phone number of the user by Dynatrace for contacting them if needed.
        """
elif False:
    MonitorUserArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class MonitorUserArgs:
    def __init__(__self__, *,
                 country: pulumi.Input[str],
                 email: pulumi.Input[str],
                 first_name: pulumi.Input[str],
                 last_name: pulumi.Input[str],
                 phone_number: pulumi.Input[str]):
        """
        :param pulumi.Input[str] country: Country of the user.
        :param pulumi.Input[str] email: Email of the user used by Dynatrace for contacting them if needed.
        :param pulumi.Input[str] first_name: First name of the user.
        :param pulumi.Input[str] last_name: Last name of the user.
        :param pulumi.Input[str] phone_number: phone number of the user by Dynatrace for contacting them if needed.
        """
        pulumi.set(__self__, "country", country)
        pulumi.set(__self__, "email", email)
        pulumi.set(__self__, "first_name", first_name)
        pulumi.set(__self__, "last_name", last_name)
        pulumi.set(__self__, "phone_number", phone_number)

    @property
    @pulumi.getter
    def country(self) -> pulumi.Input[str]:
        """
        Country of the user.
        """
        return pulumi.get(self, "country")

    @country.setter
    def country(self, value: pulumi.Input[str]):
        pulumi.set(self, "country", value)

    @property
    @pulumi.getter
    def email(self) -> pulumi.Input[str]:
        """
        Email of the user used by Dynatrace for contacting them if needed.
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: pulumi.Input[str]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter(name="firstName")
    def first_name(self) -> pulumi.Input[str]:
        """
        First name of the user.
        """
        return pulumi.get(self, "first_name")

    @first_name.setter
    def first_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "first_name", value)

    @property
    @pulumi.getter(name="lastName")
    def last_name(self) -> pulumi.Input[str]:
        """
        Last name of the user.
        """
        return pulumi.get(self, "last_name")

    @last_name.setter
    def last_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "last_name", value)

    @property
    @pulumi.getter(name="phoneNumber")
    def phone_number(self) -> pulumi.Input[str]:
        """
        phone number of the user by Dynatrace for contacting them if needed.
        """
        return pulumi.get(self, "phone_number")

    @phone_number.setter
    def phone_number(self, value: pulumi.Input[str]):
        pulumi.set(self, "phone_number", value)


