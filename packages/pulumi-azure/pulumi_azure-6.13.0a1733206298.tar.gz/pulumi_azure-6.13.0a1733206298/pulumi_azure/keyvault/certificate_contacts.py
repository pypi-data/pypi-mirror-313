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

__all__ = ['CertificateContactsArgs', 'CertificateContacts']

@pulumi.input_type
class CertificateContactsArgs:
    def __init__(__self__, *,
                 key_vault_id: pulumi.Input[str],
                 contacts: Optional[pulumi.Input[Sequence[pulumi.Input['CertificateContactsContactArgs']]]] = None):
        """
        The set of arguments for constructing a CertificateContacts resource.
        :param pulumi.Input[str] key_vault_id: The ID of the Key Vault. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['CertificateContactsContactArgs']]] contacts: One or more `contact` blocks as defined below.
               -->
        """
        pulumi.set(__self__, "key_vault_id", key_vault_id)
        if contacts is not None:
            pulumi.set(__self__, "contacts", contacts)

    @property
    @pulumi.getter(name="keyVaultId")
    def key_vault_id(self) -> pulumi.Input[str]:
        """
        The ID of the Key Vault. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "key_vault_id")

    @key_vault_id.setter
    def key_vault_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_vault_id", value)

    @property
    @pulumi.getter
    def contacts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CertificateContactsContactArgs']]]]:
        """
        One or more `contact` blocks as defined below.
        -->
        """
        return pulumi.get(self, "contacts")

    @contacts.setter
    def contacts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CertificateContactsContactArgs']]]]):
        pulumi.set(self, "contacts", value)


@pulumi.input_type
class _CertificateContactsState:
    def __init__(__self__, *,
                 contacts: Optional[pulumi.Input[Sequence[pulumi.Input['CertificateContactsContactArgs']]]] = None,
                 key_vault_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering CertificateContacts resources.
        :param pulumi.Input[Sequence[pulumi.Input['CertificateContactsContactArgs']]] contacts: One or more `contact` blocks as defined below.
               -->
        :param pulumi.Input[str] key_vault_id: The ID of the Key Vault. Changing this forces a new resource to be created.
        """
        if contacts is not None:
            pulumi.set(__self__, "contacts", contacts)
        if key_vault_id is not None:
            pulumi.set(__self__, "key_vault_id", key_vault_id)

    @property
    @pulumi.getter
    def contacts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CertificateContactsContactArgs']]]]:
        """
        One or more `contact` blocks as defined below.
        -->
        """
        return pulumi.get(self, "contacts")

    @contacts.setter
    def contacts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CertificateContactsContactArgs']]]]):
        pulumi.set(self, "contacts", value)

    @property
    @pulumi.getter(name="keyVaultId")
    def key_vault_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Key Vault. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "key_vault_id")

    @key_vault_id.setter
    def key_vault_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_id", value)


