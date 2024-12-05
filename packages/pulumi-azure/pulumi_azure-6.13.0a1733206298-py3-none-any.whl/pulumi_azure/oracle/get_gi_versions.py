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
    'GetGiVersionsResult',
    'AwaitableGetGiVersionsResult',
    'get_gi_versions',
    'get_gi_versions_output',
]

@pulumi.output_type
class GetGiVersionsResult:
    """
    A collection of values returned by getGiVersions.
    """
    def __init__(__self__, id=None, location=None, versions=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if versions and not isinstance(versions, list):
            raise TypeError("Expected argument 'versions' to be a list")
        pulumi.set(__self__, "versions", versions)

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
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def versions(self) -> Sequence[str]:
        """
        A list of valid GI software versions.
        """
        return pulumi.get(self, "versions")


class AwaitableGetGiVersionsResult(GetGiVersionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGiVersionsResult(
            id=self.id,
            location=self.location,
            versions=self.versions)


def get_gi_versions(location: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGiVersionsResult:
    """
    This data source provides the list of GI Versions in Oracle Cloud Infrastructure Database service.

    Gets a list of supported GI versions.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.oracle.get_gi_versions(location="West Europe")
    pulumi.export("example", example)
    ```


    :param str location: The Azure Region to query for the GI Versions in.
    """
    __args__ = dict()
    __args__['location'] = location
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:oracle/getGiVersions:getGiVersions', __args__, opts=opts, typ=GetGiVersionsResult).value

    return AwaitableGetGiVersionsResult(
        id=pulumi.get(__ret__, 'id'),
        location=pulumi.get(__ret__, 'location'),
        versions=pulumi.get(__ret__, 'versions'))
def get_gi_versions_output(location: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGiVersionsResult]:
    """
    This data source provides the list of GI Versions in Oracle Cloud Infrastructure Database service.

    Gets a list of supported GI versions.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.oracle.get_gi_versions(location="West Europe")
    pulumi.export("example", example)
    ```


    :param str location: The Azure Region to query for the GI Versions in.
    """
    __args__ = dict()
    __args__['location'] = location
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:oracle/getGiVersions:getGiVersions', __args__, opts=opts, typ=GetGiVersionsResult)
    return __ret__.apply(lambda __response__: GetGiVersionsResult(
        id=pulumi.get(__response__, 'id'),
        location=pulumi.get(__response__, 'location'),
        versions=pulumi.get(__response__, 'versions')))
