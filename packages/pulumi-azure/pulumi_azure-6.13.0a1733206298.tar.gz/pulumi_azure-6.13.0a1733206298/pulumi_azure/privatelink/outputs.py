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
    'EndpointCustomDnsConfig',
    'EndpointIpConfiguration',
    'EndpointNetworkInterface',
    'EndpointPrivateDnsZoneConfig',
    'EndpointPrivateDnsZoneConfigRecordSet',
    'EndpointPrivateDnsZoneGroup',
    'EndpointPrivateServiceConnection',
    'GetEndpointConnectionNetworkInterfaceResult',
    'GetEndpointConnectionPrivateServiceConnectionResult',
    'GetServiceEndpointConnectionsPrivateEndpointConnectionResult',
    'GetServiceNatIpConfigurationResult',
]

@pulumi.output_type
class EndpointCustomDnsConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipAddresses":
            suggest = "ip_addresses"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointCustomDnsConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointCustomDnsConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointCustomDnsConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 fqdn: Optional[str] = None,
                 ip_addresses: Optional[Sequence[str]] = None):
        """
        :param str fqdn: The fully qualified domain name to the `private_dns_zone`.
        :param Sequence[str] ip_addresses: A list of all IP Addresses that map to the `private_dns_zone` fqdn.
        """
        if fqdn is not None:
            pulumi.set(__self__, "fqdn", fqdn)
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)

    @property
    @pulumi.getter
    def fqdn(self) -> Optional[str]:
        """
        The fully qualified domain name to the `private_dns_zone`.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[Sequence[str]]:
        """
        A list of all IP Addresses that map to the `private_dns_zone` fqdn.
        """
        return pulumi.get(self, "ip_addresses")


@pulumi.output_type
class EndpointIpConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "privateIpAddress":
            suggest = "private_ip_address"
        elif key == "memberName":
            suggest = "member_name"
        elif key == "subresourceName":
            suggest = "subresource_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointIpConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointIpConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointIpConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: str,
                 private_ip_address: str,
                 member_name: Optional[str] = None,
                 subresource_name: Optional[str] = None):
        """
        :param str name: Specifies the Name of the IP Configuration. Changing this forces a new resource to be created.
        :param str private_ip_address: Specifies the static IP address within the private endpoint's subnet to be used. Changing this forces a new resource to be created.
        :param str member_name: Specifies the member name this IP address applies to. If it is not specified, it will use the value of `subresource_name`. Changing this forces a new resource to be created.
               
               > **NOTE:** `member_name` will be required and will not take the value of `subresource_name` in the next major version.
        :param str subresource_name: Specifies the subresource this IP address applies to. `subresource_names` corresponds to `group_id`. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "private_ip_address", private_ip_address)
        if member_name is not None:
            pulumi.set(__self__, "member_name", member_name)
        if subresource_name is not None:
            pulumi.set(__self__, "subresource_name", subresource_name)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the Name of the IP Configuration. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> str:
        """
        Specifies the static IP address within the private endpoint's subnet to be used. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="memberName")
    def member_name(self) -> Optional[str]:
        """
        Specifies the member name this IP address applies to. If it is not specified, it will use the value of `subresource_name`. Changing this forces a new resource to be created.

        > **NOTE:** `member_name` will be required and will not take the value of `subresource_name` in the next major version.
        """
        return pulumi.get(self, "member_name")

    @property
    @pulumi.getter(name="subresourceName")
    def subresource_name(self) -> Optional[str]:
        """
        Specifies the subresource this IP address applies to. `subresource_names` corresponds to `group_id`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "subresource_name")


