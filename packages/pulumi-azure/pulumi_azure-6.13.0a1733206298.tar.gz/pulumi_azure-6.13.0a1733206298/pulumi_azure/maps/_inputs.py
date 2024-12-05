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
    'AccountCorsArgs',
    'AccountCorsArgsDict',
    'AccountDataStoreArgs',
    'AccountDataStoreArgsDict',
    'AccountIdentityArgs',
    'AccountIdentityArgsDict',
]

MYPY = False

if not MYPY:
    class AccountCorsArgsDict(TypedDict):
        allowed_origins: pulumi.Input[Sequence[pulumi.Input[str]]]
        """
        A list of origins that should be allowed to make cross-origin calls.
        """
elif False:
    AccountCorsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AccountCorsArgs:
    def __init__(__self__, *,
                 allowed_origins: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_origins: A list of origins that should be allowed to make cross-origin calls.
        """
        pulumi.set(__self__, "allowed_origins", allowed_origins)

    @property
    @pulumi.getter(name="allowedOrigins")
    def allowed_origins(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of origins that should be allowed to make cross-origin calls.
        """
        return pulumi.get(self, "allowed_origins")

    @allowed_origins.setter
    def allowed_origins(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "allowed_origins", value)


if not MYPY:
    class AccountDataStoreArgsDict(TypedDict):
        unique_name: pulumi.Input[str]
        """
        The name given to the linked Storage Account.
        """
        storage_account_id: NotRequired[pulumi.Input[str]]
        """
        The ID of the Storage Account that should be linked to this Azure Maps Account.
        """
elif False:
    AccountDataStoreArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AccountDataStoreArgs:
    def __init__(__self__, *,
                 unique_name: pulumi.Input[str],
                 storage_account_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] unique_name: The name given to the linked Storage Account.
        :param pulumi.Input[str] storage_account_id: The ID of the Storage Account that should be linked to this Azure Maps Account.
        """
        pulumi.set(__self__, "unique_name", unique_name)
        if storage_account_id is not None:
            pulumi.set(__self__, "storage_account_id", storage_account_id)

    @property
    @pulumi.getter(name="uniqueName")
    def unique_name(self) -> pulumi.Input[str]:
        """
        The name given to the linked Storage Account.
        """
        return pulumi.get(self, "unique_name")

    @unique_name.setter
    def unique_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "unique_name", value)

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Storage Account that should be linked to this Azure Maps Account.
        """
        return pulumi.get(self, "storage_account_id")

    @storage_account_id.setter
    def storage_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_id", value)


if not MYPY:
    class AccountIdentityArgsDict(TypedDict):
        type: pulumi.Input[str]
        """
        Specifies the type of Managed Service Identity that should be configured on this Azure Maps Account. Possible values are `SystemAssigned`, `UserAssigned`, `SystemAssigned, UserAssigned` (to enable both).
        """
        identity_ids: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        A list of User Assigned Managed Identity IDs to be assigned to this Azure Maps Account.

        > **NOTE:** This is required when `type` is set to `UserAssigned` or `SystemAssigned, UserAssigned`.
        """
        principal_id: NotRequired[pulumi.Input[str]]
        """
        The Principal ID associated with this Managed Service Identity.
        """
        tenant_id: NotRequired[pulumi.Input[str]]
        """
        The Tenant ID associated with this Managed Service Identity.
        """
elif False:
    AccountIdentityArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AccountIdentityArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 identity_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] type: Specifies the type of Managed Service Identity that should be configured on this Azure Maps Account. Possible values are `SystemAssigned`, `UserAssigned`, `SystemAssigned, UserAssigned` (to enable both).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] identity_ids: A list of User Assigned Managed Identity IDs to be assigned to this Azure Maps Account.
               
               > **NOTE:** This is required when `type` is set to `UserAssigned` or `SystemAssigned, UserAssigned`.
        :param pulumi.Input[str] principal_id: The Principal ID associated with this Managed Service Identity.
        :param pulumi.Input[str] tenant_id: The Tenant ID associated with this Managed Service Identity.
        """
        pulumi.set(__self__, "type", type)
        if identity_ids is not None:
            pulumi.set(__self__, "identity_ids", identity_ids)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Specifies the type of Managed Service Identity that should be configured on this Azure Maps Account. Possible values are `SystemAssigned`, `UserAssigned`, `SystemAssigned, UserAssigned` (to enable both).
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="identityIds")
    def identity_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of User Assigned Managed Identity IDs to be assigned to this Azure Maps Account.

        > **NOTE:** This is required when `type` is set to `UserAssigned` or `SystemAssigned, UserAssigned`.
        """
        return pulumi.get(self, "identity_ids")

    @identity_ids.setter
    def identity_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "identity_ids", value)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Principal ID associated with this Managed Service Identity.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Tenant ID associated with this Managed Service Identity.
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)


