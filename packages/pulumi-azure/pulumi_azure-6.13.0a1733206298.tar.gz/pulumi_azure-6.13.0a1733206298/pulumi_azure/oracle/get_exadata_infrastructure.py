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
    'GetExadataInfrastructureResult',
    'AwaitableGetExadataInfrastructureResult',
    'get_exadata_infrastructure',
    'get_exadata_infrastructure_output',
]

@pulumi.output_type
class GetExadataInfrastructureResult:
    """
    A collection of values returned by getExadataInfrastructure.
    """
    def __init__(__self__, activated_storage_count=None, additional_storage_count=None, available_storage_size_in_gbs=None, compute_count=None, cpu_count=None, customer_contacts=None, data_storage_size_in_tbs=None, db_node_storage_size_in_gbs=None, db_server_version=None, display_name=None, estimated_patching_times=None, id=None, last_maintenance_run_id=None, lifecycle_details=None, lifecycle_state=None, location=None, maintenance_windows=None, max_cpu_count=None, max_data_storage_in_tbs=None, max_db_node_storage_size_in_gbs=None, max_memory_in_gbs=None, memory_size_in_gbs=None, monthly_db_server_version=None, monthly_storage_server_version=None, name=None, next_maintenance_run_id=None, oci_url=None, ocid=None, resource_group_name=None, shape=None, storage_count=None, storage_server_version=None, tags=None, time_created=None, total_storage_size_in_gbs=None, zones=None):
        if activated_storage_count and not isinstance(activated_storage_count, int):
            raise TypeError("Expected argument 'activated_storage_count' to be a int")
        pulumi.set(__self__, "activated_storage_count", activated_storage_count)
        if additional_storage_count and not isinstance(additional_storage_count, int):
            raise TypeError("Expected argument 'additional_storage_count' to be a int")
        pulumi.set(__self__, "additional_storage_count", additional_storage_count)
        if available_storage_size_in_gbs and not isinstance(available_storage_size_in_gbs, int):
            raise TypeError("Expected argument 'available_storage_size_in_gbs' to be a int")
        pulumi.set(__self__, "available_storage_size_in_gbs", available_storage_size_in_gbs)
        if compute_count and not isinstance(compute_count, int):
            raise TypeError("Expected argument 'compute_count' to be a int")
        pulumi.set(__self__, "compute_count", compute_count)
        if cpu_count and not isinstance(cpu_count, int):
            raise TypeError("Expected argument 'cpu_count' to be a int")
        pulumi.set(__self__, "cpu_count", cpu_count)
        if customer_contacts and not isinstance(customer_contacts, list):
            raise TypeError("Expected argument 'customer_contacts' to be a list")
        pulumi.set(__self__, "customer_contacts", customer_contacts)
        if data_storage_size_in_tbs and not isinstance(data_storage_size_in_tbs, float):
            raise TypeError("Expected argument 'data_storage_size_in_tbs' to be a float")
        pulumi.set(__self__, "data_storage_size_in_tbs", data_storage_size_in_tbs)
        if db_node_storage_size_in_gbs and not isinstance(db_node_storage_size_in_gbs, int):
            raise TypeError("Expected argument 'db_node_storage_size_in_gbs' to be a int")
        pulumi.set(__self__, "db_node_storage_size_in_gbs", db_node_storage_size_in_gbs)
        if db_server_version and not isinstance(db_server_version, str):
            raise TypeError("Expected argument 'db_server_version' to be a str")
        pulumi.set(__self__, "db_server_version", db_server_version)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if estimated_patching_times and not isinstance(estimated_patching_times, list):
            raise TypeError("Expected argument 'estimated_patching_times' to be a list")
        pulumi.set(__self__, "estimated_patching_times", estimated_patching_times)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_maintenance_run_id and not isinstance(last_maintenance_run_id, str):
            raise TypeError("Expected argument 'last_maintenance_run_id' to be a str")
        pulumi.set(__self__, "last_maintenance_run_id", last_maintenance_run_id)
        if lifecycle_details and not isinstance(lifecycle_details, str):
            raise TypeError("Expected argument 'lifecycle_details' to be a str")
        pulumi.set(__self__, "lifecycle_details", lifecycle_details)
        if lifecycle_state and not isinstance(lifecycle_state, str):
            raise TypeError("Expected argument 'lifecycle_state' to be a str")
        pulumi.set(__self__, "lifecycle_state", lifecycle_state)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if maintenance_windows and not isinstance(maintenance_windows, list):
            raise TypeError("Expected argument 'maintenance_windows' to be a list")
        pulumi.set(__self__, "maintenance_windows", maintenance_windows)
        if max_cpu_count and not isinstance(max_cpu_count, int):
            raise TypeError("Expected argument 'max_cpu_count' to be a int")
        pulumi.set(__self__, "max_cpu_count", max_cpu_count)
        if max_data_storage_in_tbs and not isinstance(max_data_storage_in_tbs, float):
            raise TypeError("Expected argument 'max_data_storage_in_tbs' to be a float")
        pulumi.set(__self__, "max_data_storage_in_tbs", max_data_storage_in_tbs)
        if max_db_node_storage_size_in_gbs and not isinstance(max_db_node_storage_size_in_gbs, int):
            raise TypeError("Expected argument 'max_db_node_storage_size_in_gbs' to be a int")
        pulumi.set(__self__, "max_db_node_storage_size_in_gbs", max_db_node_storage_size_in_gbs)
        if max_memory_in_gbs and not isinstance(max_memory_in_gbs, int):
            raise TypeError("Expected argument 'max_memory_in_gbs' to be a int")
        pulumi.set(__self__, "max_memory_in_gbs", max_memory_in_gbs)
        if memory_size_in_gbs and not isinstance(memory_size_in_gbs, int):
            raise TypeError("Expected argument 'memory_size_in_gbs' to be a int")
        pulumi.set(__self__, "memory_size_in_gbs", memory_size_in_gbs)
        if monthly_db_server_version and not isinstance(monthly_db_server_version, str):
            raise TypeError("Expected argument 'monthly_db_server_version' to be a str")
        pulumi.set(__self__, "monthly_db_server_version", monthly_db_server_version)
        if monthly_storage_server_version and not isinstance(monthly_storage_server_version, str):
            raise TypeError("Expected argument 'monthly_storage_server_version' to be a str")
        pulumi.set(__self__, "monthly_storage_server_version", monthly_storage_server_version)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if next_maintenance_run_id and not isinstance(next_maintenance_run_id, str):
            raise TypeError("Expected argument 'next_maintenance_run_id' to be a str")
        pulumi.set(__self__, "next_maintenance_run_id", next_maintenance_run_id)
        if oci_url and not isinstance(oci_url, str):
            raise TypeError("Expected argument 'oci_url' to be a str")
        pulumi.set(__self__, "oci_url", oci_url)
        if ocid and not isinstance(ocid, str):
            raise TypeError("Expected argument 'ocid' to be a str")
        pulumi.set(__self__, "ocid", ocid)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if shape and not isinstance(shape, str):
            raise TypeError("Expected argument 'shape' to be a str")
        pulumi.set(__self__, "shape", shape)
        if storage_count and not isinstance(storage_count, int):
            raise TypeError("Expected argument 'storage_count' to be a int")
        pulumi.set(__self__, "storage_count", storage_count)
        if storage_server_version and not isinstance(storage_server_version, str):
            raise TypeError("Expected argument 'storage_server_version' to be a str")
        pulumi.set(__self__, "storage_server_version", storage_server_version)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if time_created and not isinstance(time_created, str):
            raise TypeError("Expected argument 'time_created' to be a str")
        pulumi.set(__self__, "time_created", time_created)
        if total_storage_size_in_gbs and not isinstance(total_storage_size_in_gbs, int):
            raise TypeError("Expected argument 'total_storage_size_in_gbs' to be a int")
        pulumi.set(__self__, "total_storage_size_in_gbs", total_storage_size_in_gbs)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="activatedStorageCount")
    def activated_storage_count(self) -> int:
        """
        The requested number of additional storage servers activated for the Cloud Exadata Infrastructure.
        """
        return pulumi.get(self, "activated_storage_count")

    @property
    @pulumi.getter(name="additionalStorageCount")
    def additional_storage_count(self) -> int:
        """
        The requested number of additional storage servers for the Cloud Exadata Infrastructure.
        """
        return pulumi.get(self, "additional_storage_count")

    @property
    @pulumi.getter(name="availableStorageSizeInGbs")
    def available_storage_size_in_gbs(self) -> int:
        """
        The available storage can be allocated to the Cloud Exadata Infrastructure resource, in gigabytes (GB).
        """
        return pulumi.get(self, "available_storage_size_in_gbs")

    @property
    @pulumi.getter(name="computeCount")
    def compute_count(self) -> int:
        """
        The number of compute servers for the Cloud Exadata Infrastructure.
        """
        return pulumi.get(self, "compute_count")

    @property
    @pulumi.getter(name="cpuCount")
    def cpu_count(self) -> int:
        """
        The total number of CPU cores allocated.
        """
        return pulumi.get(self, "cpu_count")

    @property
    @pulumi.getter(name="customerContacts")
    def customer_contacts(self) -> Sequence[str]:
        """
        A `customer_contacts` block as defined below.
        """
        return pulumi.get(self, "customer_contacts")

    @property
    @pulumi.getter(name="dataStorageSizeInTbs")
    def data_storage_size_in_tbs(self) -> float:
        """
        The data storage size in terabytes of the DATA disk group.
        """
        return pulumi.get(self, "data_storage_size_in_tbs")

    @property
    @pulumi.getter(name="dbNodeStorageSizeInGbs")
    def db_node_storage_size_in_gbs(self) -> int:
        """
        The local node storage allocated in GBs.
        """
        return pulumi.get(self, "db_node_storage_size_in_gbs")

    @property
    @pulumi.getter(name="dbServerVersion")
    def db_server_version(self) -> str:
        """
        The software version of the database servers (dom0) in the Cloud Exadata Infrastructure.
        """
        return pulumi.get(self, "db_server_version")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The user-friendly name for the Cloud Exadata Infrastructure resource. The name does not need to be unique.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="estimatedPatchingTimes")
    def estimated_patching_times(self) -> Sequence['outputs.GetExadataInfrastructureEstimatedPatchingTimeResult']:
        """
        A `estimated_patching_time` block as defined below.
        """
        return pulumi.get(self, "estimated_patching_times")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastMaintenanceRunId")
    def last_maintenance_run_id(self) -> str:
        """
        The [OCID](https://docs.oracle.com/en-us/iaas/Content/General/Concepts/identifiers.htm) of the last maintenance run.
        """
        return pulumi.get(self, "last_maintenance_run_id")

    @property
    @pulumi.getter(name="lifecycleDetails")
    def lifecycle_details(self) -> str:
        """
        Additional information about the current lifecycle state.
        """
        return pulumi.get(self, "lifecycle_details")

    @property
    @pulumi.getter(name="lifecycleState")
    def lifecycle_state(self) -> str:
        """
        Cloud Exadata Infrastructure lifecycle state.
        """
        return pulumi.get(self, "lifecycle_state")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure Region where the Cloud Exadata Infrastructure exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceWindows")
    def maintenance_windows(self) -> Sequence['outputs.GetExadataInfrastructureMaintenanceWindowResult']:
        """
        A `maintenance_window` block as defined below.
        """
        return pulumi.get(self, "maintenance_windows")

    @property
    @pulumi.getter(name="maxCpuCount")
    def max_cpu_count(self) -> int:
        """
        The total number of CPU cores available.
        """
        return pulumi.get(self, "max_cpu_count")

    @property
    @pulumi.getter(name="maxDataStorageInTbs")
    def max_data_storage_in_tbs(self) -> float:
        """
        The total available DATA disk group size.
        """
        return pulumi.get(self, "max_data_storage_in_tbs")

    @property
    @pulumi.getter(name="maxDbNodeStorageSizeInGbs")
    def max_db_node_storage_size_in_gbs(self) -> int:
        """
        The total local node storage available in GBs.
        """
        return pulumi.get(self, "max_db_node_storage_size_in_gbs")

    @property
    @pulumi.getter(name="maxMemoryInGbs")
    def max_memory_in_gbs(self) -> int:
        """
        The total memory available in GBs.
        """
        return pulumi.get(self, "max_memory_in_gbs")

    @property
    @pulumi.getter(name="memorySizeInGbs")
    def memory_size_in_gbs(self) -> int:
        """
        The memory allocated in GBs.
        """
        return pulumi.get(self, "memory_size_in_gbs")

    @property
    @pulumi.getter(name="monthlyDbServerVersion")
    def monthly_db_server_version(self) -> str:
        """
        The monthly software version of the database servers (dom0) in the Cloud Exadata Infrastructure.
        """
        return pulumi.get(self, "monthly_db_server_version")

    @property
    @pulumi.getter(name="monthlyStorageServerVersion")
    def monthly_storage_server_version(self) -> str:
        """
        The monthly software version of the storage servers (cells) in the Cloud Exadata Infrastructure.
        """
        return pulumi.get(self, "monthly_storage_server_version")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nextMaintenanceRunId")
    def next_maintenance_run_id(self) -> str:
        """
        The [OCID](https://docs.oracle.com/en-us/iaas/Content/General/Concepts/identifiers.htm) of the next maintenance run.
        """
        return pulumi.get(self, "next_maintenance_run_id")

    @property
    @pulumi.getter(name="ociUrl")
    def oci_url(self) -> str:
        """
        The URL of the resource in the OCI console.
        """
        return pulumi.get(self, "oci_url")

    @property
    @pulumi.getter
    def ocid(self) -> str:
        """
        The [OCID](https://docs.oracle.com/en-us/iaas/Content/General/Concepts/identifiers.htm) of the Cloud Exadata Infrastructure.
        """
        return pulumi.get(self, "ocid")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def shape(self) -> str:
        """
        The model name of the Cloud Exadata Infrastructure resource.
        """
        return pulumi.get(self, "shape")

    @property
    @pulumi.getter(name="storageCount")
    def storage_count(self) -> int:
        """
        The number of storage servers for the Cloud Exadata Infrastructure.
        """
        return pulumi.get(self, "storage_count")

    @property
    @pulumi.getter(name="storageServerVersion")
    def storage_server_version(self) -> str:
        """
        The software version of the storage servers (cells) in the Cloud Exadata Infrastructure.
        """
        return pulumi.get(self, "storage_server_version")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the Cloud Exadata Infrastructure.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timeCreated")
    def time_created(self) -> str:
        """
        The date and time the Cloud Exadata Infrastructure resource was created.
        """
        return pulumi.get(self, "time_created")

    @property
    @pulumi.getter(name="totalStorageSizeInGbs")
    def total_storage_size_in_gbs(self) -> int:
        """
        The total storage allocated to the Cloud Exadata Infrastructure resource, in gigabytes (GB).
        """
        return pulumi.get(self, "total_storage_size_in_gbs")

    @property
    @pulumi.getter
    def zones(self) -> Sequence[str]:
        """
        The Cloud Exadata Infrastructure Azure zones.
        """
        return pulumi.get(self, "zones")


