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
    'AccountIdentity',
    'AccountStorage',
]

@pulumi.output_type
class AccountIdentity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "identityIds":
            suggest = "identity_ids"
        elif key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccountIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccountIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccountIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: str,
                 identity_ids: Optional[Sequence[str]] = None,
                 principal_id: Optional[str] = None,
                 tenant_id: Optional[str] = None):
        """
        :param str type: Specifies the identity type of the Video Indexer Account. Possible values are `SystemAssigned` (where Azure will generate a Service Principal for you), `UserAssigned` where you can specify the Service Principal IDs in the `identity_ids` field, and `SystemAssigned, UserAssigned` which assigns both a system managed identity as well as the specified user assigned identities.
        :param Sequence[str] identity_ids: Specifies a list of user managed identity ids to be assigned. Required if `type` is `UserAssigned`.
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
    def type(self) -> str:
        """
        Specifies the identity type of the Video Indexer Account. Possible values are `SystemAssigned` (where Azure will generate a Service Principal for you), `UserAssigned` where you can specify the Service Principal IDs in the `identity_ids` field, and `SystemAssigned, UserAssigned` which assigns both a system managed identity as well as the specified user assigned identities.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="identityIds")
    def identity_ids(self) -> Optional[Sequence[str]]:
        """
        Specifies a list of user managed identity ids to be assigned. Required if `type` is `UserAssigned`.
        """
        return pulumi.get(self, "identity_ids")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[str]:
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        return pulumi.get(self, "tenant_id")


@pulumi.output_type
class AccountStorage(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "storageAccountId":
            suggest = "storage_account_id"
        elif key == "userAssignedIdentityId":
            suggest = "user_assigned_identity_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccountStorage. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccountStorage.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccountStorage.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 storage_account_id: str,
                 user_assigned_identity_id: Optional[str] = None):
        """
        :param str storage_account_id: The ID of the storage account to be associated with the Video Indexer Account. Changing this forces a new Video Indexer Account to be created.
        :param str user_assigned_identity_id: The reference to the user assigned identity to use to access the Storage Account.
        """
        pulumi.set(__self__, "storage_account_id", storage_account_id)
        if user_assigned_identity_id is not None:
            pulumi.set(__self__, "user_assigned_identity_id", user_assigned_identity_id)

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> str:
        """
        The ID of the storage account to be associated with the Video Indexer Account. Changing this forces a new Video Indexer Account to be created.
        """
        return pulumi.get(self, "storage_account_id")

    @property
    @pulumi.getter(name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> Optional[str]:
        """
        The reference to the user assigned identity to use to access the Storage Account.
        """
        return pulumi.get(self, "user_assigned_identity_id")


