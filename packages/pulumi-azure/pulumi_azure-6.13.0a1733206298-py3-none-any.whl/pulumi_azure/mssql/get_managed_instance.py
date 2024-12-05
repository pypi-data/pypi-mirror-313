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
    'GetManagedInstanceResult',
    'AwaitableGetManagedInstanceResult',
    'get_managed_instance',
    'get_managed_instance_output',
]

@pulumi.output_type
class GetManagedInstanceResult:
    """
    A collection of values returned by getManagedInstance.
    """
    def __init__(__self__, administrator_login=None, collation=None, customer_managed_key_id=None, dns_zone=None, dns_zone_partner_id=None, fqdn=None, id=None, identities=None, license_type=None, location=None, minimum_tls_version=None, name=None, proxy_override=None, public_data_endpoint_enabled=None, resource_group_name=None, sku_name=None, storage_account_type=None, storage_size_in_gb=None, subnet_id=None, tags=None, timezone_id=None, vcores=None):
        if administrator_login and not isinstance(administrator_login, str):
            raise TypeError("Expected argument 'administrator_login' to be a str")
        pulumi.set(__self__, "administrator_login", administrator_login)
        if collation and not isinstance(collation, str):
            raise TypeError("Expected argument 'collation' to be a str")
        pulumi.set(__self__, "collation", collation)
        if customer_managed_key_id and not isinstance(customer_managed_key_id, str):
            raise TypeError("Expected argument 'customer_managed_key_id' to be a str")
        pulumi.set(__self__, "customer_managed_key_id", customer_managed_key_id)
        if dns_zone and not isinstance(dns_zone, str):
            raise TypeError("Expected argument 'dns_zone' to be a str")
        pulumi.set(__self__, "dns_zone", dns_zone)
        if dns_zone_partner_id and not isinstance(dns_zone_partner_id, str):
            raise TypeError("Expected argument 'dns_zone_partner_id' to be a str")
        pulumi.set(__self__, "dns_zone_partner_id", dns_zone_partner_id)
        if fqdn and not isinstance(fqdn, str):
            raise TypeError("Expected argument 'fqdn' to be a str")
        pulumi.set(__self__, "fqdn", fqdn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identities and not isinstance(identities, list):
            raise TypeError("Expected argument 'identities' to be a list")
        pulumi.set(__self__, "identities", identities)
        if license_type and not isinstance(license_type, str):
            raise TypeError("Expected argument 'license_type' to be a str")
        pulumi.set(__self__, "license_type", license_type)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if minimum_tls_version and not isinstance(minimum_tls_version, str):
            raise TypeError("Expected argument 'minimum_tls_version' to be a str")
        pulumi.set(__self__, "minimum_tls_version", minimum_tls_version)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if proxy_override and not isinstance(proxy_override, str):
            raise TypeError("Expected argument 'proxy_override' to be a str")
        pulumi.set(__self__, "proxy_override", proxy_override)
        if public_data_endpoint_enabled and not isinstance(public_data_endpoint_enabled, bool):
            raise TypeError("Expected argument 'public_data_endpoint_enabled' to be a bool")
        pulumi.set(__self__, "public_data_endpoint_enabled", public_data_endpoint_enabled)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if sku_name and not isinstance(sku_name, str):
            raise TypeError("Expected argument 'sku_name' to be a str")
        pulumi.set(__self__, "sku_name", sku_name)
        if storage_account_type and not isinstance(storage_account_type, str):
            raise TypeError("Expected argument 'storage_account_type' to be a str")
        pulumi.set(__self__, "storage_account_type", storage_account_type)
        if storage_size_in_gb and not isinstance(storage_size_in_gb, int):
            raise TypeError("Expected argument 'storage_size_in_gb' to be a int")
        pulumi.set(__self__, "storage_size_in_gb", storage_size_in_gb)
        if subnet_id and not isinstance(subnet_id, str):
            raise TypeError("Expected argument 'subnet_id' to be a str")
        pulumi.set(__self__, "subnet_id", subnet_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if timezone_id and not isinstance(timezone_id, str):
            raise TypeError("Expected argument 'timezone_id' to be a str")
        pulumi.set(__self__, "timezone_id", timezone_id)
        if vcores and not isinstance(vcores, int):
            raise TypeError("Expected argument 'vcores' to be a int")
        pulumi.set(__self__, "vcores", vcores)

    @property
    @pulumi.getter(name="administratorLogin")
    def administrator_login(self) -> str:
        """
        The administrator login name for the SQL Managed Instance.
        """
        return pulumi.get(self, "administrator_login")

    @property
    @pulumi.getter
    def collation(self) -> str:
        """
        Specifies how the SQL Managed Instance will be collated.
        """
        return pulumi.get(self, "collation")

    @property
    @pulumi.getter(name="customerManagedKeyId")
    def customer_managed_key_id(self) -> str:
        return pulumi.get(self, "customer_managed_key_id")

    @property
    @pulumi.getter(name="dnsZone")
    def dns_zone(self) -> str:
        """
        The Dns Zone where the SQL Managed Instance is located.
        """
        return pulumi.get(self, "dns_zone")

    @property
    @pulumi.getter(name="dnsZonePartnerId")
    def dns_zone_partner_id(self) -> str:
        """
        The ID of the SQL Managed Instance which shares the DNS zone.
        """
        return pulumi.get(self, "dns_zone_partner_id")

    @property
    @pulumi.getter
    def fqdn(self) -> str:
        """
        The fully qualified domain name of the Azure Managed SQL Instance.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identities(self) -> Sequence['outputs.GetManagedInstanceIdentityResult']:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, "identities")

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> str:
        """
        What type of license the SQL Managed Instance uses.
        """
        return pulumi.get(self, "license_type")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Specifies the supported Azure location where the resource exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="minimumTlsVersion")
    def minimum_tls_version(self) -> str:
        """
        The Minimum TLS Version.
        """
        return pulumi.get(self, "minimum_tls_version")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="proxyOverride")
    def proxy_override(self) -> str:
        """
        Specifies how the SQL Managed Instance will be accessed.
        """
        return pulumi.get(self, "proxy_override")

    @property
    @pulumi.getter(name="publicDataEndpointEnabled")
    def public_data_endpoint_enabled(self) -> bool:
        """
        Whether the public data endpoint is enabled.
        """
        return pulumi.get(self, "public_data_endpoint_enabled")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="skuName")
    def sku_name(self) -> str:
        """
        Specifies the SKU Name of the SQL Managed Instance.
        """
        return pulumi.get(self, "sku_name")

    @property
    @pulumi.getter(name="storageAccountType")
    def storage_account_type(self) -> str:
        """
        Specifies the storage account type used to store backups for this database.
        """
        return pulumi.get(self, "storage_account_type")

    @property
    @pulumi.getter(name="storageSizeInGb")
    def storage_size_in_gb(self) -> int:
        """
        Maximum storage space allocated for the SQL Managed Instance.
        """
        return pulumi.get(self, "storage_size_in_gb")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> str:
        """
        The subnet resource ID that the SQL Managed Instance is associated with.
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timezoneId")
    def timezone_id(self) -> str:
        """
        The TimeZone ID that the SQL Managed Instance is running in.
        """
        return pulumi.get(self, "timezone_id")

    @property
    @pulumi.getter
    def vcores(self) -> int:
        """
        Number of cores that are assigned to the SQL Managed Instance.
        """
        return pulumi.get(self, "vcores")


class AwaitableGetManagedInstanceResult(GetManagedInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagedInstanceResult(
            administrator_login=self.administrator_login,
            collation=self.collation,
            customer_managed_key_id=self.customer_managed_key_id,
            dns_zone=self.dns_zone,
            dns_zone_partner_id=self.dns_zone_partner_id,
            fqdn=self.fqdn,
            id=self.id,
            identities=self.identities,
            license_type=self.license_type,
            location=self.location,
            minimum_tls_version=self.minimum_tls_version,
            name=self.name,
            proxy_override=self.proxy_override,
            public_data_endpoint_enabled=self.public_data_endpoint_enabled,
            resource_group_name=self.resource_group_name,
            sku_name=self.sku_name,
            storage_account_type=self.storage_account_type,
            storage_size_in_gb=self.storage_size_in_gb,
            subnet_id=self.subnet_id,
            tags=self.tags,
            timezone_id=self.timezone_id,
            vcores=self.vcores)


def get_managed_instance(name: Optional[str] = None,
                         resource_group_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagedInstanceResult:
    """
    Use this data source to access information about an existing Microsoft SQL Azure Managed Instance.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.mssql.get_managed_instance(name="managedsqlinstance",
        resource_group_name=example_azurerm_resource_group["name"])
    ```


    :param str name: The name of the SQL Managed Instance.
    :param str resource_group_name: The name of the resource group where the SQL Managed Instance exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:mssql/getManagedInstance:getManagedInstance', __args__, opts=opts, typ=GetManagedInstanceResult).value

    return AwaitableGetManagedInstanceResult(
        administrator_login=pulumi.get(__ret__, 'administrator_login'),
        collation=pulumi.get(__ret__, 'collation'),
        customer_managed_key_id=pulumi.get(__ret__, 'customer_managed_key_id'),
        dns_zone=pulumi.get(__ret__, 'dns_zone'),
        dns_zone_partner_id=pulumi.get(__ret__, 'dns_zone_partner_id'),
        fqdn=pulumi.get(__ret__, 'fqdn'),
        id=pulumi.get(__ret__, 'id'),
        identities=pulumi.get(__ret__, 'identities'),
        license_type=pulumi.get(__ret__, 'license_type'),
        location=pulumi.get(__ret__, 'location'),
        minimum_tls_version=pulumi.get(__ret__, 'minimum_tls_version'),
        name=pulumi.get(__ret__, 'name'),
        proxy_override=pulumi.get(__ret__, 'proxy_override'),
        public_data_endpoint_enabled=pulumi.get(__ret__, 'public_data_endpoint_enabled'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        sku_name=pulumi.get(__ret__, 'sku_name'),
        storage_account_type=pulumi.get(__ret__, 'storage_account_type'),
        storage_size_in_gb=pulumi.get(__ret__, 'storage_size_in_gb'),
        subnet_id=pulumi.get(__ret__, 'subnet_id'),
        tags=pulumi.get(__ret__, 'tags'),
        timezone_id=pulumi.get(__ret__, 'timezone_id'),
        vcores=pulumi.get(__ret__, 'vcores'))
def get_managed_instance_output(name: Optional[pulumi.Input[str]] = None,
                                resource_group_name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetManagedInstanceResult]:
    """
    Use this data source to access information about an existing Microsoft SQL Azure Managed Instance.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.mssql.get_managed_instance(name="managedsqlinstance",
        resource_group_name=example_azurerm_resource_group["name"])
    ```


    :param str name: The name of the SQL Managed Instance.
    :param str resource_group_name: The name of the resource group where the SQL Managed Instance exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:mssql/getManagedInstance:getManagedInstance', __args__, opts=opts, typ=GetManagedInstanceResult)
    return __ret__.apply(lambda __response__: GetManagedInstanceResult(
        administrator_login=pulumi.get(__response__, 'administrator_login'),
        collation=pulumi.get(__response__, 'collation'),
        customer_managed_key_id=pulumi.get(__response__, 'customer_managed_key_id'),
        dns_zone=pulumi.get(__response__, 'dns_zone'),
        dns_zone_partner_id=pulumi.get(__response__, 'dns_zone_partner_id'),
        fqdn=pulumi.get(__response__, 'fqdn'),
        id=pulumi.get(__response__, 'id'),
        identities=pulumi.get(__response__, 'identities'),
        license_type=pulumi.get(__response__, 'license_type'),
        location=pulumi.get(__response__, 'location'),
        minimum_tls_version=pulumi.get(__response__, 'minimum_tls_version'),
        name=pulumi.get(__response__, 'name'),
        proxy_override=pulumi.get(__response__, 'proxy_override'),
        public_data_endpoint_enabled=pulumi.get(__response__, 'public_data_endpoint_enabled'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        sku_name=pulumi.get(__response__, 'sku_name'),
        storage_account_type=pulumi.get(__response__, 'storage_account_type'),
        storage_size_in_gb=pulumi.get(__response__, 'storage_size_in_gb'),
        subnet_id=pulumi.get(__response__, 'subnet_id'),
        tags=pulumi.get(__response__, 'tags'),
        timezone_id=pulumi.get(__response__, 'timezone_id'),
        vcores=pulumi.get(__response__, 'vcores')))
