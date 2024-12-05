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

__all__ = ['PointToPointVpnGatewayArgs', 'PointToPointVpnGateway']

@pulumi.input_type
class PointToPointVpnGatewayArgs:
    def __init__(__self__, *,
                 connection_configurations: pulumi.Input[Sequence[pulumi.Input['PointToPointVpnGatewayConnectionConfigurationArgs']]],
                 resource_group_name: pulumi.Input[str],
                 scale_unit: pulumi.Input[int],
                 virtual_hub_id: pulumi.Input[str],
                 vpn_server_configuration_id: pulumi.Input[str],
                 dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 routing_preference_internet_enabled: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a PointToPointVpnGateway resource.
        :param pulumi.Input[Sequence[pulumi.Input['PointToPointVpnGatewayConnectionConfigurationArgs']]] connection_configurations: A `connection_configuration` block as defined below.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[int] scale_unit: The [Scale Unit](https://docs.microsoft.com/azure/virtual-wan/virtual-wan-faq#what-is-a-virtual-wan-gateway-scale-unit) for this Point-to-Site VPN Gateway.
        :param pulumi.Input[str] virtual_hub_id: The ID of the Virtual Hub where this Point-to-Site VPN Gateway should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] vpn_server_configuration_id: The ID of the VPN Server Configuration which this Point-to-Site VPN Gateway should use. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_servers: A list of IP Addresses of DNS Servers for the Point-to-Site VPN Gateway.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] routing_preference_internet_enabled: Is the Routing Preference for the Public IP Interface of the VPN Gateway enabled? Defaults to `false`. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the Point-to-Site VPN Gateway.
        """
        pulumi.set(__self__, "connection_configurations", connection_configurations)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "scale_unit", scale_unit)
        pulumi.set(__self__, "virtual_hub_id", virtual_hub_id)
        pulumi.set(__self__, "vpn_server_configuration_id", vpn_server_configuration_id)
        if dns_servers is not None:
            pulumi.set(__self__, "dns_servers", dns_servers)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if routing_preference_internet_enabled is not None:
            pulumi.set(__self__, "routing_preference_internet_enabled", routing_preference_internet_enabled)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="connectionConfigurations")
    def connection_configurations(self) -> pulumi.Input[Sequence[pulumi.Input['PointToPointVpnGatewayConnectionConfigurationArgs']]]:
        """
        A `connection_configuration` block as defined below.
        """
        return pulumi.get(self, "connection_configurations")

    @connection_configurations.setter
    def connection_configurations(self, value: pulumi.Input[Sequence[pulumi.Input['PointToPointVpnGatewayConnectionConfigurationArgs']]]):
        pulumi.set(self, "connection_configurations", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which to create the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="scaleUnit")
    def scale_unit(self) -> pulumi.Input[int]:
        """
        The [Scale Unit](https://docs.microsoft.com/azure/virtual-wan/virtual-wan-faq#what-is-a-virtual-wan-gateway-scale-unit) for this Point-to-Site VPN Gateway.
        """
        return pulumi.get(self, "scale_unit")

    @scale_unit.setter
    def scale_unit(self, value: pulumi.Input[int]):
        pulumi.set(self, "scale_unit", value)

    @property
    @pulumi.getter(name="virtualHubId")
    def virtual_hub_id(self) -> pulumi.Input[str]:
        """
        The ID of the Virtual Hub where this Point-to-Site VPN Gateway should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_hub_id")

    @virtual_hub_id.setter
    def virtual_hub_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_hub_id", value)

    @property
    @pulumi.getter(name="vpnServerConfigurationId")
    def vpn_server_configuration_id(self) -> pulumi.Input[str]:
        """
        The ID of the VPN Server Configuration which this Point-to-Site VPN Gateway should use. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "vpn_server_configuration_id")

    @vpn_server_configuration_id.setter
    def vpn_server_configuration_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpn_server_configuration_id", value)

    @property
    @pulumi.getter(name="dnsServers")
    def dns_servers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of IP Addresses of DNS Servers for the Point-to-Site VPN Gateway.
        """
        return pulumi.get(self, "dns_servers")

    @dns_servers.setter
    def dns_servers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dns_servers", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="routingPreferenceInternetEnabled")
    def routing_preference_internet_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the Routing Preference for the Public IP Interface of the VPN Gateway enabled? Defaults to `false`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "routing_preference_internet_enabled")

    @routing_preference_internet_enabled.setter
    def routing_preference_internet_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "routing_preference_internet_enabled", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the Point-to-Site VPN Gateway.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _PointToPointVpnGatewayState:
    def __init__(__self__, *,
                 connection_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['PointToPointVpnGatewayConnectionConfigurationArgs']]]] = None,
                 dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 routing_preference_internet_enabled: Optional[pulumi.Input[bool]] = None,
                 scale_unit: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_hub_id: Optional[pulumi.Input[str]] = None,
                 vpn_server_configuration_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PointToPointVpnGateway resources.
        :param pulumi.Input[Sequence[pulumi.Input['PointToPointVpnGatewayConnectionConfigurationArgs']]] connection_configurations: A `connection_configuration` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_servers: A list of IP Addresses of DNS Servers for the Point-to-Site VPN Gateway.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] routing_preference_internet_enabled: Is the Routing Preference for the Public IP Interface of the VPN Gateway enabled? Defaults to `false`. Changing this forces a new resource to be created.
        :param pulumi.Input[int] scale_unit: The [Scale Unit](https://docs.microsoft.com/azure/virtual-wan/virtual-wan-faq#what-is-a-virtual-wan-gateway-scale-unit) for this Point-to-Site VPN Gateway.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the Point-to-Site VPN Gateway.
        :param pulumi.Input[str] virtual_hub_id: The ID of the Virtual Hub where this Point-to-Site VPN Gateway should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] vpn_server_configuration_id: The ID of the VPN Server Configuration which this Point-to-Site VPN Gateway should use. Changing this forces a new resource to be created.
        """
        if connection_configurations is not None:
            pulumi.set(__self__, "connection_configurations", connection_configurations)
        if dns_servers is not None:
            pulumi.set(__self__, "dns_servers", dns_servers)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if routing_preference_internet_enabled is not None:
            pulumi.set(__self__, "routing_preference_internet_enabled", routing_preference_internet_enabled)
        if scale_unit is not None:
            pulumi.set(__self__, "scale_unit", scale_unit)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if virtual_hub_id is not None:
            pulumi.set(__self__, "virtual_hub_id", virtual_hub_id)
        if vpn_server_configuration_id is not None:
            pulumi.set(__self__, "vpn_server_configuration_id", vpn_server_configuration_id)

    @property
    @pulumi.getter(name="connectionConfigurations")
    def connection_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PointToPointVpnGatewayConnectionConfigurationArgs']]]]:
        """
        A `connection_configuration` block as defined below.
        """
        return pulumi.get(self, "connection_configurations")

    @connection_configurations.setter
    def connection_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PointToPointVpnGatewayConnectionConfigurationArgs']]]]):
        pulumi.set(self, "connection_configurations", value)

    @property
    @pulumi.getter(name="dnsServers")
    def dns_servers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of IP Addresses of DNS Servers for the Point-to-Site VPN Gateway.
        """
        return pulumi.get(self, "dns_servers")

    @dns_servers.setter
    def dns_servers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dns_servers", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which to create the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="routingPreferenceInternetEnabled")
    def routing_preference_internet_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the Routing Preference for the Public IP Interface of the VPN Gateway enabled? Defaults to `false`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "routing_preference_internet_enabled")

    @routing_preference_internet_enabled.setter
    def routing_preference_internet_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "routing_preference_internet_enabled", value)

    @property
    @pulumi.getter(name="scaleUnit")
    def scale_unit(self) -> Optional[pulumi.Input[int]]:
        """
        The [Scale Unit](https://docs.microsoft.com/azure/virtual-wan/virtual-wan-faq#what-is-a-virtual-wan-gateway-scale-unit) for this Point-to-Site VPN Gateway.
        """
        return pulumi.get(self, "scale_unit")

    @scale_unit.setter
    def scale_unit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "scale_unit", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the Point-to-Site VPN Gateway.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="virtualHubId")
    def virtual_hub_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Virtual Hub where this Point-to-Site VPN Gateway should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_hub_id")

    @virtual_hub_id.setter
    def virtual_hub_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_hub_id", value)

    @property
    @pulumi.getter(name="vpnServerConfigurationId")
    def vpn_server_configuration_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPN Server Configuration which this Point-to-Site VPN Gateway should use. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "vpn_server_configuration_id")

    @vpn_server_configuration_id.setter
    def vpn_server_configuration_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpn_server_configuration_id", value)


