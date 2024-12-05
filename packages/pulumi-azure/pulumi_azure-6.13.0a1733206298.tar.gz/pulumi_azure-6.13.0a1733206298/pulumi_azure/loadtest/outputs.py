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
from . import outputs

__all__ = [
    'LoadTestEncryption',
    'LoadTestEncryptionIdentity',
    'LoadTestIdentity',
    'GetEncryptionResult',
    'GetEncryptionIdentityResult',
    'GetIdentityResult',
]

@pulumi.output_type
class LoadTestEncryption(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyUrl":
            suggest = "key_url"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LoadTestEncryption. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LoadTestEncryption.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LoadTestEncryption.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 identity: 'outputs.LoadTestEncryptionIdentity',
                 key_url: str):
        """
        :param 'LoadTestEncryptionIdentityArgs' identity: An `identity` block as defined below. Changing this forces a new Load Test to be created.
        :param str key_url: The URI specifying the Key vault and key to be used to encrypt data in this resource. The URI should include the key version. Changing this forces a new Load Test to be created.
        """
        pulumi.set(__self__, "identity", identity)
        pulumi.set(__self__, "key_url", key_url)

    @property
    @pulumi.getter
    def identity(self) -> 'outputs.LoadTestEncryptionIdentity':
        """
        An `identity` block as defined below. Changing this forces a new Load Test to be created.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="keyUrl")
    def key_url(self) -> str:
        """
        The URI specifying the Key vault and key to be used to encrypt data in this resource. The URI should include the key version. Changing this forces a new Load Test to be created.
        """
        return pulumi.get(self, "key_url")


@pulumi.output_type
class LoadTestEncryptionIdentity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "identityId":
            suggest = "identity_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LoadTestEncryptionIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LoadTestEncryptionIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LoadTestEncryptionIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 identity_id: str,
                 type: str):
        """
        :param str identity_id: The User Assigned Identity ID that should be assigned to this Load Test Encryption. Changing this forces a new Load Test to be created.
        :param str type: Specifies the type of Managed Identity that should be assigned to this Load Test Encryption. Possible values are `SystemAssigned` or `UserAssigned`. Changing this forces a new Load Test to be created.
        """
        pulumi.set(__self__, "identity_id", identity_id)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="identityId")
    def identity_id(self) -> str:
        """
        The User Assigned Identity ID that should be assigned to this Load Test Encryption. Changing this forces a new Load Test to be created.
        """
        return pulumi.get(self, "identity_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies the type of Managed Identity that should be assigned to this Load Test Encryption. Possible values are `SystemAssigned` or `UserAssigned`. Changing this forces a new Load Test to be created.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class LoadTestIdentity(dict):
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
            pulumi.log.warn(f"Key '{key}' not found in LoadTestIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LoadTestIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LoadTestIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: str,
                 identity_ids: Optional[Sequence[str]] = None,
                 principal_id: Optional[str] = None,
                 tenant_id: Optional[str] = None):
        """
        :param str type: Specifies the type of Managed Identity that should be assigned to this Load Test Encryption. Possible values are `SystemAssigned` or `UserAssigned`. Changing this forces a new Load Test to be created.
        :param Sequence[str] identity_ids: A list of the User Assigned Identity IDs that should be assigned to this Load Test.
        :param str principal_id: The Principal ID for the System-Assigned Managed Identity assigned to this Load Test.
               *
        :param str tenant_id: The Tenant ID for the System-Assigned Managed Identity assigned to this Load Test.
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
        Specifies the type of Managed Identity that should be assigned to this Load Test Encryption. Possible values are `SystemAssigned` or `UserAssigned`. Changing this forces a new Load Test to be created.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="identityIds")
    def identity_ids(self) -> Optional[Sequence[str]]:
        """
        A list of the User Assigned Identity IDs that should be assigned to this Load Test.
        """
        return pulumi.get(self, "identity_ids")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[str]:
        """
        The Principal ID for the System-Assigned Managed Identity assigned to this Load Test.
        *
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        """
        The Tenant ID for the System-Assigned Managed Identity assigned to this Load Test.
        """
        return pulumi.get(self, "tenant_id")


@pulumi.output_type
class GetEncryptionResult(dict):
    def __init__(__self__, *,
                 identities: Sequence['outputs.GetEncryptionIdentityResult'],
                 key_url: str):
        """
        :param Sequence['GetEncryptionIdentityArgs'] identities: An `identity` block as defined below.
        :param str key_url: The URI specifying the Key vault and key to be used to encrypt data in this resource.
        """
        pulumi.set(__self__, "identities", identities)
        pulumi.set(__self__, "key_url", key_url)

    @property
    @pulumi.getter
    def identities(self) -> Sequence['outputs.GetEncryptionIdentityResult']:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, "identities")

    @property
    @pulumi.getter(name="keyUrl")
    def key_url(self) -> str:
        """
        The URI specifying the Key vault and key to be used to encrypt data in this resource.
        """
        return pulumi.get(self, "key_url")


@pulumi.output_type
class GetEncryptionIdentityResult(dict):
    def __init__(__self__, *,
                 identity_id: str,
                 type: str):
        """
        :param str identity_id: The User Assigned Identity ID that is assigned to this Load Test Encryption.
        :param str type: Type of Managed Service Identity that is assigned to this Load Test Encryption.
        """
        pulumi.set(__self__, "identity_id", identity_id)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="identityId")
    def identity_id(self) -> str:
        """
        The User Assigned Identity ID that is assigned to this Load Test Encryption.
        """
        return pulumi.get(self, "identity_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of Managed Service Identity that is assigned to this Load Test Encryption.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class GetIdentityResult(dict):
    def __init__(__self__, *,
                 identity_ids: Sequence[str],
                 principal_id: str,
                 tenant_id: str,
                 type: str):
        """
        :param Sequence[str] identity_ids: The list of the User Assigned Identity IDs that is assigned to this Load Test Service.
        :param str principal_id: The Principal ID for the System-Assigned Managed Identity assigned to this Load Test Service.
        :param str tenant_id: The Tenant ID for the System-Assigned Managed Identity assigned to this Load Test Service.
        :param str type: Type of Managed Service Identity that is assigned to this Load Test Encryption.
        """
        pulumi.set(__self__, "identity_ids", identity_ids)
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="identityIds")
    def identity_ids(self) -> Sequence[str]:
        """
        The list of the User Assigned Identity IDs that is assigned to this Load Test Service.
        """
        return pulumi.get(self, "identity_ids")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The Principal ID for the System-Assigned Managed Identity assigned to this Load Test Service.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The Tenant ID for the System-Assigned Managed Identity assigned to this Load Test Service.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of Managed Service Identity that is assigned to this Load Test Encryption.
        """
        return pulumi.get(self, "type")


