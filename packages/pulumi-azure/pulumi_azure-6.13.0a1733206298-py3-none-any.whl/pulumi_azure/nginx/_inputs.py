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
    'ConfigurationConfigFileArgs',
    'ConfigurationConfigFileArgsDict',
    'ConfigurationProtectedFileArgs',
    'ConfigurationProtectedFileArgsDict',
    'DeploymentAutoScaleProfileArgs',
    'DeploymentAutoScaleProfileArgsDict',
    'DeploymentFrontendPrivateArgs',
    'DeploymentFrontendPrivateArgsDict',
    'DeploymentFrontendPublicArgs',
    'DeploymentFrontendPublicArgsDict',
    'DeploymentIdentityArgs',
    'DeploymentIdentityArgsDict',
    'DeploymentLoggingStorageAccountArgs',
    'DeploymentLoggingStorageAccountArgsDict',
    'DeploymentNetworkInterfaceArgs',
    'DeploymentNetworkInterfaceArgsDict',
]

MYPY = False

if not MYPY:
    class ConfigurationConfigFileArgsDict(TypedDict):
        content: pulumi.Input[str]
        """
        Specifies the base-64 encoded contents of this config file.
        """
        virtual_path: pulumi.Input[str]
        """
        Specifies the path of this config file.
        """
elif False:
    ConfigurationConfigFileArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ConfigurationConfigFileArgs:
    def __init__(__self__, *,
                 content: pulumi.Input[str],
                 virtual_path: pulumi.Input[str]):
        """
        :param pulumi.Input[str] content: Specifies the base-64 encoded contents of this config file.
        :param pulumi.Input[str] virtual_path: Specifies the path of this config file.
        """
        pulumi.set(__self__, "content", content)
        pulumi.set(__self__, "virtual_path", virtual_path)

    @property
    @pulumi.getter
    def content(self) -> pulumi.Input[str]:
        """
        Specifies the base-64 encoded contents of this config file.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: pulumi.Input[str]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter(name="virtualPath")
    def virtual_path(self) -> pulumi.Input[str]:
        """
        Specifies the path of this config file.
        """
        return pulumi.get(self, "virtual_path")

    @virtual_path.setter
    def virtual_path(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_path", value)


if not MYPY:
    class ConfigurationProtectedFileArgsDict(TypedDict):
        content: pulumi.Input[str]
        """
        Specifies the base-64 encoded contents of this config file (Sensitive).
        """
        virtual_path: pulumi.Input[str]
        """
        Specifies the path of this config file.
        """
elif False:
    ConfigurationProtectedFileArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ConfigurationProtectedFileArgs:
    def __init__(__self__, *,
                 content: pulumi.Input[str],
                 virtual_path: pulumi.Input[str]):
        """
        :param pulumi.Input[str] content: Specifies the base-64 encoded contents of this config file (Sensitive).
        :param pulumi.Input[str] virtual_path: Specifies the path of this config file.
        """
        pulumi.set(__self__, "content", content)
        pulumi.set(__self__, "virtual_path", virtual_path)

    @property
    @pulumi.getter
    def content(self) -> pulumi.Input[str]:
        """
        Specifies the base-64 encoded contents of this config file (Sensitive).
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: pulumi.Input[str]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter(name="virtualPath")
    def virtual_path(self) -> pulumi.Input[str]:
        """
        Specifies the path of this config file.
        """
        return pulumi.get(self, "virtual_path")

    @virtual_path.setter
    def virtual_path(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_path", value)


if not MYPY:
    class DeploymentAutoScaleProfileArgsDict(TypedDict):
        max_capacity: pulumi.Input[int]
        min_capacity: pulumi.Input[int]
        """
        Specify the minimum number of NGINX capacity units for this NGINX Deployment.
        """
        name: pulumi.Input[str]
        """
        Specify the name of the autoscaling profile.
        """
elif False:
    DeploymentAutoScaleProfileArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class DeploymentAutoScaleProfileArgs:
    def __init__(__self__, *,
                 max_capacity: pulumi.Input[int],
                 min_capacity: pulumi.Input[int],
                 name: pulumi.Input[str]):
        """
        :param pulumi.Input[int] min_capacity: Specify the minimum number of NGINX capacity units for this NGINX Deployment.
        :param pulumi.Input[str] name: Specify the name of the autoscaling profile.
        """
        pulumi.set(__self__, "max_capacity", max_capacity)
        pulumi.set(__self__, "min_capacity", min_capacity)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="maxCapacity")
    def max_capacity(self) -> pulumi.Input[int]:
        return pulumi.get(self, "max_capacity")

    @max_capacity.setter
    def max_capacity(self, value: pulumi.Input[int]):
        pulumi.set(self, "max_capacity", value)

    @property
    @pulumi.getter(name="minCapacity")
    def min_capacity(self) -> pulumi.Input[int]:
        """
        Specify the minimum number of NGINX capacity units for this NGINX Deployment.
        """
        return pulumi.get(self, "min_capacity")

    @min_capacity.setter
    def min_capacity(self, value: pulumi.Input[int]):
        pulumi.set(self, "min_capacity", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Specify the name of the autoscaling profile.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)


if not MYPY:
    class DeploymentFrontendPrivateArgsDict(TypedDict):
        allocation_method: pulumi.Input[str]
        """
        Specify the method for allocating the private IP. Possible values are `Static` and `Dynamic`. Changing this forces a new NGINX Deployment to be created.
        """
        ip_address: pulumi.Input[str]
        """
        Specify the private IP Address. Changing this forces a new NGINX Deployment to be created.
        """
        subnet_id: pulumi.Input[str]
        """
        Specify the Subnet Resource ID for this NGINX Deployment. Changing this forces a new NGINX Deployment to be created.
        """
