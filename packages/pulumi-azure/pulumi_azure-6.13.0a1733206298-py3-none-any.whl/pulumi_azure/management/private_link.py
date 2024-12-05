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

__all__ = ['PrivateLinkArgs', 'PrivateLink']

@pulumi.input_type
class PrivateLinkArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PrivateLink resource.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group within which this Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        :param pulumi.Input[str] location: The Azure Region where the Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        :param pulumi.Input[str] name: Specifies the name of this Resource Management Private Link. Changing this forces a new Resource Management Private Link to be created.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the Resource Group within which this Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of this Resource Management Private Link. Changing this forces a new Resource Management Private Link to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _PrivateLinkState:
    def __init__(__self__, *,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PrivateLink resources.
        :param pulumi.Input[str] location: The Azure Region where the Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        :param pulumi.Input[str] name: Specifies the name of this Resource Management Private Link. Changing this forces a new Resource Management Private Link to be created.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group within which this Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        """
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of this Resource Management Private Link. Changing this forces a new Resource Management Private Link to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Resource Group within which this Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)


class PrivateLink(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Resource Management Private Link to restrict access for managing resources in the tenant.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_private_link = azure.management.PrivateLink("example",
            name="example",
            resource_group_name=example.name,
            location=example.location)
        ```

        ## Import

        An existing Resource Management Private Link can be imported into Pulumi using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:management/privateLink:PrivateLink example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg1/providers/Microsoft.Authorization/resourceManagementPrivateLinks/link1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The Azure Region where the Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        :param pulumi.Input[str] name: Specifies the name of this Resource Management Private Link. Changing this forces a new Resource Management Private Link to be created.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group within which this Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PrivateLinkArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Resource Management Private Link to restrict access for managing resources in the tenant.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_private_link = azure.management.PrivateLink("example",
            name="example",
            resource_group_name=example.name,
            location=example.location)
        ```

        ## Import

        An existing Resource Management Private Link can be imported into Pulumi using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:management/privateLink:PrivateLink example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg1/providers/Microsoft.Authorization/resourceManagementPrivateLinks/link1
        ```

        :param str resource_name: The name of the resource.
        :param PrivateLinkArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PrivateLinkArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PrivateLinkArgs.__new__(PrivateLinkArgs)

            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
        super(PrivateLink, __self__).__init__(
            'azure:management/privateLink:PrivateLink',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None) -> 'PrivateLink':
        """
        Get an existing PrivateLink resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The Azure Region where the Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        :param pulumi.Input[str] name: Specifies the name of this Resource Management Private Link. Changing this forces a new Resource Management Private Link to be created.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group within which this Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PrivateLinkState.__new__(_PrivateLinkState)

        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        return PrivateLink(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure Region where the Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of this Resource Management Private Link. Changing this forces a new Resource Management Private Link to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Resource Group within which this Resource Management Private Link should exist. Changing this forces a new Resource Management Private Link to be created.
        """
        return pulumi.get(self, "resource_group_name")

