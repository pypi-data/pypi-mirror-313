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
    'GetConfigurationResult',
    'AwaitableGetConfigurationResult',
    'get_configuration',
    'get_configuration_output',
]

@pulumi.output_type
class GetConfigurationResult:
    """
    A collection of values returned by getConfiguration.
    """
    def __init__(__self__, id=None, in_guest_user_patch_mode=None, install_patches=None, location=None, name=None, properties=None, resource_group_name=None, scope=None, tags=None, visibility=None, windows=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if in_guest_user_patch_mode and not isinstance(in_guest_user_patch_mode, str):
            raise TypeError("Expected argument 'in_guest_user_patch_mode' to be a str")
        pulumi.set(__self__, "in_guest_user_patch_mode", in_guest_user_patch_mode)
        if install_patches and not isinstance(install_patches, list):
            raise TypeError("Expected argument 'install_patches' to be a list")
        pulumi.set(__self__, "install_patches", install_patches)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if scope and not isinstance(scope, str):
            raise TypeError("Expected argument 'scope' to be a str")
        pulumi.set(__self__, "scope", scope)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if visibility and not isinstance(visibility, str):
            raise TypeError("Expected argument 'visibility' to be a str")
        pulumi.set(__self__, "visibility", visibility)
        if windows and not isinstance(windows, list):
            raise TypeError("Expected argument 'windows' to be a list")
        pulumi.set(__self__, "windows", windows)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="inGuestUserPatchMode")
    def in_guest_user_patch_mode(self) -> str:
        """
        The in guest user patch mode.
        """
        return pulumi.get(self, "in_guest_user_patch_mode")

    @property
    @pulumi.getter(name="installPatches")
    def install_patches(self) -> Sequence['outputs.GetConfigurationInstallPatchResult']:
        """
        An `install_patches` block as defined below.
        """
        return pulumi.get(self, "install_patches")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure location where the resource exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> Mapping[str, str]:
        """
        The properties assigned to the resource.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def scope(self) -> str:
        """
        The scope of the Maintenance Configuration.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def visibility(self) -> str:
        """
        The visibility of the Maintenance Configuration.
        """
        return pulumi.get(self, "visibility")

    @property
    @pulumi.getter
    def windows(self) -> Sequence['outputs.GetConfigurationWindowResult']:
        """
        A `window` block as defined below.
        """
        return pulumi.get(self, "windows")


class AwaitableGetConfigurationResult(GetConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConfigurationResult(
            id=self.id,
            in_guest_user_patch_mode=self.in_guest_user_patch_mode,
            install_patches=self.install_patches,
            location=self.location,
            name=self.name,
            properties=self.properties,
            resource_group_name=self.resource_group_name,
            scope=self.scope,
            tags=self.tags,
            visibility=self.visibility,
            windows=self.windows)


def get_configuration(name: Optional[str] = None,
                      resource_group_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConfigurationResult:
    """
    Use this data source to access information about an existing Maintenance Configuration.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    existing = azure.maintenance.get_configuration(name="example-mc",
        resource_group_name="example-resources")
    pulumi.export("id", existing_azurerm_maintenance_configuration["id"])
    ```


    :param str name: Specifies the name of the Maintenance Configuration.
    :param str resource_group_name: Specifies the name of the Resource Group where this Maintenance Configuration exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:maintenance/getConfiguration:getConfiguration', __args__, opts=opts, typ=GetConfigurationResult).value

    return AwaitableGetConfigurationResult(
        id=pulumi.get(__ret__, 'id'),
        in_guest_user_patch_mode=pulumi.get(__ret__, 'in_guest_user_patch_mode'),
        install_patches=pulumi.get(__ret__, 'install_patches'),
        location=pulumi.get(__ret__, 'location'),
        name=pulumi.get(__ret__, 'name'),
        properties=pulumi.get(__ret__, 'properties'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        scope=pulumi.get(__ret__, 'scope'),
        tags=pulumi.get(__ret__, 'tags'),
        visibility=pulumi.get(__ret__, 'visibility'),
        windows=pulumi.get(__ret__, 'windows'))
def get_configuration_output(name: Optional[pulumi.Input[str]] = None,
                             resource_group_name: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetConfigurationResult]:
    """
    Use this data source to access information about an existing Maintenance Configuration.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    existing = azure.maintenance.get_configuration(name="example-mc",
        resource_group_name="example-resources")
    pulumi.export("id", existing_azurerm_maintenance_configuration["id"])
    ```


    :param str name: Specifies the name of the Maintenance Configuration.
    :param str resource_group_name: Specifies the name of the Resource Group where this Maintenance Configuration exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:maintenance/getConfiguration:getConfiguration', __args__, opts=opts, typ=GetConfigurationResult)
    return __ret__.apply(lambda __response__: GetConfigurationResult(
        id=pulumi.get(__response__, 'id'),
        in_guest_user_patch_mode=pulumi.get(__response__, 'in_guest_user_patch_mode'),
        install_patches=pulumi.get(__response__, 'install_patches'),
        location=pulumi.get(__response__, 'location'),
        name=pulumi.get(__response__, 'name'),
        properties=pulumi.get(__response__, 'properties'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        scope=pulumi.get(__response__, 'scope'),
        tags=pulumi.get(__response__, 'tags'),
        visibility=pulumi.get(__response__, 'visibility'),
        windows=pulumi.get(__response__, 'windows')))
