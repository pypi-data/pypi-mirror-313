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
    'GetServiceResult',
    'AwaitableGetServiceResult',
    'get_service',
    'get_service_output',
]

@pulumi.output_type
class GetServiceResult:
    """
    A collection of values returned by getService.
    """
    def __init__(__self__, aad_auth_enabled=None, hostname=None, id=None, ip_address=None, local_auth_enabled=None, location=None, name=None, primary_access_key=None, primary_connection_string=None, public_network_access_enabled=None, public_port=None, resource_group_name=None, secondary_access_key=None, secondary_connection_string=None, server_port=None, serverless_connection_timeout_in_seconds=None, tags=None, tls_client_cert_enabled=None):
        if aad_auth_enabled and not isinstance(aad_auth_enabled, bool):
            raise TypeError("Expected argument 'aad_auth_enabled' to be a bool")
        pulumi.set(__self__, "aad_auth_enabled", aad_auth_enabled)
        if hostname and not isinstance(hostname, str):
            raise TypeError("Expected argument 'hostname' to be a str")
        pulumi.set(__self__, "hostname", hostname)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip_address and not isinstance(ip_address, str):
            raise TypeError("Expected argument 'ip_address' to be a str")
        pulumi.set(__self__, "ip_address", ip_address)
        if local_auth_enabled and not isinstance(local_auth_enabled, bool):
            raise TypeError("Expected argument 'local_auth_enabled' to be a bool")
        pulumi.set(__self__, "local_auth_enabled", local_auth_enabled)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if primary_access_key and not isinstance(primary_access_key, str):
            raise TypeError("Expected argument 'primary_access_key' to be a str")
        pulumi.set(__self__, "primary_access_key", primary_access_key)
        if primary_connection_string and not isinstance(primary_connection_string, str):
            raise TypeError("Expected argument 'primary_connection_string' to be a str")
        pulumi.set(__self__, "primary_connection_string", primary_connection_string)
        if public_network_access_enabled and not isinstance(public_network_access_enabled, bool):
            raise TypeError("Expected argument 'public_network_access_enabled' to be a bool")
        pulumi.set(__self__, "public_network_access_enabled", public_network_access_enabled)
        if public_port and not isinstance(public_port, int):
            raise TypeError("Expected argument 'public_port' to be a int")
        pulumi.set(__self__, "public_port", public_port)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if secondary_access_key and not isinstance(secondary_access_key, str):
            raise TypeError("Expected argument 'secondary_access_key' to be a str")
        pulumi.set(__self__, "secondary_access_key", secondary_access_key)
        if secondary_connection_string and not isinstance(secondary_connection_string, str):
            raise TypeError("Expected argument 'secondary_connection_string' to be a str")
        pulumi.set(__self__, "secondary_connection_string", secondary_connection_string)
        if server_port and not isinstance(server_port, int):
            raise TypeError("Expected argument 'server_port' to be a int")
        pulumi.set(__self__, "server_port", server_port)
        if serverless_connection_timeout_in_seconds and not isinstance(serverless_connection_timeout_in_seconds, int):
            raise TypeError("Expected argument 'serverless_connection_timeout_in_seconds' to be a int")
        pulumi.set(__self__, "serverless_connection_timeout_in_seconds", serverless_connection_timeout_in_seconds)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if tls_client_cert_enabled and not isinstance(tls_client_cert_enabled, bool):
            raise TypeError("Expected argument 'tls_client_cert_enabled' to be a bool")
        pulumi.set(__self__, "tls_client_cert_enabled", tls_client_cert_enabled)

    @property
    @pulumi.getter(name="aadAuthEnabled")
    def aad_auth_enabled(self) -> bool:
        """
        Is aad auth enabled for this SignalR service?
        """
        return pulumi.get(self, "aad_auth_enabled")

    @property
    @pulumi.getter
    def hostname(self) -> str:
        """
        The FQDN of the SignalR service.
        """
        return pulumi.get(self, "hostname")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> str:
        """
        The publicly accessible IP of the SignalR service.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter(name="localAuthEnabled")
    def local_auth_enabled(self) -> bool:
        """
        Is local auth enable for this SignalR serviced?
        """
        return pulumi.get(self, "local_auth_enabled")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Specifies the supported Azure location where the SignalR service exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="primaryAccessKey")
    def primary_access_key(self) -> str:
        """
        The primary access key of the SignalR service.
        """
        return pulumi.get(self, "primary_access_key")

    @property
    @pulumi.getter(name="primaryConnectionString")
    def primary_connection_string(self) -> str:
        """
        The primary connection string of the SignalR service.
        """
        return pulumi.get(self, "primary_connection_string")

    @property
    @pulumi.getter(name="publicNetworkAccessEnabled")
    def public_network_access_enabled(self) -> bool:
        """
        Is public network access enabled for this SignalR service?
        """
        return pulumi.get(self, "public_network_access_enabled")

    @property
    @pulumi.getter(name="publicPort")
    def public_port(self) -> int:
        """
        The publicly accessible port of the SignalR service which is designed for browser/client use.
        """
        return pulumi.get(self, "public_port")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="secondaryAccessKey")
    def secondary_access_key(self) -> str:
        """
        The secondary access key of the SignalR service.
        """
        return pulumi.get(self, "secondary_access_key")

    @property
    @pulumi.getter(name="secondaryConnectionString")
    def secondary_connection_string(self) -> str:
        """
        The secondary connection string of the SignalR service.
        """
        return pulumi.get(self, "secondary_connection_string")

    @property
    @pulumi.getter(name="serverPort")
    def server_port(self) -> int:
        """
        The publicly accessible port of the SignalR service which is designed for customer server side use.
        """
        return pulumi.get(self, "server_port")

    @property
    @pulumi.getter(name="serverlessConnectionTimeoutInSeconds")
    def serverless_connection_timeout_in_seconds(self) -> int:
        """
        The serverless connection timeout of this SignalR service.
        """
        return pulumi.get(self, "serverless_connection_timeout_in_seconds")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tlsClientCertEnabled")
    def tls_client_cert_enabled(self) -> bool:
        """
        Is tls client cert enabled for this SignalR service?
        """
        return pulumi.get(self, "tls_client_cert_enabled")


class AwaitableGetServiceResult(GetServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceResult(
            aad_auth_enabled=self.aad_auth_enabled,
            hostname=self.hostname,
            id=self.id,
            ip_address=self.ip_address,
            local_auth_enabled=self.local_auth_enabled,
            location=self.location,
            name=self.name,
            primary_access_key=self.primary_access_key,
            primary_connection_string=self.primary_connection_string,
            public_network_access_enabled=self.public_network_access_enabled,
            public_port=self.public_port,
            resource_group_name=self.resource_group_name,
            secondary_access_key=self.secondary_access_key,
            secondary_connection_string=self.secondary_connection_string,
            server_port=self.server_port,
            serverless_connection_timeout_in_seconds=self.serverless_connection_timeout_in_seconds,
            tags=self.tags,
            tls_client_cert_enabled=self.tls_client_cert_enabled)


def get_service(name: Optional[str] = None,
                resource_group_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceResult:
    """
    Use this data source to access information about an existing Azure SignalR service.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.signalr.get_service(name="test-signalr",
        resource_group_name="signalr-resource-group")
    ```


    :param str name: Specifies the name of the SignalR service.
    :param str resource_group_name: Specifies the name of the resource group the SignalR service is located in.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:signalr/getService:getService', __args__, opts=opts, typ=GetServiceResult).value

    return AwaitableGetServiceResult(
        aad_auth_enabled=pulumi.get(__ret__, 'aad_auth_enabled'),
        hostname=pulumi.get(__ret__, 'hostname'),
        id=pulumi.get(__ret__, 'id'),
        ip_address=pulumi.get(__ret__, 'ip_address'),
        local_auth_enabled=pulumi.get(__ret__, 'local_auth_enabled'),
        location=pulumi.get(__ret__, 'location'),
        name=pulumi.get(__ret__, 'name'),
        primary_access_key=pulumi.get(__ret__, 'primary_access_key'),
        primary_connection_string=pulumi.get(__ret__, 'primary_connection_string'),
        public_network_access_enabled=pulumi.get(__ret__, 'public_network_access_enabled'),
        public_port=pulumi.get(__ret__, 'public_port'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        secondary_access_key=pulumi.get(__ret__, 'secondary_access_key'),
        secondary_connection_string=pulumi.get(__ret__, 'secondary_connection_string'),
        server_port=pulumi.get(__ret__, 'server_port'),
        serverless_connection_timeout_in_seconds=pulumi.get(__ret__, 'serverless_connection_timeout_in_seconds'),
        tags=pulumi.get(__ret__, 'tags'),
        tls_client_cert_enabled=pulumi.get(__ret__, 'tls_client_cert_enabled'))
def get_service_output(name: Optional[pulumi.Input[str]] = None,
                       resource_group_name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServiceResult]:
    """
    Use this data source to access information about an existing Azure SignalR service.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.signalr.get_service(name="test-signalr",
        resource_group_name="signalr-resource-group")
    ```


    :param str name: Specifies the name of the SignalR service.
    :param str resource_group_name: Specifies the name of the resource group the SignalR service is located in.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:signalr/getService:getService', __args__, opts=opts, typ=GetServiceResult)
    return __ret__.apply(lambda __response__: GetServiceResult(
        aad_auth_enabled=pulumi.get(__response__, 'aad_auth_enabled'),
        hostname=pulumi.get(__response__, 'hostname'),
        id=pulumi.get(__response__, 'id'),
        ip_address=pulumi.get(__response__, 'ip_address'),
        local_auth_enabled=pulumi.get(__response__, 'local_auth_enabled'),
        location=pulumi.get(__response__, 'location'),
        name=pulumi.get(__response__, 'name'),
        primary_access_key=pulumi.get(__response__, 'primary_access_key'),
        primary_connection_string=pulumi.get(__response__, 'primary_connection_string'),
        public_network_access_enabled=pulumi.get(__response__, 'public_network_access_enabled'),
        public_port=pulumi.get(__response__, 'public_port'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        secondary_access_key=pulumi.get(__response__, 'secondary_access_key'),
        secondary_connection_string=pulumi.get(__response__, 'secondary_connection_string'),
        server_port=pulumi.get(__response__, 'server_port'),
        serverless_connection_timeout_in_seconds=pulumi.get(__response__, 'serverless_connection_timeout_in_seconds'),
        tags=pulumi.get(__response__, 'tags'),
        tls_client_cert_enabled=pulumi.get(__response__, 'tls_client_cert_enabled')))
