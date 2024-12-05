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
    def __init__(__self__, all_management_group_ids=None, all_subscription_ids=None, display_name=None, id=None, management_group_ids=None, name=None, parent_management_group_id=None, subscription_ids=None, tenant_scoped_id=None):
        if all_management_group_ids and not isinstance(all_management_group_ids, list):
            raise TypeError("Expected argument 'all_management_group_ids' to be a list")
        pulumi.set(__self__, "all_management_group_ids", all_management_group_ids)
        if all_subscription_ids and not isinstance(all_subscription_ids, list):
            raise TypeError("Expected argument 'all_subscription_ids' to be a list")
        pulumi.set(__self__, "all_subscription_ids", all_subscription_ids)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if management_group_ids and not isinstance(management_group_ids, list):
            raise TypeError("Expected argument 'management_group_ids' to be a list")
        pulumi.set(__self__, "management_group_ids", management_group_ids)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if parent_management_group_id and not isinstance(parent_management_group_id, str):
            raise TypeError("Expected argument 'parent_management_group_id' to be a str")
        pulumi.set(__self__, "parent_management_group_id", parent_management_group_id)
        if subscription_ids and not isinstance(subscription_ids, list):
            raise TypeError("Expected argument 'subscription_ids' to be a list")
        pulumi.set(__self__, "subscription_ids", subscription_ids)
        if tenant_scoped_id and not isinstance(tenant_scoped_id, str):
            raise TypeError("Expected argument 'tenant_scoped_id' to be a str")
        pulumi.set(__self__, "tenant_scoped_id", tenant_scoped_id)

    @property
    @pulumi.getter(name="allManagementGroupIds")
    def all_management_group_ids(self) -> Sequence[str]:
        """
        A list of Management Group IDs which directly or indirectly belong to this Management Group.
        """
        return pulumi.get(self, "all_management_group_ids")

    @property
    @pulumi.getter(name="allSubscriptionIds")
    def all_subscription_ids(self) -> Sequence[str]:
        """
        A list of Subscription IDs which are assigned to this Management Group or its children Management Groups.
        """
        return pulumi.get(self, "all_subscription_ids")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="managementGroupIds")
    def management_group_ids(self) -> Sequence[str]:
        """
        A list of Management Group IDs which directly belong to this Management Group.
        """
        return pulumi.get(self, "management_group_ids")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="parentManagementGroupId")
    def parent_management_group_id(self) -> str:
        """
        The ID of any Parent Management Group.
        """
        return pulumi.get(self, "parent_management_group_id")

    @property
    @pulumi.getter(name="subscriptionIds")
    def subscription_ids(self) -> Sequence[str]:
        """
        A list of Subscription IDs which are directly assigned to this Management Group.
        """
        return pulumi.get(self, "subscription_ids")

    @property
    @pulumi.getter(name="tenantScopedId")
    def tenant_scoped_id(self) -> str:
        """
        The Management Group ID with the Tenant ID prefix.
        """
        return pulumi.get(self, "tenant_scoped_id")


class AwaitableGetGroupResult(GetGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGroupResult(
            all_management_group_ids=self.all_management_group_ids,
            all_subscription_ids=self.all_subscription_ids,
            display_name=self.display_name,
            id=self.id,
            management_group_ids=self.management_group_ids,
            name=self.name,
            parent_management_group_id=self.parent_management_group_id,
            subscription_ids=self.subscription_ids,
            tenant_scoped_id=self.tenant_scoped_id)


def get_group(display_name: Optional[str] = None,
              name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGroupResult:
    """
    Use this data source to access information about an existing Management Group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.management.get_group(name="00000000-0000-0000-0000-000000000000")
    pulumi.export("displayName", example.display_name)
    ```


    :param str display_name: Specifies the display name of this Management Group.
           
           > **NOTE** Whilst multiple management groups may share the same display name, when filtering, the provider expects a single management group to be found with this name.
    :param str name: Specifies the name or UUID of this Management Group.
    """
    __args__ = dict()
    __args__['displayName'] = display_name
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:management/getGroup:getGroup', __args__, opts=opts, typ=GetGroupResult).value

    return AwaitableGetGroupResult(
        all_management_group_ids=pulumi.get(__ret__, 'all_management_group_ids'),
        all_subscription_ids=pulumi.get(__ret__, 'all_subscription_ids'),
        display_name=pulumi.get(__ret__, 'display_name'),
        id=pulumi.get(__ret__, 'id'),
        management_group_ids=pulumi.get(__ret__, 'management_group_ids'),
        name=pulumi.get(__ret__, 'name'),
        parent_management_group_id=pulumi.get(__ret__, 'parent_management_group_id'),
        subscription_ids=pulumi.get(__ret__, 'subscription_ids'),
        tenant_scoped_id=pulumi.get(__ret__, 'tenant_scoped_id'))
def get_group_output(display_name: Optional[pulumi.Input[Optional[str]]] = None,
                     name: Optional[pulumi.Input[Optional[str]]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGroupResult]:
    """
    Use this data source to access information about an existing Management Group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.management.get_group(name="00000000-0000-0000-0000-000000000000")
    pulumi.export("displayName", example.display_name)
    ```


    :param str display_name: Specifies the display name of this Management Group.
           
           > **NOTE** Whilst multiple management groups may share the same display name, when filtering, the provider expects a single management group to be found with this name.
    :param str name: Specifies the name or UUID of this Management Group.
    """
    __args__ = dict()
    __args__['displayName'] = display_name
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:management/getGroup:getGroup', __args__, opts=opts, typ=GetGroupResult)
    return __ret__.apply(lambda __response__: GetGroupResult(
        all_management_group_ids=pulumi.get(__response__, 'all_management_group_ids'),
        all_subscription_ids=pulumi.get(__response__, 'all_subscription_ids'),
        display_name=pulumi.get(__response__, 'display_name'),
        id=pulumi.get(__response__, 'id'),
        management_group_ids=pulumi.get(__response__, 'management_group_ids'),
        name=pulumi.get(__response__, 'name'),
        parent_management_group_id=pulumi.get(__response__, 'parent_management_group_id'),
        subscription_ids=pulumi.get(__response__, 'subscription_ids'),
        tenant_scoped_id=pulumi.get(__response__, 'tenant_scoped_id')))
