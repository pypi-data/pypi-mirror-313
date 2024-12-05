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
    'GetDeploymentResult',
    'AwaitableGetDeploymentResult',
    'get_deployment',
    'get_deployment_output',
]

@pulumi.output_type
class GetDeploymentResult:
    """
    A collection of values returned by getDeployment.
    """
    def __init__(__self__, auto_scale_profiles=None, automatic_upgrade_channel=None, capacity=None, diagnose_support_enabled=None, email=None, frontend_privates=None, frontend_publics=None, id=None, identities=None, ip_address=None, location=None, logging_storage_accounts=None, managed_resource_group=None, name=None, network_interfaces=None, nginx_version=None, resource_group_name=None, sku=None, tags=None):
        if auto_scale_profiles and not isinstance(auto_scale_profiles, list):
            raise TypeError("Expected argument 'auto_scale_profiles' to be a list")
        pulumi.set(__self__, "auto_scale_profiles", auto_scale_profiles)
        if automatic_upgrade_channel and not isinstance(automatic_upgrade_channel, str):
            raise TypeError("Expected argument 'automatic_upgrade_channel' to be a str")
        pulumi.set(__self__, "automatic_upgrade_channel", automatic_upgrade_channel)
        if capacity and not isinstance(capacity, int):
            raise TypeError("Expected argument 'capacity' to be a int")
        pulumi.set(__self__, "capacity", capacity)
        if diagnose_support_enabled and not isinstance(diagnose_support_enabled, bool):
            raise TypeError("Expected argument 'diagnose_support_enabled' to be a bool")
        pulumi.set(__self__, "diagnose_support_enabled", diagnose_support_enabled)
        if email and not isinstance(email, str):
            raise TypeError("Expected argument 'email' to be a str")
        pulumi.set(__self__, "email", email)
        if frontend_privates and not isinstance(frontend_privates, list):
            raise TypeError("Expected argument 'frontend_privates' to be a list")
        pulumi.set(__self__, "frontend_privates", frontend_privates)
        if frontend_publics and not isinstance(frontend_publics, list):
            raise TypeError("Expected argument 'frontend_publics' to be a list")
        pulumi.set(__self__, "frontend_publics", frontend_publics)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identities and not isinstance(identities, list):
            raise TypeError("Expected argument 'identities' to be a list")
        pulumi.set(__self__, "identities", identities)
        if ip_address and not isinstance(ip_address, str):
            raise TypeError("Expected argument 'ip_address' to be a str")
        pulumi.set(__self__, "ip_address", ip_address)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if logging_storage_accounts and not isinstance(logging_storage_accounts, list):
            raise TypeError("Expected argument 'logging_storage_accounts' to be a list")
        pulumi.set(__self__, "logging_storage_accounts", logging_storage_accounts)
        if managed_resource_group and not isinstance(managed_resource_group, str):
            raise TypeError("Expected argument 'managed_resource_group' to be a str")
        pulumi.set(__self__, "managed_resource_group", managed_resource_group)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_interfaces and not isinstance(network_interfaces, list):
            raise TypeError("Expected argument 'network_interfaces' to be a list")
        pulumi.set(__self__, "network_interfaces", network_interfaces)
        if nginx_version and not isinstance(nginx_version, str):
            raise TypeError("Expected argument 'nginx_version' to be a str")
        pulumi.set(__self__, "nginx_version", nginx_version)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        pulumi.set(__self__, "sku", sku)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="autoScaleProfiles")
    def auto_scale_profiles(self) -> Sequence['outputs.GetDeploymentAutoScaleProfileResult']:
        """
        An `auto_scale_profile` block as defined below.
        """
        return pulumi.get(self, "auto_scale_profiles")

    @property
    @pulumi.getter(name="automaticUpgradeChannel")
    def automatic_upgrade_channel(self) -> str:
        """
        The automatic upgrade channel for this NGINX deployment.
        """
        return pulumi.get(self, "automatic_upgrade_channel")

    @property
    @pulumi.getter
    def capacity(self) -> int:
        """
        The number of NGINX capacity units for this NGINX Deployment.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter(name="diagnoseSupportEnabled")
    def diagnose_support_enabled(self) -> bool:
        """
        Whether metrics are exported to Azure Monitor.
        """
        return pulumi.get(self, "diagnose_support_enabled")

    @property
    @pulumi.getter
    def email(self) -> str:
        """
        Preferred email associated with the NGINX Deployment.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter(name="frontendPrivates")
    def frontend_privates(self) -> Sequence['outputs.GetDeploymentFrontendPrivateResult']:
        """
        A `frontend_private` block as defined below.
        """
        return pulumi.get(self, "frontend_privates")

    @property
    @pulumi.getter(name="frontendPublics")
    def frontend_publics(self) -> Sequence['outputs.GetDeploymentFrontendPublicResult']:
        """
        A `frontend_public` block as defined below.
        """
        return pulumi.get(self, "frontend_publics")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identities(self) -> Sequence['outputs.GetDeploymentIdentityResult']:
        """
        A `identity` block as defined below.
        """
        return pulumi.get(self, "identities")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> str:
        """
        The list of Public IP Resource IDs for this NGINX Deployment.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure Region where the NGINX Deployment exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="loggingStorageAccounts")
    def logging_storage_accounts(self) -> Sequence['outputs.GetDeploymentLoggingStorageAccountResult']:
        """
        A `logging_storage_account` block as defined below.
        """
        return pulumi.get(self, "logging_storage_accounts")

    @property
    @pulumi.getter(name="managedResourceGroup")
    def managed_resource_group(self) -> str:
        """
        Auto-generated managed resource group for the NGINX Deployment.
        """
        return pulumi.get(self, "managed_resource_group")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the autoscaling profile.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Sequence['outputs.GetDeploymentNetworkInterfaceResult']:
        """
        A `network_interface` block as defined below.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter(name="nginxVersion")
    def nginx_version(self) -> str:
        """
        NGINX version of the Deployment.
        """
        return pulumi.get(self, "nginx_version")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def sku(self) -> str:
        """
        The NGINX Deployment SKU.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the NGINX Deployment.
        """
        return pulumi.get(self, "tags")


