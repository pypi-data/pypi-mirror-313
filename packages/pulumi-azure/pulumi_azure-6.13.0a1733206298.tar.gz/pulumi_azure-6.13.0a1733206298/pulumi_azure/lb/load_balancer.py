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

__all__ = ['LoadBalancerArgs', 'LoadBalancer']

@pulumi.input_type
class LoadBalancerArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 edge_zone: Optional[pulumi.Input[str]] = None,
                 frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerFrontendIpConfigurationArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[str]] = None,
                 sku_tier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a LoadBalancer resource.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which to create the Load Balancer. Changing this forces a new resource to be created.
        :param pulumi.Input[str] edge_zone: Specifies the Edge Zone within the Azure Region where this Load Balancer should exist. Changing this forces a new Load Balancer to be created.
        :param pulumi.Input[Sequence[pulumi.Input['LoadBalancerFrontendIpConfigurationArgs']]] frontend_ip_configurations: One or more `frontend_ip_configuration` blocks as documented below.
        :param pulumi.Input[str] location: Specifies the supported Azure Region where the Load Balancer should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Load Balancer. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sku: The SKU of the Azure Load Balancer. Accepted values are `Basic`, `Standard` and `Gateway`. Defaults to `Standard`. Changing this forces a new resource to be created.
               
               > **NOTE:** The `Microsoft.Network/AllowGatewayLoadBalancer` feature is required to be registered in order to use the `Gateway` SKU. The feature can only be registered by the Azure service team, please submit an [Azure support ticket](https://azure.microsoft.com/en-us/support/create-ticket/) for that.
        :param pulumi.Input[str] sku_tier: `sku_tier` - (Optional) The SKU tier of this Load Balancer. Possible values are `Global` and `Regional`. Defaults to `Regional`. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if edge_zone is not None:
            pulumi.set(__self__, "edge_zone", edge_zone)
        if frontend_ip_configurations is not None:
            pulumi.set(__self__, "frontend_ip_configurations", frontend_ip_configurations)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if sku_tier is not None:
            pulumi.set(__self__, "sku_tier", sku_tier)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group in which to create the Load Balancer. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="edgeZone")
    def edge_zone(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Edge Zone within the Azure Region where this Load Balancer should exist. Changing this forces a new Load Balancer to be created.
        """
        return pulumi.get(self, "edge_zone")

    @edge_zone.setter
    def edge_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "edge_zone", value)

    @property
    @pulumi.getter(name="frontendIpConfigurations")
    def frontend_ip_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerFrontendIpConfigurationArgs']]]]:
        """
        One or more `frontend_ip_configuration` blocks as documented below.
        """
        return pulumi.get(self, "frontend_ip_configurations")

    @frontend_ip_configurations.setter
    def frontend_ip_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerFrontendIpConfigurationArgs']]]]):
        pulumi.set(self, "frontend_ip_configurations", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure Region where the Load Balancer should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Load Balancer. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input[str]]:
        """
        The SKU of the Azure Load Balancer. Accepted values are `Basic`, `Standard` and `Gateway`. Defaults to `Standard`. Changing this forces a new resource to be created.

        > **NOTE:** The `Microsoft.Network/AllowGatewayLoadBalancer` feature is required to be registered in order to use the `Gateway` SKU. The feature can only be registered by the Azure service team, please submit an [Azure support ticket](https://azure.microsoft.com/en-us/support/create-ticket/) for that.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="skuTier")
    def sku_tier(self) -> Optional[pulumi.Input[str]]:
        """
        `sku_tier` - (Optional) The SKU tier of this Load Balancer. Possible values are `Global` and `Regional`. Defaults to `Regional`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "sku_tier")

    @sku_tier.setter
    def sku_tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku_tier", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _LoadBalancerState:
    def __init__(__self__, *,
                 edge_zone: Optional[pulumi.Input[str]] = None,
                 frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerFrontendIpConfigurationArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_ip_address: Optional[pulumi.Input[str]] = None,
                 private_ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[str]] = None,
                 sku_tier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering LoadBalancer resources.
        :param pulumi.Input[str] edge_zone: Specifies the Edge Zone within the Azure Region where this Load Balancer should exist. Changing this forces a new Load Balancer to be created.
        :param pulumi.Input[Sequence[pulumi.Input['LoadBalancerFrontendIpConfigurationArgs']]] frontend_ip_configurations: One or more `frontend_ip_configuration` blocks as documented below.
        :param pulumi.Input[str] location: Specifies the supported Azure Region where the Load Balancer should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Load Balancer. Changing this forces a new resource to be created.
        :param pulumi.Input[str] private_ip_address: Private IP Address to assign to the Load Balancer.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] private_ip_addresses: The list of private IP address assigned to the load balancer in `frontend_ip_configuration` blocks, if any.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which to create the Load Balancer. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sku: The SKU of the Azure Load Balancer. Accepted values are `Basic`, `Standard` and `Gateway`. Defaults to `Standard`. Changing this forces a new resource to be created.
               
               > **NOTE:** The `Microsoft.Network/AllowGatewayLoadBalancer` feature is required to be registered in order to use the `Gateway` SKU. The feature can only be registered by the Azure service team, please submit an [Azure support ticket](https://azure.microsoft.com/en-us/support/create-ticket/) for that.
        :param pulumi.Input[str] sku_tier: `sku_tier` - (Optional) The SKU tier of this Load Balancer. Possible values are `Global` and `Regional`. Defaults to `Regional`. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        if edge_zone is not None:
            pulumi.set(__self__, "edge_zone", edge_zone)
        if frontend_ip_configurations is not None:
            pulumi.set(__self__, "frontend_ip_configurations", frontend_ip_configurations)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)
        if private_ip_addresses is not None:
            pulumi.set(__self__, "private_ip_addresses", private_ip_addresses)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if sku_tier is not None:
            pulumi.set(__self__, "sku_tier", sku_tier)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="edgeZone")
    def edge_zone(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Edge Zone within the Azure Region where this Load Balancer should exist. Changing this forces a new Load Balancer to be created.
        """
        return pulumi.get(self, "edge_zone")

    @edge_zone.setter
    def edge_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "edge_zone", value)

    @property
    @pulumi.getter(name="frontendIpConfigurations")
    def frontend_ip_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerFrontendIpConfigurationArgs']]]]:
        """
        One or more `frontend_ip_configuration` blocks as documented below.
        """
        return pulumi.get(self, "frontend_ip_configurations")

    @frontend_ip_configurations.setter
    def frontend_ip_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerFrontendIpConfigurationArgs']]]]):
        pulumi.set(self, "frontend_ip_configurations", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure Region where the Load Balancer should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Load Balancer. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        Private IP Address to assign to the Load Balancer.
        """
        return pulumi.get(self, "private_ip_address")

    @private_ip_address.setter
    def private_ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_ip_address", value)

    @property
    @pulumi.getter(name="privateIpAddresses")
    def private_ip_addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of private IP address assigned to the load balancer in `frontend_ip_configuration` blocks, if any.
        """
        return pulumi.get(self, "private_ip_addresses")

    @private_ip_addresses.setter
    def private_ip_addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "private_ip_addresses", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group in which to create the Load Balancer. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input[str]]:
        """
        The SKU of the Azure Load Balancer. Accepted values are `Basic`, `Standard` and `Gateway`. Defaults to `Standard`. Changing this forces a new resource to be created.

        > **NOTE:** The `Microsoft.Network/AllowGatewayLoadBalancer` feature is required to be registered in order to use the `Gateway` SKU. The feature can only be registered by the Azure service team, please submit an [Azure support ticket](https://azure.microsoft.com/en-us/support/create-ticket/) for that.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="skuTier")
    def sku_tier(self) -> Optional[pulumi.Input[str]]:
        """
        `sku_tier` - (Optional) The SKU tier of this Load Balancer. Possible values are `Global` and `Regional`. Defaults to `Regional`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "sku_tier")

    @sku_tier.setter
    def sku_tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku_tier", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class LoadBalancer(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 edge_zone: Optional[pulumi.Input[str]] = None,
                 frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['LoadBalancerFrontendIpConfigurationArgs', 'LoadBalancerFrontendIpConfigurationArgsDict']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[str]] = None,
                 sku_tier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a Load Balancer Resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="LoadBalancerRG",
            location="West Europe")
        example_public_ip = azure.network.PublicIp("example",
            name="PublicIPForLB",
            location=example.location,
            resource_group_name=example.name,
            allocation_method="Static")
        example_load_balancer = azure.lb.LoadBalancer("example",
            name="TestLoadBalancer",
            location=example.location,
            resource_group_name=example.name,
            frontend_ip_configurations=[{
                "name": "PublicIPAddress",
                "public_ip_address_id": example_public_ip.id,
            }])
        ```

        ## Import

        Load Balancers can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:lb/loadBalancer:LoadBalancer example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/loadBalancers/lb1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] edge_zone: Specifies the Edge Zone within the Azure Region where this Load Balancer should exist. Changing this forces a new Load Balancer to be created.
        :param pulumi.Input[Sequence[pulumi.Input[Union['LoadBalancerFrontendIpConfigurationArgs', 'LoadBalancerFrontendIpConfigurationArgsDict']]]] frontend_ip_configurations: One or more `frontend_ip_configuration` blocks as documented below.
        :param pulumi.Input[str] location: Specifies the supported Azure Region where the Load Balancer should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Load Balancer. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which to create the Load Balancer. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sku: The SKU of the Azure Load Balancer. Accepted values are `Basic`, `Standard` and `Gateway`. Defaults to `Standard`. Changing this forces a new resource to be created.
               
               > **NOTE:** The `Microsoft.Network/AllowGatewayLoadBalancer` feature is required to be registered in order to use the `Gateway` SKU. The feature can only be registered by the Azure service team, please submit an [Azure support ticket](https://azure.microsoft.com/en-us/support/create-ticket/) for that.
        :param pulumi.Input[str] sku_tier: `sku_tier` - (Optional) The SKU tier of this Load Balancer. Possible values are `Global` and `Regional`. Defaults to `Regional`. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LoadBalancerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Load Balancer Resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="LoadBalancerRG",
            location="West Europe")
        example_public_ip = azure.network.PublicIp("example",
            name="PublicIPForLB",
            location=example.location,
            resource_group_name=example.name,
            allocation_method="Static")
        example_load_balancer = azure.lb.LoadBalancer("example",
            name="TestLoadBalancer",
            location=example.location,
            resource_group_name=example.name,
            frontend_ip_configurations=[{
                "name": "PublicIPAddress",
                "public_ip_address_id": example_public_ip.id,
            }])
        ```

        ## Import

        Load Balancers can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:lb/loadBalancer:LoadBalancer example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Network/loadBalancers/lb1
        ```

        :param str resource_name: The name of the resource.
        :param LoadBalancerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LoadBalancerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 edge_zone: Optional[pulumi.Input[str]] = None,
                 frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['LoadBalancerFrontendIpConfigurationArgs', 'LoadBalancerFrontendIpConfigurationArgsDict']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[str]] = None,
                 sku_tier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LoadBalancerArgs.__new__(LoadBalancerArgs)

            __props__.__dict__["edge_zone"] = edge_zone
            __props__.__dict__["frontend_ip_configurations"] = frontend_ip_configurations
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["sku_tier"] = sku_tier
            __props__.__dict__["tags"] = tags
            __props__.__dict__["private_ip_address"] = None
            __props__.__dict__["private_ip_addresses"] = None
        super(LoadBalancer, __self__).__init__(
            'azure:lb/loadBalancer:LoadBalancer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            edge_zone: Optional[pulumi.Input[str]] = None,
            frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['LoadBalancerFrontendIpConfigurationArgs', 'LoadBalancerFrontendIpConfigurationArgsDict']]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            private_ip_address: Optional[pulumi.Input[str]] = None,
            private_ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            sku: Optional[pulumi.Input[str]] = None,
            sku_tier: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'LoadBalancer':
        """
        Get an existing LoadBalancer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] edge_zone: Specifies the Edge Zone within the Azure Region where this Load Balancer should exist. Changing this forces a new Load Balancer to be created.
        :param pulumi.Input[Sequence[pulumi.Input[Union['LoadBalancerFrontendIpConfigurationArgs', 'LoadBalancerFrontendIpConfigurationArgsDict']]]] frontend_ip_configurations: One or more `frontend_ip_configuration` blocks as documented below.
        :param pulumi.Input[str] location: Specifies the supported Azure Region where the Load Balancer should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Load Balancer. Changing this forces a new resource to be created.
        :param pulumi.Input[str] private_ip_address: Private IP Address to assign to the Load Balancer.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] private_ip_addresses: The list of private IP address assigned to the load balancer in `frontend_ip_configuration` blocks, if any.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which to create the Load Balancer. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sku: The SKU of the Azure Load Balancer. Accepted values are `Basic`, `Standard` and `Gateway`. Defaults to `Standard`. Changing this forces a new resource to be created.
               
               > **NOTE:** The `Microsoft.Network/AllowGatewayLoadBalancer` feature is required to be registered in order to use the `Gateway` SKU. The feature can only be registered by the Azure service team, please submit an [Azure support ticket](https://azure.microsoft.com/en-us/support/create-ticket/) for that.
        :param pulumi.Input[str] sku_tier: `sku_tier` - (Optional) The SKU tier of this Load Balancer. Possible values are `Global` and `Regional`. Defaults to `Regional`. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LoadBalancerState.__new__(_LoadBalancerState)

        __props__.__dict__["edge_zone"] = edge_zone
        __props__.__dict__["frontend_ip_configurations"] = frontend_ip_configurations
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["private_ip_address"] = private_ip_address
        __props__.__dict__["private_ip_addresses"] = private_ip_addresses
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["sku"] = sku
        __props__.__dict__["sku_tier"] = sku_tier
        __props__.__dict__["tags"] = tags
        return LoadBalancer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="edgeZone")
    def edge_zone(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the Edge Zone within the Azure Region where this Load Balancer should exist. Changing this forces a new Load Balancer to be created.
        """
        return pulumi.get(self, "edge_zone")

    @property
    @pulumi.getter(name="frontendIpConfigurations")
    def frontend_ip_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.LoadBalancerFrontendIpConfiguration']]]:
        """
        One or more `frontend_ip_configuration` blocks as documented below.
        """
        return pulumi.get(self, "frontend_ip_configurations")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the supported Azure Region where the Load Balancer should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Load Balancer. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> pulumi.Output[str]:
        """
        Private IP Address to assign to the Load Balancer.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="privateIpAddresses")
    def private_ip_addresses(self) -> pulumi.Output[Sequence[str]]:
        """
        The list of private IP address assigned to the load balancer in `frontend_ip_configuration` blocks, if any.
        """
        return pulumi.get(self, "private_ip_addresses")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group in which to create the Load Balancer. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional[str]]:
        """
        The SKU of the Azure Load Balancer. Accepted values are `Basic`, `Standard` and `Gateway`. Defaults to `Standard`. Changing this forces a new resource to be created.

        > **NOTE:** The `Microsoft.Network/AllowGatewayLoadBalancer` feature is required to be registered in order to use the `Gateway` SKU. The feature can only be registered by the Azure service team, please submit an [Azure support ticket](https://azure.microsoft.com/en-us/support/create-ticket/) for that.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="skuTier")
    def sku_tier(self) -> pulumi.Output[Optional[str]]:
        """
        `sku_tier` - (Optional) The SKU tier of this Load Balancer. Possible values are `Global` and `Regional`. Defaults to `Regional`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "sku_tier")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

