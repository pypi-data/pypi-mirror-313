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
    'GetManagedDatabaseResult',
    'AwaitableGetManagedDatabaseResult',
    'get_managed_database',
    'get_managed_database_output',
]

@pulumi.output_type
class GetManagedDatabaseResult:
    """
    A collection of values returned by getManagedDatabase.
    """
    def __init__(__self__, id=None, long_term_retention_policies=None, managed_instance_id=None, managed_instance_name=None, name=None, point_in_time_restores=None, resource_group_name=None, short_term_retention_days=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if long_term_retention_policies and not isinstance(long_term_retention_policies, list):
            raise TypeError("Expected argument 'long_term_retention_policies' to be a list")
        pulumi.set(__self__, "long_term_retention_policies", long_term_retention_policies)
        if managed_instance_id and not isinstance(managed_instance_id, str):
            raise TypeError("Expected argument 'managed_instance_id' to be a str")
        pulumi.set(__self__, "managed_instance_id", managed_instance_id)
        if managed_instance_name and not isinstance(managed_instance_name, str):
            raise TypeError("Expected argument 'managed_instance_name' to be a str")
        pulumi.set(__self__, "managed_instance_name", managed_instance_name)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if point_in_time_restores and not isinstance(point_in_time_restores, list):
            raise TypeError("Expected argument 'point_in_time_restores' to be a list")
        pulumi.set(__self__, "point_in_time_restores", point_in_time_restores)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if short_term_retention_days and not isinstance(short_term_retention_days, int):
            raise TypeError("Expected argument 'short_term_retention_days' to be a int")
        pulumi.set(__self__, "short_term_retention_days", short_term_retention_days)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="longTermRetentionPolicies")
    def long_term_retention_policies(self) -> Sequence['outputs.GetManagedDatabaseLongTermRetentionPolicyResult']:
        """
        A `long_term_retention_policy` block as defined below.
        """
        return pulumi.get(self, "long_term_retention_policies")

    @property
    @pulumi.getter(name="managedInstanceId")
    def managed_instance_id(self) -> str:
        return pulumi.get(self, "managed_instance_id")

    @property
    @pulumi.getter(name="managedInstanceName")
    def managed_instance_name(self) -> str:
        """
        The name of the Managed Instance.
        """
        return pulumi.get(self, "managed_instance_name")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pointInTimeRestores")
    def point_in_time_restores(self) -> Sequence['outputs.GetManagedDatabasePointInTimeRestoreResult']:
        """
        A `point_in_time_restore` block as defined below.
        """
        return pulumi.get(self, "point_in_time_restores")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        """
        The name of the Resource Group where the Azure SQL Azure Managed Instance exists.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="shortTermRetentionDays")
    def short_term_retention_days(self) -> int:
        """
        The backup retention period in days. This is how many days Point-in-Time Restore will be supported.
        """
        return pulumi.get(self, "short_term_retention_days")


class AwaitableGetManagedDatabaseResult(GetManagedDatabaseResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagedDatabaseResult(
            id=self.id,
            long_term_retention_policies=self.long_term_retention_policies,
            managed_instance_id=self.managed_instance_id,
            managed_instance_name=self.managed_instance_name,
            name=self.name,
            point_in_time_restores=self.point_in_time_restores,
            resource_group_name=self.resource_group_name,
            short_term_retention_days=self.short_term_retention_days)


def get_managed_database(managed_instance_id: Optional[str] = None,
                         name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagedDatabaseResult:
    """
    Use this data source to access information about an existing Azure SQL Azure Managed Database.


    :param str managed_instance_id: The SQL Managed Instance ID.
    :param str name: The name of this Azure SQL Azure Managed Database.
    """
    __args__ = dict()
    __args__['managedInstanceId'] = managed_instance_id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:mssql/getManagedDatabase:getManagedDatabase', __args__, opts=opts, typ=GetManagedDatabaseResult).value

    return AwaitableGetManagedDatabaseResult(
        id=pulumi.get(__ret__, 'id'),
        long_term_retention_policies=pulumi.get(__ret__, 'long_term_retention_policies'),
        managed_instance_id=pulumi.get(__ret__, 'managed_instance_id'),
        managed_instance_name=pulumi.get(__ret__, 'managed_instance_name'),
        name=pulumi.get(__ret__, 'name'),
        point_in_time_restores=pulumi.get(__ret__, 'point_in_time_restores'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        short_term_retention_days=pulumi.get(__ret__, 'short_term_retention_days'))
def get_managed_database_output(managed_instance_id: Optional[pulumi.Input[str]] = None,
                                name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetManagedDatabaseResult]:
    """
    Use this data source to access information about an existing Azure SQL Azure Managed Database.


    :param str managed_instance_id: The SQL Managed Instance ID.
    :param str name: The name of this Azure SQL Azure Managed Database.
    """
    __args__ = dict()
    __args__['managedInstanceId'] = managed_instance_id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:mssql/getManagedDatabase:getManagedDatabase', __args__, opts=opts, typ=GetManagedDatabaseResult)
    return __ret__.apply(lambda __response__: GetManagedDatabaseResult(
        id=pulumi.get(__response__, 'id'),
        long_term_retention_policies=pulumi.get(__response__, 'long_term_retention_policies'),
        managed_instance_id=pulumi.get(__response__, 'managed_instance_id'),
        managed_instance_name=pulumi.get(__response__, 'managed_instance_name'),
        name=pulumi.get(__response__, 'name'),
        point_in_time_restores=pulumi.get(__response__, 'point_in_time_restores'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        short_term_retention_days=pulumi.get(__response__, 'short_term_retention_days')))
