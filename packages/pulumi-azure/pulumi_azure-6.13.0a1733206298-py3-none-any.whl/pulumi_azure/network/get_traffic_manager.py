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

__all__ = [
    'GetTrafficManagerResult',
    'AwaitableGetTrafficManagerResult',
    'get_traffic_manager',
    'get_traffic_manager_output',
]

@pulumi.output_type
class GetTrafficManagerResult:
    """
    A collection of values returned by getTrafficManager.
    """
    def __init__(__self__, id=None, name=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")


class AwaitableGetTrafficManagerResult(GetTrafficManagerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTrafficManagerResult(
            id=self.id,
            name=self.name)


def get_traffic_manager(name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTrafficManagerResult:
    """
    Use this data source to access the ID of a specified Traffic Manager Geographical Location within the Geographical Hierarchy.

    ## Example Usage

    ### World)

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_traffic_manager(name="World")
    pulumi.export("locationCode", example.id)
    ```


    :param str name: Specifies the name of the Location, for example `World`, `Europe` or `Germany`.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:network/getTrafficManager:getTrafficManager', __args__, opts=opts, typ=GetTrafficManagerResult).value

    return AwaitableGetTrafficManagerResult(
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'))
def get_traffic_manager_output(name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTrafficManagerResult]:
    """
    Use this data source to access the ID of a specified Traffic Manager Geographical Location within the Geographical Hierarchy.

    ## Example Usage

    ### World)

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_traffic_manager(name="World")
    pulumi.export("locationCode", example.id)
    ```


    :param str name: Specifies the name of the Location, for example `World`, `Europe` or `Germany`.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:network/getTrafficManager:getTrafficManager', __args__, opts=opts, typ=GetTrafficManagerResult)
    return __ret__.apply(lambda __response__: GetTrafficManagerResult(
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name')))
