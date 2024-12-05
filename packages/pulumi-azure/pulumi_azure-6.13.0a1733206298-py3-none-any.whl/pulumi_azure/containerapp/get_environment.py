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
    'GetEnvironmentResult',
    'AwaitableGetEnvironmentResult',
    'get_environment',
    'get_environment_output',
]

@pulumi.output_type
class GetEnvironmentResult:
    """
    A collection of values returned by getEnvironment.
    """
    def __init__(__self__, custom_domain_verification_id=None, default_domain=None, docker_bridge_cidr=None, id=None, infrastructure_subnet_id=None, internal_load_balancer_enabled=None, location=None, log_analytics_workspace_name=None, name=None, platform_reserved_cidr=None, platform_reserved_dns_ip_address=None, resource_group_name=None, static_ip_address=None, tags=None):
        if custom_domain_verification_id and not isinstance(custom_domain_verification_id, str):
            raise TypeError("Expected argument 'custom_domain_verification_id' to be a str")
        pulumi.set(__self__, "custom_domain_verification_id", custom_domain_verification_id)
        if default_domain and not isinstance(default_domain, str):
            raise TypeError("Expected argument 'default_domain' to be a str")
        pulumi.set(__self__, "default_domain", default_domain)
        if docker_bridge_cidr and not isinstance(docker_bridge_cidr, str):
            raise TypeError("Expected argument 'docker_bridge_cidr' to be a str")
        pulumi.set(__self__, "docker_bridge_cidr", docker_bridge_cidr)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if infrastructure_subnet_id and not isinstance(infrastructure_subnet_id, str):
            raise TypeError("Expected argument 'infrastructure_subnet_id' to be a str")
        pulumi.set(__self__, "infrastructure_subnet_id", infrastructure_subnet_id)
        if internal_load_balancer_enabled and not isinstance(internal_load_balancer_enabled, bool):
            raise TypeError("Expected argument 'internal_load_balancer_enabled' to be a bool")
        pulumi.set(__self__, "internal_load_balancer_enabled", internal_load_balancer_enabled)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if log_analytics_workspace_name and not isinstance(log_analytics_workspace_name, str):
            raise TypeError("Expected argument 'log_analytics_workspace_name' to be a str")
        pulumi.set(__self__, "log_analytics_workspace_name", log_analytics_workspace_name)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if platform_reserved_cidr and not isinstance(platform_reserved_cidr, str):
            raise TypeError("Expected argument 'platform_reserved_cidr' to be a str")
        pulumi.set(__self__, "platform_reserved_cidr", platform_reserved_cidr)
        if platform_reserved_dns_ip_address and not isinstance(platform_reserved_dns_ip_address, str):
            raise TypeError("Expected argument 'platform_reserved_dns_ip_address' to be a str")
        pulumi.set(__self__, "platform_reserved_dns_ip_address", platform_reserved_dns_ip_address)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if static_ip_address and not isinstance(static_ip_address, str):
            raise TypeError("Expected argument 'static_ip_address' to be a str")
        pulumi.set(__self__, "static_ip_address", static_ip_address)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="customDomainVerificationId")
    def custom_domain_verification_id(self) -> str:
        """
        The ID of the Custom Domain Verification for this Container App Environment.
        """
        return pulumi.get(self, "custom_domain_verification_id")

    @property
    @pulumi.getter(name="defaultDomain")
    def default_domain(self) -> str:
        """
        The default publicly resolvable name of this Container App Environment. This is generated at creation time to be globally unique.
        """
        return pulumi.get(self, "default_domain")

    @property
    @pulumi.getter(name="dockerBridgeCidr")
    def docker_bridge_cidr(self) -> str:
        """
        The network addressing in which the Container Apps in this Container App Environment will reside in CIDR notation.
        """
        return pulumi.get(self, "docker_bridge_cidr")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="infrastructureSubnetId")
    def infrastructure_subnet_id(self) -> str:
        """
        The ID of the Subnet in use by the Container Apps Control Plane.
        """
        return pulumi.get(self, "infrastructure_subnet_id")

    @property
    @pulumi.getter(name="internalLoadBalancerEnabled")
    def internal_load_balancer_enabled(self) -> bool:
        """
        Does the Container App Environment operate in Internal Load Balancing Mode?
        """
        return pulumi.get(self, "internal_load_balancer_enabled")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure Location where this Container App Environment exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceName")
    def log_analytics_workspace_name(self) -> str:
        """
        The name of the Log Analytics Workspace this Container Apps Managed Environment is linked to.
        """
        return pulumi.get(self, "log_analytics_workspace_name")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="platformReservedCidr")
    def platform_reserved_cidr(self) -> str:
        """
        The IP range, in CIDR notation, that is reserved for environment infrastructure IP addresses.
        """
        return pulumi.get(self, "platform_reserved_cidr")

    @property
    @pulumi.getter(name="platformReservedDnsIpAddress")
    def platform_reserved_dns_ip_address(self) -> str:
        """
        The IP address from the IP range defined by `platform_reserved_cidr` that is reserved for the internal DNS server.
        """
        return pulumi.get(self, "platform_reserved_dns_ip_address")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="staticIpAddress")
    def static_ip_address(self) -> str:
        """
        The Static IP address of the Environment.
        """
        return pulumi.get(self, "static_ip_address")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetEnvironmentResult(GetEnvironmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEnvironmentResult(
            custom_domain_verification_id=self.custom_domain_verification_id,
            default_domain=self.default_domain,
            docker_bridge_cidr=self.docker_bridge_cidr,
            id=self.id,
            infrastructure_subnet_id=self.infrastructure_subnet_id,
            internal_load_balancer_enabled=self.internal_load_balancer_enabled,
            location=self.location,
            log_analytics_workspace_name=self.log_analytics_workspace_name,
            name=self.name,
            platform_reserved_cidr=self.platform_reserved_cidr,
            platform_reserved_dns_ip_address=self.platform_reserved_dns_ip_address,
            resource_group_name=self.resource_group_name,
            static_ip_address=self.static_ip_address,
            tags=self.tags)


def get_environment(name: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEnvironmentResult:
    """
    Use this data source to access information about an existing Container App Environment.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.containerapp.get_environment(name="example-environment",
        resource_group_name="example-resources")
    ```


    :param str name: The name of the Container Apps Managed Environment.
    :param str resource_group_name: The name of the Resource Group where this Container App Environment exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:containerapp/getEnvironment:getEnvironment', __args__, opts=opts, typ=GetEnvironmentResult).value

    return AwaitableGetEnvironmentResult(
        custom_domain_verification_id=pulumi.get(__ret__, 'custom_domain_verification_id'),
        default_domain=pulumi.get(__ret__, 'default_domain'),
        docker_bridge_cidr=pulumi.get(__ret__, 'docker_bridge_cidr'),
        id=pulumi.get(__ret__, 'id'),
        infrastructure_subnet_id=pulumi.get(__ret__, 'infrastructure_subnet_id'),
        internal_load_balancer_enabled=pulumi.get(__ret__, 'internal_load_balancer_enabled'),
        location=pulumi.get(__ret__, 'location'),
        log_analytics_workspace_name=pulumi.get(__ret__, 'log_analytics_workspace_name'),
        name=pulumi.get(__ret__, 'name'),
        platform_reserved_cidr=pulumi.get(__ret__, 'platform_reserved_cidr'),
        platform_reserved_dns_ip_address=pulumi.get(__ret__, 'platform_reserved_dns_ip_address'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        static_ip_address=pulumi.get(__ret__, 'static_ip_address'),
        tags=pulumi.get(__ret__, 'tags'))
def get_environment_output(name: Optional[pulumi.Input[str]] = None,
                           resource_group_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEnvironmentResult]:
    """
    Use this data source to access information about an existing Container App Environment.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.containerapp.get_environment(name="example-environment",
        resource_group_name="example-resources")
    ```


    :param str name: The name of the Container Apps Managed Environment.
    :param str resource_group_name: The name of the Resource Group where this Container App Environment exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:containerapp/getEnvironment:getEnvironment', __args__, opts=opts, typ=GetEnvironmentResult)
    return __ret__.apply(lambda __response__: GetEnvironmentResult(
        custom_domain_verification_id=pulumi.get(__response__, 'custom_domain_verification_id'),
        default_domain=pulumi.get(__response__, 'default_domain'),
        docker_bridge_cidr=pulumi.get(__response__, 'docker_bridge_cidr'),
        id=pulumi.get(__response__, 'id'),
        infrastructure_subnet_id=pulumi.get(__response__, 'infrastructure_subnet_id'),
        internal_load_balancer_enabled=pulumi.get(__response__, 'internal_load_balancer_enabled'),
        location=pulumi.get(__response__, 'location'),
        log_analytics_workspace_name=pulumi.get(__response__, 'log_analytics_workspace_name'),
        name=pulumi.get(__response__, 'name'),
        platform_reserved_cidr=pulumi.get(__response__, 'platform_reserved_cidr'),
        platform_reserved_dns_ip_address=pulumi.get(__response__, 'platform_reserved_dns_ip_address'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        static_ip_address=pulumi.get(__response__, 'static_ip_address'),
        tags=pulumi.get(__response__, 'tags')))