@pulumi.output_type
class EndpointNetworkInterface(dict):
    def __init__(__self__, *,
                 id: Optional[str] = None,
                 name: Optional[str] = None):
        """
        :param str id: The ID of the Private DNS Zone Config.
        :param str name: Specifies the Name of the Private Endpoint. Changing this forces a new resource to be created.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the Private DNS Zone Config.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Specifies the Name of the Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class EndpointPrivateDnsZoneConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "privateDnsZoneId":
            suggest = "private_dns_zone_id"
        elif key == "recordSets":
            suggest = "record_sets"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointPrivateDnsZoneConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointPrivateDnsZoneConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointPrivateDnsZoneConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: Optional[str] = None,
                 name: Optional[str] = None,
                 private_dns_zone_id: Optional[str] = None,
                 record_sets: Optional[Sequence['outputs.EndpointPrivateDnsZoneConfigRecordSet']] = None):
        """
        :param str id: The ID of the Private DNS Zone Config.
        :param str name: Specifies the Name of the Private Endpoint. Changing this forces a new resource to be created.
        :param str private_dns_zone_id: A list of IP Addresses
        :param Sequence['EndpointPrivateDnsZoneConfigRecordSetArgs'] record_sets: A `record_sets` block as defined below.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if private_dns_zone_id is not None:
            pulumi.set(__self__, "private_dns_zone_id", private_dns_zone_id)
        if record_sets is not None:
            pulumi.set(__self__, "record_sets", record_sets)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the Private DNS Zone Config.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Specifies the Name of the Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateDnsZoneId")
    def private_dns_zone_id(self) -> Optional[str]:
        """
        A list of IP Addresses
        """
        return pulumi.get(self, "private_dns_zone_id")

    @property
    @pulumi.getter(name="recordSets")
    def record_sets(self) -> Optional[Sequence['outputs.EndpointPrivateDnsZoneConfigRecordSet']]:
        """
        A `record_sets` block as defined below.
        """
        return pulumi.get(self, "record_sets")


