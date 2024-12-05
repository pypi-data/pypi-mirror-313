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

__all__ = ['AlertProcessingRuleActionGroupArgs', 'AlertProcessingRuleActionGroup']

@pulumi.input_type
class AlertProcessingRuleActionGroupArgs:
    def __init__(__self__, *,
                 add_action_group_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 resource_group_name: pulumi.Input[str],
                 scopes: pulumi.Input[Sequence[pulumi.Input[str]]],
                 condition: Optional[pulumi.Input['AlertProcessingRuleActionGroupConditionArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input['AlertProcessingRuleActionGroupScheduleArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a AlertProcessingRuleActionGroup resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] add_action_group_ids: Specifies a list of Action Group IDs.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Alert Processing Rule should exist. Changing this forces a new Alert Processing Rule to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] scopes: A list of resource IDs which will be the target of alert processing rule.
        :param pulumi.Input['AlertProcessingRuleActionGroupConditionArgs'] condition: A `condition` block as defined below.
        :param pulumi.Input[str] description: Specifies a description for the Alert Processing Rule.
        :param pulumi.Input[bool] enabled: Should the Alert Processing Rule be enabled? Defaults to `true`.
        :param pulumi.Input[str] name: The name which should be used for this Alert Processing Rule. Changing this forces a new Alert Processing Rule to be created.
        :param pulumi.Input['AlertProcessingRuleActionGroupScheduleArgs'] schedule: A `schedule` block as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Alert Processing Rule.
        """
        pulumi.set(__self__, "add_action_group_ids", add_action_group_ids)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "scopes", scopes)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="addActionGroupIds")
    def add_action_group_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Specifies a list of Action Group IDs.
        """
        return pulumi.get(self, "add_action_group_ids")

    @add_action_group_ids.setter
    def add_action_group_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "add_action_group_ids", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Alert Processing Rule should exist. Changing this forces a new Alert Processing Rule to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def scopes(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of resource IDs which will be the target of alert processing rule.
        """
        return pulumi.get(self, "scopes")

    @scopes.setter
    def scopes(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "scopes", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['AlertProcessingRuleActionGroupConditionArgs']]:
        """
        A `condition` block as defined below.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['AlertProcessingRuleActionGroupConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a description for the Alert Processing Rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the Alert Processing Rule be enabled? Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Alert Processing Rule. Changing this forces a new Alert Processing Rule to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input['AlertProcessingRuleActionGroupScheduleArgs']]:
        """
        A `schedule` block as defined below.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input['AlertProcessingRuleActionGroupScheduleArgs']]):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Alert Processing Rule.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _AlertProcessingRuleActionGroupState:
    def __init__(__self__, *,
                 add_action_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 condition: Optional[pulumi.Input['AlertProcessingRuleActionGroupConditionArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input['AlertProcessingRuleActionGroupScheduleArgs']] = None,
                 scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering AlertProcessingRuleActionGroup resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] add_action_group_ids: Specifies a list of Action Group IDs.
        :param pulumi.Input['AlertProcessingRuleActionGroupConditionArgs'] condition: A `condition` block as defined below.
        :param pulumi.Input[str] description: Specifies a description for the Alert Processing Rule.
        :param pulumi.Input[bool] enabled: Should the Alert Processing Rule be enabled? Defaults to `true`.
        :param pulumi.Input[str] name: The name which should be used for this Alert Processing Rule. Changing this forces a new Alert Processing Rule to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Alert Processing Rule should exist. Changing this forces a new Alert Processing Rule to be created.
        :param pulumi.Input['AlertProcessingRuleActionGroupScheduleArgs'] schedule: A `schedule` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] scopes: A list of resource IDs which will be the target of alert processing rule.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Alert Processing Rule.
        """
        if add_action_group_ids is not None:
            pulumi.set(__self__, "add_action_group_ids", add_action_group_ids)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)
        if scopes is not None:
            pulumi.set(__self__, "scopes", scopes)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="addActionGroupIds")
    def add_action_group_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies a list of Action Group IDs.
        """
        return pulumi.get(self, "add_action_group_ids")

    @add_action_group_ids.setter
    def add_action_group_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "add_action_group_ids", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['AlertProcessingRuleActionGroupConditionArgs']]:
        """
        A `condition` block as defined below.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['AlertProcessingRuleActionGroupConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a description for the Alert Processing Rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the Alert Processing Rule be enabled? Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Alert Processing Rule. Changing this forces a new Alert Processing Rule to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Alert Processing Rule should exist. Changing this forces a new Alert Processing Rule to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input['AlertProcessingRuleActionGroupScheduleArgs']]:
        """
        A `schedule` block as defined below.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input['AlertProcessingRuleActionGroupScheduleArgs']]):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter
    def scopes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of resource IDs which will be the target of alert processing rule.
        """
        return pulumi.get(self, "scopes")

    @scopes.setter
    def scopes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "scopes", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Alert Processing Rule.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class AlertProcessingRuleActionGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 add_action_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 condition: Optional[pulumi.Input[Union['AlertProcessingRuleActionGroupConditionArgs', 'AlertProcessingRuleActionGroupConditionArgsDict']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[Union['AlertProcessingRuleActionGroupScheduleArgs', 'AlertProcessingRuleActionGroupScheduleArgsDict']]] = None,
                 scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages an Alert Processing Rule which apply action group.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_action_group = azure.monitoring.ActionGroup("example",
            name="example-action-group",
            resource_group_name=example.name,
            short_name="action")
        example_alert_processing_rule_action_group = azure.monitoring.AlertProcessingRuleActionGroup("example",
            name="example",
            resource_group_name="example",
            scopes=[example.id],
            add_action_group_ids=[example_action_group.id],
            condition={
                "target_resource_type": {
                    "operator": "Equals",
                    "values": ["Microsoft.Compute/VirtualMachines"],
                },
                "severity": {
                    "operator": "Equals",
                    "values": [
                        "Sev0",
                        "Sev1",
                        "Sev2",
                    ],
                },
            },
            schedule={
                "effective_from": "2022-01-01T01:02:03",
                "effective_until": "2022-02-02T01:02:03",
                "time_zone": "Pacific Standard Time",
                "recurrence": {
                    "dailies": [{
                        "start_time": "17:00:00",
                        "end_time": "09:00:00",
                    }],
                    "weeklies": [{
                        "days_of_weeks": [
                            "Saturday",
                            "Sunday",
                        ],
                    }],
                },
            },
            tags={
                "foo": "bar",
            })
        ```

        ## Import

        Alert Processing Rules can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:monitoring/alertProcessingRuleActionGroup:AlertProcessingRuleActionGroup example /subscriptions/12345678-1234-9876-4563-123456789012/resourceGroups/group1/providers/Microsoft.AlertsManagement/actionRules/actionRule1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] add_action_group_ids: Specifies a list of Action Group IDs.
        :param pulumi.Input[Union['AlertProcessingRuleActionGroupConditionArgs', 'AlertProcessingRuleActionGroupConditionArgsDict']] condition: A `condition` block as defined below.
        :param pulumi.Input[str] description: Specifies a description for the Alert Processing Rule.
        :param pulumi.Input[bool] enabled: Should the Alert Processing Rule be enabled? Defaults to `true`.
        :param pulumi.Input[str] name: The name which should be used for this Alert Processing Rule. Changing this forces a new Alert Processing Rule to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Alert Processing Rule should exist. Changing this forces a new Alert Processing Rule to be created.
        :param pulumi.Input[Union['AlertProcessingRuleActionGroupScheduleArgs', 'AlertProcessingRuleActionGroupScheduleArgsDict']] schedule: A `schedule` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] scopes: A list of resource IDs which will be the target of alert processing rule.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Alert Processing Rule.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AlertProcessingRuleActionGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an Alert Processing Rule which apply action group.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_action_group = azure.monitoring.ActionGroup("example",
            name="example-action-group",
            resource_group_name=example.name,
            short_name="action")
        example_alert_processing_rule_action_group = azure.monitoring.AlertProcessingRuleActionGroup("example",
            name="example",
            resource_group_name="example",
            scopes=[example.id],
            add_action_group_ids=[example_action_group.id],
            condition={
                "target_resource_type": {
                    "operator": "Equals",
                    "values": ["Microsoft.Compute/VirtualMachines"],
                },
                "severity": {
                    "operator": "Equals",
                    "values": [
                        "Sev0",
                        "Sev1",
                        "Sev2",
                    ],
                },
            },
            schedule={
                "effective_from": "2022-01-01T01:02:03",
                "effective_until": "2022-02-02T01:02:03",
                "time_zone": "Pacific Standard Time",
                "recurrence": {
                    "dailies": [{
                        "start_time": "17:00:00",
                        "end_time": "09:00:00",
                    }],
                    "weeklies": [{
                        "days_of_weeks": [
                            "Saturday",
                            "Sunday",
                        ],
                    }],
                },
            },
            tags={
                "foo": "bar",
            })
        ```

        ## Import

        Alert Processing Rules can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:monitoring/alertProcessingRuleActionGroup:AlertProcessingRuleActionGroup example /subscriptions/12345678-1234-9876-4563-123456789012/resourceGroups/group1/providers/Microsoft.AlertsManagement/actionRules/actionRule1
        ```

        :param str resource_name: The name of the resource.
        :param AlertProcessingRuleActionGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AlertProcessingRuleActionGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 add_action_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 condition: Optional[pulumi.Input[Union['AlertProcessingRuleActionGroupConditionArgs', 'AlertProcessingRuleActionGroupConditionArgsDict']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[Union['AlertProcessingRuleActionGroupScheduleArgs', 'AlertProcessingRuleActionGroupScheduleArgsDict']]] = None,
                 scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AlertProcessingRuleActionGroupArgs.__new__(AlertProcessingRuleActionGroupArgs)

            if add_action_group_ids is None and not opts.urn:
                raise TypeError("Missing required property 'add_action_group_ids'")
            __props__.__dict__["add_action_group_ids"] = add_action_group_ids
            __props__.__dict__["condition"] = condition
            __props__.__dict__["description"] = description
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["schedule"] = schedule
            if scopes is None and not opts.urn:
                raise TypeError("Missing required property 'scopes'")
            __props__.__dict__["scopes"] = scopes
            __props__.__dict__["tags"] = tags
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure:monitoring/actionRuleActionGroup:ActionRuleActionGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AlertProcessingRuleActionGroup, __self__).__init__(
            'azure:monitoring/alertProcessingRuleActionGroup:AlertProcessingRuleActionGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            add_action_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            condition: Optional[pulumi.Input[Union['AlertProcessingRuleActionGroupConditionArgs', 'AlertProcessingRuleActionGroupConditionArgsDict']]] = None,
            description: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            schedule: Optional[pulumi.Input[Union['AlertProcessingRuleActionGroupScheduleArgs', 'AlertProcessingRuleActionGroupScheduleArgsDict']]] = None,
            scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'AlertProcessingRuleActionGroup':
        """
        Get an existing AlertProcessingRuleActionGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] add_action_group_ids: Specifies a list of Action Group IDs.
        :param pulumi.Input[Union['AlertProcessingRuleActionGroupConditionArgs', 'AlertProcessingRuleActionGroupConditionArgsDict']] condition: A `condition` block as defined below.
        :param pulumi.Input[str] description: Specifies a description for the Alert Processing Rule.
        :param pulumi.Input[bool] enabled: Should the Alert Processing Rule be enabled? Defaults to `true`.
        :param pulumi.Input[str] name: The name which should be used for this Alert Processing Rule. Changing this forces a new Alert Processing Rule to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Alert Processing Rule should exist. Changing this forces a new Alert Processing Rule to be created.
        :param pulumi.Input[Union['AlertProcessingRuleActionGroupScheduleArgs', 'AlertProcessingRuleActionGroupScheduleArgsDict']] schedule: A `schedule` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] scopes: A list of resource IDs which will be the target of alert processing rule.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Alert Processing Rule.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AlertProcessingRuleActionGroupState.__new__(_AlertProcessingRuleActionGroupState)

        __props__.__dict__["add_action_group_ids"] = add_action_group_ids
        __props__.__dict__["condition"] = condition
        __props__.__dict__["description"] = description
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["schedule"] = schedule
        __props__.__dict__["scopes"] = scopes
        __props__.__dict__["tags"] = tags
        return AlertProcessingRuleActionGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="addActionGroupIds")
    def add_action_group_ids(self) -> pulumi.Output[Sequence[str]]:
        """
        Specifies a list of Action Group IDs.
        """
        return pulumi.get(self, "add_action_group_ids")

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional['outputs.AlertProcessingRuleActionGroupCondition']]:
        """
        A `condition` block as defined below.
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies a description for the Alert Processing Rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Should the Alert Processing Rule be enabled? Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Alert Processing Rule. Changing this forces a new Alert Processing Rule to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Alert Processing Rule should exist. Changing this forces a new Alert Processing Rule to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Output[Optional['outputs.AlertProcessingRuleActionGroupSchedule']]:
        """
        A `schedule` block as defined below.
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter
    def scopes(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of resource IDs which will be the target of alert processing rule.
        """
        return pulumi.get(self, "scopes")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to the Alert Processing Rule.
        """
        return pulumi.get(self, "tags")

