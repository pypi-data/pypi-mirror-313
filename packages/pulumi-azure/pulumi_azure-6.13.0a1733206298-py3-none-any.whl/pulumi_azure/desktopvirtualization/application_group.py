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

__all__ = ['ApplicationGroupArgs', 'ApplicationGroup']

@pulumi.input_type
class ApplicationGroupArgs:
    def __init__(__self__, *,
                 host_pool_id: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 type: pulumi.Input[str],
                 default_desktop_display_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ApplicationGroup resource.
        :param pulumi.Input[str] host_pool_id: Resource ID for a Virtual Desktop Host Pool to associate with the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Virtual Desktop Application Group. Changing this forces a new resource to be created.
        :param pulumi.Input[str] type: Type of Virtual Desktop Application Group. Valid options are `RemoteApp` or `Desktop` application groups. Changing this forces a new resource to be created.
        :param pulumi.Input[str] default_desktop_display_name: Option to set the display name for the default sessionDesktop desktop when `type` is set to `Desktop`. A value here is mandatory for connections to the desktop using the Windows 365 portal. Without it the connection will hang at 'Loading Client'.
        :param pulumi.Input[str] description: Option to set a description for the Virtual Desktop Application Group.
        :param pulumi.Input[str] friendly_name: Option to set a friendly name for the Virtual Desktop Application Group.
        :param pulumi.Input[str] location: The location/region where the Virtual Desktop Application Group is located. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, "host_pool_id", host_pool_id)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "type", type)
        if default_desktop_display_name is not None:
            pulumi.set(__self__, "default_desktop_display_name", default_desktop_display_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if friendly_name is not None:
            pulumi.set(__self__, "friendly_name", friendly_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="hostPoolId")
    def host_pool_id(self) -> pulumi.Input[str]:
        """
        Resource ID for a Virtual Desktop Host Pool to associate with the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        """
        return pulumi.get(self, "host_pool_id")

    @host_pool_id.setter
    def host_pool_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "host_pool_id", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which to create the Virtual Desktop Application Group. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Type of Virtual Desktop Application Group. Valid options are `RemoteApp` or `Desktop` application groups. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="defaultDesktopDisplayName")
    def default_desktop_display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Option to set the display name for the default sessionDesktop desktop when `type` is set to `Desktop`. A value here is mandatory for connections to the desktop using the Windows 365 portal. Without it the connection will hang at 'Loading Client'.
        """
        return pulumi.get(self, "default_desktop_display_name")

    @default_desktop_display_name.setter
    def default_desktop_display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_desktop_display_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Option to set a description for the Virtual Desktop Application Group.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> Optional[pulumi.Input[str]]:
        """
        Option to set a friendly name for the Virtual Desktop Application Group.
        """
        return pulumi.get(self, "friendly_name")

    @friendly_name.setter
    def friendly_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "friendly_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location/region where the Virtual Desktop Application Group is located. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ApplicationGroupState:
    def __init__(__self__, *,
                 default_desktop_display_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 host_pool_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ApplicationGroup resources.
        :param pulumi.Input[str] default_desktop_display_name: Option to set the display name for the default sessionDesktop desktop when `type` is set to `Desktop`. A value here is mandatory for connections to the desktop using the Windows 365 portal. Without it the connection will hang at 'Loading Client'.
        :param pulumi.Input[str] description: Option to set a description for the Virtual Desktop Application Group.
        :param pulumi.Input[str] friendly_name: Option to set a friendly name for the Virtual Desktop Application Group.
        :param pulumi.Input[str] host_pool_id: Resource ID for a Virtual Desktop Host Pool to associate with the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        :param pulumi.Input[str] location: The location/region where the Virtual Desktop Application Group is located. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Virtual Desktop Application Group. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] type: Type of Virtual Desktop Application Group. Valid options are `RemoteApp` or `Desktop` application groups. Changing this forces a new resource to be created.
        """
        if default_desktop_display_name is not None:
            pulumi.set(__self__, "default_desktop_display_name", default_desktop_display_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if friendly_name is not None:
            pulumi.set(__self__, "friendly_name", friendly_name)
        if host_pool_id is not None:
            pulumi.set(__self__, "host_pool_id", host_pool_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="defaultDesktopDisplayName")
    def default_desktop_display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Option to set the display name for the default sessionDesktop desktop when `type` is set to `Desktop`. A value here is mandatory for connections to the desktop using the Windows 365 portal. Without it the connection will hang at 'Loading Client'.
        """
        return pulumi.get(self, "default_desktop_display_name")

    @default_desktop_display_name.setter
    def default_desktop_display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_desktop_display_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Option to set a description for the Virtual Desktop Application Group.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> Optional[pulumi.Input[str]]:
        """
        Option to set a friendly name for the Virtual Desktop Application Group.
        """
        return pulumi.get(self, "friendly_name")

    @friendly_name.setter
    def friendly_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "friendly_name", value)

    @property
    @pulumi.getter(name="hostPoolId")
    def host_pool_id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID for a Virtual Desktop Host Pool to associate with the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        """
        return pulumi.get(self, "host_pool_id")

    @host_pool_id.setter
    def host_pool_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_pool_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location/region where the Virtual Desktop Application Group is located. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which to create the Virtual Desktop Application Group. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of Virtual Desktop Application Group. Valid options are `RemoteApp` or `Desktop` application groups. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class ApplicationGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 default_desktop_display_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 host_pool_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Virtual Desktop Application Group.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="rg-example-virtualdesktop",
            location="West Europe")
        pooledbreadthfirst = azure.desktopvirtualization.HostPool("pooledbreadthfirst",
            name="pooledbreadthfirst",
            location=example.location,
            resource_group_name=example.name,
            type="Pooled",
            load_balancer_type="BreadthFirst")
        personalautomatic = azure.desktopvirtualization.HostPool("personalautomatic",
            name="personalautomatic",
            location=example.location,
            resource_group_name=example.name,
            type="Personal",
            personal_desktop_assignment_type="Automatic",
            load_balancer_type="BreadthFirst")
        remoteapp = azure.desktopvirtualization.ApplicationGroup("remoteapp",
            name="acctag",
            location=example.location,
            resource_group_name=example.name,
            type="RemoteApp",
            host_pool_id=pooledbreadthfirst.id,
            friendly_name="TestAppGroup",
            description="Acceptance Test: An application group")
        desktopapp = azure.desktopvirtualization.ApplicationGroup("desktopapp",
            name="appgroupdesktop",
            location=example.location,
            resource_group_name=example.name,
            type="Desktop",
            host_pool_id=personalautomatic.id,
            friendly_name="TestAppGroup",
            description="Acceptance Test: An application group")
        ```

        ## Import

        Virtual Desktop Application Groups can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:desktopvirtualization/applicationGroup:ApplicationGroup example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myGroup1/providers/Microsoft.DesktopVirtualization/applicationGroups/myapplicationgroup
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] default_desktop_display_name: Option to set the display name for the default sessionDesktop desktop when `type` is set to `Desktop`. A value here is mandatory for connections to the desktop using the Windows 365 portal. Without it the connection will hang at 'Loading Client'.
        :param pulumi.Input[str] description: Option to set a description for the Virtual Desktop Application Group.
        :param pulumi.Input[str] friendly_name: Option to set a friendly name for the Virtual Desktop Application Group.
        :param pulumi.Input[str] host_pool_id: Resource ID for a Virtual Desktop Host Pool to associate with the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        :param pulumi.Input[str] location: The location/region where the Virtual Desktop Application Group is located. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Virtual Desktop Application Group. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] type: Type of Virtual Desktop Application Group. Valid options are `RemoteApp` or `Desktop` application groups. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApplicationGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Virtual Desktop Application Group.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="rg-example-virtualdesktop",
            location="West Europe")
        pooledbreadthfirst = azure.desktopvirtualization.HostPool("pooledbreadthfirst",
            name="pooledbreadthfirst",
            location=example.location,
            resource_group_name=example.name,
            type="Pooled",
            load_balancer_type="BreadthFirst")
        personalautomatic = azure.desktopvirtualization.HostPool("personalautomatic",
            name="personalautomatic",
            location=example.location,
            resource_group_name=example.name,
            type="Personal",
            personal_desktop_assignment_type="Automatic",
            load_balancer_type="BreadthFirst")
        remoteapp = azure.desktopvirtualization.ApplicationGroup("remoteapp",
            name="acctag",
            location=example.location,
            resource_group_name=example.name,
            type="RemoteApp",
            host_pool_id=pooledbreadthfirst.id,
            friendly_name="TestAppGroup",
            description="Acceptance Test: An application group")
        desktopapp = azure.desktopvirtualization.ApplicationGroup("desktopapp",
            name="appgroupdesktop",
            location=example.location,
            resource_group_name=example.name,
            type="Desktop",
            host_pool_id=personalautomatic.id,
            friendly_name="TestAppGroup",
            description="Acceptance Test: An application group")
        ```

        ## Import

        Virtual Desktop Application Groups can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:desktopvirtualization/applicationGroup:ApplicationGroup example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myGroup1/providers/Microsoft.DesktopVirtualization/applicationGroups/myapplicationgroup
        ```

        :param str resource_name: The name of the resource.
        :param ApplicationGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplicationGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 default_desktop_display_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 host_pool_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApplicationGroupArgs.__new__(ApplicationGroupArgs)

            __props__.__dict__["default_desktop_display_name"] = default_desktop_display_name
            __props__.__dict__["description"] = description
            __props__.__dict__["friendly_name"] = friendly_name
            if host_pool_id is None and not opts.urn:
                raise TypeError("Missing required property 'host_pool_id'")
            __props__.__dict__["host_pool_id"] = host_pool_id
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
        super(ApplicationGroup, __self__).__init__(
            'azure:desktopvirtualization/applicationGroup:ApplicationGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            default_desktop_display_name: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            friendly_name: Optional[pulumi.Input[str]] = None,
            host_pool_id: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'ApplicationGroup':
        """
        Get an existing ApplicationGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] default_desktop_display_name: Option to set the display name for the default sessionDesktop desktop when `type` is set to `Desktop`. A value here is mandatory for connections to the desktop using the Windows 365 portal. Without it the connection will hang at 'Loading Client'.
        :param pulumi.Input[str] description: Option to set a description for the Virtual Desktop Application Group.
        :param pulumi.Input[str] friendly_name: Option to set a friendly name for the Virtual Desktop Application Group.
        :param pulumi.Input[str] host_pool_id: Resource ID for a Virtual Desktop Host Pool to associate with the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        :param pulumi.Input[str] location: The location/region where the Virtual Desktop Application Group is located. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Virtual Desktop Application Group. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] type: Type of Virtual Desktop Application Group. Valid options are `RemoteApp` or `Desktop` application groups. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ApplicationGroupState.__new__(_ApplicationGroupState)

        __props__.__dict__["default_desktop_display_name"] = default_desktop_display_name
        __props__.__dict__["description"] = description
        __props__.__dict__["friendly_name"] = friendly_name
        __props__.__dict__["host_pool_id"] = host_pool_id
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["type"] = type
        return ApplicationGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="defaultDesktopDisplayName")
    def default_desktop_display_name(self) -> pulumi.Output[Optional[str]]:
        """
        Option to set the display name for the default sessionDesktop desktop when `type` is set to `Desktop`. A value here is mandatory for connections to the desktop using the Windows 365 portal. Without it the connection will hang at 'Loading Client'.
        """
        return pulumi.get(self, "default_desktop_display_name")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Option to set a description for the Virtual Desktop Application Group.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> pulumi.Output[Optional[str]]:
        """
        Option to set a friendly name for the Virtual Desktop Application Group.
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="hostPoolId")
    def host_pool_id(self) -> pulumi.Output[str]:
        """
        Resource ID for a Virtual Desktop Host Pool to associate with the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        """
        return pulumi.get(self, "host_pool_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location/region where the Virtual Desktop Application Group is located. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Virtual Desktop Application Group. Changing the name forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which to create the Virtual Desktop Application Group. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of Virtual Desktop Application Group. Valid options are `RemoteApp` or `Desktop` application groups. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "type")

