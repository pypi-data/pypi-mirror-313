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
from ._inputs import *

__all__ = ['BackupPolicyKubernetesClusterArgs', 'BackupPolicyKubernetesCluster']

@pulumi.input_type
class BackupPolicyKubernetesClusterArgs:
    def __init__(__self__, *,
                 backup_repeating_time_intervals: pulumi.Input[Sequence[pulumi.Input[str]]],
                 default_retention_rule: pulumi.Input['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs'],
                 resource_group_name: pulumi.Input[str],
                 vault_name: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 retention_rules: Optional[pulumi.Input[Sequence[pulumi.Input['BackupPolicyKubernetesClusterRetentionRuleArgs']]]] = None,
                 time_zone: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BackupPolicyKubernetesCluster resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] backup_repeating_time_intervals: Specifies a list of repeating time interval. It supports weekly back. It should follow `ISO 8601` repeating time interval. Changing this forces a new resource to be created.
        :param pulumi.Input['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs'] default_retention_rule: A `default_retention_rule` block as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] vault_name: The name of the Backup Vault where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name which should be used for the Backup Policy Kubernetes Cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['BackupPolicyKubernetesClusterRetentionRuleArgs']]] retention_rules: One or more `retention_rule` blocks as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] time_zone: Specifies the Time Zone which should be used by the backup schedule. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "backup_repeating_time_intervals", backup_repeating_time_intervals)
        pulumi.set(__self__, "default_retention_rule", default_retention_rule)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "vault_name", vault_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if retention_rules is not None:
            pulumi.set(__self__, "retention_rules", retention_rules)
        if time_zone is not None:
            pulumi.set(__self__, "time_zone", time_zone)

    @property
    @pulumi.getter(name="backupRepeatingTimeIntervals")
    def backup_repeating_time_intervals(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Specifies a list of repeating time interval. It supports weekly back. It should follow `ISO 8601` repeating time interval. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "backup_repeating_time_intervals")

    @backup_repeating_time_intervals.setter
    def backup_repeating_time_intervals(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "backup_repeating_time_intervals", value)

    @property
    @pulumi.getter(name="defaultRetentionRule")
    def default_retention_rule(self) -> pulumi.Input['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs']:
        """
        A `default_retention_rule` block as defined below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "default_retention_rule")

    @default_retention_rule.setter
    def default_retention_rule(self, value: pulumi.Input['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs']):
        pulumi.set(self, "default_retention_rule", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="vaultName")
    def vault_name(self) -> pulumi.Input[str]:
        """
        The name of the Backup Vault where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "vault_name")

    @vault_name.setter
    def vault_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "vault_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for the Backup Policy Kubernetes Cluster. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="retentionRules")
    def retention_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BackupPolicyKubernetesClusterRetentionRuleArgs']]]]:
        """
        One or more `retention_rule` blocks as defined below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "retention_rules")

    @retention_rules.setter
    def retention_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BackupPolicyKubernetesClusterRetentionRuleArgs']]]]):
        pulumi.set(self, "retention_rules", value)

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Time Zone which should be used by the backup schedule. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "time_zone")

    @time_zone.setter
    def time_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "time_zone", value)


@pulumi.input_type
class _BackupPolicyKubernetesClusterState:
    def __init__(__self__, *,
                 backup_repeating_time_intervals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 default_retention_rule: Optional[pulumi.Input['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 retention_rules: Optional[pulumi.Input[Sequence[pulumi.Input['BackupPolicyKubernetesClusterRetentionRuleArgs']]]] = None,
                 time_zone: Optional[pulumi.Input[str]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BackupPolicyKubernetesCluster resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] backup_repeating_time_intervals: Specifies a list of repeating time interval. It supports weekly back. It should follow `ISO 8601` repeating time interval. Changing this forces a new resource to be created.
        :param pulumi.Input['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs'] default_retention_rule: A `default_retention_rule` block as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name which should be used for the Backup Policy Kubernetes Cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['BackupPolicyKubernetesClusterRetentionRuleArgs']]] retention_rules: One or more `retention_rule` blocks as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] time_zone: Specifies the Time Zone which should be used by the backup schedule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] vault_name: The name of the Backup Vault where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        """
        if backup_repeating_time_intervals is not None:
            pulumi.set(__self__, "backup_repeating_time_intervals", backup_repeating_time_intervals)
        if default_retention_rule is not None:
            pulumi.set(__self__, "default_retention_rule", default_retention_rule)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if retention_rules is not None:
            pulumi.set(__self__, "retention_rules", retention_rules)
        if time_zone is not None:
            pulumi.set(__self__, "time_zone", time_zone)
        if vault_name is not None:
            pulumi.set(__self__, "vault_name", vault_name)

    @property
    @pulumi.getter(name="backupRepeatingTimeIntervals")
    def backup_repeating_time_intervals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies a list of repeating time interval. It supports weekly back. It should follow `ISO 8601` repeating time interval. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "backup_repeating_time_intervals")

    @backup_repeating_time_intervals.setter
    def backup_repeating_time_intervals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "backup_repeating_time_intervals", value)

    @property
    @pulumi.getter(name="defaultRetentionRule")
    def default_retention_rule(self) -> Optional[pulumi.Input['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs']]:
        """
        A `default_retention_rule` block as defined below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "default_retention_rule")

    @default_retention_rule.setter
    def default_retention_rule(self, value: Optional[pulumi.Input['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs']]):
        pulumi.set(self, "default_retention_rule", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for the Backup Policy Kubernetes Cluster. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="retentionRules")
    def retention_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BackupPolicyKubernetesClusterRetentionRuleArgs']]]]:
        """
        One or more `retention_rule` blocks as defined below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "retention_rules")

    @retention_rules.setter
    def retention_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BackupPolicyKubernetesClusterRetentionRuleArgs']]]]):
        pulumi.set(self, "retention_rules", value)

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Time Zone which should be used by the backup schedule. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "time_zone")

    @time_zone.setter
    def time_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "time_zone", value)

    @property
    @pulumi.getter(name="vaultName")
    def vault_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Backup Vault where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "vault_name")

    @vault_name.setter
    def vault_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vault_name", value)


