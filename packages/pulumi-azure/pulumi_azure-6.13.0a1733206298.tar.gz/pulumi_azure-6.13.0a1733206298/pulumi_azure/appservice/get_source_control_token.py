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
    'GetSourceControlTokenResult',
    'AwaitableGetSourceControlTokenResult',
    'get_source_control_token',
    'get_source_control_token_output',
]

@pulumi.output_type
class GetSourceControlTokenResult:
    """
    A collection of values returned by getSourceControlToken.
    """
    def __init__(__self__, id=None, token=None, token_secret=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if token and not isinstance(token, str):
            raise TypeError("Expected argument 'token' to be a str")
        pulumi.set(__self__, "token", token)
        if token_secret and not isinstance(token_secret, str):
            raise TypeError("Expected argument 'token_secret' to be a str")
        pulumi.set(__self__, "token_secret", token_secret)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def token(self) -> str:
        """
        The GitHub Token value.
        """
        return pulumi.get(self, "token")

    @property
    @pulumi.getter(name="tokenSecret")
    def token_secret(self) -> str:
        return pulumi.get(self, "token_secret")

    @property
    @pulumi.getter
    def type(self) -> str:
        return pulumi.get(self, "type")


class AwaitableGetSourceControlTokenResult(GetSourceControlTokenResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSourceControlTokenResult(
            id=self.id,
            token=self.token,
            token_secret=self.token_secret,
            type=self.type)


def get_source_control_token(type: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSourceControlTokenResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.appservice.get_source_control_token(type="GitHub")
    pulumi.export("id", example_azurerm_app_service_github_token["id"])
    ```


    :param str type: The Token type. Possible values include `Bitbucket`, `Dropbox`, `Github`, and `OneDrive`.
    """
    __args__ = dict()
    __args__['type'] = type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:appservice/getSourceControlToken:getSourceControlToken', __args__, opts=opts, typ=GetSourceControlTokenResult).value

    return AwaitableGetSourceControlTokenResult(
        id=pulumi.get(__ret__, 'id'),
        token=pulumi.get(__ret__, 'token'),
        token_secret=pulumi.get(__ret__, 'token_secret'),
        type=pulumi.get(__ret__, 'type'))
def get_source_control_token_output(type: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSourceControlTokenResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.appservice.get_source_control_token(type="GitHub")
    pulumi.export("id", example_azurerm_app_service_github_token["id"])
    ```


    :param str type: The Token type. Possible values include `Bitbucket`, `Dropbox`, `Github`, and `OneDrive`.
    """
    __args__ = dict()
    __args__['type'] = type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:appservice/getSourceControlToken:getSourceControlToken', __args__, opts=opts, typ=GetSourceControlTokenResult)
    return __ret__.apply(lambda __response__: GetSourceControlTokenResult(
        id=pulumi.get(__response__, 'id'),
        token=pulumi.get(__response__, 'token'),
        token_secret=pulumi.get(__response__, 'token_secret'),
        type=pulumi.get(__response__, 'type')))
