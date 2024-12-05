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
    'GetJobResult',
    'AwaitableGetJobResult',
    'get_job',
    'get_job_output',
]

@pulumi.output_type
class GetJobResult:
    """
    A collection of values returned by getJob.
    """
    def __init__(__self__, compatibility_level=None, data_locale=None, events_late_arrival_max_delay_in_seconds=None, events_out_of_order_max_delay_in_seconds=None, events_out_of_order_policy=None, id=None, identities=None, job_id=None, last_output_time=None, location=None, name=None, output_error_policy=None, resource_group_name=None, sku_name=None, start_mode=None, start_time=None, streaming_units=None, transformation_query=None):
        if compatibility_level and not isinstance(compatibility_level, str):
            raise TypeError("Expected argument 'compatibility_level' to be a str")
        pulumi.set(__self__, "compatibility_level", compatibility_level)
        if data_locale and not isinstance(data_locale, str):
            raise TypeError("Expected argument 'data_locale' to be a str")
        pulumi.set(__self__, "data_locale", data_locale)
        if events_late_arrival_max_delay_in_seconds and not isinstance(events_late_arrival_max_delay_in_seconds, int):
            raise TypeError("Expected argument 'events_late_arrival_max_delay_in_seconds' to be a int")
        pulumi.set(__self__, "events_late_arrival_max_delay_in_seconds", events_late_arrival_max_delay_in_seconds)
        if events_out_of_order_max_delay_in_seconds and not isinstance(events_out_of_order_max_delay_in_seconds, int):
            raise TypeError("Expected argument 'events_out_of_order_max_delay_in_seconds' to be a int")
        pulumi.set(__self__, "events_out_of_order_max_delay_in_seconds", events_out_of_order_max_delay_in_seconds)
        if events_out_of_order_policy and not isinstance(events_out_of_order_policy, str):
            raise TypeError("Expected argument 'events_out_of_order_policy' to be a str")
        pulumi.set(__self__, "events_out_of_order_policy", events_out_of_order_policy)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identities and not isinstance(identities, list):
            raise TypeError("Expected argument 'identities' to be a list")
        pulumi.set(__self__, "identities", identities)
        if job_id and not isinstance(job_id, str):
            raise TypeError("Expected argument 'job_id' to be a str")
        pulumi.set(__self__, "job_id", job_id)
        if last_output_time and not isinstance(last_output_time, str):
            raise TypeError("Expected argument 'last_output_time' to be a str")
        pulumi.set(__self__, "last_output_time", last_output_time)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if output_error_policy and not isinstance(output_error_policy, str):
            raise TypeError("Expected argument 'output_error_policy' to be a str")
        pulumi.set(__self__, "output_error_policy", output_error_policy)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if sku_name and not isinstance(sku_name, str):
            raise TypeError("Expected argument 'sku_name' to be a str")
        pulumi.set(__self__, "sku_name", sku_name)
        if start_mode and not isinstance(start_mode, str):
            raise TypeError("Expected argument 'start_mode' to be a str")
        pulumi.set(__self__, "start_mode", start_mode)
        if start_time and not isinstance(start_time, str):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, "start_time", start_time)
        if streaming_units and not isinstance(streaming_units, int):
            raise TypeError("Expected argument 'streaming_units' to be a int")
        pulumi.set(__self__, "streaming_units", streaming_units)
        if transformation_query and not isinstance(transformation_query, str):
            raise TypeError("Expected argument 'transformation_query' to be a str")
        pulumi.set(__self__, "transformation_query", transformation_query)

    @property
    @pulumi.getter(name="compatibilityLevel")
    def compatibility_level(self) -> str:
        """
        The compatibility level for this job.
        """
        return pulumi.get(self, "compatibility_level")

    @property
    @pulumi.getter(name="dataLocale")
    def data_locale(self) -> str:
        """
        The Data Locale of the Job.
        """
        return pulumi.get(self, "data_locale")

    @property
    @pulumi.getter(name="eventsLateArrivalMaxDelayInSeconds")
    def events_late_arrival_max_delay_in_seconds(self) -> int:
        """
        The maximum tolerable delay in seconds where events arriving late could be included.
        """
        return pulumi.get(self, "events_late_arrival_max_delay_in_seconds")

    @property
    @pulumi.getter(name="eventsOutOfOrderMaxDelayInSeconds")
    def events_out_of_order_max_delay_in_seconds(self) -> int:
        """
        The maximum tolerable delay in seconds where out-of-order events can be adjusted to be back in order.
        """
        return pulumi.get(self, "events_out_of_order_max_delay_in_seconds")

    @property
    @pulumi.getter(name="eventsOutOfOrderPolicy")
    def events_out_of_order_policy(self) -> str:
        """
        The policy which should be applied to events which arrive out of order in the input event stream.
        """
        return pulumi.get(self, "events_out_of_order_policy")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identities(self) -> Sequence['outputs.GetJobIdentityResult']:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, "identities")

    @property
    @pulumi.getter(name="jobId")
    def job_id(self) -> str:
        """
        The Job ID assigned by the Stream Analytics Job.
        """
        return pulumi.get(self, "job_id")

    @property
    @pulumi.getter(name="lastOutputTime")
    def last_output_time(self) -> str:
        """
        The time at which the Stream Analytics job last produced an output.
        """
        return pulumi.get(self, "last_output_time")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure location where the Stream Analytics Job exists.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outputErrorPolicy")
    def output_error_policy(self) -> str:
        """
        The policy which should be applied to events which arrive at the output and cannot be written to the external storage due to being malformed (such as missing column values, column values of wrong type or size).
        """
        return pulumi.get(self, "output_error_policy")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="skuName")
    def sku_name(self) -> str:
        """
        The SKU Name to use for the Stream Analytics Job.
        """
        return pulumi.get(self, "sku_name")

    @property
    @pulumi.getter(name="startMode")
    def start_mode(self) -> str:
        """
        The starting mode set for this Stream Analytics Job.
        """
        return pulumi.get(self, "start_mode")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        """
        The time at which this Stream Analytics Job was scheduled to start.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter(name="streamingUnits")
    def streaming_units(self) -> int:
        """
        The number of streaming units that this Stream Analytics Job uses.
        """
        return pulumi.get(self, "streaming_units")

    @property
    @pulumi.getter(name="transformationQuery")
    def transformation_query(self) -> str:
        """
        The query that will be run in this Stream Analytics Job, [written in Stream Analytics Query Language (SAQL)](https://msdn.microsoft.com/library/azure/dn834998).
        """
        return pulumi.get(self, "transformation_query")


class AwaitableGetJobResult(GetJobResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetJobResult(
            compatibility_level=self.compatibility_level,
            data_locale=self.data_locale,
            events_late_arrival_max_delay_in_seconds=self.events_late_arrival_max_delay_in_seconds,
            events_out_of_order_max_delay_in_seconds=self.events_out_of_order_max_delay_in_seconds,
            events_out_of_order_policy=self.events_out_of_order_policy,
            id=self.id,
            identities=self.identities,
            job_id=self.job_id,
            last_output_time=self.last_output_time,
            location=self.location,
            name=self.name,
            output_error_policy=self.output_error_policy,
            resource_group_name=self.resource_group_name,
            sku_name=self.sku_name,
            start_mode=self.start_mode,
            start_time=self.start_time,
            streaming_units=self.streaming_units,
            transformation_query=self.transformation_query)


def get_job(name: Optional[str] = None,
            resource_group_name: Optional[str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetJobResult:
    """
    Use this data source to access information about an existing Stream Analytics Job.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.streamanalytics.get_job(name="example-job",
        resource_group_name="example-resources")
    pulumi.export("jobId", example.job_id)
    ```


    :param str name: Specifies the name of the Stream Analytics Job.
    :param str resource_group_name: Specifies the name of the resource group the Stream Analytics Job is located in.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:streamanalytics/getJob:getJob', __args__, opts=opts, typ=GetJobResult).value

    return AwaitableGetJobResult(
        compatibility_level=pulumi.get(__ret__, 'compatibility_level'),
        data_locale=pulumi.get(__ret__, 'data_locale'),
        events_late_arrival_max_delay_in_seconds=pulumi.get(__ret__, 'events_late_arrival_max_delay_in_seconds'),
        events_out_of_order_max_delay_in_seconds=pulumi.get(__ret__, 'events_out_of_order_max_delay_in_seconds'),
        events_out_of_order_policy=pulumi.get(__ret__, 'events_out_of_order_policy'),
        id=pulumi.get(__ret__, 'id'),
        identities=pulumi.get(__ret__, 'identities'),
        job_id=pulumi.get(__ret__, 'job_id'),
        last_output_time=pulumi.get(__ret__, 'last_output_time'),
        location=pulumi.get(__ret__, 'location'),
        name=pulumi.get(__ret__, 'name'),
        output_error_policy=pulumi.get(__ret__, 'output_error_policy'),
        resource_group_name=pulumi.get(__ret__, 'resource_group_name'),
        sku_name=pulumi.get(__ret__, 'sku_name'),
        start_mode=pulumi.get(__ret__, 'start_mode'),
        start_time=pulumi.get(__ret__, 'start_time'),
        streaming_units=pulumi.get(__ret__, 'streaming_units'),
        transformation_query=pulumi.get(__ret__, 'transformation_query'))
def get_job_output(name: Optional[pulumi.Input[str]] = None,
                   resource_group_name: Optional[pulumi.Input[str]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetJobResult]:
    """
    Use this data source to access information about an existing Stream Analytics Job.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.streamanalytics.get_job(name="example-job",
        resource_group_name="example-resources")
    pulumi.export("jobId", example.job_id)
    ```


    :param str name: Specifies the name of the Stream Analytics Job.
    :param str resource_group_name: Specifies the name of the resource group the Stream Analytics Job is located in.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:streamanalytics/getJob:getJob', __args__, opts=opts, typ=GetJobResult)
    return __ret__.apply(lambda __response__: GetJobResult(
        compatibility_level=pulumi.get(__response__, 'compatibility_level'),
        data_locale=pulumi.get(__response__, 'data_locale'),
        events_late_arrival_max_delay_in_seconds=pulumi.get(__response__, 'events_late_arrival_max_delay_in_seconds'),
        events_out_of_order_max_delay_in_seconds=pulumi.get(__response__, 'events_out_of_order_max_delay_in_seconds'),
        events_out_of_order_policy=pulumi.get(__response__, 'events_out_of_order_policy'),
        id=pulumi.get(__response__, 'id'),
        identities=pulumi.get(__response__, 'identities'),
        job_id=pulumi.get(__response__, 'job_id'),
        last_output_time=pulumi.get(__response__, 'last_output_time'),
        location=pulumi.get(__response__, 'location'),
        name=pulumi.get(__response__, 'name'),
        output_error_policy=pulumi.get(__response__, 'output_error_policy'),
        resource_group_name=pulumi.get(__response__, 'resource_group_name'),
        sku_name=pulumi.get(__response__, 'sku_name'),
        start_mode=pulumi.get(__response__, 'start_mode'),
        start_time=pulumi.get(__response__, 'start_time'),
        streaming_units=pulumi.get(__response__, 'streaming_units'),
        transformation_query=pulumi.get(__response__, 'transformation_query')))
