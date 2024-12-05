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

__all__ = ['UserAssignedIdentityArgs', 'UserAssignedIdentity']

@pulumi.input_type
class UserAssignedIdentityArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a UserAssignedIdentity resource.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group within which this User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        :param pulumi.Input[str] location: The Azure Region where the User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        :param pulumi.Input[str] name: Specifies the name of this User Assigned Identity. Changing this forces a new User Assigned Identity to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the User Assigned Identity.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
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
        Specifies the name of the Resource Group within which this User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of this User Assigned Identity. Changing this forces a new User Assigned Identity to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the User Assigned Identity.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _UserAssignedIdentityState:
    def __init__(__self__, *,
                 client_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering UserAssignedIdentity resources.
        :param pulumi.Input[str] client_id: The ID of the app associated with the Identity.
        :param pulumi.Input[str] location: The Azure Region where the User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        :param pulumi.Input[str] name: Specifies the name of this User Assigned Identity. Changing this forces a new User Assigned Identity to be created.
        :param pulumi.Input[str] principal_id: The ID of the Service Principal object associated with the created Identity.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group within which this User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the User Assigned Identity.
        :param pulumi.Input[str] tenant_id: The ID of the Tenant which the Identity belongs to.
        """
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the app associated with the Identity.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of this User Assigned Identity. Changing this forces a new User Assigned Identity to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Service Principal object associated with the created Identity.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Resource Group within which this User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the User Assigned Identity.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Tenant which the Identity belongs to.
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)


class UserAssignedIdentity(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        <!-- Note: This documentation is generated. Any manual changes will be overwritten -->

        Manages a User Assigned Identity.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_user_assigned_identity = azure.authorization.UserAssignedIdentity("example",
            location=example.location,
            name="example",
            resource_group_name=example.name)
        ```

        ## Import

        An existing User Assigned Identity can be imported into Pulumi using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:authorization/userAssignedIdentity:UserAssignedIdentity example /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{userAssignedIdentityName}
        ```

        * Where `{subscriptionId}` is the ID of the Azure Subscription where the User Assigned Identity exists. For example `12345678-1234-9876-4563-123456789012`.

        * Where `{resourceGroupName}` is the name of Resource Group where this User Assigned Identity exists. For example `example-resource-group`.

        * Where `{userAssignedIdentityName}` is the name of the User Assigned Identity. For example `userAssignedIdentityValue`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The Azure Region where the User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        :param pulumi.Input[str] name: Specifies the name of this User Assigned Identity. Changing this forces a new User Assigned Identity to be created.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group within which this User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the User Assigned Identity.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserAssignedIdentityArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        <!-- Note: This documentation is generated. Any manual changes will be overwritten -->

        Manages a User Assigned Identity.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_user_assigned_identity = azure.authorization.UserAssignedIdentity("example",
            location=example.location,
            name="example",
            resource_group_name=example.name)
        ```

        ## Import

        An existing User Assigned Identity can be imported into Pulumi using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:authorization/userAssignedIdentity:UserAssignedIdentity example /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{userAssignedIdentityName}
        ```

        * Where `{subscriptionId}` is the ID of the Azure Subscription where the User Assigned Identity exists. For example `12345678-1234-9876-4563-123456789012`.

        * Where `{resourceGroupName}` is the name of Resource Group where this User Assigned Identity exists. For example `example-resource-group`.

        * Where `{userAssignedIdentityName}` is the name of the User Assigned Identity. For example `userAssignedIdentityValue`.

        :param str resource_name: The name of the resource.
        :param UserAssignedIdentityArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserAssignedIdentityArgs, pulumi.ResourceOptions, *args, **kwargs)
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
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserAssignedIdentityArgs.__new__(UserAssignedIdentityArgs)

            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["client_id"] = None
            __props__.__dict__["principal_id"] = None
            __props__.__dict__["tenant_id"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure:msi/userAssignedIdentity:UserAssignedIdentity")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(UserAssignedIdentity, __self__).__init__(
            'azure:authorization/userAssignedIdentity:UserAssignedIdentity',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            client_id: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            principal_id: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tenant_id: Optional[pulumi.Input[str]] = None) -> 'UserAssignedIdentity':
        """
        Get an existing UserAssignedIdentity resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] client_id: The ID of the app associated with the Identity.
        :param pulumi.Input[str] location: The Azure Region where the User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        :param pulumi.Input[str] name: Specifies the name of this User Assigned Identity. Changing this forces a new User Assigned Identity to be created.
        :param pulumi.Input[str] principal_id: The ID of the Service Principal object associated with the created Identity.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group within which this User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the User Assigned Identity.
        :param pulumi.Input[str] tenant_id: The ID of the Tenant which the Identity belongs to.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserAssignedIdentityState.__new__(_UserAssignedIdentityState)

        __props__.__dict__["client_id"] = client_id
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["principal_id"] = principal_id
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tenant_id"] = tenant_id
        return UserAssignedIdentity(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Output[str]:
        """
        The ID of the app associated with the Identity.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure Region where the User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of this User Assigned Identity. Changing this forces a new User Assigned Identity to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> pulumi.Output[str]:
        """
        The ID of the Service Principal object associated with the created Identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Resource Group within which this User Assigned Identity should exist. Changing this forces a new User Assigned Identity to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to the User Assigned Identity.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> pulumi.Output[str]:
        """
        The ID of the Tenant which the Identity belongs to.
        """
        return pulumi.get(self, "tenant_id")

