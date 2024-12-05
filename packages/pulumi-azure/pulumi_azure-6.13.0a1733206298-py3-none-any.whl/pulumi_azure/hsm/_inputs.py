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
    'ModuleManagementNetworkProfileArgs',
    'ModuleManagementNetworkProfileArgsDict',
    'ModuleNetworkProfileArgs',
    'ModuleNetworkProfileArgsDict',
]

MYPY = False

if not MYPY:
    class ModuleManagementNetworkProfileArgsDict(TypedDict):
        network_interface_private_ip_addresses: pulumi.Input[Sequence[pulumi.Input[str]]]
        """
        The private IPv4 address of the network interface. Changing this forces a new Dedicated Hardware Security Module to be created.
        """
        subnet_id: pulumi.Input[str]
        """
        The ID of the subnet. Changing this forces a new Dedicated Hardware Security Module to be created.
        """
elif False:
    ModuleManagementNetworkProfileArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ModuleManagementNetworkProfileArgs:
    def __init__(__self__, *,
                 network_interface_private_ip_addresses: pulumi.Input[Sequence[pulumi.Input[str]]],
                 subnet_id: pulumi.Input[str]):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_interface_private_ip_addresses: The private IPv4 address of the network interface. Changing this forces a new Dedicated Hardware Security Module to be created.
        :param pulumi.Input[str] subnet_id: The ID of the subnet. Changing this forces a new Dedicated Hardware Security Module to be created.
        """
        pulumi.set(__self__, "network_interface_private_ip_addresses", network_interface_private_ip_addresses)
        pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="networkInterfacePrivateIpAddresses")
    def network_interface_private_ip_addresses(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The private IPv4 address of the network interface. Changing this forces a new Dedicated Hardware Security Module to be created.
        """
        return pulumi.get(self, "network_interface_private_ip_addresses")

    @network_interface_private_ip_addresses.setter
    def network_interface_private_ip_addresses(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "network_interface_private_ip_addresses", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Input[str]:
        """
        The ID of the subnet. Changing this forces a new Dedicated Hardware Security Module to be created.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnet_id", value)


if not MYPY:
    class ModuleNetworkProfileArgsDict(TypedDict):
        network_interface_private_ip_addresses: pulumi.Input[Sequence[pulumi.Input[str]]]
        """
        The private IPv4 address of the network interface. Changing this forces a new Dedicated Hardware Security Module to be created.
        """
        subnet_id: pulumi.Input[str]
        """
        The ID of the subnet. Changing this forces a new Dedicated Hardware Security Module to be created.
        """
elif False:
    ModuleNetworkProfileArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ModuleNetworkProfileArgs:
    def __init__(__self__, *,
                 network_interface_private_ip_addresses: pulumi.Input[Sequence[pulumi.Input[str]]],
                 subnet_id: pulumi.Input[str]):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_interface_private_ip_addresses: The private IPv4 address of the network interface. Changing this forces a new Dedicated Hardware Security Module to be created.
        :param pulumi.Input[str] subnet_id: The ID of the subnet. Changing this forces a new Dedicated Hardware Security Module to be created.
        """
        pulumi.set(__self__, "network_interface_private_ip_addresses", network_interface_private_ip_addresses)
        pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="networkInterfacePrivateIpAddresses")
    def network_interface_private_ip_addresses(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The private IPv4 address of the network interface. Changing this forces a new Dedicated Hardware Security Module to be created.
        """
        return pulumi.get(self, "network_interface_private_ip_addresses")

    @network_interface_private_ip_addresses.setter
    def network_interface_private_ip_addresses(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "network_interface_private_ip_addresses", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Input[str]:
        """
        The ID of the subnet. Changing this forces a new Dedicated Hardware Security Module to be created.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnet_id", value)