elif False:
    DeploymentFrontendPrivateArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class DeploymentFrontendPrivateArgs:
    def __init__(__self__, *,
                 allocation_method: pulumi.Input[str],
                 ip_address: pulumi.Input[str],
                 subnet_id: pulumi.Input[str]):
        """
        :param pulumi.Input[str] allocation_method: Specify the method for allocating the private IP. Possible values are `Static` and `Dynamic`. Changing this forces a new NGINX Deployment to be created.
        :param pulumi.Input[str] ip_address: Specify the private IP Address. Changing this forces a new NGINX Deployment to be created.
        :param pulumi.Input[str] subnet_id: Specify the Subnet Resource ID for this NGINX Deployment. Changing this forces a new NGINX Deployment to be created.
        """
        pulumi.set(__self__, "allocation_method", allocation_method)
        pulumi.set(__self__, "ip_address", ip_address)
        pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="allocationMethod")
    def allocation_method(self) -> pulumi.Input[str]:
        """
        Specify the method for allocating the private IP. Possible values are `Static` and `Dynamic`. Changing this forces a new NGINX Deployment to be created.
        """
        return pulumi.get(self, "allocation_method")

    @allocation_method.setter
    def allocation_method(self, value: pulumi.Input[str]):
        pulumi.set(self, "allocation_method", value)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> pulumi.Input[str]:
        """
        Specify the private IP Address. Changing this forces a new NGINX Deployment to be created.
        """
        return pulumi.get(self, "ip_address")

    @ip_address.setter
    def ip_address(self, value: pulumi.Input[str]):
        pulumi.set(self, "ip_address", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Input[str]:
        """
        Specify the Subnet Resource ID for this NGINX Deployment. Changing this forces a new NGINX Deployment to be created.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnet_id", value)


if not MYPY:
    class DeploymentFrontendPublicArgsDict(TypedDict):
        ip_addresses: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        Specifies a list of Public IP Resource ID to this NGINX Deployment. Changing this forces a new NGINX Deployment to be created.
        """
elif False:
    DeploymentFrontendPublicArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class DeploymentFrontendPublicArgs:
    def __init__(__self__, *,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_addresses: Specifies a list of Public IP Resource ID to this NGINX Deployment. Changing this forces a new NGINX Deployment to be created.
        """
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies a list of Public IP Resource ID to this NGINX Deployment. Changing this forces a new NGINX Deployment to be created.
        """
        return pulumi.get(self, "ip_addresses")

    @ip_addresses.setter
    def ip_addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_addresses", value)


if not MYPY:
    class DeploymentIdentityArgsDict(TypedDict):
        type: pulumi.Input[str]
        """
        Specifies the identity type of the NGINX Deployment. Possible values are `SystemAssigned`, `UserAssigned` or `SystemAssigned, UserAssigned`.
        """
        identity_ids: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        Specifies a list of user managed identity ids to be assigned.

        > **NOTE:** This is required when `type` is set to `UserAssigned`.
        """
        principal_id: NotRequired[pulumi.Input[str]]
        tenant_id: NotRequired[pulumi.Input[str]]
elif False:
    DeploymentIdentityArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class DeploymentIdentityArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 identity_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] type: Specifies the identity type of the NGINX Deployment. Possible values are `SystemAssigned`, `UserAssigned` or `SystemAssigned, UserAssigned`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] identity_ids: Specifies a list of user managed identity ids to be assigned.
               
               > **NOTE:** This is required when `type` is set to `UserAssigned`.
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
        Specifies the identity type of the NGINX Deployment. Possible values are `SystemAssigned`, `UserAssigned` or `SystemAssigned, UserAssigned`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="identityIds")
    def identity_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies a list of user managed identity ids to be assigned.

        > **NOTE:** This is required when `type` is set to `UserAssigned`.
        """
        return pulumi.get(self, "identity_ids")

    @identity_ids.setter
    def identity_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "identity_ids", value)

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
    class DeploymentLoggingStorageAccountArgsDict(TypedDict):
        container_name: NotRequired[pulumi.Input[str]]
        """
        Specify the container name in the Storage Account for logging.
        """
        name: NotRequired[pulumi.Input[str]]
        """
        The name of the StorageAccount for NGINX Logging.
        """
elif False:
    DeploymentLoggingStorageAccountArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class DeploymentLoggingStorageAccountArgs:
    def __init__(__self__, *,
                 container_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] container_name: Specify the container name in the Storage Account for logging.
        :param pulumi.Input[str] name: The name of the StorageAccount for NGINX Logging.
        """
        if container_name is not None:
            pulumi.set(__self__, "container_name", container_name)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specify the container name in the Storage Account for logging.
        """
        return pulumi.get(self, "container_name")

    @container_name.setter
    def container_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "container_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the StorageAccount for NGINX Logging.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


if not MYPY:
    class DeploymentNetworkInterfaceArgsDict(TypedDict):
        subnet_id: pulumi.Input[str]
        """
        Specify The Subnet Resource ID for this NGINX Deployment. Changing this forces a new NGINX Deployment to be created.
        """
elif False:
    DeploymentNetworkInterfaceArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class DeploymentNetworkInterfaceArgs:
    def __init__(__self__, *,
                 subnet_id: pulumi.Input[str]):
        """
        :param pulumi.Input[str] subnet_id: Specify The Subnet Resource ID for this NGINX Deployment. Changing this forces a new NGINX Deployment to be created.
        """
        pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Input[str]:
        """
        Specify The Subnet Resource ID for this NGINX Deployment. Changing this forces a new NGINX Deployment to be created.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnet_id", value)