class BackupPolicyKubernetesCluster(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backup_repeating_time_intervals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 default_retention_rule: Optional[pulumi.Input[Union['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs', 'BackupPolicyKubernetesClusterDefaultRetentionRuleArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 retention_rules: Optional[pulumi.Input[Sequence[pulumi.Input[Union['BackupPolicyKubernetesClusterRetentionRuleArgs', 'BackupPolicyKubernetesClusterRetentionRuleArgsDict']]]]] = None,
                 time_zone: Optional[pulumi.Input[str]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Backup Policy to back up Kubernetes Cluster.

        ## Import

        Backup Policy Kubernetes Cluster's can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:dataprotection/backupPolicyKubernetesCluster:BackupPolicyKubernetesCluster example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.DataProtection/backupVaults/vault1/backupPolicies/backupPolicy1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] backup_repeating_time_intervals: Specifies a list of repeating time interval. It supports weekly back. It should follow `ISO 8601` repeating time interval. Changing this forces a new resource to be created.
        :param pulumi.Input[Union['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs', 'BackupPolicyKubernetesClusterDefaultRetentionRuleArgsDict']] default_retention_rule: A `default_retention_rule` block as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name which should be used for the Backup Policy Kubernetes Cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[Union['BackupPolicyKubernetesClusterRetentionRuleArgs', 'BackupPolicyKubernetesClusterRetentionRuleArgsDict']]]] retention_rules: One or more `retention_rule` blocks as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] time_zone: Specifies the Time Zone which should be used by the backup schedule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] vault_name: The name of the Backup Vault where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BackupPolicyKubernetesClusterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Backup Policy to back up Kubernetes Cluster.

        ## Import

        Backup Policy Kubernetes Cluster's can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:dataprotection/backupPolicyKubernetesCluster:BackupPolicyKubernetesCluster example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.DataProtection/backupVaults/vault1/backupPolicies/backupPolicy1
        ```

        :param str resource_name: The name of the resource.
        :param BackupPolicyKubernetesClusterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BackupPolicyKubernetesClusterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backup_repeating_time_intervals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 default_retention_rule: Optional[pulumi.Input[Union['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs', 'BackupPolicyKubernetesClusterDefaultRetentionRuleArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 retention_rules: Optional[pulumi.Input[Sequence[pulumi.Input[Union['BackupPolicyKubernetesClusterRetentionRuleArgs', 'BackupPolicyKubernetesClusterRetentionRuleArgsDict']]]]] = None,
                 time_zone: Optional[pulumi.Input[str]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BackupPolicyKubernetesClusterArgs.__new__(BackupPolicyKubernetesClusterArgs)

            if backup_repeating_time_intervals is None and not opts.urn:
                raise TypeError("Missing required property 'backup_repeating_time_intervals'")
            __props__.__dict__["backup_repeating_time_intervals"] = backup_repeating_time_intervals
            if default_retention_rule is None and not opts.urn:
                raise TypeError("Missing required property 'default_retention_rule'")
            __props__.__dict__["default_retention_rule"] = default_retention_rule
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["retention_rules"] = retention_rules
            __props__.__dict__["time_zone"] = time_zone
            if vault_name is None and not opts.urn:
                raise TypeError("Missing required property 'vault_name'")
            __props__.__dict__["vault_name"] = vault_name
        super(BackupPolicyKubernetesCluster, __self__).__init__(
            'azure:dataprotection/backupPolicyKubernetesCluster:BackupPolicyKubernetesCluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            backup_repeating_time_intervals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            default_retention_rule: Optional[pulumi.Input[Union['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs', 'BackupPolicyKubernetesClusterDefaultRetentionRuleArgsDict']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            retention_rules: Optional[pulumi.Input[Sequence[pulumi.Input[Union['BackupPolicyKubernetesClusterRetentionRuleArgs', 'BackupPolicyKubernetesClusterRetentionRuleArgsDict']]]]] = None,
            time_zone: Optional[pulumi.Input[str]] = None,
            vault_name: Optional[pulumi.Input[str]] = None) -> 'BackupPolicyKubernetesCluster':
        """
        Get an existing BackupPolicyKubernetesCluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] backup_repeating_time_intervals: Specifies a list of repeating time interval. It supports weekly back. It should follow `ISO 8601` repeating time interval. Changing this forces a new resource to be created.
        :param pulumi.Input[Union['BackupPolicyKubernetesClusterDefaultRetentionRuleArgs', 'BackupPolicyKubernetesClusterDefaultRetentionRuleArgsDict']] default_retention_rule: A `default_retention_rule` block as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name which should be used for the Backup Policy Kubernetes Cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[Union['BackupPolicyKubernetesClusterRetentionRuleArgs', 'BackupPolicyKubernetesClusterRetentionRuleArgsDict']]]] retention_rules: One or more `retention_rule` blocks as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] time_zone: Specifies the Time Zone which should be used by the backup schedule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] vault_name: The name of the Backup Vault where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BackupPolicyKubernetesClusterState.__new__(_BackupPolicyKubernetesClusterState)

        __props__.__dict__["backup_repeating_time_intervals"] = backup_repeating_time_intervals
        __props__.__dict__["default_retention_rule"] = default_retention_rule
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["retention_rules"] = retention_rules
        __props__.__dict__["time_zone"] = time_zone
        __props__.__dict__["vault_name"] = vault_name
        return BackupPolicyKubernetesCluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backupRepeatingTimeIntervals")
    def backup_repeating_time_intervals(self) -> pulumi.Output[Sequence[str]]:
        """
        Specifies a list of repeating time interval. It supports weekly back. It should follow `ISO 8601` repeating time interval. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "backup_repeating_time_intervals")

    @property
    @pulumi.getter(name="defaultRetentionRule")
    def default_retention_rule(self) -> pulumi.Output['outputs.BackupPolicyKubernetesClusterDefaultRetentionRule']:
        """
        A `default_retention_rule` block as defined below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "default_retention_rule")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for the Backup Policy Kubernetes Cluster. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="retentionRules")
    def retention_rules(self) -> pulumi.Output[Optional[Sequence['outputs.BackupPolicyKubernetesClusterRetentionRule']]]:
        """
        One or more `retention_rule` blocks as defined below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "retention_rules")

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the Time Zone which should be used by the backup schedule. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "time_zone")

    @property
    @pulumi.getter(name="vaultName")
    def vault_name(self) -> pulumi.Output[str]:
        """
        The name of the Backup Vault where the Backup Policy Kubernetes Cluster should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "vault_name")

