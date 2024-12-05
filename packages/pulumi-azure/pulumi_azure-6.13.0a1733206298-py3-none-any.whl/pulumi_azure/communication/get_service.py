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
    'GetServiceResult',
    'AwaitableGetServiceResult',
    'get_service',
    'get_service_output',
]

@pulumi.output_type
class GetServiceResult:
    """
    A collection of values returned by getService.
    """
    def __init__(__self__, data_location=None, id=None, name=None, primary_connection_string=None, primary_key=None, resource_group_name=None, secondary_connection_string=None, secondary_key=None, tags=None):
        if data_location and not isinstance(data_location, str):
            raise TypeError("Expected argument 'data_location' to be a str")
        pulumi.set(__self__, "data_location", data_location)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if primary_connection_string and not isinstance(primary_connection_string, str):
            raise TypeError("Expected argument 'primary_connection_string' to be a str")
        pulumi.set(__self__, "primary_connection_string", primary_connection_string)
        if primary_key and not isinstance(primary_key, str):
            raise TypeError("Expected argument 'primary_key' to be a str")
        pulumi.set(__self__, "primary_key", primary_key)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if secondary_connection_string and not isinstance(secondary_connection_string, str):
            raise TypeError("Expected argument 'secondary_connection_string' to be a str")
        pulumi.set(__self__, "secondary_connection_string", secondary_connection_string)
        if secondary_key and not isinstance(secondary_key, str):
            raise TypeError("Expected argument 'secondary_key' to be a str")
        pulumi.set(__self__, "secondary_key", secondary_key)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="dataLocation")
    def data_location(self) -> str:
        """
        The location where the Communication service stores its data at rest.
        """
        return pulumi.get(self, "data_location")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="primaryConnectionString")
    def primary_connection_string(self) -> str:
        """
        The primary connection string of the Communication Service.
        """
        return pulumi.get(self, "primary_connection_string")

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> str:
        """
        The primary key of the Communication Service.
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="secondaryConnectionString")
    def secondary_connection_string(self) -> str:
        """
        The secondary connection string of the Communication Service.
        """
        return pulumi.get(self, "secondary_connection_string")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> str:
        """
        The secondary key of the Communication Service.
        """
        return pulumi.get(self, "secondary_key")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the Communication Service.
        """
        return pulumi.get(self, "tags")


class AwaitableGetServiceResult(GetServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceResult(
            data_location=self.data_location,
            id=self.id,
            name=self.name,
            primary_connection_string=self.primary_connection_string,
            primary_key=self.primary_key,
            resource_group_name=self.resource_group_name,
            secondary_connection_string=self.secondary_connection_string,
            secondary_key=self.secondary_key,
            tags=self.tags)


def get_service(name: Optional[str] = None,
                resource_group_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceResult:
    """
    Use this data source to access information about an existing Communication Service.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.communication.get_service(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Communication Service.
           *
    :param str resource_group_name: The name of the Resource Group where the Communication Service exists.
           *
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:communication/getService:getService', __args__, opts=opts, typ=GetServiceResult).value

    return AwaitableGetServiceResult(
        data_location=pulumi.get(__ret__, 'data_location'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        primary_connection_string=pulumi.get(__ret__, 'primary_connection_string'),
        primary_key=pulumi.get(__ret__, 'primary_key'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        secondary_connection_string=pulumi.get(__ret__, 'secondary_connection_string'),
        secondary_key=pulumi.get(__ret__, 'secondary_key'),
        tags=pulumi.get(__ret__, 'tags'))
def get_service_output(name: Optional[pulumi.Input[str]] = None,
                       resource_group_name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServiceResult]:
    """
    Use this data source to access information about an existing Communication Service.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.communication.get_service(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Communication Service.
           *
    :param str resource_group_name: The name of the Resource Group where the Communication Service exists.
           *
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:communication/getService:getService', __args__, opts=opts, typ=GetServiceResult)
    return __ret__.apply(lambda __response__: GetServiceResult(
        data_location=pulumi.get(__response__, 'data_location'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        primary_connection_string=pulumi.get(__response__, 'primary_connection_string'),
        primary_key=pulumi.get(__response__, 'primary_key'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        secondary_connection_string=pulumi.get(__response__, 'secondary_connection_string'),
        secondary_key=pulumi.get(__response__, 'secondary_key'),
        tags=pulumi.get(__response__, 'tags')))