class PointToPointVpnGateway(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['PointToPointVpnGatewayConnectionConfigurationArgs', 'PointToPointVpnGatewayConnectionConfigurationArgsDict']]]]] = None,
                 dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 routing_preference_internet_enabled: Optional[pulumi.Input[bool]] = None,
                 scale_unit: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_hub_id: Optional[pulumi.Input[str]] = None,
                 vpn_server_configuration_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Point-to-Site VPN Gateway.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_virtual_wan = azure.network.VirtualWan("example",
            name="example-virtualwan",
            resource_group_name=example.name,
            location=example.location)
        example_virtual_hub = azure.network.VirtualHub("example",
            name="example-virtualhub",
            resource_group_name=example.name,
            location=example.location,
            virtual_wan_id=example_virtual_wan.id,
            address_prefix="10.0.0.0/23")
        example_vpn_server_configuration = azure.network.VpnServerConfiguration("example",
            name="example-config",
            resource_group_name=example.name,
            location=example.location,
            vpn_authentication_types=["Certificate"],
            client_root_certificates=[{
                "name": "DigiCert-Federated-ID-Root-CA",
                "public_cert_data": \"\"\"MIIDuzCCAqOgAwIBAgIQCHTZWCM+IlfFIRXIvyKSrjANBgkqhkiG9w0BAQsFADBn
        MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
        d3cuZGlnaWNlcnQuY29tMSYwJAYDVQQDEx1EaWdpQ2VydCBGZWRlcmF0ZWQgSUQg
        Um9vdCBDQTAeFw0xMzAxMTUxMjAwMDBaFw0zMzAxMTUxMjAwMDBaMGcxCzAJBgNV
        BAYTAlVTMRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdp
        Y2VydC5jb20xJjAkBgNVBAMTHURpZ2lDZXJ0IEZlZGVyYXRlZCBJRCBSb290IENB
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvAEB4pcCqnNNOWE6Ur5j
        QPUH+1y1F9KdHTRSza6k5iDlXq1kGS1qAkuKtw9JsiNRrjltmFnzMZRBbX8Tlfl8
        zAhBmb6dDduDGED01kBsTkgywYPxXVTKec0WxYEEF0oMn4wSYNl0lt2eJAKHXjNf
        GTwiibdP8CUR2ghSM2sUTI8Nt1Omfc4SMHhGhYD64uJMbX98THQ/4LMGuYegou+d
        GTiahfHtjn7AboSEknwAMJHCh5RlYZZ6B1O4QbKJ+34Q0eKgnI3X6Vc9u0zf6DH8
        Dk+4zQDYRRTqTnVO3VT8jzqDlCRuNtq6YvryOWN74/dq8LQhUnXHvFyrsdMaE1X2
        DwIDAQABo2MwYTAPBgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBhjAdBgNV
        HQ4EFgQUGRdkFnbGt1EWjKwbUne+5OaZvRYwHwYDVR0jBBgwFoAUGRdkFnbGt1EW
        jKwbUne+5OaZvRYwDQYJKoZIhvcNAQELBQADggEBAHcqsHkrjpESqfuVTRiptJfP
        9JbdtWqRTmOf6uJi2c8YVqI6XlKXsD8C1dUUaaHKLUJzvKiazibVuBwMIT84AyqR
        QELn3e0BtgEymEygMU569b01ZPxoFSnNXc7qDZBDef8WfqAV/sxkTi8L9BkmFYfL
        uGLOhRJOFprPdoDIUBB+tmCl3oDcBy3vnUeOEioz8zAkprcb3GHwHAK+vHmmfgcn
        WsfMLH4JCLa/tRYL+Rw/N3ybCkDp00s0WUZ+AoDywSl0Q/ZEnNY0MsFiw6LyIdbq
        M/s/1JRtO3bDSzD9TazRVzn2oBqzSa8VgIo5C1nOnoAKJTlsClJKvIhnRlaLQqk=
        \"\"\",
            }])
        example_point_to_point_vpn_gateway = azure.network.PointToPointVpnGateway("example",
            name="example-vpn-gateway",
            location=example.location,
            resource_group_name=example.name,
            virtual_hub_id=example_virtual_hub.id,
            vpn_server_configuration_id=example_vpn_server_configuration.id,
            scale_unit=1,
            connection_configurations=[{
                "name": "example-gateway-config",
                "vpn_client_address_pool": {
                    "address_prefixes": ["10.0.2.0/24"],
                },
            }])
        ```

        ## Import

        Point-to-Site VPN Gateway's can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:network/pointToPointVpnGateway:PointToPointVpnGateway example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/p2sVpnGateways/gateway1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['PointToPointVpnGatewayConnectionConfigurationArgs', 'PointToPointVpnGatewayConnectionConfigurationArgsDict']]]] connection_configurations: A `connection_configuration` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_servers: A list of IP Addresses of DNS Servers for the Point-to-Site VPN Gateway.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] routing_preference_internet_enabled: Is the Routing Preference for the Public IP Interface of the VPN Gateway enabled? Defaults to `false`. Changing this forces a new resource to be created.
        :param pulumi.Input[int] scale_unit: The [Scale Unit](https://docs.microsoft.com/azure/virtual-wan/virtual-wan-faq#what-is-a-virtual-wan-gateway-scale-unit) for this Point-to-Site VPN Gateway.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the Point-to-Site VPN Gateway.
        :param pulumi.Input[str] virtual_hub_id: The ID of the Virtual Hub where this Point-to-Site VPN Gateway should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] vpn_server_configuration_id: The ID of the VPN Server Configuration which this Point-to-Site VPN Gateway should use. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PointToPointVpnGatewayArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Point-to-Site VPN Gateway.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_virtual_wan = azure.network.VirtualWan("example",
            name="example-virtualwan",
            resource_group_name=example.name,
            location=example.location)
        example_virtual_hub = azure.network.VirtualHub("example",
            name="example-virtualhub",
            resource_group_name=example.name,
            location=example.location,
            virtual_wan_id=example_virtual_wan.id,
            address_prefix="10.0.0.0/23")
        example_vpn_server_configuration = azure.network.VpnServerConfiguration("example",
            name="example-config",
            resource_group_name=example.name,
            location=example.location,
            vpn_authentication_types=["Certificate"],
            client_root_certificates=[{
                "name": "DigiCert-Federated-ID-Root-CA",
                "public_cert_data": \"\"\"MIIDuzCCAqOgAwIBAgIQCHTZWCM+IlfFIRXIvyKSrjANBgkqhkiG9w0BAQsFADBn
        MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
        d3cuZGlnaWNlcnQuY29tMSYwJAYDVQQDEx1EaWdpQ2VydCBGZWRlcmF0ZWQgSUQg
        Um9vdCBDQTAeFw0xMzAxMTUxMjAwMDBaFw0zMzAxMTUxMjAwMDBaMGcxCzAJBgNV
        BAYTAlVTMRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdp
        Y2VydC5jb20xJjAkBgNVBAMTHURpZ2lDZXJ0IEZlZGVyYXRlZCBJRCBSb290IENB
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvAEB4pcCqnNNOWE6Ur5j
        QPUH+1y1F9KdHTRSza6k5iDlXq1kGS1qAkuKtw9JsiNRrjltmFnzMZRBbX8Tlfl8
        zAhBmb6dDduDGED01kBsTkgywYPxXVTKec0WxYEEF0oMn4wSYNl0lt2eJAKHXjNf
        GTwiibdP8CUR2ghSM2sUTI8Nt1Omfc4SMHhGhYD64uJMbX98THQ/4LMGuYegou+d
        GTiahfHtjn7AboSEknwAMJHCh5RlYZZ6B1O4QbKJ+34Q0eKgnI3X6Vc9u0zf6DH8
        Dk+4zQDYRRTqTnVO3VT8jzqDlCRuNtq6YvryOWN74/dq8LQhUnXHvFyrsdMaE1X2
        DwIDAQABo2MwYTAPBgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBhjAdBgNV
        HQ4EFgQUGRdkFnbGt1EWjKwbUne+5OaZvRYwHwYDVR0jBBgwFoAUGRdkFnbGt1EW
        jKwbUne+5OaZvRYwDQYJKoZIhvcNAQELBQADggEBAHcqsHkrjpESqfuVTRiptJfP
        9JbdtWqRTmOf6uJi2c8YVqI6XlKXsD8C1dUUaaHKLUJzvKiazibVuBwMIT84AyqR
        QELn3e0BtgEymEygMU569b01ZPxoFSnNXc7qDZBDef8WfqAV/sxkTi8L9BkmFYfL
        uGLOhRJOFprPdoDIUBB+tmCl3oDcBy3vnUeOEioz8zAkprcb3GHwHAK+vHmmfgcn
        WsfMLH4JCLa/tRYL+Rw/N3ybCkDp00s0WUZ+AoDywSl0Q/ZEnNY0MsFiw6LyIdbq
        M/s/1JRtO3bDSzD9TazRVzn2oBqzSa8VgIo5C1nOnoAKJTlsClJKvIhnRlaLQqk=
        \"\"\",
            }])
        example_point_to_point_vpn_gateway = azure.network.PointToPointVpnGateway("example",
            name="example-vpn-gateway",
            location=example.location,
            resource_group_name=example.name,
            virtual_hub_id=example_virtual_hub.id,
            vpn_server_configuration_id=example_vpn_server_configuration.id,
            scale_unit=1,
            connection_configurations=[{
                "name": "example-gateway-config",
                "vpn_client_address_pool": {
                    "address_prefixes": ["10.0.2.0/24"],
                },
            }])
        ```

        ## Import

        Point-to-Site VPN Gateway's can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:network/pointToPointVpnGateway:PointToPointVpnGateway example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/p2sVpnGateways/gateway1
        ```

        :param str resource_name: The name of the resource.
        :param PointToPointVpnGatewayArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PointToPointVpnGatewayArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['PointToPointVpnGatewayConnectionConfigurationArgs', 'PointToPointVpnGatewayConnectionConfigurationArgsDict']]]]] = None,
                 dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 routing_preference_internet_enabled: Optional[pulumi.Input[bool]] = None,
                 scale_unit: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_hub_id: Optional[pulumi.Input[str]] = None,
                 vpn_server_configuration_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PointToPointVpnGatewayArgs.__new__(PointToPointVpnGatewayArgs)

            if connection_configurations is None and not opts.urn:
                raise TypeError("Missing required property 'connection_configurations'")
            __props__.__dict__["connection_configurations"] = connection_configurations
            __props__.__dict__["dns_servers"] = dns_servers
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["routing_preference_internet_enabled"] = routing_preference_internet_enabled
            if scale_unit is None and not opts.urn:
                raise TypeError("Missing required property 'scale_unit'")
            __props__.__dict__["scale_unit"] = scale_unit
            __props__.__dict__["tags"] = tags
            if virtual_hub_id is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_hub_id'")
            __props__.__dict__["virtual_hub_id"] = virtual_hub_id
            if vpn_server_configuration_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpn_server_configuration_id'")
            __props__.__dict__["vpn_server_configuration_id"] = vpn_server_configuration_id
        super(PointToPointVpnGateway, __self__).__init__(
            'azure:network/pointToPointVpnGateway:PointToPointVpnGateway',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            connection_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['PointToPointVpnGatewayConnectionConfigurationArgs', 'PointToPointVpnGatewayConnectionConfigurationArgsDict']]]]] = None,
            dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            routing_preference_internet_enabled: Optional[pulumi.Input[bool]] = None,
            scale_unit: Optional[pulumi.Input[int]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            virtual_hub_id: Optional[pulumi.Input[str]] = None,
            vpn_server_configuration_id: Optional[pulumi.Input[str]] = None) -> 'PointToPointVpnGateway':
        """
        Get an existing PointToPointVpnGateway resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['PointToPointVpnGatewayConnectionConfigurationArgs', 'PointToPointVpnGatewayConnectionConfigurationArgsDict']]]] connection_configurations: A `connection_configuration` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_servers: A list of IP Addresses of DNS Servers for the Point-to-Site VPN Gateway.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] routing_preference_internet_enabled: Is the Routing Preference for the Public IP Interface of the VPN Gateway enabled? Defaults to `false`. Changing this forces a new resource to be created.
        :param pulumi.Input[int] scale_unit: The [Scale Unit](https://docs.microsoft.com/azure/virtual-wan/virtual-wan-faq#what-is-a-virtual-wan-gateway-scale-unit) for this Point-to-Site VPN Gateway.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the Point-to-Site VPN Gateway.
        :param pulumi.Input[str] virtual_hub_id: The ID of the Virtual Hub where this Point-to-Site VPN Gateway should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] vpn_server_configuration_id: The ID of the VPN Server Configuration which this Point-to-Site VPN Gateway should use. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PointToPointVpnGatewayState.__new__(_PointToPointVpnGatewayState)

        __props__.__dict__["connection_configurations"] = connection_configurations
        __props__.__dict__["dns_servers"] = dns_servers
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["routing_preference_internet_enabled"] = routing_preference_internet_enabled
        __props__.__dict__["scale_unit"] = scale_unit
        __props__.__dict__["tags"] = tags
        __props__.__dict__["virtual_hub_id"] = virtual_hub_id
        __props__.__dict__["vpn_server_configuration_id"] = vpn_server_configuration_id
        return PointToPointVpnGateway(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectionConfigurations")
    def connection_configurations(self) -> pulumi.Output[Sequence['outputs.PointToPointVpnGatewayConnectionConfiguration']]:
        """
        A `connection_configuration` block as defined below.
        """
        return pulumi.get(self, "connection_configurations")

    @property
    @pulumi.getter(name="dnsServers")
    def dns_servers(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of IP Addresses of DNS Servers for the Point-to-Site VPN Gateway.
        """
        return pulumi.get(self, "dns_servers")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which to create the Point-to-Site VPN Gateway. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="routingPreferenceInternetEnabled")
    def routing_preference_internet_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Is the Routing Preference for the Public IP Interface of the VPN Gateway enabled? Defaults to `false`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "routing_preference_internet_enabled")

    @property
    @pulumi.getter(name="scaleUnit")
    def scale_unit(self) -> pulumi.Output[int]:
        """
        The [Scale Unit](https://docs.microsoft.com/azure/virtual-wan/virtual-wan-faq#what-is-a-virtual-wan-gateway-scale-unit) for this Point-to-Site VPN Gateway.
        """
        return pulumi.get(self, "scale_unit")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the Point-to-Site VPN Gateway.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="virtualHubId")
    def virtual_hub_id(self) -> pulumi.Output[str]:
        """
        The ID of the Virtual Hub where this Point-to-Site VPN Gateway should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_hub_id")

    @property
    @pulumi.getter(name="vpnServerConfigurationId")
    def vpn_server_configuration_id(self) -> pulumi.Output[str]:
        """
        The ID of the VPN Server Configuration which this Point-to-Site VPN Gateway should use. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "vpn_server_configuration_id")

