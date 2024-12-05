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
from ._inputs import *

__all__ = ['AssignmentDynamicScopeArgs', 'AssignmentDynamicScope']

@pulumi.input_type
class AssignmentDynamicScopeArgs:
    def __init__(__self__, *,
                 filter: pulumi.Input['AssignmentDynamicScopeFilterArgs'],
                 maintenance_configuration_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AssignmentDynamicScope resource.
        :param pulumi.Input['AssignmentDynamicScopeFilterArgs'] filter: A `filter` block as defined below.
        :param pulumi.Input[str] maintenance_configuration_id: The ID of the Maintenance Configuration Resource. Changing this forces a new Dynamic Maintenance Assignment to be created.
        :param pulumi.Input[str] name: The name which should be used for this Dynamic Maintenance Assignment. Changing this forces a new Dynamic Maintenance Assignment to be created.
               
               > **Note:** The `name` must be unique per subscription.
        """
        pulumi.set(__self__, "filter", filter)
        pulumi.set(__self__, "maintenance_configuration_id", maintenance_configuration_id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Input['AssignmentDynamicScopeFilterArgs']:
        """
        A `filter` block as defined below.
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: pulumi.Input['AssignmentDynamicScopeFilterArgs']):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> pulumi.Input[str]:
        """
        The ID of the Maintenance Configuration Resource. Changing this forces a new Dynamic Maintenance Assignment to be created.
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @maintenance_configuration_id.setter
    def maintenance_configuration_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "maintenance_configuration_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Dynamic Maintenance Assignment. Changing this forces a new Dynamic Maintenance Assignment to be created.

        > **Note:** The `name` must be unique per subscription.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _AssignmentDynamicScopeState:
    def __init__(__self__, *,
                 filter: Optional[pulumi.Input['AssignmentDynamicScopeFilterArgs']] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AssignmentDynamicScope resources.
        :param pulumi.Input['AssignmentDynamicScopeFilterArgs'] filter: A `filter` block as defined below.
        :param pulumi.Input[str] maintenance_configuration_id: The ID of the Maintenance Configuration Resource. Changing this forces a new Dynamic Maintenance Assignment to be created.
        :param pulumi.Input[str] name: The name which should be used for this Dynamic Maintenance Assignment. Changing this forces a new Dynamic Maintenance Assignment to be created.
               
               > **Note:** The `name` must be unique per subscription.
        """
        if filter is not None:
            pulumi.set(__self__, "filter", filter)
        if maintenance_configuration_id is not None:
            pulumi.set(__self__, "maintenance_configuration_id", maintenance_configuration_id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input['AssignmentDynamicScopeFilterArgs']]:
        """
        A `filter` block as defined below.
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: Optional[pulumi.Input['AssignmentDynamicScopeFilterArgs']]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Maintenance Configuration Resource. Changing this forces a new Dynamic Maintenance Assignment to be created.
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @maintenance_configuration_id.setter
    def maintenance_configuration_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "maintenance_configuration_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Dynamic Maintenance Assignment. Changing this forces a new Dynamic Maintenance Assignment to be created.

        > **Note:** The `name` must be unique per subscription.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class AssignmentDynamicScope(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 filter: Optional[pulumi.Input[Union['AssignmentDynamicScopeFilterArgs', 'AssignmentDynamicScopeFilterArgsDict']]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Dynamic Maintenance Assignment.

        > **Note:** Only valid for `InGuestPatch` Maintenance Configuration Scopes.

        ## Import

        Dynamic Maintenance Assignments can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:maintenance/assignmentDynamicScope:AssignmentDynamicScope example /subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.Maintenance/configurationAssignments/assignmentName
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['AssignmentDynamicScopeFilterArgs', 'AssignmentDynamicScopeFilterArgsDict']] filter: A `filter` block as defined below.
        :param pulumi.Input[str] maintenance_configuration_id: The ID of the Maintenance Configuration Resource. Changing this forces a new Dynamic Maintenance Assignment to be created.
        :param pulumi.Input[str] name: The name which should be used for this Dynamic Maintenance Assignment. Changing this forces a new Dynamic Maintenance Assignment to be created.
               
               > **Note:** The `name` must be unique per subscription.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AssignmentDynamicScopeArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Dynamic Maintenance Assignment.

        > **Note:** Only valid for `InGuestPatch` Maintenance Configuration Scopes.

        ## Import

        Dynamic Maintenance Assignments can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:maintenance/assignmentDynamicScope:AssignmentDynamicScope example /subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.Maintenance/configurationAssignments/assignmentName
        ```

        :param str resource_name: The name of the resource.
        :param AssignmentDynamicScopeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AssignmentDynamicScopeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 filter: Optional[pulumi.Input[Union['AssignmentDynamicScopeFilterArgs', 'AssignmentDynamicScopeFilterArgsDict']]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AssignmentDynamicScopeArgs.__new__(AssignmentDynamicScopeArgs)

            if filter is None and not opts.urn:
                raise TypeError("Missing required property 'filter'")
            __props__.__dict__["filter"] = filter
            if maintenance_configuration_id is None and not opts.urn:
                raise TypeError("Missing required property 'maintenance_configuration_id'")
            __props__.__dict__["maintenance_configuration_id"] = maintenance_configuration_id
            __props__.__dict__["name"] = name
        super(AssignmentDynamicScope, __self__).__init__(
            'azure:maintenance/assignmentDynamicScope:AssignmentDynamicScope',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            filter: Optional[pulumi.Input[Union['AssignmentDynamicScopeFilterArgs', 'AssignmentDynamicScopeFilterArgsDict']]] = None,
            maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'AssignmentDynamicScope':
        """
        Get an existing AssignmentDynamicScope resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['AssignmentDynamicScopeFilterArgs', 'AssignmentDynamicScopeFilterArgsDict']] filter: A `filter` block as defined below.
        :param pulumi.Input[str] maintenance_configuration_id: The ID of the Maintenance Configuration Resource. Changing this forces a new Dynamic Maintenance Assignment to be created.
        :param pulumi.Input[str] name: The name which should be used for this Dynamic Maintenance Assignment. Changing this forces a new Dynamic Maintenance Assignment to be created.
               
               > **Note:** The `name` must be unique per subscription.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AssignmentDynamicScopeState.__new__(_AssignmentDynamicScopeState)

        __props__.__dict__["filter"] = filter
        __props__.__dict__["maintenance_configuration_id"] = maintenance_configuration_id
        __props__.__dict__["name"] = name
        return AssignmentDynamicScope(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Output['outputs.AssignmentDynamicScopeFilter']:
        """
        A `filter` block as defined below.
        """
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> pulumi.Output[str]:
        """
        The ID of the Maintenance Configuration Resource. Changing this forces a new Dynamic Maintenance Assignment to be created.
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Dynamic Maintenance Assignment. Changing this forces a new Dynamic Maintenance Assignment to be created.

        > **Note:** The `name` must be unique per subscription.
        """
        return pulumi.get(self, "name")