class CertificateContacts(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 contacts: Optional[pulumi.Input[Sequence[pulumi.Input[Union['CertificateContactsContactArgs', 'CertificateContactsContactArgsDict']]]]] = None,
                 key_vault_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages Key Vault Certificate Contacts.

        ## Disclaimers

        <!-- TODO: Remove Note in 4.0 -->
        > **Note:** It's possible to define Key Vault Certificate Contacts both within the `keyvault.KeyVault` resource via the `contact` block and by using the `keyvault.CertificateContacts` resource. However it's not possible to use both methods to manage Certificate Contacts within a KeyVault, since there'll be conflicts.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_key_vault = azure.keyvault.KeyVault("example",
            name="examplekeyvault",
            location=example.location,
            resource_group_name=example.name,
            tenant_id=current.tenant_id,
            sku_name="premium")
        example_access_policy = azure.keyvault.AccessPolicy("example",
            key_vault_id=example_key_vault.id,
            tenant_id=current.tenant_id,
            object_id=current.object_id,
            certificate_permissions=["ManageContacts"],
            key_permissions=["Create"],
            secret_permissions=["Set"])
        example_certificate_contacts = azure.keyvault.CertificateContacts("example",
            key_vault_id=example_key_vault.id,
            contacts=[
                {
                    "email": "example@example.com",
                    "name": "example",
                    "phone": "01234567890",
                },
                {
                    "email": "example2@example.com",
                },
            ],
            opts = pulumi.ResourceOptions(depends_on=[example_access_policy]))
        ```

        ## Import

        Key Vault Certificate Contacts can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:keyvault/certificateContacts:CertificateContacts example https://example-keyvault.vault.azure.net/certificates/contacts
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['CertificateContactsContactArgs', 'CertificateContactsContactArgsDict']]]] contacts: One or more `contact` blocks as defined below.
               -->
        :param pulumi.Input[str] key_vault_id: The ID of the Key Vault. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CertificateContactsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages Key Vault Certificate Contacts.

        ## Disclaimers

        <!-- TODO: Remove Note in 4.0 -->
        > **Note:** It's possible to define Key Vault Certificate Contacts both within the `keyvault.KeyVault` resource via the `contact` block and by using the `keyvault.CertificateContacts` resource. However it's not possible to use both methods to manage Certificate Contacts within a KeyVault, since there'll be conflicts.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_key_vault = azure.keyvault.KeyVault("example",
            name="examplekeyvault",
            location=example.location,
            resource_group_name=example.name,
            tenant_id=current.tenant_id,
            sku_name="premium")
        example_access_policy = azure.keyvault.AccessPolicy("example",
            key_vault_id=example_key_vault.id,
            tenant_id=current.tenant_id,
            object_id=current.object_id,
            certificate_permissions=["ManageContacts"],
            key_permissions=["Create"],
            secret_permissions=["Set"])
        example_certificate_contacts = azure.keyvault.CertificateContacts("example",
            key_vault_id=example_key_vault.id,
            contacts=[
                {
                    "email": "example@example.com",
                    "name": "example",
                    "phone": "01234567890",
                },
                {
                    "email": "example2@example.com",
                },
            ],
            opts = pulumi.ResourceOptions(depends_on=[example_access_policy]))
        ```

        ## Import

        Key Vault Certificate Contacts can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:keyvault/certificateContacts:CertificateContacts example https://example-keyvault.vault.azure.net/certificates/contacts
        ```

        :param str resource_name: The name of the resource.
        :param CertificateContactsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CertificateContactsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 contacts: Optional[pulumi.Input[Sequence[pulumi.Input[Union['CertificateContactsContactArgs', 'CertificateContactsContactArgsDict']]]]] = None,
                 key_vault_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CertificateContactsArgs.__new__(CertificateContactsArgs)

            __props__.__dict__["contacts"] = contacts
            if key_vault_id is None and not opts.urn:
                raise TypeError("Missing required property 'key_vault_id'")
            __props__.__dict__["key_vault_id"] = key_vault_id
        super(CertificateContacts, __self__).__init__(
            'azure:keyvault/certificateContacts:CertificateContacts',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            contacts: Optional[pulumi.Input[Sequence[pulumi.Input[Union['CertificateContactsContactArgs', 'CertificateContactsContactArgsDict']]]]] = None,
            key_vault_id: Optional[pulumi.Input[str]] = None) -> 'CertificateContacts':
        """
        Get an existing CertificateContacts resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['CertificateContactsContactArgs', 'CertificateContactsContactArgsDict']]]] contacts: One or more `contact` blocks as defined below.
               -->
        :param pulumi.Input[str] key_vault_id: The ID of the Key Vault. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CertificateContactsState.__new__(_CertificateContactsState)

        __props__.__dict__["contacts"] = contacts
        __props__.__dict__["key_vault_id"] = key_vault_id
        return CertificateContacts(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def contacts(self) -> pulumi.Output[Optional[Sequence['outputs.CertificateContactsContact']]]:
        """
        One or more `contact` blocks as defined below.
        -->
        """
        return pulumi.get(self, "contacts")

    @property
    @pulumi.getter(name="keyVaultId")
    def key_vault_id(self) -> pulumi.Output[str]:
        """
        The ID of the Key Vault. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "key_vault_id")