class AwaitableGetExadataInfrastructureResult(GetExadataInfrastructureResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetExadataInfrastructureResult(
            activated_storage_count=self.activated_storage_count,
            additional_storage_count=self.additional_storage_count,
            available_storage_size_in_gbs=self.available_storage_size_in_gbs,
            compute_count=self.compute_count,
            cpu_count=self.cpu_count,
            customer_contacts=self.customer_contacts,
            data_storage_size_in_tbs=self.data_storage_size_in_tbs,
            db_node_storage_size_in_gbs=self.db_node_storage_size_in_gbs,
            db_server_version=self.db_server_version,
            display_name=self.display_name,
            estimated_patching_times=self.estimated_patching_times,
            id=self.id,
            last_maintenance_run_id=self.last_maintenance_run_id,
            lifecycle_details=self.lifecycle_details,
            lifecycle_state=self.lifecycle_state,
            location=self.location,
            maintenance_windows=self.maintenance_windows,
            max_cpu_count=self.max_cpu_count,
            max_data_storage_in_tbs=self.max_data_storage_in_tbs,
            max_db_node_storage_size_in_gbs=self.max_db_node_storage_size_in_gbs,
            max_memory_in_gbs=self.max_memory_in_gbs,
            memory_size_in_gbs=self.memory_size_in_gbs,
            monthly_db_server_version=self.monthly_db_server_version,
            monthly_storage_server_version=self.monthly_storage_server_version,
            name=self.name,
            next_maintenance_run_id=self.next_maintenance_run_id,
            oci_url=self.oci_url,
            ocid=self.ocid,
            resource_group_name=self.resource_group_name,
            shape=self.shape,
            storage_count=self.storage_count,
            storage_server_version=self.storage_server_version,
            tags=self.tags,
            time_created=self.time_created,
            total_storage_size_in_gbs=self.total_storage_size_in_gbs,
            zones=self.zones)


def get_exadata_infrastructure(name: Optional[str] = None,
                               resource_group_name: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetExadataInfrastructureResult:
    """
    Use this data source to access information about an existing Cloud Exadata Infrastructure.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.oracle.get_exadata_infrastructure(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Cloud Exadata Infrastructure.
    :param str resource_group_name: The name of the Resource Group where the Cloud Exadata Infrastructure exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:oracle/getExadataInfrastructure:getExadataInfrastructure', __args__, opts=opts, typ=GetExadataInfrastructureResult).value

    return AwaitableGetExadataInfrastructureResult(
        activated_storage_count=pulumi.get(__ret__, 'activated_storage_count'),
        additional_storage_count=pulumi.get(__ret__, 'additional_storage_count'),
        available_storage_size_in_gbs=pulumi.get(__ret__, 'available_storage_size_in_gbs'),
        compute_count=pulumi.get(__ret__, 'compute_count'),
        cpu_count=pulumi.get(__ret__, 'cpu_count'),
        customer_contacts=pulumi.get(__ret__, 'customer_contacts'),
        data_storage_size_in_tbs=pulumi.get(__ret__, 'data_storage_size_in_tbs'),
        db_node_storage_size_in_gbs=pulumi.get(__ret__, 'db_node_storage_size_in_gbs'),
        db_server_version=pulumi.get(__ret__, 'db_server_version'),
        display_name=pulumi.get(__ret__, 'display_name'),
        estimated_patching_times=pulumi.get(__ret__, 'estimated_patching_times'),
        id=pulumi.get(__ret__, 'id'),
        last_maintenance_run_id=pulumi.get(__ret__, 'last_maintenance_run_id'),
        lifecycle_details=pulumi.get(__ret__, 'lifecycle_details'),
        lifecycle_state=pulumi.get(__ret__, 'lifecycle_state'),
        location=pulumi.get(__ret__, 'location'),
        maintenance_windows=pulumi.get(__ret__, 'maintenance_windows'),
        max_cpu_count=pulumi.get(__ret__, 'max_cpu_count'),
        max_data_storage_in_tbs=pulumi.get(__ret__, 'max_data_storage_in_tbs'),
        max_db_node_storage_size_in_gbs=pulumi.get(__ret__, 'max_db_node_storage_size_in_gbs'),
        max_memory_in_gbs=pulumi.get(__ret__, 'max_memory_in_gbs'),
        memory_size_in_gbs=pulumi.get(__ret__, 'memory_size_in_gbs'),
        monthly_db_server_version=pulumi.get(__ret__, 'monthly_db_server_version'),
        monthly_storage_server_version=pulumi.get(__ret__, 'monthly_storage_server_version'),
        name=pulumi.get(__ret__, 'name'),
        next_maintenance_run_id=pulumi.get(__ret__, 'next_maintenance_run_id'),
        oci_url=pulumi.get(__ret__, 'oci_url'),
        ocid=pulumi.get(__ret__, 'ocid'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        shape=pulumi.get(__ret__, 'shape'),
        storage_count=pulumi.get(__ret__, 'storage_count'),
        storage_server_version=pulumi.get(__ret__, 'storage_server_version'),
        tags=pulumi.get(__ret__, 'tags'),
        time_created=pulumi.get(__ret__, 'time_created'),
        total_storage_size_in_gbs=pulumi.get(__ret__, 'total_storage_size_in_gbs'),
        zones=pulumi.get(__ret__, 'zones'))
def get_exadata_infrastructure_output(name: Optional[pulumi.Input[str]] = None,
                                      resource_group_name: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetExadataInfrastructureResult]:
    """
    Use this data source to access information about an existing Cloud Exadata Infrastructure.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.oracle.get_exadata_infrastructure(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Cloud Exadata Infrastructure.
    :param str resource_group_name: The name of the Resource Group where the Cloud Exadata Infrastructure exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:oracle/getExadataInfrastructure:getExadataInfrastructure', __args__, opts=opts, typ=GetExadataInfrastructureResult)
    return __ret__.apply(lambda __response__: GetExadataInfrastructureResult(
        activated_storage_count=pulumi.get(__response__, 'activated_storage_count'),
        additional_storage_count=pulumi.get(__response__, 'additional_storage_count'),
        available_storage_size_in_gbs=pulumi.get(__response__, 'available_storage_size_in_gbs'),
        compute_count=pulumi.get(__response__, 'compute_count'),
        cpu_count=pulumi.get(__response__, 'cpu_count'),
        customer_contacts=pulumi.get(__response__, 'customer_contacts'),
        data_storage_size_in_tbs=pulumi.get(__response__, 'data_storage_size_in_tbs'),
        db_node_storage_size_in_gbs=pulumi.get(__response__, 'db_node_storage_size_in_gbs'),
        db_server_version=pulumi.get(__response__, 'db_server_version'),
        display_name=pulumi.get(__response__, 'display_name'),
        estimated_patching_times=pulumi.get(__response__, 'estimated_patching_times'),
        id=pulumi.get(__response__, 'id'),
        last_maintenance_run_id=pulumi.get(__response__, 'last_maintenance_run_id'),
        lifecycle_details=pulumi.get(__response__, 'lifecycle_details'),
        lifecycle_state=pulumi.get(__response__, 'lifecycle_state'),
        location=pulumi.get(__response__, 'location'),
        maintenance_windows=pulumi.get(__response__, 'maintenance_windows'),
        max_cpu_count=pulumi.get(__response__, 'max_cpu_count'),
        max_data_storage_in_tbs=pulumi.get(__response__, 'max_data_storage_in_tbs'),
        max_db_node_storage_size_in_gbs=pulumi.get(__response__, 'max_db_node_storage_size_in_gbs'),
        max_memory_in_gbs=pulumi.get(__response__, 'max_memory_in_gbs'),
        memory_size_in_gbs=pulumi.get(__response__, 'memory_size_in_gbs'),
        monthly_db_server_version=pulumi.get(__response__, 'monthly_db_server_version'),
        monthly_storage_server_version=pulumi.get(__response__, 'monthly_storage_server_version'),
        name=pulumi.get(__response__, 'name'),
        next_maintenance_run_id=pulumi.get(__response__, 'next_maintenance_run_id'),
        oci_url=pulumi.get(__response__, 'oci_url'),
        ocid=pulumi.get(__response__, 'ocid'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        shape=pulumi.get(__response__, 'shape'),
        storage_count=pulumi.get(__response__, 'storage_count'),
        storage_server_version=pulumi.get(__response__, 'storage_server_version'),
        tags=pulumi.get(__response__, 'tags'),
        time_created=pulumi.get(__response__, 'time_created'),
        total_storage_size_in_gbs=pulumi.get(__response__, 'total_storage_size_in_gbs'),
        zones=pulumi.get(__response__, 'zones')))
