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
    'GetPoolResult',
    'AwaitableGetPoolResult',
    'get_pool',
    'get_pool_output',
]

@pulumi.output_type
class GetPoolResult:
    """
    A collection of values returned by getPool.
    """
    def __init__(__self__, account_name=None, auto_scales=None, certificates=None, container_configurations=None, data_disks=None, disk_encryptions=None, display_name=None, extensions=None, fixed_scales=None, id=None, inter_node_communication=None, license_type=None, max_tasks_per_node=None, metadata=None, mounts=None, name=None, network_configurations=None, node_agent_sku_id=None, node_placements=None, os_disk_placement=None, resource_group_name=None, start_tasks=None, storage_image_references=None, task_scheduling_policies=None, user_accounts=None, vm_size=None, windows=None):
        if account_name and not isinstance(account_name, str):
            raise TypeError("Expected argument 'account_name' to be a str")
        pulumi.set(__self__, "account_name", account_name)
        if auto_scales and not isinstance(auto_scales, list):
            raise TypeError("Expected argument 'auto_scales' to be a list")
        pulumi.set(__self__, "auto_scales", auto_scales)
        if certificates and not isinstance(certificates, list):
            raise TypeError("Expected argument 'certificates' to be a list")
        pulumi.set(__self__, "certificates", certificates)
        if container_configurations and not isinstance(container_configurations, list):
            raise TypeError("Expected argument 'container_configurations' to be a list")
        pulumi.set(__self__, "container_configurations", container_configurations)
        if data_disks and not isinstance(data_disks, list):
            raise TypeError("Expected argument 'data_disks' to be a list")
        pulumi.set(__self__, "data_disks", data_disks)
        if disk_encryptions and not isinstance(disk_encryptions, list):
            raise TypeError("Expected argument 'disk_encryptions' to be a list")
        pulumi.set(__self__, "disk_encryptions", disk_encryptions)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if extensions and not isinstance(extensions, list):
            raise TypeError("Expected argument 'extensions' to be a list")
        pulumi.set(__self__, "extensions", extensions)
        if fixed_scales and not isinstance(fixed_scales, list):
            raise TypeError("Expected argument 'fixed_scales' to be a list")
        pulumi.set(__self__, "fixed_scales", fixed_scales)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if inter_node_communication and not isinstance(inter_node_communication, str):
            raise TypeError("Expected argument 'inter_node_communication' to be a str")
        pulumi.set(__self__, "inter_node_communication", inter_node_communication)
        if license_type and not isinstance(license_type, str):
            raise TypeError("Expected argument 'license_type' to be a str")
        pulumi.set(__self__, "license_type", license_type)
        if max_tasks_per_node and not isinstance(max_tasks_per_node, int):
            raise TypeError("Expected argument 'max_tasks_per_node' to be a int")
        pulumi.set(__self__, "max_tasks_per_node", max_tasks_per_node)
        if metadata and not isinstance(metadata, dict):
            raise TypeError("Expected argument 'metadata' to be a dict")
        pulumi.set(__self__, "metadata", metadata)
        if mounts and not isinstance(mounts, list):
            raise TypeError("Expected argument 'mounts' to be a list")
        pulumi.set(__self__, "mounts", mounts)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_configurations and not isinstance(network_configurations, list):
            raise TypeError("Expected argument 'network_configurations' to be a list")
        pulumi.set(__self__, "network_configurations", network_configurations)
        if node_agent_sku_id and not isinstance(node_agent_sku_id, str):
            raise TypeError("Expected argument 'node_agent_sku_id' to be a str")
        pulumi.set(__self__, "node_agent_sku_id", node_agent_sku_id)
        if node_placements and not isinstance(node_placements, list):
            raise TypeError("Expected argument 'node_placements' to be a list")
        pulumi.set(__self__, "node_placements", node_placements)
        if os_disk_placement and not isinstance(os_disk_placement, str):
            raise TypeError("Expected argument 'os_disk_placement' to be a str")
        pulumi.set(__self__, "os_disk_placement", os_disk_placement)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if start_tasks and not isinstance(start_tasks, list):
            raise TypeError("Expected argument 'start_tasks' to be a list")
        pulumi.set(__self__, "start_tasks", start_tasks)
        if storage_image_references and not isinstance(storage_image_references, list):
            raise TypeError("Expected argument 'storage_image_references' to be a list")
        pulumi.set(__self__, "storage_image_references", storage_image_references)
        if task_scheduling_policies and not isinstance(task_scheduling_policies, list):
            raise TypeError("Expected argument 'task_scheduling_policies' to be a list")
        pulumi.set(__self__, "task_scheduling_policies", task_scheduling_policies)
        if user_accounts and not isinstance(user_accounts, list):
            raise TypeError("Expected argument 'user_accounts' to be a list")
        pulumi.set(__self__, "user_accounts", user_accounts)
        if vm_size and not isinstance(vm_size, str):
            raise TypeError("Expected argument 'vm_size' to be a str")
        pulumi.set(__self__, "vm_size", vm_size)
        if windows and not isinstance(windows, list):
            raise TypeError("Expected argument 'windows' to be a list")
        pulumi.set(__self__, "windows", windows)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> str:
        """
        The Azure Storage Account name.
        """
        return pulumi.get(self, "account_name")

    @property
    @pulumi.getter(name="autoScales")
    def auto_scales(self) -> Sequence['outputs.GetPoolAutoScaleResult']:
        """
        A `auto_scale` block that describes the scale settings when using auto scale.
        """
        return pulumi.get(self, "auto_scales")

    @property
    @pulumi.getter
    def certificates(self) -> Sequence['outputs.GetPoolCertificateResult']:
        """
        One or more `certificate` blocks that describe the certificates installed on each compute node in the pool.
        """
        return pulumi.get(self, "certificates")

    @property
    @pulumi.getter(name="containerConfigurations")
    def container_configurations(self) -> Sequence['outputs.GetPoolContainerConfigurationResult']:
        """
        The container configuration used in the pool's VMs.
        """
        return pulumi.get(self, "container_configurations")

    @property
    @pulumi.getter(name="dataDisks")
    def data_disks(self) -> Sequence['outputs.GetPoolDataDiskResult']:
        """
        A `data_disks` block describes the data disk settings.
        """
        return pulumi.get(self, "data_disks")

    @property
    @pulumi.getter(name="diskEncryptions")
    def disk_encryptions(self) -> Sequence['outputs.GetPoolDiskEncryptionResult']:
        """
        A `disk_encryption` block describes the disk encryption configuration applied on compute nodes in the pool.
        """
        return pulumi.get(self, "disk_encryptions")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def extensions(self) -> Sequence['outputs.GetPoolExtensionResult']:
        """
        An `extensions` block describes the extension settings
        """
        return pulumi.get(self, "extensions")

    @property
    @pulumi.getter(name="fixedScales")
    def fixed_scales(self) -> Sequence['outputs.GetPoolFixedScaleResult']:
        """
        A `fixed_scale` block that describes the scale settings when using fixed scale.
        """
        return pulumi.get(self, "fixed_scales")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="interNodeCommunication")
    def inter_node_communication(self) -> str:
        """
        Whether the pool permits direct communication between nodes. This imposes restrictions on which nodes can be assigned to the pool. Enabling this value can reduce the chance of the requested number of nodes to be allocated in the pool.
        """
        return pulumi.get(self, "inter_node_communication")

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> str:
        """
        The type of on-premises license to be used when deploying the operating system.
        """
        return pulumi.get(self, "license_type")

    @property
    @pulumi.getter(name="maxTasksPerNode")
    def max_tasks_per_node(self) -> int:
        """
        The maximum number of tasks that can run concurrently on a single compute node in the pool.
        """
        return pulumi.get(self, "max_tasks_per_node")

    @property
    @pulumi.getter
    def metadata(self) -> Mapping[str, str]:
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def mounts(self) -> Sequence['outputs.GetPoolMountResult']:
        """
        A `mount` block that describes mount configuration.
        """
        return pulumi.get(self, "mounts")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the user account.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkConfigurations")
    def network_configurations(self) -> Sequence['outputs.GetPoolNetworkConfigurationResult']:
        return pulumi.get(self, "network_configurations")

    @property
    @pulumi.getter(name="nodeAgentSkuId")
    def node_agent_sku_id(self) -> str:
        """
        The SKU of the node agents in the Batch pool.
        """
        return pulumi.get(self, "node_agent_sku_id")

    @property
    @pulumi.getter(name="nodePlacements")
    def node_placements(self) -> Sequence['outputs.GetPoolNodePlacementResult']:
        """
        A `node_placement` block that describes the placement policy for allocating nodes in the pool.
        """
        return pulumi.get(self, "node_placements")

    @property
    @pulumi.getter(name="osDiskPlacement")
    def os_disk_placement(self) -> str:
        """
        Specifies the ephemeral disk placement for operating system disk for all VMs in the pool.
        """
        return pulumi.get(self, "os_disk_placement")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="startTasks")
    def start_tasks(self) -> Sequence['outputs.GetPoolStartTaskResult']:
        """
        A `start_task` block that describes the start task settings for the Batch pool.
        """
        return pulumi.get(self, "start_tasks")

    @property
    @pulumi.getter(name="storageImageReferences")
    def storage_image_references(self) -> Sequence['outputs.GetPoolStorageImageReferenceResult']:
        """
        The reference of the storage image used by the nodes in the Batch pool.
        """
        return pulumi.get(self, "storage_image_references")

    @property
    @pulumi.getter(name="taskSchedulingPolicies")
    def task_scheduling_policies(self) -> Sequence['outputs.GetPoolTaskSchedulingPolicyResult']:
        """
        A `task_scheduling_policy` block that describes how tasks are distributed across compute nodes in a pool.
        """
        return pulumi.get(self, "task_scheduling_policies")

    @property
    @pulumi.getter(name="userAccounts")
    def user_accounts(self) -> Sequence['outputs.GetPoolUserAccountResult']:
        """
        A `user_accounts` block that describes the list of user accounts to be created on each node in the pool.
        """
        return pulumi.get(self, "user_accounts")

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> str:
        """
        The size of the VM created in the Batch pool.
        """
        return pulumi.get(self, "vm_size")

    @property
    @pulumi.getter
    def windows(self) -> Sequence['outputs.GetPoolWindowResult']:
        """
        A `windows` block that describes the Windows configuration in the pool.
        """
        return pulumi.get(self, "windows")


