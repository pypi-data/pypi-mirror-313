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
    'GetAccessPolicyResult',
    'AwaitableGetAccessPolicyResult',
    'get_access_policy',
    'get_access_policy_output',
]

@pulumi.output_type
class GetAccessPolicyResult:
    """
    A collection of values returned by getAccessPolicy.
    """
    def __init__(__self__, certificate_permissions=None, id=None, key_permissions=None, name=None, secret_permissions=None):
        if certificate_permissions and not isinstance(certificate_permissions, list):
            raise TypeError("Expected argument 'certificate_permissions' to be a list")
        pulumi.set(__self__, "certificate_permissions", certificate_permissions)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if key_permissions and not isinstance(key_permissions, list):
            raise TypeError("Expected argument 'key_permissions' to be a list")
        pulumi.set(__self__, "key_permissions", key_permissions)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if secret_permissions and not isinstance(secret_permissions, list):
            raise TypeError("Expected argument 'secret_permissions' to be a list")
        pulumi.set(__self__, "secret_permissions", secret_permissions)

    @property
    @pulumi.getter(name="certificatePermissions")
    def certificate_permissions(self) -> Sequence[str]:
        """
        the certificate permissions for the access policy
        """
        return pulumi.get(self, "certificate_permissions")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="keyPermissions")
    def key_permissions(self) -> Sequence[str]:
        """
        the key permissions for the access policy
        """
        return pulumi.get(self, "key_permissions")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="secretPermissions")
    def secret_permissions(self) -> Sequence[str]:
        """
        the secret permissions for the access policy
        """
        return pulumi.get(self, "secret_permissions")


class AwaitableGetAccessPolicyResult(GetAccessPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccessPolicyResult(
            certificate_permissions=self.certificate_permissions,
            id=self.id,
            key_permissions=self.key_permissions,
            name=self.name,
            secret_permissions=self.secret_permissions)


def get_access_policy(name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccessPolicyResult:
    """
    Use this data source to access information about the permissions from the Management Key Vault Templates.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    contributor = azure.keyvault.get_access_policy(name="Key Management")
    pulumi.export("accessPolicyKeyPermissions", contributor.key_permissions)
    ```


    :param str name: Specifies the name of the Management Template. Possible values are: `Key Management`,
           `Secret Management`, `Certificate Management`, `Key & Secret Management`, `Key & Certificate Management`,
           `Secret & Certificate Management`,  `Key, Secret, & Certificate Management`
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:keyvault/getAccessPolicy:getAccessPolicy', __args__, opts=opts, typ=GetAccessPolicyResult).value

    return AwaitableGetAccessPolicyResult(
        certificate_permissions=pulumi.get(__ret__, 'certificate_permissions'),
        id=pulumi.get(__ret__, 'id'),
        key_permissions=pulumi.get(__ret__, 'key_permissions'),
        name=pulumi.get(__ret__, 'name'),
        secret_permissions=pulumi.get(__ret__, 'secret_permissions'))
def get_access_policy_output(name: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAccessPolicyResult]:
    """
    Use this data source to access information about the permissions from the Management Key Vault Templates.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    contributor = azure.keyvault.get_access_policy(name="Key Management")
    pulumi.export("accessPolicyKeyPermissions", contributor.key_permissions)
    ```


    :param str name: Specifies the name of the Management Template. Possible values are: `Key Management`,
           `Secret Management`, `Certificate Management`, `Key & Secret Management`, `Key & Certificate Management`,
           `Secret & Certificate Management`,  `Key, Secret, & Certificate Management`
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:keyvault/getAccessPolicy:getAccessPolicy', __args__, opts=opts, typ=GetAccessPolicyResult)
    return __ret__.apply(lambda __response__: GetAccessPolicyResult(
        certificate_permissions=pulumi.get(__response__, 'certificate_permissions'),
        id=pulumi.get(__response__, 'id'),
        key_permissions=pulumi.get(__response__, 'key_permissions'),
        name=pulumi.get(__response__, 'name'),
        secret_permissions=pulumi.get(__response__, 'secret_permissions')))
