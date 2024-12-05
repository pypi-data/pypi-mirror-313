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
    'GetVirtualNetworkPeeringResult',
    'AwaitableGetVirtualNetworkPeeringResult',
    'get_virtual_network_peering',
    'get_virtual_network_peering_output',
]

@pulumi.output_type
class GetVirtualNetworkPeeringResult:
    """
    A collection of values returned by getVirtualNetworkPeering.
    """
    def __init__(__self__, allow_forwarded_traffic=None, allow_gateway_transit=None, allow_virtual_network_access=None, id=None, name=None, only_ipv6_peering_enabled=None, peer_complete_virtual_networks_enabled=None, remote_virtual_network_id=None, use_remote_gateways=None, virtual_network_id=None):
        if allow_forwarded_traffic and not isinstance(allow_forwarded_traffic, bool):
            raise TypeError("Expected argument 'allow_forwarded_traffic' to be a bool")
        pulumi.set(__self__, "allow_forwarded_traffic", allow_forwarded_traffic)
        if allow_gateway_transit and not isinstance(allow_gateway_transit, bool):
            raise TypeError("Expected argument 'allow_gateway_transit' to be a bool")
        pulumi.set(__self__, "allow_gateway_transit", allow_gateway_transit)
        if allow_virtual_network_access and not isinstance(allow_virtual_network_access, bool):
            raise TypeError("Expected argument 'allow_virtual_network_access' to be a bool")
        pulumi.set(__self__, "allow_virtual_network_access", allow_virtual_network_access)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if only_ipv6_peering_enabled and not isinstance(only_ipv6_peering_enabled, bool):
            raise TypeError("Expected argument 'only_ipv6_peering_enabled' to be a bool")
        pulumi.set(__self__, "only_ipv6_peering_enabled", only_ipv6_peering_enabled)
        if peer_complete_virtual_networks_enabled and not isinstance(peer_complete_virtual_networks_enabled, bool):
            raise TypeError("Expected argument 'peer_complete_virtual_networks_enabled' to be a bool")
        pulumi.set(__self__, "peer_complete_virtual_networks_enabled", peer_complete_virtual_networks_enabled)
        if remote_virtual_network_id and not isinstance(remote_virtual_network_id, str):
            raise TypeError("Expected argument 'remote_virtual_network_id' to be a str")
        pulumi.set(__self__, "remote_virtual_network_id", remote_virtual_network_id)
        if use_remote_gateways and not isinstance(use_remote_gateways, bool):
            raise TypeError("Expected argument 'use_remote_gateways' to be a bool")
        pulumi.set(__self__, "use_remote_gateways", use_remote_gateways)
        if virtual_network_id and not isinstance(virtual_network_id, str):
            raise TypeError("Expected argument 'virtual_network_id' to be a str")
        pulumi.set(__self__, "virtual_network_id", virtual_network_id)

    @property
    @pulumi.getter(name="allowForwardedTraffic")
    def allow_forwarded_traffic(self) -> bool:
        """
        Controls if forwarded traffic from VMs in the remote virtual network is allowed.
        """
        return pulumi.get(self, "allow_forwarded_traffic")

    @property
    @pulumi.getter(name="allowGatewayTransit")
    def allow_gateway_transit(self) -> bool:
        """
        Controls gatewayLinks can be used in the remote virtual network’s link to the local virtual network.
        """
        return pulumi.get(self, "allow_gateway_transit")

    @property
    @pulumi.getter(name="allowVirtualNetworkAccess")
    def allow_virtual_network_access(self) -> bool:
        """
        Controls if the traffic from the local virtual network can reach the remote virtual network.
        """
        return pulumi.get(self, "allow_virtual_network_access")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="onlyIpv6PeeringEnabled")
    def only_ipv6_peering_enabled(self) -> bool:
        """
        Specifies whether only IPv6 address space is peered for Subnet peering.
        """
        return pulumi.get(self, "only_ipv6_peering_enabled")

    @property
    @pulumi.getter(name="peerCompleteVirtualNetworksEnabled")
    def peer_complete_virtual_networks_enabled(self) -> bool:
        """
        Specifies whether complete Virtual Network address space is peered.
        """
        return pulumi.get(self, "peer_complete_virtual_networks_enabled")

    @property
    @pulumi.getter(name="remoteVirtualNetworkId")
    def remote_virtual_network_id(self) -> str:
        """
        The full Azure resource ID of the remote virtual network.
        """
        return pulumi.get(self, "remote_virtual_network_id")

    @property
    @pulumi.getter(name="useRemoteGateways")
    def use_remote_gateways(self) -> bool:
        """
        Controls if remote gateways can be used on the local virtual network.
        """
        return pulumi.get(self, "use_remote_gateways")

    @property
    @pulumi.getter(name="virtualNetworkId")
    def virtual_network_id(self) -> str:
        return pulumi.get(self, "virtual_network_id")


