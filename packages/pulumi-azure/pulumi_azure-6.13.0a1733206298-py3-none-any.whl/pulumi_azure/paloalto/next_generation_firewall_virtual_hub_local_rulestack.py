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

__all__ = ['NextGenerationFirewallVirtualHubLocalRulestackArgs', 'NextGenerationFirewallVirtualHubLocalRulestack']

@pulumi.input_type
class NextGenerationFirewallVirtualHubLocalRulestackArgs:
    def __init__(__self__, *,
                 network_profile: pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackNetworkProfileArgs'],
                 resource_group_name: pulumi.Input[str],
                 rulestack_id: pulumi.Input[str],
                 destination_nats: Optional[pulumi.Input[Sequence[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackDestinationNatArgs']]]] = None,
                 dns_settings: Optional[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackDnsSettingsArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a NextGenerationFirewallVirtualHubLocalRulestack resource.
        """
        pulumi.set(__self__, "network_profile", network_profile)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "rulestack_id", rulestack_id)
        if destination_nats is not None:
            pulumi.set(__self__, "destination_nats", destination_nats)
        if dns_settings is not None:
            pulumi.set(__self__, "dns_settings", dns_settings)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="networkProfile")
    def network_profile(self) -> pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackNetworkProfileArgs']:
        return pulumi.get(self, "network_profile")

    @network_profile.setter
    def network_profile(self, value: pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackNetworkProfileArgs']):
        pulumi.set(self, "network_profile", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="rulestackId")
    def rulestack_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "rulestack_id")

    @rulestack_id.setter
    def rulestack_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "rulestack_id", value)

    @property
    @pulumi.getter(name="destinationNats")
    def destination_nats(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackDestinationNatArgs']]]]:
        return pulumi.get(self, "destination_nats")

    @destination_nats.setter
    def destination_nats(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackDestinationNatArgs']]]]):
        pulumi.set(self, "destination_nats", value)

    @property
    @pulumi.getter(name="dnsSettings")
    def dns_settings(self) -> Optional[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackDnsSettingsArgs']]:
        return pulumi.get(self, "dns_settings")

    @dns_settings.setter
    def dns_settings(self, value: Optional[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackDnsSettingsArgs']]):
        pulumi.set(self, "dns_settings", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _NextGenerationFirewallVirtualHubLocalRulestackState:
    def __init__(__self__, *,
                 destination_nats: Optional[pulumi.Input[Sequence[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackDestinationNatArgs']]]] = None,
                 dns_settings: Optional[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackDnsSettingsArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_profile: Optional[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackNetworkProfileArgs']] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rulestack_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering NextGenerationFirewallVirtualHubLocalRulestack resources.
        """
        if destination_nats is not None:
            pulumi.set(__self__, "destination_nats", destination_nats)
        if dns_settings is not None:
            pulumi.set(__self__, "dns_settings", dns_settings)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network_profile is not None:
            pulumi.set(__self__, "network_profile", network_profile)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if rulestack_id is not None:
            pulumi.set(__self__, "rulestack_id", rulestack_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="destinationNats")
    def destination_nats(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackDestinationNatArgs']]]]:
        return pulumi.get(self, "destination_nats")

    @destination_nats.setter
    def destination_nats(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackDestinationNatArgs']]]]):
        pulumi.set(self, "destination_nats", value)

    @property
    @pulumi.getter(name="dnsSettings")
    def dns_settings(self) -> Optional[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackDnsSettingsArgs']]:
        return pulumi.get(self, "dns_settings")

    @dns_settings.setter
    def dns_settings(self, value: Optional[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackDnsSettingsArgs']]):
        pulumi.set(self, "dns_settings", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="networkProfile")
    def network_profile(self) -> Optional[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackNetworkProfileArgs']]:
        return pulumi.get(self, "network_profile")

    @network_profile.setter
    def network_profile(self, value: Optional[pulumi.Input['NextGenerationFirewallVirtualHubLocalRulestackNetworkProfileArgs']]):
        pulumi.set(self, "network_profile", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="rulestackId")
    def rulestack_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "rulestack_id")

    @rulestack_id.setter
    def rulestack_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rulestack_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class NextGenerationFirewallVirtualHubLocalRulestack(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_nats: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NextGenerationFirewallVirtualHubLocalRulestackDestinationNatArgs', 'NextGenerationFirewallVirtualHubLocalRulestackDestinationNatArgsDict']]]]] = None,
                 dns_settings: Optional[pulumi.Input[Union['NextGenerationFirewallVirtualHubLocalRulestackDnsSettingsArgs', 'NextGenerationFirewallVirtualHubLocalRulestackDnsSettingsArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_profile: Optional[pulumi.Input[Union['NextGenerationFirewallVirtualHubLocalRulestackNetworkProfileArgs', 'NextGenerationFirewallVirtualHubLocalRulestackNetworkProfileArgsDict']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rulestack_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Create a NextGenerationFirewallVirtualHubLocalRulestack resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NextGenerationFirewallVirtualHubLocalRulestackArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a NextGenerationFirewallVirtualHubLocalRulestack resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param NextGenerationFirewallVirtualHubLocalRulestackArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NextGenerationFirewallVirtualHubLocalRulestackArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_nats: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NextGenerationFirewallVirtualHubLocalRulestackDestinationNatArgs', 'NextGenerationFirewallVirtualHubLocalRulestackDestinationNatArgsDict']]]]] = None,
                 dns_settings: Optional[pulumi.Input[Union['NextGenerationFirewallVirtualHubLocalRulestackDnsSettingsArgs', 'NextGenerationFirewallVirtualHubLocalRulestackDnsSettingsArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_profile: Optional[pulumi.Input[Union['NextGenerationFirewallVirtualHubLocalRulestackNetworkProfileArgs', 'NextGenerationFirewallVirtualHubLocalRulestackNetworkProfileArgsDict']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rulestack_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NextGenerationFirewallVirtualHubLocalRulestackArgs.__new__(NextGenerationFirewallVirtualHubLocalRulestackArgs)

            __props__.__dict__["destination_nats"] = destination_nats
            __props__.__dict__["dns_settings"] = dns_settings
            __props__.__dict__["name"] = name
            if network_profile is None and not opts.urn:
                raise TypeError("Missing required property 'network_profile'")
            __props__.__dict__["network_profile"] = network_profile
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if rulestack_id is None and not opts.urn:
                raise TypeError("Missing required property 'rulestack_id'")
            __props__.__dict__["rulestack_id"] = rulestack_id
            __props__.__dict__["tags"] = tags
        super(NextGenerationFirewallVirtualHubLocalRulestack, __self__).__init__(
            'azure:paloalto/nextGenerationFirewallVirtualHubLocalRulestack:NextGenerationFirewallVirtualHubLocalRulestack',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            destination_nats: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NextGenerationFirewallVirtualHubLocalRulestackDestinationNatArgs', 'NextGenerationFirewallVirtualHubLocalRulestackDestinationNatArgsDict']]]]] = None,
            dns_settings: Optional[pulumi.Input[Union['NextGenerationFirewallVirtualHubLocalRulestackDnsSettingsArgs', 'NextGenerationFirewallVirtualHubLocalRulestackDnsSettingsArgsDict']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network_profile: Optional[pulumi.Input[Union['NextGenerationFirewallVirtualHubLocalRulestackNetworkProfileArgs', 'NextGenerationFirewallVirtualHubLocalRulestackNetworkProfileArgsDict']]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            rulestack_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'NextGenerationFirewallVirtualHubLocalRulestack':
        """
        Get an existing NextGenerationFirewallVirtualHubLocalRulestack resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NextGenerationFirewallVirtualHubLocalRulestackState.__new__(_NextGenerationFirewallVirtualHubLocalRulestackState)

        __props__.__dict__["destination_nats"] = destination_nats
        __props__.__dict__["dns_settings"] = dns_settings
        __props__.__dict__["name"] = name
        __props__.__dict__["network_profile"] = network_profile
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["rulestack_id"] = rulestack_id
        __props__.__dict__["tags"] = tags
        return NextGenerationFirewallVirtualHubLocalRulestack(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="destinationNats")
    def destination_nats(self) -> pulumi.Output[Optional[Sequence['outputs.NextGenerationFirewallVirtualHubLocalRulestackDestinationNat']]]:
        return pulumi.get(self, "destination_nats")

    @property
    @pulumi.getter(name="dnsSettings")
    def dns_settings(self) -> pulumi.Output[Optional['outputs.NextGenerationFirewallVirtualHubLocalRulestackDnsSettings']]:
        return pulumi.get(self, "dns_settings")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkProfile")
    def network_profile(self) -> pulumi.Output['outputs.NextGenerationFirewallVirtualHubLocalRulestackNetworkProfile']:
        return pulumi.get(self, "network_profile")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="rulestackId")
    def rulestack_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "rulestack_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        return pulumi.get(self, "tags")

