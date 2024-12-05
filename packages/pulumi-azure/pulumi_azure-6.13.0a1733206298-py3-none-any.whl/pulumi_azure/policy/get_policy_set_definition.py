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
    'GetPolicySetDefinitionResult',
    'AwaitableGetPolicySetDefinitionResult',
    'get_policy_set_definition',
    'get_policy_set_definition_output',
]

@pulumi.output_type
class GetPolicySetDefinitionResult:
    """
    A collection of values returned by getPolicySetDefinition.
    """
    def __init__(__self__, description=None, display_name=None, id=None, management_group_name=None, metadata=None, name=None, parameters=None, policy_definition_groups=None, policy_definition_references=None, policy_definitions=None, policy_type=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if management_group_name and not isinstance(management_group_name, str):
            raise TypeError("Expected argument 'management_group_name' to be a str")
        pulumi.set(__self__, "management_group_name", management_group_name)
        if metadata and not isinstance(metadata, str):
            raise TypeError("Expected argument 'metadata' to be a str")
        pulumi.set(__self__, "metadata", metadata)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if parameters and not isinstance(parameters, str):
            raise TypeError("Expected argument 'parameters' to be a str")
        pulumi.set(__self__, "parameters", parameters)
        if policy_definition_groups and not isinstance(policy_definition_groups, list):
            raise TypeError("Expected argument 'policy_definition_groups' to be a list")
        pulumi.set(__self__, "policy_definition_groups", policy_definition_groups)
        if policy_definition_references and not isinstance(policy_definition_references, list):
            raise TypeError("Expected argument 'policy_definition_references' to be a list")
        pulumi.set(__self__, "policy_definition_references", policy_definition_references)
        if policy_definitions and not isinstance(policy_definitions, str):
            raise TypeError("Expected argument 'policy_definitions' to be a str")
        pulumi.set(__self__, "policy_definitions", policy_definitions)
        if policy_type and not isinstance(policy_type, str):
            raise TypeError("Expected argument 'policy_type' to be a str")
        pulumi.set(__self__, "policy_type", policy_type)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of this policy definition group.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The display name of this policy definition group.
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
    @pulumi.getter(name="managementGroupName")
    def management_group_name(self) -> Optional[str]:
        return pulumi.get(self, "management_group_name")

    @property
    @pulumi.getter
    def metadata(self) -> str:
        """
        Any Metadata defined in the Policy Set Definition.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of this policy definition group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> str:
        """
        The mapping of the parameter values for the referenced policy rule. The keys are the parameter names.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="policyDefinitionGroups")
    def policy_definition_groups(self) -> Sequence['outputs.GetPolicySetDefinitionPolicyDefinitionGroupResult']:
        """
        One or more `policy_definition_group` blocks as defined below.
        """
        return pulumi.get(self, "policy_definition_groups")

    @property
    @pulumi.getter(name="policyDefinitionReferences")
    def policy_definition_references(self) -> Sequence['outputs.GetPolicySetDefinitionPolicyDefinitionReferenceResult']:
        """
        One or more `policy_definition_reference` blocks as defined below.
        """
        return pulumi.get(self, "policy_definition_references")

    @property
    @pulumi.getter(name="policyDefinitions")
    def policy_definitions(self) -> str:
        """
        The policy definitions contained within the policy set definition.
        """
        return pulumi.get(self, "policy_definitions")

    @property
    @pulumi.getter(name="policyType")
    def policy_type(self) -> str:
        """
        The Type of the Policy Set Definition.
        """
        return pulumi.get(self, "policy_type")


class AwaitableGetPolicySetDefinitionResult(GetPolicySetDefinitionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicySetDefinitionResult(
            description=self.description,
            display_name=self.display_name,
            id=self.id,
            management_group_name=self.management_group_name,
            metadata=self.metadata,
            name=self.name,
            parameters=self.parameters,
            policy_definition_groups=self.policy_definition_groups,
            policy_definition_references=self.policy_definition_references,
            policy_definitions=self.policy_definitions,
            policy_type=self.policy_type)


def get_policy_set_definition(display_name: Optional[str] = None,
                              management_group_name: Optional[str] = None,
                              name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicySetDefinitionResult:
    """
    Use this data source to access information about an existing Policy Set Definition.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.policy.get_policy_set_definition(display_name="Policy Set Definition Example")
    pulumi.export("id", example.id)
    ```


    :param str display_name: Specifies the display name of the Policy Set Definition. Conflicts with `name`.
           
           **NOTE** As `display_name` is not unique errors may occur when there are multiple policy set definitions with same display name.
    :param str management_group_name: Only retrieve Policy Set Definitions from this Management Group.
    :param str name: Specifies the name of the Policy Set Definition. Conflicts with `display_name`.
    """
    __args__ = dict()
    __args__['displayName'] = display_name
    __args__['managementGroupName'] = management_group_name
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure:policy/getPolicySetDefinition:getPolicySetDefinition', __args__, opts=opts, typ=GetPolicySetDefinitionResult).value

    return AwaitableGetPolicySetDefinitionResult(
        description=pulumi.get(__ret__, 'description'),
        display_name=pulumi.get(__ret__, 'display_name'),
        id=pulumi.get(__ret__, 'id'),
        management_group_name=pulumi.get(__ret__, 'management_group_name'),
        metadata=pulumi.get(__ret__, 'metadata'),
        name=pulumi.get(__ret__, 'name'),
        parameters=pulumi.get(__ret__, 'parameters'),
        policy_definition_groups=pulumi.get(__ret__, 'policy_definition_groups'),
        policy_definition_references=pulumi.get(__ret__, 'policy_definition_references'),
        policy_definitions=pulumi.get(__ret__, 'policy_definitions'),
        policy_type=pulumi.get(__ret__, 'policy_type'))
def get_policy_set_definition_output(display_name: Optional[pulumi.Input[Optional[str]]] = None,
                                     management_group_name: Optional[pulumi.Input[Optional[str]]] = None,
                                     name: Optional[pulumi.Input[Optional[str]]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPolicySetDefinitionResult]:
    """
    Use this data source to access information about an existing Policy Set Definition.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.policy.get_policy_set_definition(display_name="Policy Set Definition Example")
    pulumi.export("id", example.id)
    ```


    :param str display_name: Specifies the display name of the Policy Set Definition. Conflicts with `name`.
           
           **NOTE** As `display_name` is not unique errors may occur when there are multiple policy set definitions with same display name.
    :param str management_group_name: Only retrieve Policy Set Definitions from this Management Group.
    :param str name: Specifies the name of the Policy Set Definition. Conflicts with `display_name`.
    """
    __args__ = dict()
    __args__['displayName'] = display_name
    __args__['managementGroupName'] = management_group_name
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure:policy/getPolicySetDefinition:getPolicySetDefinition', __args__, opts=opts, typ=GetPolicySetDefinitionResult)
    return __ret__.apply(lambda __response__: GetPolicySetDefinitionResult(
        description=pulumi.get(__response__, 'description'),
        display_name=pulumi.get(__response__, 'display_name'),
        id=pulumi.get(__response__, 'id'),
        management_group_name=pulumi.get(__response__, 'management_group_name'),
        metadata=pulumi.get(__response__, 'metadata'),
        name=pulumi.get(__response__, 'name'),
        parameters=pulumi.get(__response__, 'parameters'),
        policy_definition_groups=pulumi.get(__response__, 'policy_definition_groups'),
        policy_definition_references=pulumi.get(__response__, 'policy_definition_references'),
        policy_definitions=pulumi.get(__response__, 'policy_definitions'),
        policy_type=pulumi.get(__response__, 'policy_type')))