class AwaitableGetDeploymentResult(GetDeploymentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDeploymentResult(
            auto_scale_profiles=self.auto_scale_profiles,
            automatic_upgrade_channel=self.automatic_upgrade_channel,
            capacity=self.capacity,
            diagnose_support_enabled=self.diagnose_support_enabled,
            email=self.email,
            frontend_privates=self.frontend_privates,
            frontend_publics=self.frontend_publics,
            id=self.id,
            identities=self.identities,
            ip_address=self.ip_address,
            location=self.location,
            logging_storage_accounts=self.logging_storage_accounts,
            managed_resource_group=self.managed_resource_group,
            name=self.name,
            network_interfaces=self.network_interfaces,
            nginx_version=self.nginx_version,
            resource_group_name=self.resource_group_name,
            sku=self.sku,
            tags=self.tags)


def get_deployment(name: Optional[str] = None,
                   resource_group_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDeploymentResult:
    """
    Use this data source to access information about an existing NGINX Deployment.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.nginx.get_deployment(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this NGINX Deployment.
    :param str resource_group_name: The name of the Resource Group where the NGINX Deployment exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:nginx/getDeployment:getDeployment', __args__, opts=opts, typ=GetDeploymentResult).value

    return AwaitableGetDeploymentResult(
        auto_scale_profiles=pulumi.get(__ret__, 'auto_scale_profiles'),
        automatic_upgrade_channel=pulumi.get(__ret__, 'automatic_upgrade_channel'),
        capacity=pulumi.get(__ret__, 'capacity'),
        diagnose_support_enabled=pulumi.get(__ret__, 'diagnose_support_enabled'),
        email=pulumi.get(__ret__, 'email'),
        frontend_privates=pulumi.get(__ret__, 'frontend_privates'),
        frontend_publics=pulumi.get(__ret__, 'frontend_publics'),
        id=pulumi.get(__ret__, 'id'),
        identities=pulumi.get(__ret__, 'identities'),
        ip_address=pulumi.get(__ret__, 'ip_address'),
        location=pulumi.get(__ret__, 'location'),
        logging_storage_accounts=pulumi.get(__ret__, 'logging_storage_accounts'),
        managed_resource_group=pulumi.get(__ret__, 'managed_resource_group'),
        name=pulumi.get(__ret__, 'name'),
        network_interfaces=pulumi.get(__ret__, 'network_interfaces'),
        nginx_version=pulumi.get(__ret__, 'nginx_version'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        sku=pulumi.get(__ret__, 'sku'),
        tags=pulumi.get(__ret__, 'tags'))
def get_deployment_output(name: Optional[pulumi.Input[str]] = None,
                          resource_group_name: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDeploymentResult]:
    """
    Use this data source to access information about an existing NGINX Deployment.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.nginx.get_deployment(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this NGINX Deployment.
    :param str resource_group_name: The name of the Resource Group where the NGINX Deployment exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:nginx/getDeployment:getDeployment', __args__, opts=opts, typ=GetDeploymentResult)
    return __ret__.apply(lambda __response__: GetDeploymentResult(
        auto_scale_profiles=pulumi.get(__response__, 'auto_scale_profiles'),
        automatic_upgrade_channel=pulumi.get(__response__, 'automatic_upgrade_channel'),
        capacity=pulumi.get(__response__, 'capacity'),
        diagnose_support_enabled=pulumi.get(__response__, 'diagnose_support_enabled'),
        email=pulumi.get(__response__, 'email'),
        frontend_privates=pulumi.get(__response__, 'frontend_privates'),
        frontend_publics=pulumi.get(__response__, 'frontend_publics'),
        id=pulumi.get(__response__, 'id'),
        identities=pulumi.get(__response__, 'identities'),
        ip_address=pulumi.get(__response__, 'ip_address'),
        location=pulumi.get(__response__, 'location'),
        logging_storage_accounts=pulumi.get(__response__, 'logging_storage_accounts'),
        managed_resource_group=pulumi.get(__response__, 'managed_resource_group'),
        name=pulumi.get(__response__, 'name'),
        network_interfaces=pulumi.get(__response__, 'network_interfaces'),
        nginx_version=pulumi.get(__response__, 'nginx_version'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        sku=pulumi.get(__response__, 'sku'),
        tags=pulumi.get(__response__, 'tags')))
