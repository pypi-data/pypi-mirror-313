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

__all__ = ['DataConnectorAzureSecurityCenterArgs', 'DataConnectorAzureSecurityCenter']

@pulumi.input_type
class DataConnectorAzureSecurityCenterArgs:
    def __init__(__self__, *,
                 log_analytics_workspace_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 subscription_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DataConnectorAzureSecurityCenter resource.
        :param pulumi.Input[str] log_analytics_workspace_id: The ID of the Log Analytics Workspace that this Azure Security Center Data Connector resides in. Changing this forces a new Azure Security Center Data Connector to be created.
        :param pulumi.Input[str] name: The name which should be used for this Azure Security Center Data Connector. Changing this forces a new Azure Security Center Data Connector to be created.
        :param pulumi.Input[str] subscription_id: The ID of the subscription that this Azure Security Center Data Connector connects to. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        pulumi.set(__self__, "log_analytics_workspace_id", log_analytics_workspace_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if subscription_id is not None:
            pulumi.set(__self__, "subscription_id", subscription_id)

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> pulumi.Input[str]:
        """
        The ID of the Log Analytics Workspace that this Azure Security Center Data Connector resides in. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        return pulumi.get(self, "log_analytics_workspace_id")

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_analytics_workspace_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Azure Security Center Data Connector. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="subscriptionId")
    def subscription_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the subscription that this Azure Security Center Data Connector connects to. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        return pulumi.get(self, "subscription_id")

    @subscription_id.setter
    def subscription_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subscription_id", value)


@pulumi.input_type
class _DataConnectorAzureSecurityCenterState:
    def __init__(__self__, *,
                 log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 subscription_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DataConnectorAzureSecurityCenter resources.
        :param pulumi.Input[str] log_analytics_workspace_id: The ID of the Log Analytics Workspace that this Azure Security Center Data Connector resides in. Changing this forces a new Azure Security Center Data Connector to be created.
        :param pulumi.Input[str] name: The name which should be used for this Azure Security Center Data Connector. Changing this forces a new Azure Security Center Data Connector to be created.
        :param pulumi.Input[str] subscription_id: The ID of the subscription that this Azure Security Center Data Connector connects to. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        if log_analytics_workspace_id is not None:
            pulumi.set(__self__, "log_analytics_workspace_id", log_analytics_workspace_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if subscription_id is not None:
            pulumi.set(__self__, "subscription_id", subscription_id)

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Log Analytics Workspace that this Azure Security Center Data Connector resides in. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        return pulumi.get(self, "log_analytics_workspace_id")

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_analytics_workspace_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Azure Security Center Data Connector. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="subscriptionId")
    def subscription_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the subscription that this Azure Security Center Data Connector connects to. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        return pulumi.get(self, "subscription_id")

    @subscription_id.setter
    def subscription_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subscription_id", value)


class DataConnectorAzureSecurityCenter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 subscription_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Azure Security Center Data Connector.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-rg",
            location="west europe")
        example_analytics_workspace = azure.operationalinsights.AnalyticsWorkspace("example",
            name="example-workspace",
            location=example.location,
            resource_group_name=example.name,
            sku="PerGB2018")
        example_log_analytics_workspace_onboarding = azure.sentinel.LogAnalyticsWorkspaceOnboarding("example", workspace_id=example_analytics_workspace.id)
        example_data_connector_azure_security_center = azure.sentinel.DataConnectorAzureSecurityCenter("example",
            name="example",
            log_analytics_workspace_id=example_log_analytics_workspace_onboarding.workspace_id)
        ```

        ## Import

        Azure Security Center Data Connectors can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:sentinel/dataConnectorAzureSecurityCenter:DataConnectorAzureSecurityCenter example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.OperationalInsights/workspaces/workspace1/providers/Microsoft.SecurityInsights/dataConnectors/dc1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] log_analytics_workspace_id: The ID of the Log Analytics Workspace that this Azure Security Center Data Connector resides in. Changing this forces a new Azure Security Center Data Connector to be created.
        :param pulumi.Input[str] name: The name which should be used for this Azure Security Center Data Connector. Changing this forces a new Azure Security Center Data Connector to be created.
        :param pulumi.Input[str] subscription_id: The ID of the subscription that this Azure Security Center Data Connector connects to. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DataConnectorAzureSecurityCenterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Azure Security Center Data Connector.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-rg",
            location="west europe")
        example_analytics_workspace = azure.operationalinsights.AnalyticsWorkspace("example",
            name="example-workspace",
            location=example.location,
            resource_group_name=example.name,
            sku="PerGB2018")
        example_log_analytics_workspace_onboarding = azure.sentinel.LogAnalyticsWorkspaceOnboarding("example", workspace_id=example_analytics_workspace.id)
        example_data_connector_azure_security_center = azure.sentinel.DataConnectorAzureSecurityCenter("example",
            name="example",
            log_analytics_workspace_id=example_log_analytics_workspace_onboarding.workspace_id)
        ```

        ## Import

        Azure Security Center Data Connectors can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:sentinel/dataConnectorAzureSecurityCenter:DataConnectorAzureSecurityCenter example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.OperationalInsights/workspaces/workspace1/providers/Microsoft.SecurityInsights/dataConnectors/dc1
        ```

        :param str resource_name: The name of the resource.
        :param DataConnectorAzureSecurityCenterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DataConnectorAzureSecurityCenterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 subscription_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DataConnectorAzureSecurityCenterArgs.__new__(DataConnectorAzureSecurityCenterArgs)

            if log_analytics_workspace_id is None and not opts.urn:
                raise TypeError("Missing required property 'log_analytics_workspace_id'")
            __props__.__dict__["log_analytics_workspace_id"] = log_analytics_workspace_id
            __props__.__dict__["name"] = name
            __props__.__dict__["subscription_id"] = subscription_id
        super(DataConnectorAzureSecurityCenter, __self__).__init__(
            'azure:sentinel/dataConnectorAzureSecurityCenter:DataConnectorAzureSecurityCenter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            subscription_id: Optional[pulumi.Input[str]] = None) -> 'DataConnectorAzureSecurityCenter':
        """
        Get an existing DataConnectorAzureSecurityCenter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] log_analytics_workspace_id: The ID of the Log Analytics Workspace that this Azure Security Center Data Connector resides in. Changing this forces a new Azure Security Center Data Connector to be created.
        :param pulumi.Input[str] name: The name which should be used for this Azure Security Center Data Connector. Changing this forces a new Azure Security Center Data Connector to be created.
        :param pulumi.Input[str] subscription_id: The ID of the subscription that this Azure Security Center Data Connector connects to. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DataConnectorAzureSecurityCenterState.__new__(_DataConnectorAzureSecurityCenterState)

        __props__.__dict__["log_analytics_workspace_id"] = log_analytics_workspace_id
        __props__.__dict__["name"] = name
        __props__.__dict__["subscription_id"] = subscription_id
        return DataConnectorAzureSecurityCenter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> pulumi.Output[str]:
        """
        The ID of the Log Analytics Workspace that this Azure Security Center Data Connector resides in. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        return pulumi.get(self, "log_analytics_workspace_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Azure Security Center Data Connector. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="subscriptionId")
    def subscription_id(self) -> pulumi.Output[str]:
        """
        The ID of the subscription that this Azure Security Center Data Connector connects to. Changing this forces a new Azure Security Center Data Connector to be created.
        """
        return pulumi.get(self, "subscription_id")

