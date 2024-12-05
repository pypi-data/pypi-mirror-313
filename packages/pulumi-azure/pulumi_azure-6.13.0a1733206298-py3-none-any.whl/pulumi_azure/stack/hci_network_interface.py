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

__all__ = ['HciNetworkInterfaceArgs', 'HciNetworkInterface']

@pulumi.input_type
class HciNetworkInterfaceArgs:
    def __init__(__self__, *,
                 custom_location_id: pulumi.Input[str],
                 ip_configuration: pulumi.Input['HciNetworkInterfaceIpConfigurationArgs'],
                 resource_group_name: pulumi.Input[str],
                 dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mac_address: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a HciNetworkInterface resource.
        :param pulumi.Input[str] custom_location_id: The ID of the Custom Location where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        :param pulumi.Input['HciNetworkInterfaceIpConfigurationArgs'] ip_configuration: An `ip_configuration` block as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_servers: A list of IPv4 addresses of DNS servers available to VMs deployed in the Network Interface. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: The Azure Region where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] mac_address: The MAC address of the Network Interface. Changing this forces a new resource to be created.
               
               > **Note:** If `mac_address` is not specified, it will be assigned by the server. If you experience a diff you may need to add this to `ignore_changes`.
        :param pulumi.Input[str] name: The name which should be used for this Azure Stack HCI Network Interface. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Azure Stack HCI Network Interface.
        """
        pulumi.set(__self__, "custom_location_id", custom_location_id)
        pulumi.set(__self__, "ip_configuration", ip_configuration)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if dns_servers is not None:
            pulumi.set(__self__, "dns_servers", dns_servers)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if mac_address is not None:
            pulumi.set(__self__, "mac_address", mac_address)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="customLocationId")
    def custom_location_id(self) -> pulumi.Input[str]:
        """
        The ID of the Custom Location where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "custom_location_id")

    @custom_location_id.setter
    def custom_location_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "custom_location_id", value)

    @property
    @pulumi.getter(name="ipConfiguration")
    def ip_configuration(self) -> pulumi.Input['HciNetworkInterfaceIpConfigurationArgs']:
        """
        An `ip_configuration` block as defined below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "ip_configuration")

    @ip_configuration.setter
    def ip_configuration(self, value: pulumi.Input['HciNetworkInterfaceIpConfigurationArgs']):
        pulumi.set(self, "ip_configuration", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="dnsServers")
    def dns_servers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of IPv4 addresses of DNS servers available to VMs deployed in the Network Interface. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "dns_servers")

    @dns_servers.setter
    def dns_servers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dns_servers", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="macAddress")
    def mac_address(self) -> Optional[pulumi.Input[str]]:
        """
        The MAC address of the Network Interface. Changing this forces a new resource to be created.

        > **Note:** If `mac_address` is not specified, it will be assigned by the server. If you experience a diff you may need to add this to `ignore_changes`.
        """
        return pulumi.get(self, "mac_address")

    @mac_address.setter
    def mac_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mac_address", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Azure Stack HCI Network Interface. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Azure Stack HCI Network Interface.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _HciNetworkInterfaceState:
    def __init__(__self__, *,
                 custom_location_id: Optional[pulumi.Input[str]] = None,
                 dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ip_configuration: Optional[pulumi.Input['HciNetworkInterfaceIpConfigurationArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mac_address: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering HciNetworkInterface resources.
        :param pulumi.Input[str] custom_location_id: The ID of the Custom Location where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_servers: A list of IPv4 addresses of DNS servers available to VMs deployed in the Network Interface. Changing this forces a new resource to be created.
        :param pulumi.Input['HciNetworkInterfaceIpConfigurationArgs'] ip_configuration: An `ip_configuration` block as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: The Azure Region where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] mac_address: The MAC address of the Network Interface. Changing this forces a new resource to be created.
               
               > **Note:** If `mac_address` is not specified, it will be assigned by the server. If you experience a diff you may need to add this to `ignore_changes`.
        :param pulumi.Input[str] name: The name which should be used for this Azure Stack HCI Network Interface. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Azure Stack HCI Network Interface.
        """
        if custom_location_id is not None:
            pulumi.set(__self__, "custom_location_id", custom_location_id)
        if dns_servers is not None:
            pulumi.set(__self__, "dns_servers", dns_servers)
        if ip_configuration is not None:
            pulumi.set(__self__, "ip_configuration", ip_configuration)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if mac_address is not None:
            pulumi.set(__self__, "mac_address", mac_address)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="customLocationId")
    def custom_location_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Custom Location where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "custom_location_id")

    @custom_location_id.setter
    def custom_location_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_location_id", value)

    @property
    @pulumi.getter(name="dnsServers")
    def dns_servers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of IPv4 addresses of DNS servers available to VMs deployed in the Network Interface. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "dns_servers")

    @dns_servers.setter
    def dns_servers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dns_servers", value)

    @property
    @pulumi.getter(name="ipConfiguration")
    def ip_configuration(self) -> Optional[pulumi.Input['HciNetworkInterfaceIpConfigurationArgs']]:
        """
        An `ip_configuration` block as defined below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "ip_configuration")

    @ip_configuration.setter
    def ip_configuration(self, value: Optional[pulumi.Input['HciNetworkInterfaceIpConfigurationArgs']]):
        pulumi.set(self, "ip_configuration", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="macAddress")
    def mac_address(self) -> Optional[pulumi.Input[str]]:
        """
        The MAC address of the Network Interface. Changing this forces a new resource to be created.

        > **Note:** If `mac_address` is not specified, it will be assigned by the server. If you experience a diff you may need to add this to `ignore_changes`.
        """
        return pulumi.get(self, "mac_address")

    @mac_address.setter
    def mac_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mac_address", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Azure Stack HCI Network Interface. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Azure Stack HCI Network Interface.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class HciNetworkInterface(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 custom_location_id: Optional[pulumi.Input[str]] = None,
                 dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ip_configuration: Optional[pulumi.Input[Union['HciNetworkInterfaceIpConfigurationArgs', 'HciNetworkInterfaceIpConfigurationArgsDict']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mac_address: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages an Azure Stack HCI Network Interface.

        ## Import

        Azure Stack HCI Network Interfaces can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:stack/hciNetworkInterface:HciNetworkInterface example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.AzureStackHCI/networkInterfaces/ni1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] custom_location_id: The ID of the Custom Location where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_servers: A list of IPv4 addresses of DNS servers available to VMs deployed in the Network Interface. Changing this forces a new resource to be created.
        :param pulumi.Input[Union['HciNetworkInterfaceIpConfigurationArgs', 'HciNetworkInterfaceIpConfigurationArgsDict']] ip_configuration: An `ip_configuration` block as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: The Azure Region where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] mac_address: The MAC address of the Network Interface. Changing this forces a new resource to be created.
               
               > **Note:** If `mac_address` is not specified, it will be assigned by the server. If you experience a diff you may need to add this to `ignore_changes`.
        :param pulumi.Input[str] name: The name which should be used for this Azure Stack HCI Network Interface. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Azure Stack HCI Network Interface.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: HciNetworkInterfaceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an Azure Stack HCI Network Interface.

        ## Import

        Azure Stack HCI Network Interfaces can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:stack/hciNetworkInterface:HciNetworkInterface example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.AzureStackHCI/networkInterfaces/ni1
        ```

        :param str resource_name: The name of the resource.
        :param HciNetworkInterfaceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(HciNetworkInterfaceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 custom_location_id: Optional[pulumi.Input[str]] = None,
                 dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ip_configuration: Optional[pulumi.Input[Union['HciNetworkInterfaceIpConfigurationArgs', 'HciNetworkInterfaceIpConfigurationArgsDict']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mac_address: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = HciNetworkInterfaceArgs.__new__(HciNetworkInterfaceArgs)

            if custom_location_id is None and not opts.urn:
                raise TypeError("Missing required property 'custom_location_id'")
            __props__.__dict__["custom_location_id"] = custom_location_id
            __props__.__dict__["dns_servers"] = dns_servers
            if ip_configuration is None and not opts.urn:
                raise TypeError("Missing required property 'ip_configuration'")
            __props__.__dict__["ip_configuration"] = ip_configuration
            __props__.__dict__["location"] = location
            __props__.__dict__["mac_address"] = mac_address
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
        super(HciNetworkInterface, __self__).__init__(
            'azure:stack/hciNetworkInterface:HciNetworkInterface',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            custom_location_id: Optional[pulumi.Input[str]] = None,
            dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            ip_configuration: Optional[pulumi.Input[Union['HciNetworkInterfaceIpConfigurationArgs', 'HciNetworkInterfaceIpConfigurationArgsDict']]] = None,
            location: Optional[pulumi.Input[str]] = None,
            mac_address: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'HciNetworkInterface':
        """
        Get an existing HciNetworkInterface resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] custom_location_id: The ID of the Custom Location where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_servers: A list of IPv4 addresses of DNS servers available to VMs deployed in the Network Interface. Changing this forces a new resource to be created.
        :param pulumi.Input[Union['HciNetworkInterfaceIpConfigurationArgs', 'HciNetworkInterfaceIpConfigurationArgsDict']] ip_configuration: An `ip_configuration` block as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: The Azure Region where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] mac_address: The MAC address of the Network Interface. Changing this forces a new resource to be created.
               
               > **Note:** If `mac_address` is not specified, it will be assigned by the server. If you experience a diff you may need to add this to `ignore_changes`.
        :param pulumi.Input[str] name: The name which should be used for this Azure Stack HCI Network Interface. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Azure Stack HCI Network Interface.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _HciNetworkInterfaceState.__new__(_HciNetworkInterfaceState)

        __props__.__dict__["custom_location_id"] = custom_location_id
        __props__.__dict__["dns_servers"] = dns_servers
        __props__.__dict__["ip_configuration"] = ip_configuration
        __props__.__dict__["location"] = location
        __props__.__dict__["mac_address"] = mac_address
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["tags"] = tags
        return HciNetworkInterface(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="customLocationId")
    def custom_location_id(self) -> pulumi.Output[str]:
        """
        The ID of the Custom Location where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "custom_location_id")

    @property
    @pulumi.getter(name="dnsServers")
    def dns_servers(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of IPv4 addresses of DNS servers available to VMs deployed in the Network Interface. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "dns_servers")

    @property
    @pulumi.getter(name="ipConfiguration")
    def ip_configuration(self) -> pulumi.Output['outputs.HciNetworkInterfaceIpConfiguration']:
        """
        An `ip_configuration` block as defined below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "ip_configuration")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure Region where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="macAddress")
    def mac_address(self) -> pulumi.Output[Optional[str]]:
        """
        The MAC address of the Network Interface. Changing this forces a new resource to be created.

        > **Note:** If `mac_address` is not specified, it will be assigned by the server. If you experience a diff you may need to add this to `ignore_changes`.
        """
        return pulumi.get(self, "mac_address")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Azure Stack HCI Network Interface. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Azure Stack HCI Network Interface should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to the Azure Stack HCI Network Interface.
        """
        return pulumi.get(self, "tags")

