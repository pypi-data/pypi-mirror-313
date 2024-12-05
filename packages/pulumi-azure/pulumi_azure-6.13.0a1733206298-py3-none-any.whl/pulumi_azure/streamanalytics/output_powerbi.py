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

__all__ = ['OutputPowerbiArgs', 'OutputPowerbi']

@pulumi.input_type
class OutputPowerbiArgs:
    def __init__(__self__, *,
                 dataset: pulumi.Input[str],
                 group_id: pulumi.Input[str],
                 group_name: pulumi.Input[str],
                 stream_analytics_job_id: pulumi.Input[str],
                 table: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 token_user_display_name: Optional[pulumi.Input[str]] = None,
                 token_user_principal_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a OutputPowerbi resource.
        :param pulumi.Input[str] dataset: The name of the Power BI dataset.
        :param pulumi.Input[str] group_id: The ID of the Power BI group, this must be a valid UUID.
        :param pulumi.Input[str] group_name: The name of the Power BI group. Use this property to help remember which specific Power BI group id was used.
        :param pulumi.Input[str] stream_analytics_job_id: The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        :param pulumi.Input[str] table: The name of the Power BI table under the specified dataset.
        :param pulumi.Input[str] name: The name of the Stream Output. Changing this forces a new resource to be created.
        :param pulumi.Input[str] token_user_display_name: The user display name of the user that was used to obtain the refresh token.
        :param pulumi.Input[str] token_user_principal_name: The user principal name (UPN) of the user that was used to obtain the refresh token.
        """
        pulumi.set(__self__, "dataset", dataset)
        pulumi.set(__self__, "group_id", group_id)
        pulumi.set(__self__, "group_name", group_name)
        pulumi.set(__self__, "stream_analytics_job_id", stream_analytics_job_id)
        pulumi.set(__self__, "table", table)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if token_user_display_name is not None:
            pulumi.set(__self__, "token_user_display_name", token_user_display_name)
        if token_user_principal_name is not None:
            pulumi.set(__self__, "token_user_principal_name", token_user_principal_name)

    @property
    @pulumi.getter
    def dataset(self) -> pulumi.Input[str]:
        """
        The name of the Power BI dataset.
        """
        return pulumi.get(self, "dataset")

    @dataset.setter
    def dataset(self, value: pulumi.Input[str]):
        pulumi.set(self, "dataset", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Input[str]:
        """
        The ID of the Power BI group, this must be a valid UUID.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> pulumi.Input[str]:
        """
        The name of the Power BI group. Use this property to help remember which specific Power BI group id was used.
        """
        return pulumi.get(self, "group_name")

    @group_name.setter
    def group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "group_name", value)

    @property
    @pulumi.getter(name="streamAnalyticsJobId")
    def stream_analytics_job_id(self) -> pulumi.Input[str]:
        """
        The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "stream_analytics_job_id")

    @stream_analytics_job_id.setter
    def stream_analytics_job_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "stream_analytics_job_id", value)

    @property
    @pulumi.getter
    def table(self) -> pulumi.Input[str]:
        """
        The name of the Power BI table under the specified dataset.
        """
        return pulumi.get(self, "table")

    @table.setter
    def table(self, value: pulumi.Input[str]):
        pulumi.set(self, "table", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Stream Output. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="tokenUserDisplayName")
    def token_user_display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The user display name of the user that was used to obtain the refresh token.
        """
        return pulumi.get(self, "token_user_display_name")

    @token_user_display_name.setter
    def token_user_display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_user_display_name", value)

    @property
    @pulumi.getter(name="tokenUserPrincipalName")
    def token_user_principal_name(self) -> Optional[pulumi.Input[str]]:
        """
        The user principal name (UPN) of the user that was used to obtain the refresh token.
        """
        return pulumi.get(self, "token_user_principal_name")

    @token_user_principal_name.setter
    def token_user_principal_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_user_principal_name", value)


