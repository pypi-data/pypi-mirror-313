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
    'GetManagedDiskResult',
    'AwaitableGetManagedDiskResult',
    'get_managed_disk',
    'get_managed_disk_output',
]

@pulumi.output_type
class GetManagedDiskResult:
    """
    A collection of values returned by getManagedDisk.
    """
    def __init__(__self__, create_option=None, disk_access_id=None, disk_encryption_set_id=None, disk_iops_read_write=None, disk_mbps_read_write=None, disk_size_gb=None, encryption_settings=None, id=None, image_reference_id=None, name=None, network_access_policy=None, os_type=None, resource_group_name=None, source_resource_id=None, source_uri=None, storage_account_id=None, storage_account_type=None, tags=None, zones=None):
        if create_option and not isinstance(create_option, str):
            raise TypeError("Expected argument 'create_option' to be a str")
        pulumi.set(__self__, "create_option", create_option)
        if disk_access_id and not isinstance(disk_access_id, str):
            raise TypeError("Expected argument 'disk_access_id' to be a str")
        pulumi.set(__self__, "disk_access_id", disk_access_id)
        if disk_encryption_set_id and not isinstance(disk_encryption_set_id, str):
            raise TypeError("Expected argument 'disk_encryption_set_id' to be a str")
        pulumi.set(__self__, "disk_encryption_set_id", disk_encryption_set_id)
        if disk_iops_read_write and not isinstance(disk_iops_read_write, int):
            raise TypeError("Expected argument 'disk_iops_read_write' to be a int")
        pulumi.set(__self__, "disk_iops_read_write", disk_iops_read_write)
        if disk_mbps_read_write and not isinstance(disk_mbps_read_write, int):
            raise TypeError("Expected argument 'disk_mbps_read_write' to be a int")
        pulumi.set(__self__, "disk_mbps_read_write", disk_mbps_read_write)
        if disk_size_gb and not isinstance(disk_size_gb, int):
            raise TypeError("Expected argument 'disk_size_gb' to be a int")
        pulumi.set(__self__, "disk_size_gb", disk_size_gb)
        if encryption_settings and not isinstance(encryption_settings, list):
            raise TypeError("Expected argument 'encryption_settings' to be a list")
        pulumi.set(__self__, "encryption_settings", encryption_settings)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if image_reference_id and not isinstance(image_reference_id, str):
            raise TypeError("Expected argument 'image_reference_id' to be a str")
        pulumi.set(__self__, "image_reference_id", image_reference_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_access_policy and not isinstance(network_access_policy, str):
            raise TypeError("Expected argument 'network_access_policy' to be a str")
        pulumi.set(__self__, "network_access_policy", network_access_policy)
        if os_type and not isinstance(os_type, str):
            raise TypeError("Expected argument 'os_type' to be a str")
        pulumi.set(__self__, "os_type", os_type)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if source_resource_id and not isinstance(source_resource_id, str):
            raise TypeError("Expected argument 'source_resource_id' to be a str")
        pulumi.set(__self__, "source_resource_id", source_resource_id)
        if source_uri and not isinstance(source_uri, str):
            raise TypeError("Expected argument 'source_uri' to be a str")
        pulumi.set(__self__, "source_uri", source_uri)
        if storage_account_id and not isinstance(storage_account_id, str):
            raise TypeError("Expected argument 'storage_account_id' to be a str")
        pulumi.set(__self__, "storage_account_id", storage_account_id)
        if storage_account_type and not isinstance(storage_account_type, str):
            raise TypeError("Expected argument 'storage_account_type' to be a str")
        pulumi.set(__self__, "storage_account_type", storage_account_type)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="createOption")
    def create_option(self) -> str:
        return pulumi.get(self, "create_option")

    @property
    @pulumi.getter(name="diskAccessId")
    def disk_access_id(self) -> str:
        """
        The ID of the disk access resource for using private endpoints on disks.
        """
        return pulumi.get(self, "disk_access_id")

    @property
    @pulumi.getter(name="diskEncryptionSetId")
    def disk_encryption_set_id(self) -> str:
        """
        The ID of the Disk Encryption Set used to encrypt this Managed Disk.
        """
        return pulumi.get(self, "disk_encryption_set_id")

    @property
    @pulumi.getter(name="diskIopsReadWrite")
    def disk_iops_read_write(self) -> int:
        """
        The number of IOPS allowed for this disk, where one operation can transfer between 4k and 256k bytes.
        """
        return pulumi.get(self, "disk_iops_read_write")

    @property
    @pulumi.getter(name="diskMbpsReadWrite")
    def disk_mbps_read_write(self) -> int:
        """
        The bandwidth allowed for this disk.
        """
        return pulumi.get(self, "disk_mbps_read_write")

    @property
    @pulumi.getter(name="diskSizeGb")
    def disk_size_gb(self) -> int:
        """
        The size of the Managed Disk in gigabytes.
        """
        return pulumi.get(self, "disk_size_gb")

    @property
    @pulumi.getter(name="encryptionSettings")
    def encryption_settings(self) -> Sequence['outputs.GetManagedDiskEncryptionSettingResult']:
        """
        A `encryption_settings` block as defined below.
        """
        return pulumi.get(self, "encryption_settings")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="imageReferenceId")
    def image_reference_id(self) -> str:
        """
        The ID of the source image used for creating this Managed Disk.
        """
        return pulumi.get(self, "image_reference_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkAccessPolicy")
    def network_access_policy(self) -> str:
        """
        Policy for accessing the disk via network.
        """
        return pulumi.get(self, "network_access_policy")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> str:
        """
        The operating system used for this Managed Disk.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="sourceResourceId")
    def source_resource_id(self) -> str:
        """
        The ID of an existing Managed Disk which this Disk was created from.
        """
        return pulumi.get(self, "source_resource_id")

    @property
    @pulumi.getter(name="sourceUri")
    def source_uri(self) -> str:
        """
        The Source URI for this Managed Disk.
        """
        return pulumi.get(self, "source_uri")

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> str:
        """
        The ID of the Storage Account where the `source_uri` is located.
        """
        return pulumi.get(self, "storage_account_id")

    @property
    @pulumi.getter(name="storageAccountType")
    def storage_account_type(self) -> str:
        """
        The storage account type for the Managed Disk.
        """
        return pulumi.get(self, "storage_account_type")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def zones(self) -> Sequence[str]:
        """
        A list of Availability Zones where the Managed Disk exists.
        """
        return pulumi.get(self, "zones")


class AwaitableGetManagedDiskResult(GetManagedDiskResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagedDiskResult(
            create_option=self.create_option,
            disk_access_id=self.disk_access_id,
            disk_encryption_set_id=self.disk_encryption_set_id,
            disk_iops_read_write=self.disk_iops_read_write,
            disk_mbps_read_write=self.disk_mbps_read_write,
            disk_size_gb=self.disk_size_gb,
            encryption_settings=self.encryption_settings,
            id=self.id,
            image_reference_id=self.image_reference_id,
            name=self.name,
            network_access_policy=self.network_access_policy,
            os_type=self.os_type,
            resource_group_name=self.resource_group_name,
            source_resource_id=self.source_resource_id,
            source_uri=self.source_uri,
            storage_account_id=self.storage_account_id,
            storage_account_type=self.storage_account_type,
            tags=self.tags,
            zones=self.zones)


def get_managed_disk(name: Optional[str] = None,
                     resource_group_name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagedDiskResult:
    """
    Use this data source to access information about an existing Managed Disk.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    existing = azure.compute.get_managed_disk(name="example-datadisk",
        resource_group_name="example-resources")
    pulumi.export("id", existing.id)
    ```


    :param str name: Specifies the name of the Managed Disk.
    :param str resource_group_name: Specifies the name of the Resource Group where this Managed Disk exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:compute/getManagedDisk:getManagedDisk', __args__, opts=opts, typ=GetManagedDiskResult).value

    return AwaitableGetManagedDiskResult(
        create_option=pulumi.get(__ret__, 'create_option'),
        disk_access_id=pulumi.get(__ret__, 'disk_access_id'),
        disk_encryption_set_id=pulumi.get(__ret__, 'disk_encryption_set_id'),
        disk_iops_read_write=pulumi.get(__ret__, 'disk_iops_read_write'),
        disk_mbps_read_write=pulumi.get(__ret__, 'disk_mbps_read_write'),
        disk_size_gb=pulumi.get(__ret__, 'disk_size_gb'),
        encryption_settings=pulumi.get(__ret__, 'encryption_settings'),
        id=pulumi.get(__ret__, 'id'),
        image_reference_id=pulumi.get(__ret__, 'image_reference_id'),
        name=pulumi.get(__ret__, 'name'),
        network_access_policy=pulumi.get(__ret__, 'network_access_policy'),
        os_type=pulumi.get(__ret__, 'os_type'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        source_resource_id=pulumi.get(__ret__, 'source_resource_id'),
        source_uri=pulumi.get(__ret__, 'source_uri'),
        storage_account_id=pulumi.get(__ret__, 'storage_account_id'),
        storage_account_type=pulumi.get(__ret__, 'storage_account_type'),
        tags=pulumi.get(__ret__, 'tags'),
        zones=pulumi.get(__ret__, 'zones'))
def get_managed_disk_output(name: Optional[pulumi.Input[str]] = None,
                            resource_group_name: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetManagedDiskResult]:
    """
    Use this data source to access information about an existing Managed Disk.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    existing = azure.compute.get_managed_disk(name="example-datadisk",
        resource_group_name="example-resources")
    pulumi.export("id", existing.id)
    ```


    :param str name: Specifies the name of the Managed Disk.
    :param str resource_group_name: Specifies the name of the Resource Group where this Managed Disk exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:compute/getManagedDisk:getManagedDisk', __args__, opts=opts, typ=GetManagedDiskResult)
    return __ret__.apply(lambda __response__: GetManagedDiskResult(
        create_option=pulumi.get(__response__, 'create_option'),
        disk_access_id=pulumi.get(__response__, 'disk_access_id'),
        disk_encryption_set_id=pulumi.get(__response__, 'disk_encryption_set_id'),
        disk_iops_read_write=pulumi.get(__response__, 'disk_iops_read_write'),
        disk_mbps_read_write=pulumi.get(__response__, 'disk_mbps_read_write'),
        disk_size_gb=pulumi.get(__response__, 'disk_size_gb'),
        encryption_settings=pulumi.get(__response__, 'encryption_settings'),
        id=pulumi.get(__response__, 'id'),
        image_reference_id=pulumi.get(__response__, 'image_reference_id'),
        name=pulumi.get(__response__, 'name'),
        network_access_policy=pulumi.get(__response__, 'network_access_policy'),
        os_type=pulumi.get(__response__, 'os_type'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        source_resource_id=pulumi.get(__response__, 'source_resource_id'),
        source_uri=pulumi.get(__response__, 'source_uri'),
        storage_account_id=pulumi.get(__response__, 'storage_account_id'),
        storage_account_type=pulumi.get(__response__, 'storage_account_type'),
        tags=pulumi.get(__response__, 'tags'),
        zones=pulumi.get(__response__, 'zones')))