class AwaitableGetVirtualNetworkPeeringResult(GetVirtualNetworkPeeringResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualNetworkPeeringResult(
            allow_forwarded_traffic=self.allow_forwarded_traffic,
            allow_gateway_transit=self.allow_gateway_transit,
            allow_virtual_network_access=self.allow_virtual_network_access,
            id=self.id,
            name=self.name,
            only_ipv6_peering_enabled=self.only_ipv6_peering_enabled,
            peer_complete_virtual_networks_enabled=self.peer_complete_virtual_networks_enabled,
            remote_virtual_network_id=self.remote_virtual_network_id,
            use_remote_gateways=self.use_remote_gateways,
            virtual_network_id=self.virtual_network_id)


def get_virtual_network_peering(name: Optional[str] = None,
                                virtual_network_id: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualNetworkPeeringResult:
    """
    Use this data source to access information about an existing virtual network peering.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_virtual_network(name="vnet01",
        resource_group_name="networking")
    example_get_virtual_network_peering = azure.network.get_virtual_network_peering(name="peer-vnet01-to-vnet02",
        virtual_network_id=example.id)
    pulumi.export("id", example_get_virtual_network_peering.id)
    ```


    :param str name: The name of this virtual network peering.
    :param str virtual_network_id: The resource ID of the virtual network.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['virtualNetworkId'] = virtual_network_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:network/getVirtualNetworkPeering:getVirtualNetworkPeering', __args__, opts=opts, typ=GetVirtualNetworkPeeringResult).value

    return AwaitableGetVirtualNetworkPeeringResult(
        allow_forwarded_traffic=pulumi.get(__ret__, 'allow_forwarded_traffic'),
        allow_gateway_transit=pulumi.get(__ret__, 'allow_gateway_transit'),
        allow_virtual_network_access=pulumi.get(__ret__, 'allow_virtual_network_access'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        only_ipv6_peering_enabled=pulumi.get(__ret__, 'only_ipv6_peering_enabled'),
        peer_complete_virtual_networks_enabled=pulumi.get(__ret__, 'peer_complete_virtual_networks_enabled'),
        remote_virtual_network_id=pulumi.get(__ret__, 'remote_virtual_network_id'),
        use_remote_gateways=pulumi.get(__ret__, 'use_remote_gateways'),
        virtual_network_id=pulumi.get(__ret__, 'virtual_network_id'))
def get_virtual_network_peering_output(name: Optional[pulumi.Input[str]] = None,
                                       virtual_network_id: Optional[pulumi.Input[str]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVirtualNetworkPeeringResult]:
    """
    Use this data source to access information about an existing virtual network peering.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_virtual_network(name="vnet01",
        resource_group_name="networking")
    example_get_virtual_network_peering = azure.network.get_virtual_network_peering(name="peer-vnet01-to-vnet02",
        virtual_network_id=example.id)
    pulumi.export("id", example_get_virtual_network_peering.id)
    ```


    :param str name: The name of this virtual network peering.
    :param str virtual_network_id: The resource ID of the virtual network.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['virtualNetworkId'] = virtual_network_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:network/getVirtualNetworkPeering:getVirtualNetworkPeering', __args__, opts=opts, typ=GetVirtualNetworkPeeringResult)
    return __ret__.apply(lambda __response__: GetVirtualNetworkPeeringResult(
        allow_forwarded_traffic=pulumi.get(__response__, 'allow_forwarded_traffic'),
        allow_gateway_transit=pulumi.get(__response__, 'allow_gateway_transit'),
        allow_virtual_network_access=pulumi.get(__response__, 'allow_virtual_network_access'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        only_ipv6_peering_enabled=pulumi.get(__response__, 'only_ipv6_peering_enabled'),
        peer_complete_virtual_networks_enabled=pulumi.get(__response__, 'peer_complete_virtual_networks_enabled'),
        remote_virtual_network_id=pulumi.get(__response__, 'remote_virtual_network_id'),
        use_remote_gateways=pulumi.get(__response__, 'use_remote_gateways'),
        virtual_network_id=pulumi.get(__response__, 'virtual_network_id')))
