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
    'GetGroupResult',
    'AwaitableGetGroupResult',
    'get_group',
    'get_group_output',
]

@pulumi.output_type
class GetGroupResult:
    """
    A collection of values returned by getGroup.
    """
    def __init__(__self__, api_management_name=None, description=None, display_name=None, external_id=None, id=None, name=None, resource_group_name=None, type=None):
        if api_management_name and not isinstance(api_management_name, str):
            raise TypeError("Expected argument 'api_management_name' to be a str")
        pulumi.set(__self__, "api_management_name", api_management_name)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if external_id and not isinstance(external_id, str):
            raise TypeError("Expected argument 'external_id' to be a str")
        pulumi.set(__self__, "external_id", external_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="apiManagementName")
    def api_management_name(self) -> str:
        return pulumi.get(self, "api_management_name")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of this API Management Group.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The display name of this API Management Group.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="externalId")
    def external_id(self) -> str:
        """
        The identifier of the external Group.
        """
        return pulumi.get(self, "external_id")

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
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of this API Management Group, such as `custom` or `external`.
        """
        return pulumi.get(self, "type")


class AwaitableGetGroupResult(GetGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGroupResult(
            api_management_name=self.api_management_name,
            description=self.description,
            display_name=self.display_name,
            external_id=self.external_id,
            id=self.id,
            name=self.name,
            resource_group_name=self.resource_group_name,
            type=self.type)


def get_group(api_management_name: Optional[str] = None,
              name: Optional[str] = None,
              resource_group_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGroupResult:
    """
    Use this data source to access information about an existing API Management Group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.apimanagement.get_group(name="my-group",
        api_management_name="example-apim",
        resource_group_name="search-service")
    pulumi.export("groupType", example.type)
    ```


    :param str api_management_name: The Name of the API Management Service in which this Group exists.
    :param str name: The Name of the API Management Group.
    :param str resource_group_name: The Name of the Resource Group in which the API Management Service exists.
    """
    __args__ = dict()
    __args__['apiManagementName'] = api_management_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:apimanagement/getGroup:getGroup', __args__, opts=opts, typ=GetGroupResult).value

    return AwaitableGetGroupResult(
        api_management_name=pulumi.get(__ret__, 'api_management_name'),
        description=pulumi.get(__ret__, 'description'),
        display_name=pulumi.get(__ret__, 'display_name'),
        external_id=pulumi.get(__ret__, 'external_id'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        type=pulumi.get(__ret__, 'type'))
def get_group_output(api_management_name: Optional[pulumi.Input[str]] = None,
                     name: Optional[pulumi.Input[str]] = None,
                     resource_group_name: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGroupResult]:
    """
    Use this data source to access information about an existing API Management Group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.apimanagement.get_group(name="my-group",
        api_management_name="example-apim",
        resource_group_name="search-service")
    pulumi.export("groupType", example.type)
    ```


    :param str api_management_name: The Name of the API Management Service in which this Group exists.
    :param str name: The Name of the API Management Group.
    :param str resource_group_name: The Name of the Resource Group in which the API Management Service exists.
    """
    __args__ = dict()
    __args__['apiManagementName'] = api_management_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:apimanagement/getGroup:getGroup', __args__, opts=opts, typ=GetGroupResult)
    return __ret__.apply(lambda __response__: GetGroupResult(
        api_management_name=pulumi.get(__response__, 'api_management_name'),
        description=pulumi.get(__response__, 'description'),
        display_name=pulumi.get(__response__, 'display_name'),
        external_id=pulumi.get(__response__, 'external_id'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        type=pulumi.get(__response__, 'type')))