@pulumi.input_type
class _OutputPowerbiState:
    def __init__(__self__, *,
                 dataset: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 group_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 stream_analytics_job_id: Optional[pulumi.Input[str]] = None,
                 table: Optional[pulumi.Input[str]] = None,
                 token_user_display_name: Optional[pulumi.Input[str]] = None,
                 token_user_principal_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering OutputPowerbi resources.
        :param pulumi.Input[str] dataset: The name of the Power BI dataset.
        :param pulumi.Input[str] group_id: The ID of the Power BI group, this must be a valid UUID.
        :param pulumi.Input[str] group_name: The name of the Power BI group. Use this property to help remember which specific Power BI group id was used.
        :param pulumi.Input[str] name: The name of the Stream Output. Changing this forces a new resource to be created.
        :param pulumi.Input[str] stream_analytics_job_id: The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        :param pulumi.Input[str] table: The name of the Power BI table under the specified dataset.
        :param pulumi.Input[str] token_user_display_name: The user display name of the user that was used to obtain the refresh token.
        :param pulumi.Input[str] token_user_principal_name: The user principal name (UPN) of the user that was used to obtain the refresh token.
        """
        if dataset is not None:
            pulumi.set(__self__, "dataset", dataset)
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if group_name is not None:
            pulumi.set(__self__, "group_name", group_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if stream_analytics_job_id is not None:
            pulumi.set(__self__, "stream_analytics_job_id", stream_analytics_job_id)
        if table is not None:
            pulumi.set(__self__, "table", table)
        if token_user_display_name is not None:
            pulumi.set(__self__, "token_user_display_name", token_user_display_name)
        if token_user_principal_name is not None:
            pulumi.set(__self__, "token_user_principal_name", token_user_principal_name)

    @property
    @pulumi.getter
    def dataset(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Power BI dataset.
        """
        return pulumi.get(self, "dataset")

    @dataset.setter
    def dataset(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dataset", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Power BI group, this must be a valid UUID.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Power BI group. Use this property to help remember which specific Power BI group id was used.
        """
        return pulumi.get(self, "group_name")

    @group_name.setter
    def group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Stream Output. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="streamAnalyticsJobId")
    def stream_analytics_job_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "stream_analytics_job_id")

    @stream_analytics_job_id.setter
    def stream_analytics_job_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stream_analytics_job_id", value)

    @property
    @pulumi.getter
    def table(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Power BI table under the specified dataset.
        """
        return pulumi.get(self, "table")

    @table.setter
    def table(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "table", value)

    @property
    @pulumi.getter(name="tokenUserDisplayName")
    def token_user_display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The user display name of the user that was used to obtain the refresh token.
        """
        return pulumi.get(self, "token_user_display_name")

    @token_user_display_name.setter
    def token_user_display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_user_display_name", value)

    @property
    @pulumi.getter(name="tokenUserPrincipalName")
    def token_user_principal_name(self) -> Optional[pulumi.Input[str]]:
        """
        The user principal name (UPN) of the user that was used to obtain the refresh token.
        """
        return pulumi.get(self, "token_user_principal_name")

    @token_user_principal_name.setter
    def token_user_principal_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_user_principal_name", value)


class OutputPowerbi(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dataset: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 group_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 stream_analytics_job_id: Optional[pulumi.Input[str]] = None,
                 table: Optional[pulumi.Input[str]] = None,
                 token_user_display_name: Optional[pulumi.Input[str]] = None,
                 token_user_principal_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Stream Analytics Output powerBI.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.get_resource_group(name="example-resources")
        example_get_job = azure.streamanalytics.get_job(name="example-job",
            resource_group_name=example.name)
        example_output_powerbi = azure.streamanalytics.OutputPowerbi("example",
            name="output-to-powerbi",
            stream_analytics_job_id=example_get_job.id,
            dataset="example-dataset",
            table="example-table",
            group_id="00000000-0000-0000-0000-000000000000",
            group_name="some-group-name")
        ```

        ## Import

        Stream Analytics Output to Power BI can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:streamanalytics/outputPowerbi:OutputPowerbi example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.StreamAnalytics/streamingJobs/job1/outputs/output1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dataset: The name of the Power BI dataset.
        :param pulumi.Input[str] group_id: The ID of the Power BI group, this must be a valid UUID.
        :param pulumi.Input[str] group_name: The name of the Power BI group. Use this property to help remember which specific Power BI group id was used.
        :param pulumi.Input[str] name: The name of the Stream Output. Changing this forces a new resource to be created.
        :param pulumi.Input[str] stream_analytics_job_id: The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        :param pulumi.Input[str] table: The name of the Power BI table under the specified dataset.
        :param pulumi.Input[str] token_user_display_name: The user display name of the user that was used to obtain the refresh token.
        :param pulumi.Input[str] token_user_principal_name: The user principal name (UPN) of the user that was used to obtain the refresh token.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OutputPowerbiArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Stream Analytics Output powerBI.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.get_resource_group(name="example-resources")
        example_get_job = azure.streamanalytics.get_job(name="example-job",
            resource_group_name=example.name)
        example_output_powerbi = azure.streamanalytics.OutputPowerbi("example",
            name="output-to-powerbi",
            stream_analytics_job_id=example_get_job.id,
            dataset="example-dataset",
            table="example-table",
            group_id="00000000-0000-0000-0000-000000000000",
            group_name="some-group-name")
        ```

        ## Import

        Stream Analytics Output to Power BI can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:streamanalytics/outputPowerbi:OutputPowerbi example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.StreamAnalytics/streamingJobs/job1/outputs/output1
        ```

        :param str resource_name: The name of the resource.
        :param OutputPowerbiArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OutputPowerbiArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dataset: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 group_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 stream_analytics_job_id: Optional[pulumi.Input[str]] = None,
                 table: Optional[pulumi.Input[str]] = None,
                 token_user_display_name: Optional[pulumi.Input[str]] = None,
                 token_user_principal_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OutputPowerbiArgs.__new__(OutputPowerbiArgs)

            if dataset is None and not opts.urn:
                raise TypeError("Missing required property 'dataset'")
            __props__.__dict__["dataset"] = dataset
            if group_id is None and not opts.urn:
                raise TypeError("Missing required property 'group_id'")
            __props__.__dict__["group_id"] = group_id
            if group_name is None and not opts.urn:
                raise TypeError("Missing required property 'group_name'")
            __props__.__dict__["group_name"] = group_name
            __props__.__dict__["name"] = name
            if stream_analytics_job_id is None and not opts.urn:
                raise TypeError("Missing required property 'stream_analytics_job_id'")
            __props__.__dict__["stream_analytics_job_id"] = stream_analytics_job_id
            if table is None and not opts.urn:
                raise TypeError("Missing required property 'table'")
            __props__.__dict__["table"] = table
            __props__.__dict__["token_user_display_name"] = token_user_display_name
            __props__.__dict__["token_user_principal_name"] = token_user_principal_name
        super(OutputPowerbi, __self__).__init__(
            'azure:streamanalytics/outputPowerbi:OutputPowerbi',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            dataset: Optional[pulumi.Input[str]] = None,
            group_id: Optional[pulumi.Input[str]] = None,
            group_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            stream_analytics_job_id: Optional[pulumi.Input[str]] = None,
            table: Optional[pulumi.Input[str]] = None,
            token_user_display_name: Optional[pulumi.Input[str]] = None,
            token_user_principal_name: Optional[pulumi.Input[str]] = None) -> 'OutputPowerbi':
        """
        Get an existing OutputPowerbi resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dataset: The name of the Power BI dataset.
        :param pulumi.Input[str] group_id: The ID of the Power BI group, this must be a valid UUID.
        :param pulumi.Input[str] group_name: The name of the Power BI group. Use this property to help remember which specific Power BI group id was used.
        :param pulumi.Input[str] name: The name of the Stream Output. Changing this forces a new resource to be created.
        :param pulumi.Input[str] stream_analytics_job_id: The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        :param pulumi.Input[str] table: The name of the Power BI table under the specified dataset.
        :param pulumi.Input[str] token_user_display_name: The user display name of the user that was used to obtain the refresh token.
        :param pulumi.Input[str] token_user_principal_name: The user principal name (UPN) of the user that was used to obtain the refresh token.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OutputPowerbiState.__new__(_OutputPowerbiState)

        __props__.__dict__["dataset"] = dataset
        __props__.__dict__["group_id"] = group_id
        __props__.__dict__["group_name"] = group_name
        __props__.__dict__["name"] = name
        __props__.__dict__["stream_analytics_job_id"] = stream_analytics_job_id
        __props__.__dict__["table"] = table
        __props__.__dict__["token_user_display_name"] = token_user_display_name
        __props__.__dict__["token_user_principal_name"] = token_user_principal_name
        return OutputPowerbi(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def dataset(self) -> pulumi.Output[str]:
        """
        The name of the Power BI dataset.
        """
        return pulumi.get(self, "dataset")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Output[str]:
        """
        The ID of the Power BI group, this must be a valid UUID.
        """
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> pulumi.Output[str]:
        """
        The name of the Power BI group. Use this property to help remember which specific Power BI group id was used.
        """
        return pulumi.get(self, "group_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Stream Output. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="streamAnalyticsJobId")
    def stream_analytics_job_id(self) -> pulumi.Output[str]:
        """
        The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "stream_analytics_job_id")

    @property
    @pulumi.getter
    def table(self) -> pulumi.Output[str]:
        """
        The name of the Power BI table under the specified dataset.
        """
        return pulumi.get(self, "table")

    @property
    @pulumi.getter(name="tokenUserDisplayName")
    def token_user_display_name(self) -> pulumi.Output[Optional[str]]:
        """
        The user display name of the user that was used to obtain the refresh token.
        """
        return pulumi.get(self, "token_user_display_name")

    @property
    @pulumi.getter(name="tokenUserPrincipalName")
    def token_user_principal_name(self) -> pulumi.Output[Optional[str]]:
        """
        The user principal name (UPN) of the user that was used to obtain the refresh token.
        """
        return pulumi.get(self, "token_user_principal_name")

