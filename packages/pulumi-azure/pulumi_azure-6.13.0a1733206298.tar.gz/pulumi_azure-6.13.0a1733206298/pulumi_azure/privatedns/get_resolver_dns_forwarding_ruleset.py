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
    'GetResolverDnsForwardingRulesetResult',
    'AwaitableGetResolverDnsForwardingRulesetResult',
    'get_resolver_dns_forwarding_ruleset',
    'get_resolver_dns_forwarding_ruleset_output',
]

@pulumi.output_type
class GetResolverDnsForwardingRulesetResult:
    """
    A collection of values returned by getResolverDnsForwardingRuleset.
    """
    def __init__(__self__, id=None, location=None, name=None, private_dns_resolver_outbound_endpoint_ids=None, resource_group_name=None, tags=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if private_dns_resolver_outbound_endpoint_ids and not isinstance(private_dns_resolver_outbound_endpoint_ids, list):
            raise TypeError("Expected argument 'private_dns_resolver_outbound_endpoint_ids' to be a list")
        pulumi.set(__self__, "private_dns_resolver_outbound_endpoint_ids", private_dns_resolver_outbound_endpoint_ids)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

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
        """
        The Azure Region where the Private DNS Resolver Dns Forwarding Ruleset exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateDnsResolverOutboundEndpointIds")
    def private_dns_resolver_outbound_endpoint_ids(self) -> Sequence[str]:
        """
        The IDs list of the Private DNS Resolver Outbound Endpoints that are linked to the Private DNS Resolver Dns Forwarding Ruleset.
        """
        return pulumi.get(self, "private_dns_resolver_outbound_endpoint_ids")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        The tags assigned to the Private DNS Resolver Dns Forwarding Ruleset.
        """
        return pulumi.get(self, "tags")


class AwaitableGetResolverDnsForwardingRulesetResult(GetResolverDnsForwardingRulesetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResolverDnsForwardingRulesetResult(
            id=self.id,
            location=self.location,
            name=self.name,
            private_dns_resolver_outbound_endpoint_ids=self.private_dns_resolver_outbound_endpoint_ids,
            resource_group_name=self.resource_group_name,
            tags=self.tags)


def get_resolver_dns_forwarding_ruleset(name: Optional[str] = None,
                                        resource_group_name: Optional[str] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResolverDnsForwardingRulesetResult:
    """
    Gets information about an existing Private DNS Resolver Dns Forwarding Ruleset.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.privatedns.get_resolver_dns_forwarding_ruleset(name="example-ruleset",
        resource_group_name="example-ruleset-resourcegroup")
    ```


    :param str name: Name of the existing Private DNS Resolver Dns Forwarding Ruleset.
    :param str resource_group_name: Name of the Resource Group where the Private DNS Resolver Dns Forwarding Ruleset exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:privatedns/getResolverDnsForwardingRuleset:getResolverDnsForwardingRuleset', __args__, opts=opts, typ=GetResolverDnsForwardingRulesetResult).value

    return AwaitableGetResolverDnsForwardingRulesetResult(
        id=pulumi.get(__ret__, 'id'),
        location=pulumi.get(__ret__, 'location'),
        name=pulumi.get(__ret__, 'name'),
        private_dns_resolver_outbound_endpoint_ids=pulumi.get(__ret__, 'private_dns_resolver_outbound_endpoint_ids'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        tags=pulumi.get(__ret__, 'tags'))
def get_resolver_dns_forwarding_ruleset_output(name: Optional[pulumi.Input[str]] = None,
                                               resource_group_name: Optional[pulumi.Input[str]] = None,
                                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResolverDnsForwardingRulesetResult]:
    """
    Gets information about an existing Private DNS Resolver Dns Forwarding Ruleset.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.privatedns.get_resolver_dns_forwarding_ruleset(name="example-ruleset",
        resource_group_name="example-ruleset-resourcegroup")
    ```


    :param str name: Name of the existing Private DNS Resolver Dns Forwarding Ruleset.
    :param str resource_group_name: Name of the Resource Group where the Private DNS Resolver Dns Forwarding Ruleset exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:privatedns/getResolverDnsForwardingRuleset:getResolverDnsForwardingRuleset', __args__, opts=opts, typ=GetResolverDnsForwardingRulesetResult)
    return __ret__.apply(lambda __response__: GetResolverDnsForwardingRulesetResult(
        id=pulumi.get(__response__, 'id'),
        location=pulumi.get(__response__, 'location'),
        name=pulumi.get(__response__, 'name'),
        private_dns_resolver_outbound_endpoint_ids=pulumi.get(__response__, 'private_dns_resolver_outbound_endpoint_ids'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        tags=pulumi.get(__response__, 'tags')))
