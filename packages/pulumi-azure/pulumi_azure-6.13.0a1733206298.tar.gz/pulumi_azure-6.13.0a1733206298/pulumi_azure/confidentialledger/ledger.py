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
from ._inputs import *

__all__ = ['LedgerArgs', 'Ledger']

@pulumi.input_type
class LedgerArgs:
    def __init__(__self__, *,
                 azuread_based_service_principals: pulumi.Input[Sequence[pulumi.Input['LedgerAzureadBasedServicePrincipalArgs']]],
                 ledger_type: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 certificate_based_security_principals: Optional[pulumi.Input[Sequence[pulumi.Input['LedgerCertificateBasedSecurityPrincipalArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Ledger resource.
        :param pulumi.Input[Sequence[pulumi.Input['LedgerAzureadBasedServicePrincipalArgs']]] azuread_based_service_principals: A list of `azuread_based_service_principal` blocks as defined below.
        :param pulumi.Input[str] ledger_type: Specifies the type of Confidential Ledger. Possible values are `Private` and `Public`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Confidential Ledger exists. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['LedgerCertificateBasedSecurityPrincipalArgs']]] certificate_based_security_principals: A list of `certificate_based_security_principal` blocks as defined below.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the Confidential Ledger exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Confidential Ledger. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the Confidential Ledger.
        """
        pulumi.set(__self__, "azuread_based_service_principals", azuread_based_service_principals)
        pulumi.set(__self__, "ledger_type", ledger_type)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if certificate_based_security_principals is not None:
            pulumi.set(__self__, "certificate_based_security_principals", certificate_based_security_principals)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="azureadBasedServicePrincipals")
    def azuread_based_service_principals(self) -> pulumi.Input[Sequence[pulumi.Input['LedgerAzureadBasedServicePrincipalArgs']]]:
        """
        A list of `azuread_based_service_principal` blocks as defined below.
        """
        return pulumi.get(self, "azuread_based_service_principals")

    @azuread_based_service_principals.setter
    def azuread_based_service_principals(self, value: pulumi.Input[Sequence[pulumi.Input['LedgerAzureadBasedServicePrincipalArgs']]]):
        pulumi.set(self, "azuread_based_service_principals", value)

    @property
    @pulumi.getter(name="ledgerType")
    def ledger_type(self) -> pulumi.Input[str]:
        """
        Specifies the type of Confidential Ledger. Possible values are `Private` and `Public`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "ledger_type")

    @ledger_type.setter
    def ledger_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "ledger_type", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Confidential Ledger exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="certificateBasedSecurityPrincipals")
    def certificate_based_security_principals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LedgerCertificateBasedSecurityPrincipalArgs']]]]:
        """
        A list of `certificate_based_security_principal` blocks as defined below.
        """
        return pulumi.get(self, "certificate_based_security_principals")

    @certificate_based_security_principals.setter
    def certificate_based_security_principals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LedgerCertificateBasedSecurityPrincipalArgs']]]]):
        pulumi.set(self, "certificate_based_security_principals", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the Confidential Ledger exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Confidential Ledger. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the Confidential Ledger.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _LedgerState:
    def __init__(__self__, *,
                 azuread_based_service_principals: Optional[pulumi.Input[Sequence[pulumi.Input['LedgerAzureadBasedServicePrincipalArgs']]]] = None,
                 certificate_based_security_principals: Optional[pulumi.Input[Sequence[pulumi.Input['LedgerCertificateBasedSecurityPrincipalArgs']]]] = None,
                 identity_service_endpoint: Optional[pulumi.Input[str]] = None,
                 ledger_endpoint: Optional[pulumi.Input[str]] = None,
                 ledger_type: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Ledger resources.
        :param pulumi.Input[Sequence[pulumi.Input['LedgerAzureadBasedServicePrincipalArgs']]] azuread_based_service_principals: A list of `azuread_based_service_principal` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['LedgerCertificateBasedSecurityPrincipalArgs']]] certificate_based_security_principals: A list of `certificate_based_security_principal` blocks as defined below.
        :param pulumi.Input[str] identity_service_endpoint: The Identity Service Endpoint for this Confidential Ledger.
        :param pulumi.Input[str] ledger_endpoint: The Endpoint for this Confidential Ledger.
        :param pulumi.Input[str] ledger_type: Specifies the type of Confidential Ledger. Possible values are `Private` and `Public`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the Confidential Ledger exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Confidential Ledger. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Confidential Ledger exists. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the Confidential Ledger.
        """
        if azuread_based_service_principals is not None:
            pulumi.set(__self__, "azuread_based_service_principals", azuread_based_service_principals)
        if certificate_based_security_principals is not None:
            pulumi.set(__self__, "certificate_based_security_principals", certificate_based_security_principals)
        if identity_service_endpoint is not None:
            pulumi.set(__self__, "identity_service_endpoint", identity_service_endpoint)
        if ledger_endpoint is not None:
            pulumi.set(__self__, "ledger_endpoint", ledger_endpoint)
        if ledger_type is not None:
            pulumi.set(__self__, "ledger_type", ledger_type)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="azureadBasedServicePrincipals")
    def azuread_based_service_principals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LedgerAzureadBasedServicePrincipalArgs']]]]:
        """
        A list of `azuread_based_service_principal` blocks as defined below.
        """
        return pulumi.get(self, "azuread_based_service_principals")

    @azuread_based_service_principals.setter
    def azuread_based_service_principals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LedgerAzureadBasedServicePrincipalArgs']]]]):
        pulumi.set(self, "azuread_based_service_principals", value)

    @property
    @pulumi.getter(name="certificateBasedSecurityPrincipals")
    def certificate_based_security_principals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LedgerCertificateBasedSecurityPrincipalArgs']]]]:
        """
        A list of `certificate_based_security_principal` blocks as defined below.
        """
        return pulumi.get(self, "certificate_based_security_principals")

    @certificate_based_security_principals.setter
    def certificate_based_security_principals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LedgerCertificateBasedSecurityPrincipalArgs']]]]):
        pulumi.set(self, "certificate_based_security_principals", value)

    @property
    @pulumi.getter(name="identityServiceEndpoint")
    def identity_service_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The Identity Service Endpoint for this Confidential Ledger.
        """
        return pulumi.get(self, "identity_service_endpoint")

    @identity_service_endpoint.setter
    def identity_service_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity_service_endpoint", value)

    @property
    @pulumi.getter(name="ledgerEndpoint")
    def ledger_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The Endpoint for this Confidential Ledger.
        """
        return pulumi.get(self, "ledger_endpoint")

    @ledger_endpoint.setter
    def ledger_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ledger_endpoint", value)

    @property
    @pulumi.getter(name="ledgerType")
    def ledger_type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of Confidential Ledger. Possible values are `Private` and `Public`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "ledger_type")

    @ledger_type.setter
    def ledger_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ledger_type", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the Confidential Ledger exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Confidential Ledger. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Confidential Ledger exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the Confidential Ledger.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class Ledger(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 azuread_based_service_principals: Optional[pulumi.Input[Sequence[pulumi.Input[Union['LedgerAzureadBasedServicePrincipalArgs', 'LedgerAzureadBasedServicePrincipalArgsDict']]]]] = None,
                 certificate_based_security_principals: Optional[pulumi.Input[Sequence[pulumi.Input[Union['LedgerCertificateBasedSecurityPrincipalArgs', 'LedgerCertificateBasedSecurityPrincipalArgsDict']]]]] = None,
                 ledger_type: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a Confidential Ledger.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        ledger = azure.confidentialledger.Ledger("ledger",
            name="example-ledger",
            resource_group_name=example.name,
            location=example.location,
            ledger_type="Private",
            azuread_based_service_principals=[{
                "principal_id": current.object_id,
                "tenant_id": current.tenant_id,
                "ledger_role_name": "Administrator",
            }])
        ```

        ## Import

        Confidential Ledgers can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:confidentialledger/ledger:Ledger example /subscriptions/12345678-1234-9876-4563-123456789012/resourceGroups/example-group/providers/Microsoft.ConfidentialLedger/ledgers/example-ledger
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['LedgerAzureadBasedServicePrincipalArgs', 'LedgerAzureadBasedServicePrincipalArgsDict']]]] azuread_based_service_principals: A list of `azuread_based_service_principal` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[Union['LedgerCertificateBasedSecurityPrincipalArgs', 'LedgerCertificateBasedSecurityPrincipalArgsDict']]]] certificate_based_security_principals: A list of `certificate_based_security_principal` blocks as defined below.
        :param pulumi.Input[str] ledger_type: Specifies the type of Confidential Ledger. Possible values are `Private` and `Public`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the Confidential Ledger exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Confidential Ledger. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Confidential Ledger exists. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the Confidential Ledger.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LedgerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Confidential Ledger.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        ledger = azure.confidentialledger.Ledger("ledger",
            name="example-ledger",
            resource_group_name=example.name,
            location=example.location,
            ledger_type="Private",
            azuread_based_service_principals=[{
                "principal_id": current.object_id,
                "tenant_id": current.tenant_id,
                "ledger_role_name": "Administrator",
            }])
        ```

        ## Import

        Confidential Ledgers can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:confidentialledger/ledger:Ledger example /subscriptions/12345678-1234-9876-4563-123456789012/resourceGroups/example-group/providers/Microsoft.ConfidentialLedger/ledgers/example-ledger
        ```

        :param str resource_name: The name of the resource.
        :param LedgerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LedgerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 azuread_based_service_principals: Optional[pulumi.Input[Sequence[pulumi.Input[Union['LedgerAzureadBasedServicePrincipalArgs', 'LedgerAzureadBasedServicePrincipalArgsDict']]]]] = None,
                 certificate_based_security_principals: Optional[pulumi.Input[Sequence[pulumi.Input[Union['LedgerCertificateBasedSecurityPrincipalArgs', 'LedgerCertificateBasedSecurityPrincipalArgsDict']]]]] = None,
                 ledger_type: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LedgerArgs.__new__(LedgerArgs)

            if azuread_based_service_principals is None and not opts.urn:
                raise TypeError("Missing required property 'azuread_based_service_principals'")
            __props__.__dict__["azuread_based_service_principals"] = azuread_based_service_principals
            __props__.__dict__["certificate_based_security_principals"] = certificate_based_security_principals
            if ledger_type is None and not opts.urn:
                raise TypeError("Missing required property 'ledger_type'")
            __props__.__dict__["ledger_type"] = ledger_type
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["identity_service_endpoint"] = None
            __props__.__dict__["ledger_endpoint"] = None
        super(Ledger, __self__).__init__(
            'azure:confidentialledger/ledger:Ledger',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            azuread_based_service_principals: Optional[pulumi.Input[Sequence[pulumi.Input[Union['LedgerAzureadBasedServicePrincipalArgs', 'LedgerAzureadBasedServicePrincipalArgsDict']]]]] = None,
            certificate_based_security_principals: Optional[pulumi.Input[Sequence[pulumi.Input[Union['LedgerCertificateBasedSecurityPrincipalArgs', 'LedgerCertificateBasedSecurityPrincipalArgsDict']]]]] = None,
            identity_service_endpoint: Optional[pulumi.Input[str]] = None,
            ledger_endpoint: Optional[pulumi.Input[str]] = None,
            ledger_type: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Ledger':
        """
        Get an existing Ledger resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['LedgerAzureadBasedServicePrincipalArgs', 'LedgerAzureadBasedServicePrincipalArgsDict']]]] azuread_based_service_principals: A list of `azuread_based_service_principal` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[Union['LedgerCertificateBasedSecurityPrincipalArgs', 'LedgerCertificateBasedSecurityPrincipalArgsDict']]]] certificate_based_security_principals: A list of `certificate_based_security_principal` blocks as defined below.
        :param pulumi.Input[str] identity_service_endpoint: The Identity Service Endpoint for this Confidential Ledger.
        :param pulumi.Input[str] ledger_endpoint: The Endpoint for this Confidential Ledger.
        :param pulumi.Input[str] ledger_type: Specifies the type of Confidential Ledger. Possible values are `Private` and `Public`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the Confidential Ledger exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Confidential Ledger. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Confidential Ledger exists. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the Confidential Ledger.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LedgerState.__new__(_LedgerState)

        __props__.__dict__["azuread_based_service_principals"] = azuread_based_service_principals
        __props__.__dict__["certificate_based_security_principals"] = certificate_based_security_principals
        __props__.__dict__["identity_service_endpoint"] = identity_service_endpoint
        __props__.__dict__["ledger_endpoint"] = ledger_endpoint
        __props__.__dict__["ledger_type"] = ledger_type
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["tags"] = tags
        return Ledger(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="azureadBasedServicePrincipals")
    def azuread_based_service_principals(self) -> pulumi.Output[Sequence['outputs.LedgerAzureadBasedServicePrincipal']]:
        """
        A list of `azuread_based_service_principal` blocks as defined below.
        """
        return pulumi.get(self, "azuread_based_service_principals")

    @property
    @pulumi.getter(name="certificateBasedSecurityPrincipals")
    def certificate_based_security_principals(self) -> pulumi.Output[Optional[Sequence['outputs.LedgerCertificateBasedSecurityPrincipal']]]:
        """
        A list of `certificate_based_security_principal` blocks as defined below.
        """
        return pulumi.get(self, "certificate_based_security_principals")

    @property
    @pulumi.getter(name="identityServiceEndpoint")
    def identity_service_endpoint(self) -> pulumi.Output[str]:
        """
        The Identity Service Endpoint for this Confidential Ledger.
        """
        return pulumi.get(self, "identity_service_endpoint")

    @property
    @pulumi.getter(name="ledgerEndpoint")
    def ledger_endpoint(self) -> pulumi.Output[str]:
        """
        The Endpoint for this Confidential Ledger.
        """
        return pulumi.get(self, "ledger_endpoint")

    @property
    @pulumi.getter(name="ledgerType")
    def ledger_type(self) -> pulumi.Output[str]:
        """
        Specifies the type of Confidential Ledger. Possible values are `Private` and `Public`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "ledger_type")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the supported Azure location where the Confidential Ledger exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Confidential Ledger. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Confidential Ledger exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the Confidential Ledger.
        """
        return pulumi.get(self, "tags")

