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
    'GetNetworkSimPolicyResult',
    'AwaitableGetNetworkSimPolicyResult',
    'get_network_sim_policy',
    'get_network_sim_policy_output',
]

@pulumi.output_type
class GetNetworkSimPolicyResult:
    """
    A collection of values returned by getNetworkSimPolicy.
    """
    def __init__(__self__, default_slice_id=None, id=None, location=None, mobile_network_id=None, name=None, rat_frequency_selection_priority_index=None, registration_timer_in_seconds=None, slices=None, tags=None, user_equipment_aggregate_maximum_bit_rates=None):
        if default_slice_id and not isinstance(default_slice_id, str):
            raise TypeError("Expected argument 'default_slice_id' to be a str")
        pulumi.set(__self__, "default_slice_id", default_slice_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if mobile_network_id and not isinstance(mobile_network_id, str):
            raise TypeError("Expected argument 'mobile_network_id' to be a str")
        pulumi.set(__self__, "mobile_network_id", mobile_network_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if rat_frequency_selection_priority_index and not isinstance(rat_frequency_selection_priority_index, int):
            raise TypeError("Expected argument 'rat_frequency_selection_priority_index' to be a int")
        pulumi.set(__self__, "rat_frequency_selection_priority_index", rat_frequency_selection_priority_index)
        if registration_timer_in_seconds and not isinstance(registration_timer_in_seconds, int):
            raise TypeError("Expected argument 'registration_timer_in_seconds' to be a int")
        pulumi.set(__self__, "registration_timer_in_seconds", registration_timer_in_seconds)
        if slices and not isinstance(slices, list):
            raise TypeError("Expected argument 'slices' to be a list")
        pulumi.set(__self__, "slices", slices)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if user_equipment_aggregate_maximum_bit_rates and not isinstance(user_equipment_aggregate_maximum_bit_rates, list):
            raise TypeError("Expected argument 'user_equipment_aggregate_maximum_bit_rates' to be a list")
        pulumi.set(__self__, "user_equipment_aggregate_maximum_bit_rates", user_equipment_aggregate_maximum_bit_rates)

    @property
    @pulumi.getter(name="defaultSliceId")
    def default_slice_id(self) -> str:
        """
        The ID of default slice to use if the UE does not explicitly specify it.
        """
        return pulumi.get(self, "default_slice_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure Region where the Mobile Network Sim Policy should exist.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="mobileNetworkId")
    def mobile_network_id(self) -> str:
        return pulumi.get(self, "mobile_network_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="ratFrequencySelectionPriorityIndex")
    def rat_frequency_selection_priority_index(self) -> int:
        """
        RAT/Frequency Selection Priority Index, defined in 3GPP TS 36.413.
        """
        return pulumi.get(self, "rat_frequency_selection_priority_index")

    @property
    @pulumi.getter(name="registrationTimerInSeconds")
    def registration_timer_in_seconds(self) -> int:
        """
        Interval for the UE periodic registration update procedure.
        """
        return pulumi.get(self, "registration_timer_in_seconds")

    @property
    @pulumi.getter
    def slices(self) -> Sequence['outputs.GetNetworkSimPolicySliceResult']:
        """
        An array of `slice` block as defined below. The allowed slices and the settings to use for them.
        """
        return pulumi.get(self, "slices")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags which should be assigned to the Mobile Network Sim Policies.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="userEquipmentAggregateMaximumBitRates")
    def user_equipment_aggregate_maximum_bit_rates(self) -> Sequence['outputs.GetNetworkSimPolicyUserEquipmentAggregateMaximumBitRateResult']:
        """
        A `user_equipment_aggregate_maximum_bit_rate` block as defined below.
        """
        return pulumi.get(self, "user_equipment_aggregate_maximum_bit_rates")


class AwaitableGetNetworkSimPolicyResult(GetNetworkSimPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworkSimPolicyResult(
            default_slice_id=self.default_slice_id,
            id=self.id,
            location=self.location,
            mobile_network_id=self.mobile_network_id,
            name=self.name,
            rat_frequency_selection_priority_index=self.rat_frequency_selection_priority_index,
            registration_timer_in_seconds=self.registration_timer_in_seconds,
            slices=self.slices,
            tags=self.tags,
            user_equipment_aggregate_maximum_bit_rates=self.user_equipment_aggregate_maximum_bit_rates)


def get_network_sim_policy(mobile_network_id: Optional[str] = None,
                           name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNetworkSimPolicyResult:
    """
    Get information about a Mobile Network Sim Policy.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.mobile.get_network(name="example-mn",
        resource_group_name="example-rg")
    example_get_network_sim_policy = azure.mobile.get_network_sim_policy(name="example-mnsp",
        mobile_network_id=example.id)
    ```


    :param str mobile_network_id: The ID of the Mobile Network which the Sim Policy belongs to.
    :param str name: The name which should be used for this Mobile Network Sim Policies.
    """
    __args__ = dict()
    __args__['mobileNetworkId'] = mobile_network_id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:mobile/getNetworkSimPolicy:getNetworkSimPolicy', __args__, opts=opts, typ=GetNetworkSimPolicyResult).value

    return AwaitableGetNetworkSimPolicyResult(
        default_slice_id=pulumi.get(__ret__, 'default_slice_id'),
        id=pulumi.get(__ret__, 'id'),
        location=pulumi.get(__ret__, 'location'),
        mobile_network_id=pulumi.get(__ret__, 'mobile_network_id'),
        name=pulumi.get(__ret__, 'name'),
        rat_frequency_selection_priority_index=pulumi.get(__ret__, 'rat_frequency_selection_priority_index'),
        registration_timer_in_seconds=pulumi.get(__ret__, 'registration_timer_in_seconds'),
        slices=pulumi.get(__ret__, 'slices'),
        tags=pulumi.get(__ret__, 'tags'),
        user_equipment_aggregate_maximum_bit_rates=pulumi.get(__ret__, 'user_equipment_aggregate_maximum_bit_rates'))
def get_network_sim_policy_output(mobile_network_id: Optional[pulumi.Input[str]] = None,
                                  name: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNetworkSimPolicyResult]:
    """
    Get information about a Mobile Network Sim Policy.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.mobile.get_network(name="example-mn",
        resource_group_name="example-rg")
    example_get_network_sim_policy = azure.mobile.get_network_sim_policy(name="example-mnsp",
        mobile_network_id=example.id)
    ```


    :param str mobile_network_id: The ID of the Mobile Network which the Sim Policy belongs to.
    :param str name: The name which should be used for this Mobile Network Sim Policies.
    """
    __args__ = dict()
    __args__['mobileNetworkId'] = mobile_network_id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:mobile/getNetworkSimPolicy:getNetworkSimPolicy', __args__, opts=opts, typ=GetNetworkSimPolicyResult)
    return __ret__.apply(lambda __response__: GetNetworkSimPolicyResult(
        default_slice_id=pulumi.get(__response__, 'default_slice_id'),
        id=pulumi.get(__response__, 'id'),
        location=pulumi.get(__response__, 'location'),
        mobile_network_id=pulumi.get(__response__, 'mobile_network_id'),
        name=pulumi.get(__response__, 'name'),
        rat_frequency_selection_priority_index=pulumi.get(__response__, 'rat_frequency_selection_priority_index'),
        registration_timer_in_seconds=pulumi.get(__response__, 'registration_timer_in_seconds'),
        slices=pulumi.get(__response__, 'slices'),
        tags=pulumi.get(__response__, 'tags'),
        user_equipment_aggregate_maximum_bit_rates=pulumi.get(__response__, 'user_equipment_aggregate_maximum_bit_rates')))
