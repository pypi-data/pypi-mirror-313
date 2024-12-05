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
    'GetTriggerScheduleResult',
    'AwaitableGetTriggerScheduleResult',
    'get_trigger_schedule',
    'get_trigger_schedule_output',
]

@pulumi.output_type
class GetTriggerScheduleResult:
    """
    A collection of values returned by getTriggerSchedule.
    """
    def __init__(__self__, activated=None, annotations=None, data_factory_id=None, description=None, end_time=None, frequency=None, id=None, interval=None, name=None, pipeline_name=None, schedules=None, start_time=None, time_zone=None):
        if activated and not isinstance(activated, bool):
            raise TypeError("Expected argument 'activated' to be a bool")
        pulumi.set(__self__, "activated", activated)
        if annotations and not isinstance(annotations, list):
            raise TypeError("Expected argument 'annotations' to be a list")
        pulumi.set(__self__, "annotations", annotations)
        if data_factory_id and not isinstance(data_factory_id, str):
            raise TypeError("Expected argument 'data_factory_id' to be a str")
        pulumi.set(__self__, "data_factory_id", data_factory_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if end_time and not isinstance(end_time, str):
            raise TypeError("Expected argument 'end_time' to be a str")
        pulumi.set(__self__, "end_time", end_time)
        if frequency and not isinstance(frequency, str):
            raise TypeError("Expected argument 'frequency' to be a str")
        pulumi.set(__self__, "frequency", frequency)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if interval and not isinstance(interval, int):
            raise TypeError("Expected argument 'interval' to be a int")
        pulumi.set(__self__, "interval", interval)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if pipeline_name and not isinstance(pipeline_name, str):
            raise TypeError("Expected argument 'pipeline_name' to be a str")
        pulumi.set(__self__, "pipeline_name", pipeline_name)
        if schedules and not isinstance(schedules, list):
            raise TypeError("Expected argument 'schedules' to be a list")
        pulumi.set(__self__, "schedules", schedules)
        if start_time and not isinstance(start_time, str):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, "start_time", start_time)
        if time_zone and not isinstance(time_zone, str):
            raise TypeError("Expected argument 'time_zone' to be a str")
        pulumi.set(__self__, "time_zone", time_zone)

    @property
    @pulumi.getter
    def activated(self) -> bool:
        """
        Specifies if the Data Factory Schedule Trigger is activated.
        """
        return pulumi.get(self, "activated")

    @property
    @pulumi.getter
    def annotations(self) -> Sequence[str]:
        """
        List of tags that can be used for describing the Data Factory Schedule Trigger.
        """
        return pulumi.get(self, "annotations")

    @property
    @pulumi.getter(name="dataFactoryId")
    def data_factory_id(self) -> str:
        return pulumi.get(self, "data_factory_id")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The Schedule Trigger's description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> str:
        """
        The time the Schedule Trigger should end. The time will be represented in UTC.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter
    def frequency(self) -> str:
        """
        The trigger frequency.
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def interval(self) -> int:
        """
        The interval for how often the trigger occurs.
        """
        return pulumi.get(self, "interval")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pipelineName")
    def pipeline_name(self) -> str:
        """
        The Data Factory Pipeline name that the trigger will act on.
        """
        return pulumi.get(self, "pipeline_name")

    @property
    @pulumi.getter
    def schedules(self) -> Sequence['outputs.GetTriggerScheduleScheduleResult']:
        """
        A `schedule` block as described below, which further specifies the recurrence schedule for the trigger.
        """
        return pulumi.get(self, "schedules")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        """
        The time the Schedule Trigger will start. The time will be represented in UTC.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> str:
        """
        The timezone of the start/end time.
        """
        return pulumi.get(self, "time_zone")


class AwaitableGetTriggerScheduleResult(GetTriggerScheduleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTriggerScheduleResult(
            activated=self.activated,
            annotations=self.annotations,
            data_factory_id=self.data_factory_id,
            description=self.description,
            end_time=self.end_time,
            frequency=self.frequency,
            id=self.id,
            interval=self.interval,
            name=self.name,
            pipeline_name=self.pipeline_name,
            schedules=self.schedules,
            start_time=self.start_time,
            time_zone=self.time_zone)


def get_trigger_schedule(data_factory_id: Optional[str] = None,
                         name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTriggerScheduleResult:
    """
    Use this data source to access information about a trigger schedule in Azure Data Factory.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.datafactory.get_trigger_schedule(name="example_trigger",
        data_factory_id="/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg1/providers/Microsoft.DataFactory/factories/datafactory1")
    pulumi.export("id", example.id)
    ```


    :param str data_factory_id: The ID of the Azure Data Factory to fetch trigger schedule from.
    :param str name: The name of the trigger schedule.
    """
    __args__ = dict()
    __args__['dataFactoryId'] = data_factory_id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:datafactory/getTriggerSchedule:getTriggerSchedule', __args__, opts=opts, typ=GetTriggerScheduleResult).value

    return AwaitableGetTriggerScheduleResult(
        activated=pulumi.get(__ret__, 'activated'),
        annotations=pulumi.get(__ret__, 'annotations'),
        data_factory_id=pulumi.get(__ret__, 'data_factory_id'),
        description=pulumi.get(__ret__, 'description'),
        end_time=pulumi.get(__ret__, 'end_time'),
        frequency=pulumi.get(__ret__, 'frequency'),
        id=pulumi.get(__ret__, 'id'),
        interval=pulumi.get(__ret__, 'interval'),
        name=pulumi.get(__ret__, 'name'),
        pipeline_name=pulumi.get(__ret__, 'pipeline_name'),
        schedules=pulumi.get(__ret__, 'schedules'),
        start_time=pulumi.get(__ret__, 'start_time'),
        time_zone=pulumi.get(__ret__, 'time_zone'))
def get_trigger_schedule_output(data_factory_id: Optional[pulumi.Input[str]] = None,
                                name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTriggerScheduleResult]:
    """
    Use this data source to access information about a trigger schedule in Azure Data Factory.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.datafactory.get_trigger_schedule(name="example_trigger",
        data_factory_id="/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg1/providers/Microsoft.DataFactory/factories/datafactory1")
    pulumi.export("id", example.id)
    ```


    :param str data_factory_id: The ID of the Azure Data Factory to fetch trigger schedule from.
    :param str name: The name of the trigger schedule.
    """
    __args__ = dict()
    __args__['dataFactoryId'] = data_factory_id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:datafactory/getTriggerSchedule:getTriggerSchedule', __args__, opts=opts, typ=GetTriggerScheduleResult)
    return __ret__.apply(lambda __response__: GetTriggerScheduleResult(
        activated=pulumi.get(__response__, 'activated'),
        annotations=pulumi.get(__response__, 'annotations'),
        data_factory_id=pulumi.get(__response__, 'data_factory_id'),
        description=pulumi.get(__response__, 'description'),
        end_time=pulumi.get(__response__, 'end_time'),
        frequency=pulumi.get(__response__, 'frequency'),
        id=pulumi.get(__response__, 'id'),
        interval=pulumi.get(__response__, 'interval'),
        name=pulumi.get(__response__, 'name'),
        pipeline_name=pulumi.get(__response__, 'pipeline_name'),
        schedules=pulumi.get(__response__, 'schedules'),
        start_time=pulumi.get(__response__, 'start_time'),
        time_zone=pulumi.get(__response__, 'time_zone')))
