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
    'GetFirewallPolicyResult',
    'AwaitableGetFirewallPolicyResult',
    'get_firewall_policy',
    'get_firewall_policy_output',
]

@pulumi.output_type
class GetFirewallPolicyResult:
    """
    A collection of values returned by getFirewallPolicy.
    """
    def __init__(__self__, base_policy_id=None, child_policies=None, dns=None, firewalls=None, id=None, location=None, name=None, resource_group_name=None, rule_collection_groups=None, tags=None, threat_intelligence_allowlists=None, threat_intelligence_mode=None):
        if base_policy_id and not isinstance(base_policy_id, str):
            raise TypeError("Expected argument 'base_policy_id' to be a str")
        pulumi.set(__self__, "base_policy_id", base_policy_id)
        if child_policies and not isinstance(child_policies, list):
            raise TypeError("Expected argument 'child_policies' to be a list")
        pulumi.set(__self__, "child_policies", child_policies)
        if dns and not isinstance(dns, list):
            raise TypeError("Expected argument 'dns' to be a list")
        pulumi.set(__self__, "dns", dns)
        if firewalls and not isinstance(firewalls, list):
            raise TypeError("Expected argument 'firewalls' to be a list")
        pulumi.set(__self__, "firewalls", firewalls)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if rule_collection_groups and not isinstance(rule_collection_groups, list):
            raise TypeError("Expected argument 'rule_collection_groups' to be a list")
        pulumi.set(__self__, "rule_collection_groups", rule_collection_groups)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if threat_intelligence_allowlists and not isinstance(threat_intelligence_allowlists, list):
            raise TypeError("Expected argument 'threat_intelligence_allowlists' to be a list")
        pulumi.set(__self__, "threat_intelligence_allowlists", threat_intelligence_allowlists)
        if threat_intelligence_mode and not isinstance(threat_intelligence_mode, str):
            raise TypeError("Expected argument 'threat_intelligence_mode' to be a str")
        pulumi.set(__self__, "threat_intelligence_mode", threat_intelligence_mode)

    @property
    @pulumi.getter(name="basePolicyId")
    def base_policy_id(self) -> str:
        return pulumi.get(self, "base_policy_id")

    @property
    @pulumi.getter(name="childPolicies")
    def child_policies(self) -> Sequence[str]:
        return pulumi.get(self, "child_policies")

    @property
    @pulumi.getter
    def dns(self) -> Sequence['outputs.GetFirewallPolicyDnResult']:
        return pulumi.get(self, "dns")

    @property
    @pulumi.getter
    def firewalls(self) -> Sequence[str]:
        return pulumi.get(self, "firewalls")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="ruleCollectionGroups")
    def rule_collection_groups(self) -> Sequence[str]:
        return pulumi.get(self, "rule_collection_groups")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the Firewall Policy.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="threatIntelligenceAllowlists")
    def threat_intelligence_allowlists(self) -> Sequence['outputs.GetFirewallPolicyThreatIntelligenceAllowlistResult']:
        return pulumi.get(self, "threat_intelligence_allowlists")

    @property
    @pulumi.getter(name="threatIntelligenceMode")
    def threat_intelligence_mode(self) -> str:
        return pulumi.get(self, "threat_intelligence_mode")


class AwaitableGetFirewallPolicyResult(GetFirewallPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFirewallPolicyResult(
            base_policy_id=self.base_policy_id,
            child_policies=self.child_policies,
            dns=self.dns,
            firewalls=self.firewalls,
            id=self.id,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            rule_collection_groups=self.rule_collection_groups,
            tags=self.tags,
            threat_intelligence_allowlists=self.threat_intelligence_allowlists,
            threat_intelligence_mode=self.threat_intelligence_mode)


def get_firewall_policy(name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFirewallPolicyResult:
    """
    Use this data source to access information about an existing Firewall Policy.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_firewall_policy(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Firewall Policy.
    :param str resource_group_name: The name of the Resource Group where the Firewall Policy exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:network/getFirewallPolicy:getFirewallPolicy', __args__, opts=opts, typ=GetFirewallPolicyResult).value

    return AwaitableGetFirewallPolicyResult(
        base_policy_id=pulumi.get(__ret__, 'base_policy_id'),
        child_policies=pulumi.get(__ret__, 'child_policies'),
        dns=pulumi.get(__ret__, 'dns'),
        firewalls=pulumi.get(__ret__, 'firewalls'),
        id=pulumi.get(__ret__, 'id'),
        location=pulumi.get(__ret__, 'location'),
        name=pulumi.get(__ret__, 'name'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        rule_collection_groups=pulumi.get(__ret__, 'rule_collection_groups'),
        tags=pulumi.get(__ret__, 'tags'),
        threat_intelligence_allowlists=pulumi.get(__ret__, 'threat_intelligence_allowlists'),
        threat_intelligence_mode=pulumi.get(__ret__, 'threat_intelligence_mode'))
def get_firewall_policy_output(name: Optional[pulumi.Input[str]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFirewallPolicyResult]:
    """
    Use this data source to access information about an existing Firewall Policy.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_firewall_policy(name="existing",
        resource_group_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Firewall Policy.
    :param str resource_group_name: The name of the Resource Group where the Firewall Policy exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:network/getFirewallPolicy:getFirewallPolicy', __args__, opts=opts, typ=GetFirewallPolicyResult)
    return __ret__.apply(lambda __response__: GetFirewallPolicyResult(
        base_policy_id=pulumi.get(__response__, 'base_policy_id'),
        child_policies=pulumi.get(__response__, 'child_policies'),
        dns=pulumi.get(__response__, 'dns'),
        firewalls=pulumi.get(__response__, 'firewalls'),
        id=pulumi.get(__response__, 'id'),
        location=pulumi.get(__response__, 'location'),
        name=pulumi.get(__response__, 'name'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        rule_collection_groups=pulumi.get(__response__, 'rule_collection_groups'),
        tags=pulumi.get(__response__, 'tags'),
        threat_intelligence_allowlists=pulumi.get(__response__, 'threat_intelligence_allowlists'),
        threat_intelligence_mode=pulumi.get(__response__, 'threat_intelligence_mode')))
