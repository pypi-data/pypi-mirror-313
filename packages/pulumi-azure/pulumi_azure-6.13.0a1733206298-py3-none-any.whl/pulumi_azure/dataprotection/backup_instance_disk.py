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

__all__ = ['BackupInstanceDiskArgs', 'BackupInstanceDisk']

@pulumi.input_type
class BackupInstanceDiskArgs:
    def __init__(__self__, *,
                 backup_policy_id: pulumi.Input[str],
                 disk_id: pulumi.Input[str],
                 snapshot_resource_group_name: pulumi.Input[str],
                 vault_id: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BackupInstanceDisk resource.
        :param pulumi.Input[str] backup_policy_id: The ID of the Backup Policy.
        :param pulumi.Input[str] disk_id: The ID of the source Disk. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] snapshot_resource_group_name: The name of the Resource Group where snapshots are stored. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] vault_id: The ID of the Backup Vault within which the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] location: The Azure Region where the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] name: The name which should be used for this Backup Instance Disk. Changing this forces a new Backup Instance Disk to be created.
        """
        pulumi.set(__self__, "backup_policy_id", backup_policy_id)
        pulumi.set(__self__, "disk_id", disk_id)
        pulumi.set(__self__, "snapshot_resource_group_name", snapshot_resource_group_name)
        pulumi.set(__self__, "vault_id", vault_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="backupPolicyId")
    def backup_policy_id(self) -> pulumi.Input[str]:
        """
        The ID of the Backup Policy.
        """
        return pulumi.get(self, "backup_policy_id")

    @backup_policy_id.setter
    def backup_policy_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "backup_policy_id", value)

    @property
    @pulumi.getter(name="diskId")
    def disk_id(self) -> pulumi.Input[str]:
        """
        The ID of the source Disk. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "disk_id")

    @disk_id.setter
    def disk_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "disk_id", value)

    @property
    @pulumi.getter(name="snapshotResourceGroupName")
    def snapshot_resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where snapshots are stored. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "snapshot_resource_group_name")

    @snapshot_resource_group_name.setter
    def snapshot_resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "snapshot_resource_group_name", value)

    @property
    @pulumi.getter(name="vaultId")
    def vault_id(self) -> pulumi.Input[str]:
        """
        The ID of the Backup Vault within which the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "vault_id")

    @vault_id.setter
    def vault_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vault_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Backup Instance Disk. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _BackupInstanceDiskState:
    def __init__(__self__, *,
                 backup_policy_id: Optional[pulumi.Input[str]] = None,
                 disk_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 snapshot_resource_group_name: Optional[pulumi.Input[str]] = None,
                 vault_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BackupInstanceDisk resources.
        :param pulumi.Input[str] backup_policy_id: The ID of the Backup Policy.
        :param pulumi.Input[str] disk_id: The ID of the source Disk. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] location: The Azure Region where the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] name: The name which should be used for this Backup Instance Disk. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] snapshot_resource_group_name: The name of the Resource Group where snapshots are stored. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] vault_id: The ID of the Backup Vault within which the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        """
        if backup_policy_id is not None:
            pulumi.set(__self__, "backup_policy_id", backup_policy_id)
        if disk_id is not None:
            pulumi.set(__self__, "disk_id", disk_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if snapshot_resource_group_name is not None:
            pulumi.set(__self__, "snapshot_resource_group_name", snapshot_resource_group_name)
        if vault_id is not None:
            pulumi.set(__self__, "vault_id", vault_id)

    @property
    @pulumi.getter(name="backupPolicyId")
    def backup_policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Backup Policy.
        """
        return pulumi.get(self, "backup_policy_id")

    @backup_policy_id.setter
    def backup_policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backup_policy_id", value)

    @property
    @pulumi.getter(name="diskId")
    def disk_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the source Disk. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "disk_id")

    @disk_id.setter
    def disk_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "disk_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Backup Instance Disk. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="snapshotResourceGroupName")
    def snapshot_resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where snapshots are stored. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "snapshot_resource_group_name")

    @snapshot_resource_group_name.setter
    def snapshot_resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "snapshot_resource_group_name", value)

    @property
    @pulumi.getter(name="vaultId")
    def vault_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Backup Vault within which the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "vault_id")

    @vault_id.setter
    def vault_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vault_id", value)


class BackupInstanceDisk(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backup_policy_id: Optional[pulumi.Input[str]] = None,
                 disk_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 snapshot_resource_group_name: Optional[pulumi.Input[str]] = None,
                 vault_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Backup Instance to back up Disk.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_managed_disk = azure.compute.ManagedDisk("example",
            name="example-disk",
            location=example.location,
            resource_group_name=example.name,
            storage_account_type="Standard_LRS",
            create_option="Empty",
            disk_size_gb=1)
        example_backup_vault = azure.dataprotection.BackupVault("example",
            name="example-backup-vault",
            resource_group_name=example.name,
            location=example.location,
            datastore_type="VaultStore",
            redundancy="LocallyRedundant",
            identity={
                "type": "SystemAssigned",
            })
        example1 = azure.authorization.Assignment("example1",
            scope=example.id,
            role_definition_name="Disk Snapshot Contributor",
            principal_id=example_backup_vault.identity.principal_id)
        example2 = azure.authorization.Assignment("example2",
            scope=example_managed_disk.id,
            role_definition_name="Disk Backup Reader",
            principal_id=example_backup_vault.identity.principal_id)
        example_backup_policy_disk = azure.dataprotection.BackupPolicyDisk("example",
            name="example-backup-policy",
            vault_id=example_backup_vault.id,
            backup_repeating_time_intervals=["R/2021-05-19T06:33:16+00:00/PT4H"],
            default_retention_duration="P7D")
        example_backup_instance_disk = azure.dataprotection.BackupInstanceDisk("example",
            name="example-backup-instance",
            location=example_backup_vault.location,
            vault_id=example_backup_vault.id,
            disk_id=example_managed_disk.id,
            snapshot_resource_group_name=example.name,
            backup_policy_id=example_backup_policy_disk.id)
        ```

        ## Import

        Backup Instance Disks can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:dataprotection/backupInstanceDisk:BackupInstanceDisk example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.DataProtection/backupVaults/vault1/backupInstances/backupInstance1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backup_policy_id: The ID of the Backup Policy.
        :param pulumi.Input[str] disk_id: The ID of the source Disk. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] location: The Azure Region where the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] name: The name which should be used for this Backup Instance Disk. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] snapshot_resource_group_name: The name of the Resource Group where snapshots are stored. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] vault_id: The ID of the Backup Vault within which the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BackupInstanceDiskArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Backup Instance to back up Disk.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_managed_disk = azure.compute.ManagedDisk("example",
            name="example-disk",
            location=example.location,
            resource_group_name=example.name,
            storage_account_type="Standard_LRS",
            create_option="Empty",
            disk_size_gb=1)
        example_backup_vault = azure.dataprotection.BackupVault("example",
            name="example-backup-vault",
            resource_group_name=example.name,
            location=example.location,
            datastore_type="VaultStore",
            redundancy="LocallyRedundant",
            identity={
                "type": "SystemAssigned",
            })
        example1 = azure.authorization.Assignment("example1",
            scope=example.id,
            role_definition_name="Disk Snapshot Contributor",
            principal_id=example_backup_vault.identity.principal_id)
        example2 = azure.authorization.Assignment("example2",
            scope=example_managed_disk.id,
            role_definition_name="Disk Backup Reader",
            principal_id=example_backup_vault.identity.principal_id)
        example_backup_policy_disk = azure.dataprotection.BackupPolicyDisk("example",
            name="example-backup-policy",
            vault_id=example_backup_vault.id,
            backup_repeating_time_intervals=["R/2021-05-19T06:33:16+00:00/PT4H"],
            default_retention_duration="P7D")
        example_backup_instance_disk = azure.dataprotection.BackupInstanceDisk("example",
            name="example-backup-instance",
            location=example_backup_vault.location,
            vault_id=example_backup_vault.id,
            disk_id=example_managed_disk.id,
            snapshot_resource_group_name=example.name,
            backup_policy_id=example_backup_policy_disk.id)
        ```

        ## Import

        Backup Instance Disks can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:dataprotection/backupInstanceDisk:BackupInstanceDisk example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.DataProtection/backupVaults/vault1/backupInstances/backupInstance1
        ```

        :param str resource_name: The name of the resource.
        :param BackupInstanceDiskArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BackupInstanceDiskArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backup_policy_id: Optional[pulumi.Input[str]] = None,
                 disk_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 snapshot_resource_group_name: Optional[pulumi.Input[str]] = None,
                 vault_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BackupInstanceDiskArgs.__new__(BackupInstanceDiskArgs)

            if backup_policy_id is None and not opts.urn:
                raise TypeError("Missing required property 'backup_policy_id'")
            __props__.__dict__["backup_policy_id"] = backup_policy_id
            if disk_id is None and not opts.urn:
                raise TypeError("Missing required property 'disk_id'")
            __props__.__dict__["disk_id"] = disk_id
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if snapshot_resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'snapshot_resource_group_name'")
            __props__.__dict__["snapshot_resource_group_name"] = snapshot_resource_group_name
            if vault_id is None and not opts.urn:
                raise TypeError("Missing required property 'vault_id'")
            __props__.__dict__["vault_id"] = vault_id
        super(BackupInstanceDisk, __self__).__init__(
            'azure:dataprotection/backupInstanceDisk:BackupInstanceDisk',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            backup_policy_id: Optional[pulumi.Input[str]] = None,
            disk_id: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            snapshot_resource_group_name: Optional[pulumi.Input[str]] = None,
            vault_id: Optional[pulumi.Input[str]] = None) -> 'BackupInstanceDisk':
        """
        Get an existing BackupInstanceDisk resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backup_policy_id: The ID of the Backup Policy.
        :param pulumi.Input[str] disk_id: The ID of the source Disk. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] location: The Azure Region where the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] name: The name which should be used for this Backup Instance Disk. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] snapshot_resource_group_name: The name of the Resource Group where snapshots are stored. Changing this forces a new Backup Instance Disk to be created.
        :param pulumi.Input[str] vault_id: The ID of the Backup Vault within which the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BackupInstanceDiskState.__new__(_BackupInstanceDiskState)

        __props__.__dict__["backup_policy_id"] = backup_policy_id
        __props__.__dict__["disk_id"] = disk_id
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["snapshot_resource_group_name"] = snapshot_resource_group_name
        __props__.__dict__["vault_id"] = vault_id
        return BackupInstanceDisk(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backupPolicyId")
    def backup_policy_id(self) -> pulumi.Output[str]:
        """
        The ID of the Backup Policy.
        """
        return pulumi.get(self, "backup_policy_id")

    @property
    @pulumi.getter(name="diskId")
    def disk_id(self) -> pulumi.Output[str]:
        """
        The ID of the source Disk. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "disk_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure Region where the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Backup Instance Disk. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="snapshotResourceGroupName")
    def snapshot_resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where snapshots are stored. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "snapshot_resource_group_name")

    @property
    @pulumi.getter(name="vaultId")
    def vault_id(self) -> pulumi.Output[str]:
        """
        The ID of the Backup Vault within which the Backup Instance Disk should exist. Changing this forces a new Backup Instance Disk to be created.
        """
        return pulumi.get(self, "vault_id")

