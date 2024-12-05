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
    'GetSnapshotPolicyResult',
    'AwaitableGetSnapshotPolicyResult',
    'get_snapshot_policy',
    'get_snapshot_policy_output',
]

@pulumi.output_type
class GetSnapshotPolicyResult:
    """
    A collection of values returned by getSnapshotPolicy.
    """
    def __init__(__self__, account_name=None, daily_schedules=None, enabled=None, hourly_schedules=None, id=None, location=None, monthly_schedules=None, name=None, resource_group_name=None, tags=None, weekly_schedules=None):
        if account_name and not isinstance(account_name, str):
            raise TypeError("Expected argument 'account_name' to be a str")
        pulumi.set(__self__, "account_name", account_name)
        if daily_schedules and not isinstance(daily_schedules, list):
            raise TypeError("Expected argument 'daily_schedules' to be a list")
        pulumi.set(__self__, "daily_schedules", daily_schedules)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if hourly_schedules and not isinstance(hourly_schedules, list):
            raise TypeError("Expected argument 'hourly_schedules' to be a list")
        pulumi.set(__self__, "hourly_schedules", hourly_schedules)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if monthly_schedules and not isinstance(monthly_schedules, list):
            raise TypeError("Expected argument 'monthly_schedules' to be a list")
        pulumi.set(__self__, "monthly_schedules", monthly_schedules)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if weekly_schedules and not isinstance(weekly_schedules, list):
            raise TypeError("Expected argument 'weekly_schedules' to be a list")
        pulumi.set(__self__, "weekly_schedules", weekly_schedules)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> str:
        """
        The name of the NetApp Account in which the NetApp Snapshot Policy was created.
        """
        return pulumi.get(self, "account_name")

    @property
    @pulumi.getter(name="dailySchedules")
    def daily_schedules(self) -> Sequence['outputs.GetSnapshotPolicyDailyScheduleResult']:
        """
        Daily snapshot schedule.
        """
        return pulumi.get(self, "daily_schedules")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Defines that the NetApp Snapshot Policy is enabled or not.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="hourlySchedules")
    def hourly_schedules(self) -> Sequence['outputs.GetSnapshotPolicyHourlyScheduleResult']:
        """
        Hourly snapshot schedule.
        """
        return pulumi.get(self, "hourly_schedules")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Specifies the supported Azure location where the resource exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="monthlySchedules")
    def monthly_schedules(self) -> Sequence['outputs.GetSnapshotPolicyMonthlyScheduleResult']:
        """
        List of the days of the month when the snapshots will be created.
        """
        return pulumi.get(self, "monthly_schedules")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the NetApp Snapshot Policy.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        """
        The name of the resource group where the NetApp Snapshot Policy should be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="weeklySchedules")
    def weekly_schedules(self) -> Sequence['outputs.GetSnapshotPolicyWeeklyScheduleResult']:
        """
        Weekly snapshot schedule.
        """
        return pulumi.get(self, "weekly_schedules")


class AwaitableGetSnapshotPolicyResult(GetSnapshotPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSnapshotPolicyResult(
            account_name=self.account_name,
            daily_schedules=self.daily_schedules,
            enabled=self.enabled,
            hourly_schedules=self.hourly_schedules,
            id=self.id,
            location=self.location,
            monthly_schedules=self.monthly_schedules,
            name=self.name,
            resource_group_name=self.resource_group_name,
            tags=self.tags,
            weekly_schedules=self.weekly_schedules)


def get_snapshot_policy(account_name: Optional[str] = None,
                        name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSnapshotPolicyResult:
    """
    Uses this data source to access information about an existing NetApp Snapshot Policy.

    ## NetApp Snapshot Policy Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.netapp.get_snapshot_policy(resource_group_name="acctestRG",
        account_name="acctestnetappaccount",
        name="example-snapshot-policy")
    pulumi.export("id", example.id)
    pulumi.export("name", example.name)
    pulumi.export("enabled", example.enabled)
    pulumi.export("hourlySchedule", example.hourly_schedules)
    pulumi.export("dailySchedule", example.daily_schedules)
    pulumi.export("weeklySchedule", example.weekly_schedules)
    pulumi.export("monthlySchedule", example.monthly_schedules)
    ```


    :param str account_name: The name of the NetApp account where the NetApp Snapshot Policy exists.
    :param str name: The name of the NetApp Snapshot Policy.
    :param str resource_group_name: The Name of the Resource Group where the NetApp Snapshot Policy exists.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:netapp/getSnapshotPolicy:getSnapshotPolicy', __args__, opts=opts, typ=GetSnapshotPolicyResult).value

    return AwaitableGetSnapshotPolicyResult(
        account_name=pulumi.get(__ret__, 'account_name'),
        daily_schedules=pulumi.get(__ret__, 'daily_schedules'),
        enabled=pulumi.get(__ret__, 'enabled'),
        hourly_schedules=pulumi.get(__ret__, 'hourly_schedules'),
        id=pulumi.get(__ret__, 'id'),
        location=pulumi.get(__ret__, 'location'),
        monthly_schedules=pulumi.get(__ret__, 'monthly_schedules'),
        name=pulumi.get(__ret__, 'name'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        tags=pulumi.get(__ret__, 'tags'),
        weekly_schedules=pulumi.get(__ret__, 'weekly_schedules'))
def get_snapshot_policy_output(account_name: Optional[pulumi.Input[str]] = None,
                               name: Optional[pulumi.Input[str]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSnapshotPolicyResult]:
    """
    Uses this data source to access information about an existing NetApp Snapshot Policy.

    ## NetApp Snapshot Policy Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.netapp.get_snapshot_policy(resource_group_name="acctestRG",
        account_name="acctestnetappaccount",
        name="example-snapshot-policy")
    pulumi.export("id", example.id)
    pulumi.export("name", example.name)
    pulumi.export("enabled", example.enabled)
    pulumi.export("hourlySchedule", example.hourly_schedules)
    pulumi.export("dailySchedule", example.daily_schedules)
    pulumi.export("weeklySchedule", example.weekly_schedules)
    pulumi.export("monthlySchedule", example.monthly_schedules)
    ```


    :param str account_name: The name of the NetApp account where the NetApp Snapshot Policy exists.
    :param str name: The name of the NetApp Snapshot Policy.
    :param str resource_group_name: The Name of the Resource Group where the NetApp Snapshot Policy exists.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:netapp/getSnapshotPolicy:getSnapshotPolicy', __args__, opts=opts, typ=GetSnapshotPolicyResult)
    return __ret__.apply(lambda __response__: GetSnapshotPolicyResult(
        account_name=pulumi.get(__response__, 'account_name'),
        daily_schedules=pulumi.get(__response__, 'daily_schedules'),
        enabled=pulumi.get(__response__, 'enabled'),
        hourly_schedules=pulumi.get(__response__, 'hourly_schedules'),
        id=pulumi.get(__response__, 'id'),
        location=pulumi.get(__response__, 'location'),
        monthly_schedules=pulumi.get(__response__, 'monthly_schedules'),
        name=pulumi.get(__response__, 'name'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        tags=pulumi.get(__response__, 'tags'),
        weekly_schedules=pulumi.get(__response__, 'weekly_schedules')))