class AwaitableGetPoolResult(GetPoolResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPoolResult(
            account_name=self.account_name,
            auto_scales=self.auto_scales,
            certificates=self.certificates,
            container_configurations=self.container_configurations,
            data_disks=self.data_disks,
            disk_encryptions=self.disk_encryptions,
            display_name=self.display_name,
            extensions=self.extensions,
            fixed_scales=self.fixed_scales,
            id=self.id,
            inter_node_communication=self.inter_node_communication,
            license_type=self.license_type,
            max_tasks_per_node=self.max_tasks_per_node,
            metadata=self.metadata,
            mounts=self.mounts,
            name=self.name,
            network_configurations=self.network_configurations,
            node_agent_sku_id=self.node_agent_sku_id,
            node_placements=self.node_placements,
            os_disk_placement=self.os_disk_placement,
            resource_group_name=self.resource_group_name,
            start_tasks=self.start_tasks,
            storage_image_references=self.storage_image_references,
            task_scheduling_policies=self.task_scheduling_policies,
            user_accounts=self.user_accounts,
            vm_size=self.vm_size,
            windows=self.windows)


def get_pool(account_name: Optional[str] = None,
             name: Optional[str] = None,
             resource_group_name: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPoolResult:
    """
    Use this data source to access information about an existing Batch pool

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.batch.get_pool(name="testbatchpool",
        account_name="testbatchaccount",
        resource_group_name="test")
    ```


    :param str account_name: The Azure Storage Account name.
    :param str name: The name of the user account.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:batch/getPool:getPool', __args__, opts=opts, typ=GetPoolResult).value

    return AwaitableGetPoolResult(
        account_name=pulumi.get(__ret__, 'account_name'),
        auto_scales=pulumi.get(__ret__, 'auto_scales'),
        certificates=pulumi.get(__ret__, 'certificates'),
        container_configurations=pulumi.get(__ret__, 'container_configurations'),
        data_disks=pulumi.get(__ret__, 'data_disks'),
        disk_encryptions=pulumi.get(__ret__, 'disk_encryptions'),
        display_name=pulumi.get(__ret__, 'display_name'),
        extensions=pulumi.get(__ret__, 'extensions'),
        fixed_scales=pulumi.get(__ret__, 'fixed_scales'),
        id=pulumi.get(__ret__, 'id'),
        inter_node_communication=pulumi.get(__ret__, 'inter_node_communication'),
        license_type=pulumi.get(__ret__, 'license_type'),
        max_tasks_per_node=pulumi.get(__ret__, 'max_tasks_per_node'),
        metadata=pulumi.get(__ret__, 'metadata'),
        mounts=pulumi.get(__ret__, 'mounts'),
        name=pulumi.get(__ret__, 'name'),
        network_configurations=pulumi.get(__ret__, 'network_configurations'),
        node_agent_sku_id=pulumi.get(__ret__, 'node_agent_sku_id'),
        node_placements=pulumi.get(__ret__, 'node_placements'),
        os_disk_placement=pulumi.get(__ret__, 'os_disk_placement'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        start_tasks=pulumi.get(__ret__, 'start_tasks'),
        storage_image_references=pulumi.get(__ret__, 'storage_image_references'),
        task_scheduling_policies=pulumi.get(__ret__, 'task_scheduling_policies'),
        user_accounts=pulumi.get(__ret__, 'user_accounts'),
        vm_size=pulumi.get(__ret__, 'vm_size'),
        windows=pulumi.get(__ret__, 'windows'))
def get_pool_output(account_name: Optional[pulumi.Input[str]] = None,
                    name: Optional[pulumi.Input[str]] = None,
                    resource_group_name: Optional[pulumi.Input[str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPoolResult]:
    """
    Use this data source to access information about an existing Batch pool

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.batch.get_pool(name="testbatchpool",
        account_name="testbatchaccount",
        resource_group_name="test")
    ```


    :param str account_name: The Azure Storage Account name.
    :param str name: The name of the user account.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:batch/getPool:getPool', __args__, opts=opts, typ=GetPoolResult)
    return __ret__.apply(lambda __response__: GetPoolResult(
        account_name=pulumi.get(__response__, 'account_name'),
        auto_scales=pulumi.get(__response__, 'auto_scales'),
        certificates=pulumi.get(__response__, 'certificates'),
        container_configurations=pulumi.get(__response__, 'container_configurations'),
        data_disks=pulumi.get(__response__, 'data_disks'),
        disk_encryptions=pulumi.get(__response__, 'disk_encryptions'),
        display_name=pulumi.get(__response__, 'display_name'),
        extensions=pulumi.get(__response__, 'extensions'),
        fixed_scales=pulumi.get(__response__, 'fixed_scales'),
        id=pulumi.get(__response__, 'id'),
        inter_node_communication=pulumi.get(__response__, 'inter_node_communication'),
        license_type=pulumi.get(__response__, 'license_type'),
        max_tasks_per_node=pulumi.get(__response__, 'max_tasks_per_node'),
        metadata=pulumi.get(__response__, 'metadata'),
        mounts=pulumi.get(__response__, 'mounts'),
        name=pulumi.get(__response__, 'name'),
        network_configurations=pulumi.get(__response__, 'network_configurations'),
        node_agent_sku_id=pulumi.get(__response__, 'node_agent_sku_id'),
        node_placements=pulumi.get(__response__, 'node_placements'),
        os_disk_placement=pulumi.get(__response__, 'os_disk_placement'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        start_tasks=pulumi.get(__response__, 'start_tasks'),
        storage_image_references=pulumi.get(__response__, 'storage_image_references'),
        task_scheduling_policies=pulumi.get(__response__, 'task_scheduling_policies'),
        user_accounts=pulumi.get(__response__, 'user_accounts'),
        vm_size=pulumi.get(__response__, 'vm_size'),
        windows=pulumi.get(__response__, 'windows')))
