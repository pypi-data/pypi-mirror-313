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
    'GetApplicationGatewayResult',
    'AwaitableGetApplicationGatewayResult',
    'get_application_gateway',
    'get_application_gateway_output',
]

@pulumi.output_type
class GetApplicationGatewayResult:
    """
    A collection of values returned by getApplicationGateway.
    """
    def __init__(__self__, authentication_certificates=None, autoscale_configurations=None, backend_address_pools=None, backend_http_settings=None, custom_error_configurations=None, fips_enabled=None, firewall_policy_id=None, force_firewall_policy_association=None, frontend_ip_configurations=None, frontend_ports=None, gateway_ip_configurations=None, globals=None, http2_enabled=None, http_listeners=None, id=None, identities=None, location=None, name=None, private_endpoint_connections=None, private_link_configurations=None, probes=None, redirect_configurations=None, request_routing_rules=None, resource_group_name=None, rewrite_rule_sets=None, skus=None, ssl_certificates=None, ssl_policies=None, ssl_profiles=None, tags=None, trusted_client_certificates=None, trusted_root_certificates=None, url_path_maps=None, waf_configurations=None, zones=None):
        if authentication_certificates and not isinstance(authentication_certificates, list):
            raise TypeError("Expected argument 'authentication_certificates' to be a list")
        pulumi.set(__self__, "authentication_certificates", authentication_certificates)
        if autoscale_configurations and not isinstance(autoscale_configurations, list):
            raise TypeError("Expected argument 'autoscale_configurations' to be a list")
        pulumi.set(__self__, "autoscale_configurations", autoscale_configurations)
        if backend_address_pools and not isinstance(backend_address_pools, list):
            raise TypeError("Expected argument 'backend_address_pools' to be a list")
        pulumi.set(__self__, "backend_address_pools", backend_address_pools)
        if backend_http_settings and not isinstance(backend_http_settings, list):
            raise TypeError("Expected argument 'backend_http_settings' to be a list")
        pulumi.set(__self__, "backend_http_settings", backend_http_settings)
        if custom_error_configurations and not isinstance(custom_error_configurations, list):
            raise TypeError("Expected argument 'custom_error_configurations' to be a list")
        pulumi.set(__self__, "custom_error_configurations", custom_error_configurations)
        if fips_enabled and not isinstance(fips_enabled, bool):
            raise TypeError("Expected argument 'fips_enabled' to be a bool")
        pulumi.set(__self__, "fips_enabled", fips_enabled)
        if firewall_policy_id and not isinstance(firewall_policy_id, str):
            raise TypeError("Expected argument 'firewall_policy_id' to be a str")
        pulumi.set(__self__, "firewall_policy_id", firewall_policy_id)
        if force_firewall_policy_association and not isinstance(force_firewall_policy_association, bool):
            raise TypeError("Expected argument 'force_firewall_policy_association' to be a bool")
        pulumi.set(__self__, "force_firewall_policy_association", force_firewall_policy_association)
        if frontend_ip_configurations and not isinstance(frontend_ip_configurations, list):
            raise TypeError("Expected argument 'frontend_ip_configurations' to be a list")
        pulumi.set(__self__, "frontend_ip_configurations", frontend_ip_configurations)
        if frontend_ports and not isinstance(frontend_ports, list):
            raise TypeError("Expected argument 'frontend_ports' to be a list")
        pulumi.set(__self__, "frontend_ports", frontend_ports)
        if gateway_ip_configurations and not isinstance(gateway_ip_configurations, list):
            raise TypeError("Expected argument 'gateway_ip_configurations' to be a list")
        pulumi.set(__self__, "gateway_ip_configurations", gateway_ip_configurations)
        if globals and not isinstance(globals, list):
            raise TypeError("Expected argument 'globals' to be a list")
        pulumi.set(__self__, "globals", globals)
        if http2_enabled and not isinstance(http2_enabled, bool):
            raise TypeError("Expected argument 'http2_enabled' to be a bool")
        pulumi.set(__self__, "http2_enabled", http2_enabled)
        if http_listeners and not isinstance(http_listeners, list):
            raise TypeError("Expected argument 'http_listeners' to be a list")
        pulumi.set(__self__, "http_listeners", http_listeners)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identities and not isinstance(identities, list):
            raise TypeError("Expected argument 'identities' to be a list")
        pulumi.set(__self__, "identities", identities)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if private_endpoint_connections and not isinstance(private_endpoint_connections, list):
            raise TypeError("Expected argument 'private_endpoint_connections' to be a list")
        pulumi.set(__self__, "private_endpoint_connections", private_endpoint_connections)
        if private_link_configurations and not isinstance(private_link_configurations, list):
            raise TypeError("Expected argument 'private_link_configurations' to be a list")
        pulumi.set(__self__, "private_link_configurations", private_link_configurations)
        if probes and not isinstance(probes, list):
            raise TypeError("Expected argument 'probes' to be a list")
        pulumi.set(__self__, "probes", probes)
        if redirect_configurations and not isinstance(redirect_configurations, list):
            raise TypeError("Expected argument 'redirect_configurations' to be a list")
        pulumi.set(__self__, "redirect_configurations", redirect_configurations)
        if request_routing_rules and not isinstance(request_routing_rules, list):
            raise TypeError("Expected argument 'request_routing_rules' to be a list")
        pulumi.set(__self__, "request_routing_rules", request_routing_rules)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if rewrite_rule_sets and not isinstance(rewrite_rule_sets, list):
            raise TypeError("Expected argument 'rewrite_rule_sets' to be a list")
        pulumi.set(__self__, "rewrite_rule_sets", rewrite_rule_sets)
        if skus and not isinstance(skus, list):
            raise TypeError("Expected argument 'skus' to be a list")
        pulumi.set(__self__, "skus", skus)
        if ssl_certificates and not isinstance(ssl_certificates, list):
            raise TypeError("Expected argument 'ssl_certificates' to be a list")
        pulumi.set(__self__, "ssl_certificates", ssl_certificates)
        if ssl_policies and not isinstance(ssl_policies, list):
            raise TypeError("Expected argument 'ssl_policies' to be a list")
        pulumi.set(__self__, "ssl_policies", ssl_policies)
        if ssl_profiles and not isinstance(ssl_profiles, list):
            raise TypeError("Expected argument 'ssl_profiles' to be a list")
        pulumi.set(__self__, "ssl_profiles", ssl_profiles)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if trusted_client_certificates and not isinstance(trusted_client_certificates, list):
            raise TypeError("Expected argument 'trusted_client_certificates' to be a list")
        pulumi.set(__self__, "trusted_client_certificates", trusted_client_certificates)
        if trusted_root_certificates and not isinstance(trusted_root_certificates, list):
            raise TypeError("Expected argument 'trusted_root_certificates' to be a list")
        pulumi.set(__self__, "trusted_root_certificates", trusted_root_certificates)
        if url_path_maps and not isinstance(url_path_maps, list):
            raise TypeError("Expected argument 'url_path_maps' to be a list")
        pulumi.set(__self__, "url_path_maps", url_path_maps)
        if waf_configurations and not isinstance(waf_configurations, list):
            raise TypeError("Expected argument 'waf_configurations' to be a list")
        pulumi.set(__self__, "waf_configurations", waf_configurations)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="authenticationCertificates")
    def authentication_certificates(self) -> Sequence['outputs.GetApplicationGatewayAuthenticationCertificateResult']:
        """
        One or more `authentication_certificate` blocks as defined below.
        """
        return pulumi.get(self, "authentication_certificates")

    @property
    @pulumi.getter(name="autoscaleConfigurations")
    def autoscale_configurations(self) -> Sequence['outputs.GetApplicationGatewayAutoscaleConfigurationResult']:
        """
        An `autoscale_configuration` block as defined below.
        """
        return pulumi.get(self, "autoscale_configurations")

    @property
    @pulumi.getter(name="backendAddressPools")
    def backend_address_pools(self) -> Sequence['outputs.GetApplicationGatewayBackendAddressPoolResult']:
        """
        One or more `backend_address_pool` blocks as defined below.
        """
        return pulumi.get(self, "backend_address_pools")

    @property
    @pulumi.getter(name="backendHttpSettings")
    def backend_http_settings(self) -> Sequence['outputs.GetApplicationGatewayBackendHttpSettingResult']:
        """
        One or more `backend_http_settings` blocks as defined below.
        """
        return pulumi.get(self, "backend_http_settings")

    @property
    @pulumi.getter(name="customErrorConfigurations")
    def custom_error_configurations(self) -> Sequence['outputs.GetApplicationGatewayCustomErrorConfigurationResult']:
        """
        One or more `custom_error_configuration` blocks as defined below.
        """
        return pulumi.get(self, "custom_error_configurations")

    @property
    @pulumi.getter(name="fipsEnabled")
    def fips_enabled(self) -> bool:
        """
        Is FIPS enabled on the Application Gateway?
        """
        return pulumi.get(self, "fips_enabled")

    @property
    @pulumi.getter(name="firewallPolicyId")
    def firewall_policy_id(self) -> str:
        """
        The ID of the Web Application Firewall Policy which is used as an HTTP Listener for this Path Rule.
        """
        return pulumi.get(self, "firewall_policy_id")

    @property
    @pulumi.getter(name="forceFirewallPolicyAssociation")
    def force_firewall_policy_association(self) -> bool:
        """
        Is the Firewall Policy associated with the Application Gateway?
        """
        return pulumi.get(self, "force_firewall_policy_association")

    @property
    @pulumi.getter(name="frontendIpConfigurations")
    def frontend_ip_configurations(self) -> Sequence['outputs.GetApplicationGatewayFrontendIpConfigurationResult']:
        """
        One or more `frontend_ip_configuration` blocks as defined below.
        """
        return pulumi.get(self, "frontend_ip_configurations")

    @property
    @pulumi.getter(name="frontendPorts")
    def frontend_ports(self) -> Sequence['outputs.GetApplicationGatewayFrontendPortResult']:
        """
        One or more `frontend_port` blocks as defined below.
        """
        return pulumi.get(self, "frontend_ports")

    @property
    @pulumi.getter(name="gatewayIpConfigurations")
    def gateway_ip_configurations(self) -> Sequence['outputs.GetApplicationGatewayGatewayIpConfigurationResult']:
        """
        One or more `gateway_ip_configuration` blocks as defined below.
        """
        return pulumi.get(self, "gateway_ip_configurations")

    @property
    @pulumi.getter
    def globals(self) -> Sequence['outputs.GetApplicationGatewayGlobalResult']:
        """
        A `global` block as defined below.
        """
        return pulumi.get(self, "globals")

    @property
    @pulumi.getter(name="http2Enabled")
    def http2_enabled(self) -> bool:
        """
        Is HTTP2 enabled on the application gateway resource?
        """
        return pulumi.get(self, "http2_enabled")

    @property
    @pulumi.getter(name="httpListeners")
    def http_listeners(self) -> Sequence['outputs.GetApplicationGatewayHttpListenerResult']:
        """
        One or more `http_listener` blocks as defined below.
        """
        return pulumi.get(self, "http_listeners")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identities(self) -> Sequence['outputs.GetApplicationGatewayIdentityResult']:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, "identities")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure region where the Application Gateway exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Unique name of the Rewrite Rule
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> Sequence['outputs.GetApplicationGatewayPrivateEndpointConnectionResult']:
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="privateLinkConfigurations")
    def private_link_configurations(self) -> Sequence['outputs.GetApplicationGatewayPrivateLinkConfigurationResult']:
        """
        One or more `private_link_configuration` blocks as defined below.
        """
        return pulumi.get(self, "private_link_configurations")

    @property
    @pulumi.getter
    def probes(self) -> Sequence['outputs.GetApplicationGatewayProbeResult']:
        """
        One or more `probe` blocks as defined below.
        """
        return pulumi.get(self, "probes")

    @property
    @pulumi.getter(name="redirectConfigurations")
    def redirect_configurations(self) -> Sequence['outputs.GetApplicationGatewayRedirectConfigurationResult']:
        """
        One or more `redirect_configuration` blocks as defined below.
        """
        return pulumi.get(self, "redirect_configurations")

    @property
    @pulumi.getter(name="requestRoutingRules")
    def request_routing_rules(self) -> Sequence['outputs.GetApplicationGatewayRequestRoutingRuleResult']:
        """
        One or more `request_routing_rule` blocks as defined below.
        """
        return pulumi.get(self, "request_routing_rules")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="rewriteRuleSets")
    def rewrite_rule_sets(self) -> Sequence['outputs.GetApplicationGatewayRewriteRuleSetResult']:
        """
        One or more `rewrite_rule_set` blocks as defined below.
        """
        return pulumi.get(self, "rewrite_rule_sets")

    @property
    @pulumi.getter
    def skus(self) -> Sequence['outputs.GetApplicationGatewaySkusResult']:
        """
        A `sku` block as defined below.
        """
        return pulumi.get(self, "skus")

    @property
    @pulumi.getter(name="sslCertificates")
    def ssl_certificates(self) -> Sequence['outputs.GetApplicationGatewaySslCertificateResult']:
        """
        One or more `ssl_certificate` blocks as defined below.
        """
        return pulumi.get(self, "ssl_certificates")

    @property
    @pulumi.getter(name="sslPolicies")
    def ssl_policies(self) -> Sequence['outputs.GetApplicationGatewaySslPolicyResult']:
        """
        a `ssl_policy` block as defined below.
        """
        return pulumi.get(self, "ssl_policies")

    @property
    @pulumi.getter(name="sslProfiles")
    def ssl_profiles(self) -> Sequence['outputs.GetApplicationGatewaySslProfileResult']:
        """
        One or more `ssl_profile` blocks as defined below.
        """
        return pulumi.get(self, "ssl_profiles")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="trustedClientCertificates")
    def trusted_client_certificates(self) -> Sequence['outputs.GetApplicationGatewayTrustedClientCertificateResult']:
        """
        One or more `trusted_client_certificate` blocks as defined below.
        """
        return pulumi.get(self, "trusted_client_certificates")

    @property
    @pulumi.getter(name="trustedRootCertificates")
    def trusted_root_certificates(self) -> Sequence['outputs.GetApplicationGatewayTrustedRootCertificateResult']:
        """
        One or more `trusted_root_certificate` blocks as defined below.
        """
        return pulumi.get(self, "trusted_root_certificates")

    @property
    @pulumi.getter(name="urlPathMaps")
    def url_path_maps(self) -> Sequence['outputs.GetApplicationGatewayUrlPathMapResult']:
        """
        One or more `url_path_map` blocks as defined below.
        """
        return pulumi.get(self, "url_path_maps")

    @property
    @pulumi.getter(name="wafConfigurations")
    def waf_configurations(self) -> Sequence['outputs.GetApplicationGatewayWafConfigurationResult']:
        """
        A `waf_configuration` block as defined below.
        """
        return pulumi.get(self, "waf_configurations")

    @property
    @pulumi.getter
    def zones(self) -> Sequence[str]:
        """
        The list of Availability Zones in which this Application Gateway can use.
        """
        return pulumi.get(self, "zones")


