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

__all__ = ['RouteMapArgs', 'RouteMap']

@pulumi.input_type
class RouteMapArgs:
    def __init__(__self__, *,
                 virtual_hub_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input['RouteMapRuleArgs']]]] = None):
        """
        The set of arguments for constructing a RouteMap resource.
        :param pulumi.Input[str] virtual_hub_id: The resource ID of the Virtual Hub. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name which should be used for this Route Map. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['RouteMapRuleArgs']]] rules: A `rule` block as defined below.
        """
        pulumi.set(__self__, "virtual_hub_id", virtual_hub_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)

    @property
    @pulumi.getter(name="virtualHubId")
    def virtual_hub_id(self) -> pulumi.Input[str]:
        """
        The resource ID of the Virtual Hub. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_hub_id")

    @virtual_hub_id.setter
    def virtual_hub_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_hub_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Route Map. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RouteMapRuleArgs']]]]:
        """
        A `rule` block as defined below.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RouteMapRuleArgs']]]]):
        pulumi.set(self, "rules", value)


@pulumi.input_type
class _RouteMapState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input['RouteMapRuleArgs']]]] = None,
                 virtual_hub_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RouteMap resources.
        :param pulumi.Input[str] name: The name which should be used for this Route Map. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['RouteMapRuleArgs']]] rules: A `rule` block as defined below.
        :param pulumi.Input[str] virtual_hub_id: The resource ID of the Virtual Hub. Changing this forces a new resource to be created.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)
        if virtual_hub_id is not None:
            pulumi.set(__self__, "virtual_hub_id", virtual_hub_id)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Route Map. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RouteMapRuleArgs']]]]:
        """
        A `rule` block as defined below.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RouteMapRuleArgs']]]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter(name="virtualHubId")
    def virtual_hub_id(self) -> Optional[pulumi.Input[str]]:
        """
        The resource ID of the Virtual Hub. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_hub_id")

    @virtual_hub_id.setter
    def virtual_hub_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_hub_id", value)


class RouteMap(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[Union['RouteMapRuleArgs', 'RouteMapRuleArgsDict']]]]] = None,
                 virtual_hub_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Route Map.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_virtual_wan = azure.network.VirtualWan("example",
            name="example-vwan",
            resource_group_name=example.name,
            location=example.location)
        example_virtual_hub = azure.network.VirtualHub("example",
            name="example-vhub",
            resource_group_name=example.name,
            location=example.location,
            virtual_wan_id=example_virtual_wan.id,
            address_prefix="10.0.1.0/24")
        example_route_map = azure.network.RouteMap("example",
            name="example-rm",
            virtual_hub_id=example_virtual_hub.id,
            rules=[{
                "name": "rule1",
                "next_step_if_matched": "Continue",
                "actions": [{
                    "type": "Add",
                    "parameters": [{
                        "as_paths": ["22334"],
                    }],
                }],
                "match_criterions": [{
                    "match_condition": "Contains",
                    "route_prefixes": ["10.0.0.0/8"],
                }],
            }])
        ```

        ## Import

        Route Maps can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:network/routeMap:RouteMap example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourceGroup1/providers/Microsoft.Network/virtualHubs/virtualHub1/routeMaps/routeMap1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name which should be used for this Route Map. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[Union['RouteMapRuleArgs', 'RouteMapRuleArgsDict']]]] rules: A `rule` block as defined below.
        :param pulumi.Input[str] virtual_hub_id: The resource ID of the Virtual Hub. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RouteMapArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Route Map.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_virtual_wan = azure.network.VirtualWan("example",
            name="example-vwan",
            resource_group_name=example.name,
            location=example.location)
        example_virtual_hub = azure.network.VirtualHub("example",
            name="example-vhub",
            resource_group_name=example.name,
            location=example.location,
            virtual_wan_id=example_virtual_wan.id,
            address_prefix="10.0.1.0/24")
        example_route_map = azure.network.RouteMap("example",
            name="example-rm",
            virtual_hub_id=example_virtual_hub.id,
            rules=[{
                "name": "rule1",
                "next_step_if_matched": "Continue",
                "actions": [{
                    "type": "Add",
                    "parameters": [{
                        "as_paths": ["22334"],
                    }],
                }],
                "match_criterions": [{
                    "match_condition": "Contains",
                    "route_prefixes": ["10.0.0.0/8"],
                }],
            }])
        ```

        ## Import

        Route Maps can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:network/routeMap:RouteMap example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourceGroup1/providers/Microsoft.Network/virtualHubs/virtualHub1/routeMaps/routeMap1
        ```

        :param str resource_name: The name of the resource.
        :param RouteMapArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RouteMapArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[Union['RouteMapRuleArgs', 'RouteMapRuleArgsDict']]]]] = None,
                 virtual_hub_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RouteMapArgs.__new__(RouteMapArgs)

            __props__.__dict__["name"] = name
            __props__.__dict__["rules"] = rules
            if virtual_hub_id is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_hub_id'")
            __props__.__dict__["virtual_hub_id"] = virtual_hub_id
        super(RouteMap, __self__).__init__(
            'azure:network/routeMap:RouteMap',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            rules: Optional[pulumi.Input[Sequence[pulumi.Input[Union['RouteMapRuleArgs', 'RouteMapRuleArgsDict']]]]] = None,
            virtual_hub_id: Optional[pulumi.Input[str]] = None) -> 'RouteMap':
        """
        Get an existing RouteMap resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name which should be used for this Route Map. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[Union['RouteMapRuleArgs', 'RouteMapRuleArgsDict']]]] rules: A `rule` block as defined below.
        :param pulumi.Input[str] virtual_hub_id: The resource ID of the Virtual Hub. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RouteMapState.__new__(_RouteMapState)

        __props__.__dict__["name"] = name
        __props__.__dict__["rules"] = rules
        __props__.__dict__["virtual_hub_id"] = virtual_hub_id
        return RouteMap(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Route Map. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Output[Optional[Sequence['outputs.RouteMapRule']]]:
        """
        A `rule` block as defined below.
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter(name="virtualHubId")
    def virtual_hub_id(self) -> pulumi.Output[str]:
        """
        The resource ID of the Virtual Hub. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "virtual_hub_id")

