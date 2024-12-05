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
    'GetApplicationResult',
    'AwaitableGetApplicationResult',
    'get_application',
    'get_application_output',
]

@pulumi.output_type
class GetApplicationResult:
    """
    A collection of values returned by getApplication.
    """
    def __init__(__self__, account_name=None, allow_updates=None, default_version=None, display_name=None, id=None, name=None, resource_group_name=None):
        if account_name and not isinstance(account_name, str):
            raise TypeError("Expected argument 'account_name' to be a str")
        pulumi.set(__self__, "account_name", account_name)
        if allow_updates and not isinstance(allow_updates, bool):
            raise TypeError("Expected argument 'allow_updates' to be a bool")
        pulumi.set(__self__, "allow_updates", allow_updates)
        if default_version and not isinstance(default_version, str):
            raise TypeError("Expected argument 'default_version' to be a str")
        pulumi.set(__self__, "default_version", default_version)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> str:
        return pulumi.get(self, "account_name")

    @property
    @pulumi.getter(name="allowUpdates")
    def allow_updates(self) -> bool:
        """
        May packages within the application be overwritten using the same version string.
        """
        return pulumi.get(self, "allow_updates")

    @property
    @pulumi.getter(name="defaultVersion")
    def default_version(self) -> str:
        """
        The package to use if a client requests the application but does not specify a version.
        """
        return pulumi.get(self, "default_version")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The display name for the application.
        """
        return pulumi.get(self, "display_name")

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
        The Batch application name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")


class AwaitableGetApplicationResult(GetApplicationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationResult(
            account_name=self.account_name,
            allow_updates=self.allow_updates,
            default_version=self.default_version,
            display_name=self.display_name,
            id=self.id,
            name=self.name,
            resource_group_name=self.resource_group_name)


def get_application(account_name: Optional[str] = None,
                    name: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationResult:
    """
    Use this data source to access information about an existing Batch Application instance.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.batch.get_application(name="testapplication",
        resource_group_name="test",
        account_name="testbatchaccount")
    pulumi.export("batchApplicationId", example.id)
    ```


    :param str account_name: The name of the Batch account.
    :param str name: The name of the Application.
    :param str resource_group_name: The name of the Resource Group where this Batch account exists.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:batch/getApplication:getApplication', __args__, opts=opts, typ=GetApplicationResult).value

    return AwaitableGetApplicationResult(
        account_name=pulumi.get(__ret__, 'account_name'),
        allow_updates=pulumi.get(__ret__, 'allow_updates'),
        default_version=pulumi.get(__ret__, 'default_version'),
        display_name=pulumi.get(__ret__, 'display_name'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'))
def get_application_output(account_name: Optional[pulumi.Input[str]] = None,
                           name: Optional[pulumi.Input[str]] = None,
                           resource_group_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetApplicationResult]:
    """
    Use this data source to access information about an existing Batch Application instance.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.batch.get_application(name="testapplication",
        resource_group_name="test",
        account_name="testbatchaccount")
    pulumi.export("batchApplicationId", example.id)
    ```


    :param str account_name: The name of the Batch account.
    :param str name: The name of the Application.
    :param str resource_group_name: The name of the Resource Group where this Batch account exists.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:batch/getApplication:getApplication', __args__, opts=opts, typ=GetApplicationResult)
    return __ret__.apply(lambda __response__: GetApplicationResult(
        account_name=pulumi.get(__response__, 'account_name'),
        allow_updates=pulumi.get(__response__, 'allow_updates'),
        default_version=pulumi.get(__response__, 'default_version'),
        display_name=pulumi.get(__response__, 'display_name'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name')))
