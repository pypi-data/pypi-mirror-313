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
    'GetResourcesResult',
    'AwaitableGetResourcesResult',
    'get_resources',
    'get_resources_output',
]

@pulumi.output_type
class GetResourcesResult:
    """
    A collection of values returned by getResources.
    """
    def __init__(__self__, id=None, name=None, required_tags=None, resource_group_name=None, resources=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if required_tags and not isinstance(required_tags, dict):
            raise TypeError("Expected argument 'required_tags' to be a dict")
        pulumi.set(__self__, "required_tags", required_tags)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if resources and not isinstance(resources, list):
            raise TypeError("Expected argument 'resources' to be a list")
        pulumi.set(__self__, "resources", resources)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

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
        """
        The name of this Resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="requiredTags")
    def required_tags(self) -> Optional[Mapping[str, str]]:
        return pulumi.get(self, "required_tags")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        """
        The name of the Resource Group in which this Resource exists.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def resources(self) -> Sequence['outputs.GetResourcesResourceResult']:
        """
        One or more `resource` blocks as defined below.
        """
        return pulumi.get(self, "resources")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of this Resource. (e.g. `Microsoft.Network/virtualNetworks`).
        """
        return pulumi.get(self, "type")


class AwaitableGetResourcesResult(GetResourcesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResourcesResult(
            id=self.id,
            name=self.name,
            required_tags=self.required_tags,
            resource_group_name=self.resource_group_name,
            resources=self.resources,
            type=self.type)


def get_resources(name: Optional[str] = None,
                  required_tags: Optional[Mapping[str, str]] = None,
                  resource_group_name: Optional[str] = None,
                  type: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResourcesResult:
    """
    Use this data source to access information about existing resources.


    :param str name: The name of the Resource.
    :param Mapping[str, str] required_tags: A mapping of tags which the resource has to have in order to be included in the result.
    :param str resource_group_name: The name of the Resource group where the Resources are located.
    :param str type: The Resource Type of the Resources you want to list (e.g. `Microsoft.Network/virtualNetworks`). A resource type's name follows the format: `{resource-provider}/{resource-type}`. The resource type for a key vault is `Microsoft.KeyVault/vaults`. A full list of available Resource Providers can be found [here](https://docs.microsoft.com/azure/azure-resource-manager/azure-services-resource-providers). A full list of Resources Types can be found [here](https://learn.microsoft.com/en-us/azure/templates/#find-resources).
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['requiredTags'] = required_tags
    __args__['resourceGroupName'] = resource_group_name
    __args__['type'] = type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:core/getResources:getResources', __args__, opts=opts, typ=GetResourcesResult).value

    return AwaitableGetResourcesResult(
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        required_tags=pulumi.get(__ret__, 'required_tags'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        resources=pulumi.get(__ret__, 'resources'),
        type=pulumi.get(__ret__, 'type'))
def get_resources_output(name: Optional[pulumi.Input[Optional[str]]] = None,
                         required_tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                         resource_group_name: Optional[pulumi.Input[Optional[str]]] = None,
                         type: Optional[pulumi.Input[Optional[str]]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResourcesResult]:
    """
    Use this data source to access information about existing resources.


    :param str name: The name of the Resource.
    :param Mapping[str, str] required_tags: A mapping of tags which the resource has to have in order to be included in the result.
    :param str resource_group_name: The name of the Resource group where the Resources are located.
    :param str type: The Resource Type of the Resources you want to list (e.g. `Microsoft.Network/virtualNetworks`). A resource type's name follows the format: `{resource-provider}/{resource-type}`. The resource type for a key vault is `Microsoft.KeyVault/vaults`. A full list of available Resource Providers can be found [here](https://docs.microsoft.com/azure/azure-resource-manager/azure-services-resource-providers). A full list of Resources Types can be found [here](https://learn.microsoft.com/en-us/azure/templates/#find-resources).
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['requiredTags'] = required_tags
    __args__['resourceGroupName'] = resource_group_name
    __args__['type'] = type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:core/getResources:getResources', __args__, opts=opts, typ=GetResourcesResult)
    return __ret__.apply(lambda __response__: GetResourcesResult(
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        required_tags=pulumi.get(__response__, 'required_tags'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        resources=pulumi.get(__response__, 'resources'),
        type=pulumi.get(__response__, 'type')))