class AwaitableGetApplicationGatewayResult(GetApplicationGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationGatewayResult(
            authentication_certificates=self.authentication_certificates,
            autoscale_configurations=self.autoscale_configurations,
            backend_address_pools=self.backend_address_pools,
            backend_http_settings=self.backend_http_settings,
            custom_error_configurations=self.custom_error_configurations,
            fips_enabled=self.fips_enabled,
            firewall_policy_id=self.firewall_policy_id,
            force_firewall_policy_association=self.force_firewall_policy_association,
            frontend_ip_configurations=self.frontend_ip_configurations,
            frontend_ports=self.frontend_ports,
            gateway_ip_configurations=self.gateway_ip_configurations,
            globals=self.globals,
            http2_enabled=self.http2_enabled,
            http_listeners=self.http_listeners,
            id=self.id,
            identities=self.identities,
            location=self.location,
            name=self.name,
            private_endpoint_connections=self.private_endpoint_connections,
            private_link_configurations=self.private_link_configurations,
            probes=self.probes,
            redirect_configurations=self.redirect_configurations,
            request_routing_rules=self.request_routing_rules,
            resource_group_name=self.resource_group_name,
            rewrite_rule_sets=self.rewrite_rule_sets,
            skus=self.skus,
            ssl_certificates=self.ssl_certificates,
            ssl_policies=self.ssl_policies,
            ssl_profiles=self.ssl_profiles,
            tags=self.tags,
            trusted_client_certificates=self.trusted_client_certificates,
            trusted_root_certificates=self.trusted_root_certificates,
            url_path_maps=self.url_path_maps,
            waf_configurations=self.waf_configurations,
            zones=self.zones)


def get_application_gateway(name: Optional[str] = None,
                            resource_group_name: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationGatewayResult:
    """
    Use this data source to access information about an existing Application Gateway.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_application_gateway(name="existing-app-gateway",
        resource_group_name="existing-resources")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Application Gateway.
    :param str resource_group_name: The name of the Resource Group where the Application Gateway exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:network/getApplicationGateway:getApplicationGateway', __args__, opts=opts, typ=GetApplicationGatewayResult).value

    return AwaitableGetApplicationGatewayResult(
        authentication_certificates=pulumi.get(__ret__, 'authentication_certificates'),
        autoscale_configurations=pulumi.get(__ret__, 'autoscale_configurations'),
        backend_address_pools=pulumi.get(__ret__, 'backend_address_pools'),
        backend_http_settings=pulumi.get(__ret__, 'backend_http_settings'),
        custom_error_configurations=pulumi.get(__ret__, 'custom_error_configurations'),
        fips_enabled=pulumi.get(__ret__, 'fips_enabled'),
        firewall_policy_id=pulumi.get(__ret__, 'firewall_policy_id'),
        force_firewall_policy_association=pulumi.get(__ret__, 'force_firewall_policy_association'),
        frontend_ip_configurations=pulumi.get(__ret__, 'frontend_ip_configurations'),
        frontend_ports=pulumi.get(__ret__, 'frontend_ports'),
        gateway_ip_configurations=pulumi.get(__ret__, 'gateway_ip_configurations'),
        globals=pulumi.get(__ret__, 'globals'),
        http2_enabled=pulumi.get(__ret__, 'http2_enabled'),
        http_listeners=pulumi.get(__ret__, 'http_listeners'),
        id=pulumi.get(__ret__, 'id'),
        identities=pulumi.get(__ret__, 'identities'),
        location=pulumi.get(__ret__, 'location'),
        name=pulumi.get(__ret__, 'name'),
        private_endpoint_connections=pulumi.get(__ret__, 'private_endpoint_connections'),
        private_link_configurations=pulumi.get(__ret__, 'private_link_configurations'),
        probes=pulumi.get(__ret__, 'probes'),
        redirect_configurations=pulumi.get(__ret__, 'redirect_configurations'),
        request_routing_rules=pulumi.get(__ret__, 'request_routing_rules'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        rewrite_rule_sets=pulumi.get(__ret__, 'rewrite_rule_sets'),
        skus=pulumi.get(__ret__, 'skus'),
        ssl_certificates=pulumi.get(__ret__, 'ssl_certificates'),
        ssl_policies=pulumi.get(__ret__, 'ssl_policies'),
        ssl_profiles=pulumi.get(__ret__, 'ssl_profiles'),
        tags=pulumi.get(__ret__, 'tags'),
        trusted_client_certificates=pulumi.get(__ret__, 'trusted_client_certificates'),
        trusted_root_certificates=pulumi.get(__ret__, 'trusted_root_certificates'),
        url_path_maps=pulumi.get(__ret__, 'url_path_maps'),
        waf_configurations=pulumi.get(__ret__, 'waf_configurations'),
        zones=pulumi.get(__ret__, 'zones'))
def get_application_gateway_output(name: Optional[pulumi.Input[str]] = None,
                                   resource_group_name: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetApplicationGatewayResult]:
    """
    Use this data source to access information about an existing Application Gateway.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_application_gateway(name="existing-app-gateway",
        resource_group_name="existing-resources")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Application Gateway.
    :param str resource_group_name: The name of the Resource Group where the Application Gateway exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:network/getApplicationGateway:getApplicationGateway', __args__, opts=opts, typ=GetApplicationGatewayResult)
    return __ret__.apply(lambda __response__: GetApplicationGatewayResult(
        authentication_certificates=pulumi.get(__response__, 'authentication_certificates'),
        autoscale_configurations=pulumi.get(__response__, 'autoscale_configurations'),
        backend_address_pools=pulumi.get(__response__, 'backend_address_pools'),
        backend_http_settings=pulumi.get(__response__, 'backend_http_settings'),
        custom_error_configurations=pulumi.get(__response__, 'custom_error_configurations'),
        fips_enabled=pulumi.get(__response__, 'fips_enabled'),
        firewall_policy_id=pulumi.get(__response__, 'firewall_policy_id'),
        force_firewall_policy_association=pulumi.get(__response__, 'force_firewall_policy_association'),
        frontend_ip_configurations=pulumi.get(__response__, 'frontend_ip_configurations'),
        frontend_ports=pulumi.get(__response__, 'frontend_ports'),
        gateway_ip_configurations=pulumi.get(__response__, 'gateway_ip_configurations'),
        globals=pulumi.get(__response__, 'globals'),
        http2_enabled=pulumi.get(__response__, 'http2_enabled'),
        http_listeners=pulumi.get(__response__, 'http_listeners'),
        id=pulumi.get(__response__, 'id'),
        identities=pulumi.get(__response__, 'identities'),
        location=pulumi.get(__response__, 'location'),
        name=pulumi.get(__response__, 'name'),
        private_endpoint_connections=pulumi.get(__response__, 'private_endpoint_connections'),
        private_link_configurations=pulumi.get(__response__, 'private_link_configurations'),
        probes=pulumi.get(__response__, 'probes'),
        redirect_configurations=pulumi.get(__response__, 'redirect_configurations'),
        request_routing_rules=pulumi.get(__response__, 'request_routing_rules'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        rewrite_rule_sets=pulumi.get(__response__, 'rewrite_rule_sets'),
        skus=pulumi.get(__response__, 'skus'),
        ssl_certificates=pulumi.get(__response__, 'ssl_certificates'),
        ssl_policies=pulumi.get(__response__, 'ssl_policies'),
        ssl_profiles=pulumi.get(__response__, 'ssl_profiles'),
        tags=pulumi.get(__response__, 'tags'),
        trusted_client_certificates=pulumi.get(__response__, 'trusted_client_certificates'),
        trusted_root_certificates=pulumi.get(__response__, 'trusted_root_certificates'),
        url_path_maps=pulumi.get(__response__, 'url_path_maps'),
        waf_configurations=pulumi.get(__response__, 'waf_configurations'),
        zones=pulumi.get(__response__, 'zones')))