@pulumi.output_type
class EndpointPrivateDnsZoneConfigRecordSet(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipAddresses":
            suggest = "ip_addresses"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointPrivateDnsZoneConfigRecordSet. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointPrivateDnsZoneConfigRecordSet.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointPrivateDnsZoneConfigRecordSet.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 fqdn: Optional[str] = None,
                 ip_addresses: Optional[Sequence[str]] = None,
                 name: Optional[str] = None,
                 ttl: Optional[int] = None,
                 type: Optional[str] = None):
        """
        :param str fqdn: The fully qualified domain name to the `private_dns_zone`.
        :param Sequence[str] ip_addresses: A list of all IP Addresses that map to the `private_dns_zone` fqdn.
        :param str name: Specifies the Name of the Private Endpoint. Changing this forces a new resource to be created.
        :param int ttl: The time to live for each connection to the `private_dns_zone`.
        :param str type: The type of DNS record.
        """
        if fqdn is not None:
            pulumi.set(__self__, "fqdn", fqdn)
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def fqdn(self) -> Optional[str]:
        """
        The fully qualified domain name to the `private_dns_zone`.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[Sequence[str]]:
        """
        A list of all IP Addresses that map to the `private_dns_zone` fqdn.
        """
        return pulumi.get(self, "ip_addresses")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Specifies the Name of the Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def ttl(self) -> Optional[int]:
        """
        The time to live for each connection to the `private_dns_zone`.
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of DNS record.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class EndpointPrivateDnsZoneGroup(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "privateDnsZoneIds":
            suggest = "private_dns_zone_ids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointPrivateDnsZoneGroup. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointPrivateDnsZoneGroup.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointPrivateDnsZoneGroup.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: str,
                 private_dns_zone_ids: Sequence[str],
                 id: Optional[str] = None):
        """
        :param str name: Specifies the Name of the Private DNS Zone Group.
        :param Sequence[str] private_dns_zone_ids: Specifies the list of Private DNS Zones to include within the `private_dns_zone_group`.
        :param str id: The ID of the Private DNS Zone Config.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "private_dns_zone_ids", private_dns_zone_ids)
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the Name of the Private DNS Zone Group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateDnsZoneIds")
    def private_dns_zone_ids(self) -> Sequence[str]:
        """
        Specifies the list of Private DNS Zones to include within the `private_dns_zone_group`.
        """
        return pulumi.get(self, "private_dns_zone_ids")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the Private DNS Zone Config.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class EndpointPrivateServiceConnection(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "isManualConnection":
            suggest = "is_manual_connection"
        elif key == "privateConnectionResourceAlias":
            suggest = "private_connection_resource_alias"
        elif key == "privateConnectionResourceId":
            suggest = "private_connection_resource_id"
        elif key == "privateIpAddress":
            suggest = "private_ip_address"
        elif key == "requestMessage":
            suggest = "request_message"
        elif key == "subresourceNames":
            suggest = "subresource_names"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointPrivateServiceConnection. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointPrivateServiceConnection.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointPrivateServiceConnection.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 is_manual_connection: bool,
                 name: str,
                 private_connection_resource_alias: Optional[str] = None,
                 private_connection_resource_id: Optional[str] = None,
                 private_ip_address: Optional[str] = None,
                 request_message: Optional[str] = None,
                 subresource_names: Optional[Sequence[str]] = None):
        """
        :param bool is_manual_connection: Does the Private Endpoint require Manual Approval from the remote resource owner? Changing this forces a new resource to be created.
               
               > **NOTE:** If you are trying to connect the Private Endpoint to a remote resource without having the correct RBAC permissions on the remote resource set this value to `true`.
        :param str name: Specifies the Name of the Private Service Connection. Changing this forces a new resource to be created.
        :param str private_connection_resource_alias: The Service Alias of the Private Link Enabled Remote Resource which this Private Endpoint should be connected to. One of `private_connection_resource_id` or `private_connection_resource_alias` must be specified. Changing this forces a new resource to be created.
        :param str private_connection_resource_id: The ID of the Private Link Enabled Remote Resource which this Private Endpoint should be connected to. One of `private_connection_resource_id` or `private_connection_resource_alias` must be specified. Changing this forces a new resource to be created. For a web app or function app slot, the parent web app should be used in this field instead of a reference to the slot itself.
        :param str private_ip_address: (Required) The static IP address set by this configuration. It is recommended to use the private IP address exported in the `private_service_connection` block to obtain the address associated with the private endpoint.
        :param str request_message: A message passed to the owner of the remote resource when the private endpoint attempts to establish the connection to the remote resource. The provider allows a maximum request message length of `140` characters, however the request message maximum length is dependent on the service the private endpoint is connected to. Only valid if `is_manual_connection` is set to `true`.
               
               > **NOTE:** When connected to an SQL resource the `request_message` maximum length is `128`.
        :param Sequence[str] subresource_names: A list of subresource names which the Private Endpoint is able to connect to. `subresource_names` corresponds to `group_id`. Possible values are detailed in the product [documentation](https://docs.microsoft.com/azure/private-link/private-endpoint-overview#private-link-resource) in the `Subresources` column. Changing this forces a new resource to be created. 
               
               > **NOTE:** Some resource types (such as Storage Account) only support 1 subresource per private endpoint.
               
               > **NOTE:** For most Private Links one or more `subresource_names` will need to be specified, please see the linked documentation for details.
        """
        pulumi.set(__self__, "is_manual_connection", is_manual_connection)
        pulumi.set(__self__, "name", name)
        if private_connection_resource_alias is not None:
            pulumi.set(__self__, "private_connection_resource_alias", private_connection_resource_alias)
        if private_connection_resource_id is not None:
            pulumi.set(__self__, "private_connection_resource_id", private_connection_resource_id)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)
        if request_message is not None:
            pulumi.set(__self__, "request_message", request_message)
        if subresource_names is not None:
            pulumi.set(__self__, "subresource_names", subresource_names)

    @property
    @pulumi.getter(name="isManualConnection")
    def is_manual_connection(self) -> bool:
        """
        Does the Private Endpoint require Manual Approval from the remote resource owner? Changing this forces a new resource to be created.

        > **NOTE:** If you are trying to connect the Private Endpoint to a remote resource without having the correct RBAC permissions on the remote resource set this value to `true`.
        """
        return pulumi.get(self, "is_manual_connection")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the Name of the Private Service Connection. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateConnectionResourceAlias")
    def private_connection_resource_alias(self) -> Optional[str]:
        """
        The Service Alias of the Private Link Enabled Remote Resource which this Private Endpoint should be connected to. One of `private_connection_resource_id` or `private_connection_resource_alias` must be specified. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "private_connection_resource_alias")

    @property
    @pulumi.getter(name="privateConnectionResourceId")
    def private_connection_resource_id(self) -> Optional[str]:
        """
        The ID of the Private Link Enabled Remote Resource which this Private Endpoint should be connected to. One of `private_connection_resource_id` or `private_connection_resource_alias` must be specified. Changing this forces a new resource to be created. For a web app or function app slot, the parent web app should be used in this field instead of a reference to the slot itself.
        """
        return pulumi.get(self, "private_connection_resource_id")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[str]:
        """
        (Required) The static IP address set by this configuration. It is recommended to use the private IP address exported in the `private_service_connection` block to obtain the address associated with the private endpoint.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="requestMessage")
    def request_message(self) -> Optional[str]:
        """
        A message passed to the owner of the remote resource when the private endpoint attempts to establish the connection to the remote resource. The provider allows a maximum request message length of `140` characters, however the request message maximum length is dependent on the service the private endpoint is connected to. Only valid if `is_manual_connection` is set to `true`.

        > **NOTE:** When connected to an SQL resource the `request_message` maximum length is `128`.
        """
        return pulumi.get(self, "request_message")

    @property
    @pulumi.getter(name="subresourceNames")
    def subresource_names(self) -> Optional[Sequence[str]]:
        """
        A list of subresource names which the Private Endpoint is able to connect to. `subresource_names` corresponds to `group_id`. Possible values are detailed in the product [documentation](https://docs.microsoft.com/azure/private-link/private-endpoint-overview#private-link-resource) in the `Subresources` column. Changing this forces a new resource to be created. 

        > **NOTE:** Some resource types (such as Storage Account) only support 1 subresource per private endpoint.

        > **NOTE:** For most Private Links one or more `subresource_names` will need to be specified, please see the linked documentation for details.
        """
        return pulumi.get(self, "subresource_names")


@pulumi.output_type
class GetEndpointConnectionNetworkInterfaceResult(dict):
    def __init__(__self__, *,
                 id: str,
                 name: str):
        """
        :param str id: The ID of the network interface associated with the private endpoint.
        :param str name: Specifies the Name of the private endpoint.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the network interface associated with the private endpoint.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the Name of the private endpoint.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class GetEndpointConnectionPrivateServiceConnectionResult(dict):
    def __init__(__self__, *,
                 name: str,
                 private_ip_address: str,
                 request_response: str,
                 status: str):
        """
        :param str name: Specifies the Name of the private endpoint.
        :param str private_ip_address: The private IP address associated with the private endpoint, note that you will have a private IP address assigned to the private endpoint even if the connection request was `Rejected`.
        :param str request_response: Possible values are as follows:
               Value | Meaning
               -- | --
               `Auto-Approved` | The remote resource owner has added you to the `Auto-Approved` RBAC permission list for the remote resource, all private endpoint connection requests will be automatically `Approved`.
               `Deleted state` | The resource owner has `Rejected` the private endpoint connection request and has removed your private endpoint request from the remote resource.
               `request/response message` | If you submitted a manual private endpoint connection request, while in the `Pending` status the `request_response` will display the same text from your `request_message` in the `private_service_connection` block above. If the private endpoint connection request was `Rejected` by the owner of the remote resource, the text for the rejection will be displayed as the `request_response` text, if the private endpoint connection request was `Approved` by the owner of the remote resource, the text for the approval will be displayed as the `request_response` text
        :param str status: The current status of the private endpoint request, possible values will be `Pending`, `Approved`, `Rejected`, or `Disconnected`.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "private_ip_address", private_ip_address)
        pulumi.set(__self__, "request_response", request_response)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the Name of the private endpoint.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> str:
        """
        The private IP address associated with the private endpoint, note that you will have a private IP address assigned to the private endpoint even if the connection request was `Rejected`.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="requestResponse")
    def request_response(self) -> str:
        """
        Possible values are as follows:
        Value | Meaning
        -- | --
        `Auto-Approved` | The remote resource owner has added you to the `Auto-Approved` RBAC permission list for the remote resource, all private endpoint connection requests will be automatically `Approved`.
        `Deleted state` | The resource owner has `Rejected` the private endpoint connection request and has removed your private endpoint request from the remote resource.
        `request/response message` | If you submitted a manual private endpoint connection request, while in the `Pending` status the `request_response` will display the same text from your `request_message` in the `private_service_connection` block above. If the private endpoint connection request was `Rejected` by the owner of the remote resource, the text for the rejection will be displayed as the `request_response` text, if the private endpoint connection request was `Approved` by the owner of the remote resource, the text for the approval will be displayed as the `request_response` text
        """
        return pulumi.get(self, "request_response")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The current status of the private endpoint request, possible values will be `Pending`, `Approved`, `Rejected`, or `Disconnected`.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class GetServiceEndpointConnectionsPrivateEndpointConnectionResult(dict):
    def __init__(__self__, *,
                 action_required: str,
                 connection_id: str,
                 connection_name: str,
                 description: str,
                 private_endpoint_id: str,
                 private_endpoint_name: str,
                 status: str):
        """
        :param str action_required: A message indicating if changes on the service provider require any updates or not.
        :param str connection_id: The resource id of the private link service connection between the private link service and the private link endpoint.
        :param str connection_name: The name of the connection between the private link service and the private link endpoint.
        :param str description: The request for approval message or the reason for rejection message.
        :param str private_endpoint_id: The resource id of the private link endpoint.
        :param str private_endpoint_name: The name of the private link endpoint.
        :param str status: Indicates the state of the connection between the private link service and the private link endpoint, possible values are `Pending`, `Approved` or `Rejected`.
        """
        pulumi.set(__self__, "action_required", action_required)
        pulumi.set(__self__, "connection_id", connection_id)
        pulumi.set(__self__, "connection_name", connection_name)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "private_endpoint_id", private_endpoint_id)
        pulumi.set(__self__, "private_endpoint_name", private_endpoint_name)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionRequired")
    def action_required(self) -> str:
        """
        A message indicating if changes on the service provider require any updates or not.
        """
        return pulumi.get(self, "action_required")

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> str:
        """
        The resource id of the private link service connection between the private link service and the private link endpoint.
        """
        return pulumi.get(self, "connection_id")

    @property
    @pulumi.getter(name="connectionName")
    def connection_name(self) -> str:
        """
        The name of the connection between the private link service and the private link endpoint.
        """
        return pulumi.get(self, "connection_name")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The request for approval message or the reason for rejection message.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="privateEndpointId")
    def private_endpoint_id(self) -> str:
        """
        The resource id of the private link endpoint.
        """
        return pulumi.get(self, "private_endpoint_id")

    @property
    @pulumi.getter(name="privateEndpointName")
    def private_endpoint_name(self) -> str:
        """
        The name of the private link endpoint.
        """
        return pulumi.get(self, "private_endpoint_name")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Indicates the state of the connection between the private link service and the private link endpoint, possible values are `Pending`, `Approved` or `Rejected`.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class GetServiceNatIpConfigurationResult(dict):
    def __init__(__self__, *,
                 name: str,
                 primary: bool,
                 private_ip_address: str,
                 private_ip_address_version: str,
                 subnet_id: str):
        """
        :param str name: The name of the private link service.
        :param bool primary: Value that indicates if the IP configuration is the primary configuration or not.
        :param str private_ip_address: The private IP address of the NAT IP configuration.
        :param str private_ip_address_version: The version of the IP Protocol.
        :param str subnet_id: The ID of the subnet to be used by the service.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "primary", primary)
        pulumi.set(__self__, "private_ip_address", private_ip_address)
        pulumi.set(__self__, "private_ip_address_version", private_ip_address_version)
        pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the private link service.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def primary(self) -> bool:
        """
        Value that indicates if the IP configuration is the primary configuration or not.
        """
        return pulumi.get(self, "primary")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> str:
        """
        The private IP address of the NAT IP configuration.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="privateIpAddressVersion")
    def private_ip_address_version(self) -> str:
        """
        The version of the IP Protocol.
        """
        return pulumi.get(self, "private_ip_address_version")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> str:
        """
        The ID of the subnet to be used by the service.
        """
        return pulumi.get(self, "subnet_id")


