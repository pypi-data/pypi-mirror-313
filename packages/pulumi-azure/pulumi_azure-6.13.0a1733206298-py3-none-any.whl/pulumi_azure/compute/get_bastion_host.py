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
    'GetBastionHostResult',
    'AwaitableGetBastionHostResult',
    'get_bastion_host',
    'get_bastion_host_output',
]

@pulumi.output_type
class GetBastionHostResult:
    """
    A collection of values returned by getBastionHost.
    """
    def __init__(__self__, copy_paste_enabled=None, dns_name=None, file_copy_enabled=None, id=None, ip_configurations=None, ip_connect_enabled=None, location=None, name=None, resource_group_name=None, scale_units=None, session_recording_enabled=None, shareable_link_enabled=None, sku=None, tags=None, tunneling_enabled=None, zones=None):
        if copy_paste_enabled and not isinstance(copy_paste_enabled, bool):
            raise TypeError("Expected argument 'copy_paste_enabled' to be a bool")
        pulumi.set(__self__, "copy_paste_enabled", copy_paste_enabled)
        if dns_name and not isinstance(dns_name, str):
            raise TypeError("Expected argument 'dns_name' to be a str")
        pulumi.set(__self__, "dns_name", dns_name)
        if file_copy_enabled and not isinstance(file_copy_enabled, bool):
            raise TypeError("Expected argument 'file_copy_enabled' to be a bool")
        pulumi.set(__self__, "file_copy_enabled", file_copy_enabled)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip_configurations and not isinstance(ip_configurations, list):
            raise TypeError("Expected argument 'ip_configurations' to be a list")
        pulumi.set(__self__, "ip_configurations", ip_configurations)
        if ip_connect_enabled and not isinstance(ip_connect_enabled, bool):
            raise TypeError("Expected argument 'ip_connect_enabled' to be a bool")
        pulumi.set(__self__, "ip_connect_enabled", ip_connect_enabled)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if scale_units and not isinstance(scale_units, int):
            raise TypeError("Expected argument 'scale_units' to be a int")
        pulumi.set(__self__, "scale_units", scale_units)
        if session_recording_enabled and not isinstance(session_recording_enabled, bool):
            raise TypeError("Expected argument 'session_recording_enabled' to be a bool")
        pulumi.set(__self__, "session_recording_enabled", session_recording_enabled)
        if shareable_link_enabled and not isinstance(shareable_link_enabled, bool):
            raise TypeError("Expected argument 'shareable_link_enabled' to be a bool")
        pulumi.set(__self__, "shareable_link_enabled", shareable_link_enabled)
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        pulumi.set(__self__, "sku", sku)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if tunneling_enabled and not isinstance(tunneling_enabled, bool):
            raise TypeError("Expected argument 'tunneling_enabled' to be a bool")
        pulumi.set(__self__, "tunneling_enabled", tunneling_enabled)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="copyPasteEnabled")
    def copy_paste_enabled(self) -> bool:
        """
        Is Copy/Paste feature enabled for the Bastion Host.
        """
        return pulumi.get(self, "copy_paste_enabled")

    @property
    @pulumi.getter(name="dnsName")
    def dns_name(self) -> str:
        """
        The FQDN for the Bastion Host.
        """
        return pulumi.get(self, "dns_name")

    @property
    @pulumi.getter(name="fileCopyEnabled")
    def file_copy_enabled(self) -> bool:
        """
        Is File Copy feature enabled for the Bastion Host.
        """
        return pulumi.get(self, "file_copy_enabled")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipConfigurations")
    def ip_configurations(self) -> Sequence['outputs.GetBastionHostIpConfigurationResult']:
        """
        A `ip_configuration` block as defined below.
        """
        return pulumi.get(self, "ip_configurations")

    @property
    @pulumi.getter(name="ipConnectEnabled")
    def ip_connect_enabled(self) -> bool:
        """
        Is IP Connect feature enabled for the Bastion Host.
        """
        return pulumi.get(self, "ip_connect_enabled")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure Region where the Bastion Host exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the IP configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="scaleUnits")
    def scale_units(self) -> int:
        """
        The number of scale units provisioned for the Bastion Host.
        """
        return pulumi.get(self, "scale_units")

    @property
    @pulumi.getter(name="sessionRecordingEnabled")
    def session_recording_enabled(self) -> bool:
        """
        Is Session Recording feature enabled for the Bastion Host.
        """
        return pulumi.get(self, "session_recording_enabled")

    @property
    @pulumi.getter(name="shareableLinkEnabled")
    def shareable_link_enabled(self) -> bool:
        """
        Is Shareable Link feature enabled for the Bastion Host.
        """
        return pulumi.get(self, "shareable_link_enabled")

    @property
    @pulumi.getter
    def sku(self) -> str:
        """
        The SKU of the Bastion Host.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the Bastion Host.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tunnelingEnabled")
    def tunneling_enabled(self) -> bool:
        """
        Is Tunneling feature enabled for the Bastion Host.
        """
        return pulumi.get(self, "tunneling_enabled")

    @property
    @pulumi.getter
    def zones(self) -> Sequence[str]:
        """
        A list of Availability Zones in which this Bastion Host is located.
        """
        return pulumi.get(self, "zones")


class AwaitableGetBastionHostResult(GetBastionHostResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBastionHostResult(
            copy_paste_enabled=self.copy_paste_enabled,
            dns_name=self.dns_name,
            file_copy_enabled=self.file_copy_enabled,
            id=self.id,
            ip_configurations=self.ip_configurations,
            ip_connect_enabled=self.ip_connect_enabled,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            scale_units=self.scale_units,
            session_recording_enabled=self.session_recording_enabled,
            shareable_link_enabled=self.shareable_link_enabled,
            sku=self.sku,
            tags=self.tags,
            tunneling_enabled=self.tunneling_enabled,
            zones=self.zones)


def get_bastion_host(name: Optional[str] = None,
                     resource_group_name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBastionHostResult:
    """
    Use this data source to access information about an existing Bastion Host.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.compute.get_bastion_host(name="existing-bastion",
        resource_group_name="existing-resources")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of the Bastion Host.
    :param str resource_group_name: The name of the Resource Group where the Bastion Host exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:compute/getBastionHost:getBastionHost', __args__, opts=opts, typ=GetBastionHostResult).value

    return AwaitableGetBastionHostResult(
        copy_paste_enabled=pulumi.get(__ret__, 'copy_paste_enabled'),
        dns_name=pulumi.get(__ret__, 'dns_name'),
        file_copy_enabled=pulumi.get(__ret__, 'file_copy_enabled'),
        id=pulumi.get(__ret__, 'id'),
        ip_configurations=pulumi.get(__ret__, 'ip_configurations'),
        ip_connect_enabled=pulumi.get(__ret__, 'ip_connect_enabled'),
        location=pulumi.get(__ret__, 'location'),
        name=pulumi.get(__ret__, 'name'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        scale_units=pulumi.get(__ret__, 'scale_units'),
        session_recording_enabled=pulumi.get(__ret__, 'session_recording_enabled'),
        shareable_link_enabled=pulumi.get(__ret__, 'shareable_link_enabled'),
        sku=pulumi.get(__ret__, 'sku'),
        tags=pulumi.get(__ret__, 'tags'),
        tunneling_enabled=pulumi.get(__ret__, 'tunneling_enabled'),
        zones=pulumi.get(__ret__, 'zones'))
def get_bastion_host_output(name: Optional[pulumi.Input[str]] = None,
                            resource_group_name: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBastionHostResult]:
    """
    Use this data source to access information about an existing Bastion Host.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.compute.get_bastion_host(name="existing-bastion",
        resource_group_name="existing-resources")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of the Bastion Host.
    :param str resource_group_name: The name of the Resource Group where the Bastion Host exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:compute/getBastionHost:getBastionHost', __args__, opts=opts, typ=GetBastionHostResult)
    return __ret__.apply(lambda __response__: GetBastionHostResult(
        copy_paste_enabled=pulumi.get(__response__, 'copy_paste_enabled'),
        dns_name=pulumi.get(__response__, 'dns_name'),
        file_copy_enabled=pulumi.get(__response__, 'file_copy_enabled'),
        id=pulumi.get(__response__, 'id'),
        ip_configurations=pulumi.get(__response__, 'ip_configurations'),
        ip_connect_enabled=pulumi.get(__response__, 'ip_connect_enabled'),
        location=pulumi.get(__response__, 'location'),
        name=pulumi.get(__response__, 'name'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        scale_units=pulumi.get(__response__, 'scale_units'),
        session_recording_enabled=pulumi.get(__response__, 'session_recording_enabled'),
        shareable_link_enabled=pulumi.get(__response__, 'shareable_link_enabled'),
        sku=pulumi.get(__response__, 'sku'),
        tags=pulumi.get(__response__, 'tags'),
        tunneling_enabled=pulumi.get(__response__, 'tunneling_enabled'),
        zones=pulumi.get(__response__, 'zones')))
