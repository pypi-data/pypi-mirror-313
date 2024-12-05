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
    'GetDefinitionResult',
    'AwaitableGetDefinitionResult',
    'get_definition',
    'get_definition_output',
]

@pulumi.output_type
class GetDefinitionResult:
    """
    A collection of values returned by getDefinition.
    """
    def __init__(__self__, description=None, display_name=None, id=None, last_modified=None, name=None, scope_id=None, target_scope=None, time_created=None, versions=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_modified and not isinstance(last_modified, str):
            raise TypeError("Expected argument 'last_modified' to be a str")
        pulumi.set(__self__, "last_modified", last_modified)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if scope_id and not isinstance(scope_id, str):
            raise TypeError("Expected argument 'scope_id' to be a str")
        pulumi.set(__self__, "scope_id", scope_id)
        if target_scope and not isinstance(target_scope, str):
            raise TypeError("Expected argument 'target_scope' to be a str")
        pulumi.set(__self__, "target_scope", target_scope)
        if time_created and not isinstance(time_created, str):
            raise TypeError("Expected argument 'time_created' to be a str")
        pulumi.set(__self__, "time_created", time_created)
        if versions and not isinstance(versions, list):
            raise TypeError("Expected argument 'versions' to be a list")
        pulumi.set(__self__, "versions", versions)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of the Blueprint Definition.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The display name of the Blueprint Definition.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> str:
        """
        The timestamp of when this last modification was saved to the Blueprint Definition.
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="scopeId")
    def scope_id(self) -> str:
        return pulumi.get(self, "scope_id")

    @property
    @pulumi.getter(name="targetScope")
    def target_scope(self) -> str:
        """
        The target scope.
        """
        return pulumi.get(self, "target_scope")

    @property
    @pulumi.getter(name="timeCreated")
    def time_created(self) -> str:
        """
        The timestamp of when this Blueprint Definition was created.
        """
        return pulumi.get(self, "time_created")

    @property
    @pulumi.getter
    def versions(self) -> Sequence[str]:
        """
        A list of versions published for this Blueprint Definition.
        """
        return pulumi.get(self, "versions")


class AwaitableGetDefinitionResult(GetDefinitionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDefinitionResult(
            description=self.description,
            display_name=self.display_name,
            id=self.id,
            last_modified=self.last_modified,
            name=self.name,
            scope_id=self.scope_id,
            target_scope=self.target_scope,
            time_created=self.time_created,
            versions=self.versions)


def get_definition(name: Optional[str] = None,
                   scope_id: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDefinitionResult:
    """
    Use this data source to access information about an existing Azure Blueprint Definition

    > **NOTE:** Azure Blueprints are in Preview and potentially subject to breaking change without notice.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    current = azure.core.get_client_config()
    root = azure.management.get_group(name=current.tenant_id)
    example = azure.blueprint.get_definition(name="exampleManagementGroupBP",
        scope_id=root.id)
    ```


    :param str name: The name of the Blueprint.
    :param str scope_id: The ID of the Subscription or Management Group, as the scope at which the blueprint definition is stored.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['scopeId'] = scope_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:blueprint/getDefinition:getDefinition', __args__, opts=opts, typ=GetDefinitionResult).value

    return AwaitableGetDefinitionResult(
        description=pulumi.get(__ret__, 'description'),
        display_name=pulumi.get(__ret__, 'display_name'),
        id=pulumi.get(__ret__, 'id'),
        last_modified=pulumi.get(__ret__, 'last_modified'),
        name=pulumi.get(__ret__, 'name'),
        scope_id=pulumi.get(__ret__, 'scope_id'),
        target_scope=pulumi.get(__ret__, 'target_scope'),
        time_created=pulumi.get(__ret__, 'time_created'),
        versions=pulumi.get(__ret__, 'versions'))
def get_definition_output(name: Optional[pulumi.Input[str]] = None,
                          scope_id: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDefinitionResult]:
    """
    Use this data source to access information about an existing Azure Blueprint Definition

    > **NOTE:** Azure Blueprints are in Preview and potentially subject to breaking change without notice.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    current = azure.core.get_client_config()
    root = azure.management.get_group(name=current.tenant_id)
    example = azure.blueprint.get_definition(name="exampleManagementGroupBP",
        scope_id=root.id)
    ```


    :param str name: The name of the Blueprint.
    :param str scope_id: The ID of the Subscription or Management Group, as the scope at which the blueprint definition is stored.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['scopeId'] = scope_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:blueprint/getDefinition:getDefinition', __args__, opts=opts, typ=GetDefinitionResult)
    return __ret__.apply(lambda __response__: GetDefinitionResult(
        description=pulumi.get(__response__, 'description'),
        display_name=pulumi.get(__response__, 'display_name'),
        id=pulumi.get(__response__, 'id'),
        last_modified=pulumi.get(__response__, 'last_modified'),
        name=pulumi.get(__response__, 'name'),
        scope_id=pulumi.get(__response__, 'scope_id'),
        target_scope=pulumi.get(__response__, 'target_scope'),
        time_created=pulumi.get(__response__, 'time_created'),
        versions=pulumi.get(__response__, 'versions')))
