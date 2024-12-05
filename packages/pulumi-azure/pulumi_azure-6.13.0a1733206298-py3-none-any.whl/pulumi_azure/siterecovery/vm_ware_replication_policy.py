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

__all__ = ['VMWareReplicationPolicyArgs', 'VMWareReplicationPolicy']

@pulumi.input_type
class VMWareReplicationPolicyArgs:
    def __init__(__self__, *,
                 application_consistent_snapshot_frequency_in_minutes: pulumi.Input[int],
                 recovery_point_retention_in_minutes: pulumi.Input[int],
                 recovery_vault_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a VMWareReplicationPolicy resource.
        :param pulumi.Input[int] application_consistent_snapshot_frequency_in_minutes: Specifies the frequency at which to create application consistent recovery points. Must between `0` to `720`.
        :param pulumi.Input[int] recovery_point_retention_in_minutes: Specifies the period up to which the recovery points will be retained. Must between `0` to `21600`.
        :param pulumi.Input[str] recovery_vault_id: ID of the Recovery Services Vault. Changing this forces a new Replication Policy to be created.
        :param pulumi.Input[str] name: The name which should be used for this Classic Replication Policy. Changing this forces a new Replication Policy to be created.
        """
        pulumi.set(__self__, "application_consistent_snapshot_frequency_in_minutes", application_consistent_snapshot_frequency_in_minutes)
        pulumi.set(__self__, "recovery_point_retention_in_minutes", recovery_point_retention_in_minutes)
        pulumi.set(__self__, "recovery_vault_id", recovery_vault_id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="applicationConsistentSnapshotFrequencyInMinutes")
    def application_consistent_snapshot_frequency_in_minutes(self) -> pulumi.Input[int]:
        """
        Specifies the frequency at which to create application consistent recovery points. Must between `0` to `720`.
        """
        return pulumi.get(self, "application_consistent_snapshot_frequency_in_minutes")

    @application_consistent_snapshot_frequency_in_minutes.setter
    def application_consistent_snapshot_frequency_in_minutes(self, value: pulumi.Input[int]):
        pulumi.set(self, "application_consistent_snapshot_frequency_in_minutes", value)

    @property
    @pulumi.getter(name="recoveryPointRetentionInMinutes")
    def recovery_point_retention_in_minutes(self) -> pulumi.Input[int]:
        """
        Specifies the period up to which the recovery points will be retained. Must between `0` to `21600`.
        """
        return pulumi.get(self, "recovery_point_retention_in_minutes")

    @recovery_point_retention_in_minutes.setter
    def recovery_point_retention_in_minutes(self, value: pulumi.Input[int]):
        pulumi.set(self, "recovery_point_retention_in_minutes", value)

    @property
    @pulumi.getter(name="recoveryVaultId")
    def recovery_vault_id(self) -> pulumi.Input[str]:
        """
        ID of the Recovery Services Vault. Changing this forces a new Replication Policy to be created.
        """
        return pulumi.get(self, "recovery_vault_id")

    @recovery_vault_id.setter
    def recovery_vault_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "recovery_vault_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Classic Replication Policy. Changing this forces a new Replication Policy to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _VMWareReplicationPolicyState:
    def __init__(__self__, *,
                 application_consistent_snapshot_frequency_in_minutes: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recovery_point_retention_in_minutes: Optional[pulumi.Input[int]] = None,
                 recovery_vault_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering VMWareReplicationPolicy resources.
        :param pulumi.Input[int] application_consistent_snapshot_frequency_in_minutes: Specifies the frequency at which to create application consistent recovery points. Must between `0` to `720`.
        :param pulumi.Input[str] name: The name which should be used for this Classic Replication Policy. Changing this forces a new Replication Policy to be created.
        :param pulumi.Input[int] recovery_point_retention_in_minutes: Specifies the period up to which the recovery points will be retained. Must between `0` to `21600`.
        :param pulumi.Input[str] recovery_vault_id: ID of the Recovery Services Vault. Changing this forces a new Replication Policy to be created.
        """
        if application_consistent_snapshot_frequency_in_minutes is not None:
            pulumi.set(__self__, "application_consistent_snapshot_frequency_in_minutes", application_consistent_snapshot_frequency_in_minutes)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if recovery_point_retention_in_minutes is not None:
            pulumi.set(__self__, "recovery_point_retention_in_minutes", recovery_point_retention_in_minutes)
        if recovery_vault_id is not None:
            pulumi.set(__self__, "recovery_vault_id", recovery_vault_id)

    @property
    @pulumi.getter(name="applicationConsistentSnapshotFrequencyInMinutes")
    def application_consistent_snapshot_frequency_in_minutes(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the frequency at which to create application consistent recovery points. Must between `0` to `720`.
        """
        return pulumi.get(self, "application_consistent_snapshot_frequency_in_minutes")

    @application_consistent_snapshot_frequency_in_minutes.setter
    def application_consistent_snapshot_frequency_in_minutes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "application_consistent_snapshot_frequency_in_minutes", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Classic Replication Policy. Changing this forces a new Replication Policy to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="recoveryPointRetentionInMinutes")
    def recovery_point_retention_in_minutes(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the period up to which the recovery points will be retained. Must between `0` to `21600`.
        """
        return pulumi.get(self, "recovery_point_retention_in_minutes")

    @recovery_point_retention_in_minutes.setter
    def recovery_point_retention_in_minutes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "recovery_point_retention_in_minutes", value)

    @property
    @pulumi.getter(name="recoveryVaultId")
    def recovery_vault_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the Recovery Services Vault. Changing this forces a new Replication Policy to be created.
        """
        return pulumi.get(self, "recovery_vault_id")

    @recovery_vault_id.setter
    def recovery_vault_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "recovery_vault_id", value)


class VMWareReplicationPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_consistent_snapshot_frequency_in_minutes: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recovery_point_retention_in_minutes: Optional[pulumi.Input[int]] = None,
                 recovery_vault_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a VMWare Replication Policy.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-rg",
            location="eastus")
        example_vault = azure.recoveryservices.Vault("example",
            name="example-vault",
            location=example.location,
            resource_group_name=example.name,
            sku="Standard",
            classic_vmware_replication_enabled=True,
            soft_delete_enabled=False)
        example_vm_ware_replication_policy = azure.siterecovery.VMWareReplicationPolicy("example",
            name="example-policy",
            recovery_vault_id=example_vault.id,
            recovery_point_retention_in_minutes=1440,
            application_consistent_snapshot_frequency_in_minutes=240)
        ```

        ## Import

        VMWare Replication Policy can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:siterecovery/vMWareReplicationPolicy:VMWareReplicationPolicy example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/vault1/providers/Microsoft.RecoveryServices/vaults/vault1/replicationPolicies/policy1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] application_consistent_snapshot_frequency_in_minutes: Specifies the frequency at which to create application consistent recovery points. Must between `0` to `720`.
        :param pulumi.Input[str] name: The name which should be used for this Classic Replication Policy. Changing this forces a new Replication Policy to be created.
        :param pulumi.Input[int] recovery_point_retention_in_minutes: Specifies the period up to which the recovery points will be retained. Must between `0` to `21600`.
        :param pulumi.Input[str] recovery_vault_id: ID of the Recovery Services Vault. Changing this forces a new Replication Policy to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VMWareReplicationPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a VMWare Replication Policy.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-rg",
            location="eastus")
        example_vault = azure.recoveryservices.Vault("example",
            name="example-vault",
            location=example.location,
            resource_group_name=example.name,
            sku="Standard",
            classic_vmware_replication_enabled=True,
            soft_delete_enabled=False)
        example_vm_ware_replication_policy = azure.siterecovery.VMWareReplicationPolicy("example",
            name="example-policy",
            recovery_vault_id=example_vault.id,
            recovery_point_retention_in_minutes=1440,
            application_consistent_snapshot_frequency_in_minutes=240)
        ```

        ## Import

        VMWare Replication Policy can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:siterecovery/vMWareReplicationPolicy:VMWareReplicationPolicy example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/vault1/providers/Microsoft.RecoveryServices/vaults/vault1/replicationPolicies/policy1
        ```

        :param str resource_name: The name of the resource.
        :param VMWareReplicationPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VMWareReplicationPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_consistent_snapshot_frequency_in_minutes: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recovery_point_retention_in_minutes: Optional[pulumi.Input[int]] = None,
                 recovery_vault_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VMWareReplicationPolicyArgs.__new__(VMWareReplicationPolicyArgs)

            if application_consistent_snapshot_frequency_in_minutes is None and not opts.urn:
                raise TypeError("Missing required property 'application_consistent_snapshot_frequency_in_minutes'")
            __props__.__dict__["application_consistent_snapshot_frequency_in_minutes"] = application_consistent_snapshot_frequency_in_minutes
            __props__.__dict__["name"] = name
            if recovery_point_retention_in_minutes is None and not opts.urn:
                raise TypeError("Missing required property 'recovery_point_retention_in_minutes'")
            __props__.__dict__["recovery_point_retention_in_minutes"] = recovery_point_retention_in_minutes
            if recovery_vault_id is None and not opts.urn:
                raise TypeError("Missing required property 'recovery_vault_id'")
            __props__.__dict__["recovery_vault_id"] = recovery_vault_id
        super(VMWareReplicationPolicy, __self__).__init__(
            'azure:siterecovery/vMWareReplicationPolicy:VMWareReplicationPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            application_consistent_snapshot_frequency_in_minutes: Optional[pulumi.Input[int]] = None,
            name: Optional[pulumi.Input[str]] = None,
            recovery_point_retention_in_minutes: Optional[pulumi.Input[int]] = None,
            recovery_vault_id: Optional[pulumi.Input[str]] = None) -> 'VMWareReplicationPolicy':
        """
        Get an existing VMWareReplicationPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] application_consistent_snapshot_frequency_in_minutes: Specifies the frequency at which to create application consistent recovery points. Must between `0` to `720`.
        :param pulumi.Input[str] name: The name which should be used for this Classic Replication Policy. Changing this forces a new Replication Policy to be created.
        :param pulumi.Input[int] recovery_point_retention_in_minutes: Specifies the period up to which the recovery points will be retained. Must between `0` to `21600`.
        :param pulumi.Input[str] recovery_vault_id: ID of the Recovery Services Vault. Changing this forces a new Replication Policy to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VMWareReplicationPolicyState.__new__(_VMWareReplicationPolicyState)

        __props__.__dict__["application_consistent_snapshot_frequency_in_minutes"] = application_consistent_snapshot_frequency_in_minutes
        __props__.__dict__["name"] = name
        __props__.__dict__["recovery_point_retention_in_minutes"] = recovery_point_retention_in_minutes
        __props__.__dict__["recovery_vault_id"] = recovery_vault_id
        return VMWareReplicationPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationConsistentSnapshotFrequencyInMinutes")
    def application_consistent_snapshot_frequency_in_minutes(self) -> pulumi.Output[int]:
        """
        Specifies the frequency at which to create application consistent recovery points. Must between `0` to `720`.
        """
        return pulumi.get(self, "application_consistent_snapshot_frequency_in_minutes")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Classic Replication Policy. Changing this forces a new Replication Policy to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="recoveryPointRetentionInMinutes")
    def recovery_point_retention_in_minutes(self) -> pulumi.Output[int]:
        """
        Specifies the period up to which the recovery points will be retained. Must between `0` to `21600`.
        """
        return pulumi.get(self, "recovery_point_retention_in_minutes")

    @property
    @pulumi.getter(name="recoveryVaultId")
    def recovery_vault_id(self) -> pulumi.Output[str]:
        """
        ID of the Recovery Services Vault. Changing this forces a new Replication Policy to be created.
        """
        return pulumi.get(self, "recovery_vault_id")

