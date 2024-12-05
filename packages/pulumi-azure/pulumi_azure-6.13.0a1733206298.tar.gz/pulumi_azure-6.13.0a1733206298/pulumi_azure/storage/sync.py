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

__all__ = ['SyncArgs', 'Sync']

@pulumi.input_type
class SyncArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 incoming_traffic_policy: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Sync resource.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        :param pulumi.Input[str] incoming_traffic_policy: Incoming traffic policy. Possible values are `AllowAllTraffic` and `AllowVirtualNetworksOnly`. Defaults to `AllowAllTraffic`.
        :param pulumi.Input[str] location: The Azure Region where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        :param pulumi.Input[str] name: The name which should be used for this Storage Sync. Changing this forces a new Storage Sync to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Storage Sync.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if incoming_traffic_policy is not None:
            pulumi.set(__self__, "incoming_traffic_policy", incoming_traffic_policy)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="incomingTrafficPolicy")
    def incoming_traffic_policy(self) -> Optional[pulumi.Input[str]]:
        """
        Incoming traffic policy. Possible values are `AllowAllTraffic` and `AllowVirtualNetworksOnly`. Defaults to `AllowAllTraffic`.
        """
        return pulumi.get(self, "incoming_traffic_policy")

    @incoming_traffic_policy.setter
    def incoming_traffic_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "incoming_traffic_policy", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Storage Sync. Changing this forces a new Storage Sync to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Storage Sync.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _SyncState:
    def __init__(__self__, *,
                 incoming_traffic_policy: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 registered_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Sync resources.
        :param pulumi.Input[str] incoming_traffic_policy: Incoming traffic policy. Possible values are `AllowAllTraffic` and `AllowVirtualNetworksOnly`. Defaults to `AllowAllTraffic`.
        :param pulumi.Input[str] location: The Azure Region where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        :param pulumi.Input[str] name: The name which should be used for this Storage Sync. Changing this forces a new Storage Sync to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] registered_servers: A list of registered servers owned by this Storage Sync.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Storage Sync.
        """
        if incoming_traffic_policy is not None:
            pulumi.set(__self__, "incoming_traffic_policy", incoming_traffic_policy)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if registered_servers is not None:
            pulumi.set(__self__, "registered_servers", registered_servers)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="incomingTrafficPolicy")
    def incoming_traffic_policy(self) -> Optional[pulumi.Input[str]]:
        """
        Incoming traffic policy. Possible values are `AllowAllTraffic` and `AllowVirtualNetworksOnly`. Defaults to `AllowAllTraffic`.
        """
        return pulumi.get(self, "incoming_traffic_policy")

    @incoming_traffic_policy.setter
    def incoming_traffic_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "incoming_traffic_policy", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Storage Sync. Changing this forces a new Storage Sync to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="registeredServers")
    def registered_servers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of registered servers owned by this Storage Sync.
        """
        return pulumi.get(self, "registered_servers")

    @registered_servers.setter
    def registered_servers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "registered_servers", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Storage Sync.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class Sync(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 incoming_traffic_policy: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a Storage Sync.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_sync = azure.storage.Sync("example",
            name="example-storage-sync",
            resource_group_name=example.name,
            location=example.location,
            tags={
                "foo": "bar",
            })
        ```

        ## Import

        Storage Syncs can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:storage/sync:Sync example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.StorageSync/storageSyncServices/sync1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] incoming_traffic_policy: Incoming traffic policy. Possible values are `AllowAllTraffic` and `AllowVirtualNetworksOnly`. Defaults to `AllowAllTraffic`.
        :param pulumi.Input[str] location: The Azure Region where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        :param pulumi.Input[str] name: The name which should be used for this Storage Sync. Changing this forces a new Storage Sync to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Storage Sync.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SyncArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Storage Sync.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_sync = azure.storage.Sync("example",
            name="example-storage-sync",
            resource_group_name=example.name,
            location=example.location,
            tags={
                "foo": "bar",
            })
        ```

        ## Import

        Storage Syncs can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:storage/sync:Sync example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.StorageSync/storageSyncServices/sync1
        ```

        :param str resource_name: The name of the resource.
        :param SyncArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SyncArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 incoming_traffic_policy: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SyncArgs.__new__(SyncArgs)

            __props__.__dict__["incoming_traffic_policy"] = incoming_traffic_policy
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["registered_servers"] = None
        super(Sync, __self__).__init__(
            'azure:storage/sync:Sync',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            incoming_traffic_policy: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            registered_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Sync':
        """
        Get an existing Sync resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] incoming_traffic_policy: Incoming traffic policy. Possible values are `AllowAllTraffic` and `AllowVirtualNetworksOnly`. Defaults to `AllowAllTraffic`.
        :param pulumi.Input[str] location: The Azure Region where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        :param pulumi.Input[str] name: The name which should be used for this Storage Sync. Changing this forces a new Storage Sync to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] registered_servers: A list of registered servers owned by this Storage Sync.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Storage Sync.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SyncState.__new__(_SyncState)

        __props__.__dict__["incoming_traffic_policy"] = incoming_traffic_policy
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["registered_servers"] = registered_servers
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["tags"] = tags
        return Sync(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="incomingTrafficPolicy")
    def incoming_traffic_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Incoming traffic policy. Possible values are `AllowAllTraffic` and `AllowVirtualNetworksOnly`. Defaults to `AllowAllTraffic`.
        """
        return pulumi.get(self, "incoming_traffic_policy")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure Region where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Storage Sync. Changing this forces a new Storage Sync to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="registeredServers")
    def registered_servers(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of registered servers owned by this Storage Sync.
        """
        return pulumi.get(self, "registered_servers")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Storage Sync should exist. Changing this forces a new Storage Sync to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to the Storage Sync.
        """
        return pulumi.get(self, "tags")

