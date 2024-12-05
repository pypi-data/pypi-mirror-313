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

__all__ = ['ManagedHardwareSecurityModuleKeyArgs', 'ManagedHardwareSecurityModuleKey']

@pulumi.input_type
class ManagedHardwareSecurityModuleKeyArgs:
    def __init__(__self__, *,
                 key_opts: pulumi.Input[Sequence[pulumi.Input[str]]],
                 key_type: pulumi.Input[str],
                 managed_hsm_id: pulumi.Input[str],
                 curve: Optional[pulumi.Input[str]] = None,
                 expiration_date: Optional[pulumi.Input[str]] = None,
                 key_size: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_before_date: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ManagedHardwareSecurityModuleKey resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] key_opts: A list of JSON web key operations. Possible values include: `decrypt`, `encrypt`, `sign`, `unwrapKey`, `verify` and `wrapKey`. Please note these values are case-sensitive.
        :param pulumi.Input[str] key_type: Specifies the Key Type to use for this Key Vault Managed Hardware Security Module Key. Possible values are `EC-HSM` and `RSA-HSM`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] managed_hsm_id: Specifies the ID of the Key Vault Managed Hardware Security Module that they key will be owned by. Changing this forces a new resource to be created.
        :param pulumi.Input[str] curve: Specifies the curve to use when creating an `EC-HSM` key. Possible values are `P-256`, `P-256K`, `P-384`, and `P-521`. This field is required if `key_type` is `EC-HSM`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] expiration_date: Expiration UTC datetime (Y-m-d'T'H:M:S'Z'). When this parameter gets changed on reruns, if newer date is ahead of current date, an update is performed. If the newer date is before the current date, resource will be force created.
        :param pulumi.Input[int] key_size: Specifies the Size of the RSA key to create in bytes. For example, 1024 or 2048. *Note*: This field is required if `key_type` is `RSA-HSM`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Key Vault Managed Hardware Security Module Key. Changing this forces a new resource to be created.
        :param pulumi.Input[str] not_before_date: Key not usable before the provided UTC datetime (Y-m-d'T'H:M:S'Z').
               
               > **Note:** Once `expiration_date` is set, it's not possible to unset the key even if it is deleted & recreated as underlying Azure API uses the restore of the purged key.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, "key_opts", key_opts)
        pulumi.set(__self__, "key_type", key_type)
        pulumi.set(__self__, "managed_hsm_id", managed_hsm_id)
        if curve is not None:
            pulumi.set(__self__, "curve", curve)
        if expiration_date is not None:
            pulumi.set(__self__, "expiration_date", expiration_date)
        if key_size is not None:
            pulumi.set(__self__, "key_size", key_size)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if not_before_date is not None:
            pulumi.set(__self__, "not_before_date", not_before_date)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="keyOpts")
    def key_opts(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of JSON web key operations. Possible values include: `decrypt`, `encrypt`, `sign`, `unwrapKey`, `verify` and `wrapKey`. Please note these values are case-sensitive.
        """
        return pulumi.get(self, "key_opts")

    @key_opts.setter
    def key_opts(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "key_opts", value)

    @property
    @pulumi.getter(name="keyType")
    def key_type(self) -> pulumi.Input[str]:
        """
        Specifies the Key Type to use for this Key Vault Managed Hardware Security Module Key. Possible values are `EC-HSM` and `RSA-HSM`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "key_type")

    @key_type.setter
    def key_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_type", value)

    @property
    @pulumi.getter(name="managedHsmId")
    def managed_hsm_id(self) -> pulumi.Input[str]:
        """
        Specifies the ID of the Key Vault Managed Hardware Security Module that they key will be owned by. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "managed_hsm_id")

    @managed_hsm_id.setter
    def managed_hsm_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "managed_hsm_id", value)

    @property
    @pulumi.getter
    def curve(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the curve to use when creating an `EC-HSM` key. Possible values are `P-256`, `P-256K`, `P-384`, and `P-521`. This field is required if `key_type` is `EC-HSM`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "curve")

    @curve.setter
    def curve(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "curve", value)

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> Optional[pulumi.Input[str]]:
        """
        Expiration UTC datetime (Y-m-d'T'H:M:S'Z'). When this parameter gets changed on reruns, if newer date is ahead of current date, an update is performed. If the newer date is before the current date, resource will be force created.
        """
        return pulumi.get(self, "expiration_date")

    @expiration_date.setter
    def expiration_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expiration_date", value)

    @property
    @pulumi.getter(name="keySize")
    def key_size(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the Size of the RSA key to create in bytes. For example, 1024 or 2048. *Note*: This field is required if `key_type` is `RSA-HSM`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "key_size")

    @key_size.setter
    def key_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "key_size", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Key Vault Managed Hardware Security Module Key. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="notBeforeDate")
    def not_before_date(self) -> Optional[pulumi.Input[str]]:
        """
        Key not usable before the provided UTC datetime (Y-m-d'T'H:M:S'Z').

        > **Note:** Once `expiration_date` is set, it's not possible to unset the key even if it is deleted & recreated as underlying Azure API uses the restore of the purged key.
        """
        return pulumi.get(self, "not_before_date")

    @not_before_date.setter
    def not_before_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "not_before_date", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ManagedHardwareSecurityModuleKeyState:
    def __init__(__self__, *,
                 curve: Optional[pulumi.Input[str]] = None,
                 expiration_date: Optional[pulumi.Input[str]] = None,
                 key_opts: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 key_size: Optional[pulumi.Input[int]] = None,
                 key_type: Optional[pulumi.Input[str]] = None,
                 managed_hsm_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_before_date: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 versioned_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ManagedHardwareSecurityModuleKey resources.
        :param pulumi.Input[str] curve: Specifies the curve to use when creating an `EC-HSM` key. Possible values are `P-256`, `P-256K`, `P-384`, and `P-521`. This field is required if `key_type` is `EC-HSM`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] expiration_date: Expiration UTC datetime (Y-m-d'T'H:M:S'Z'). When this parameter gets changed on reruns, if newer date is ahead of current date, an update is performed. If the newer date is before the current date, resource will be force created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] key_opts: A list of JSON web key operations. Possible values include: `decrypt`, `encrypt`, `sign`, `unwrapKey`, `verify` and `wrapKey`. Please note these values are case-sensitive.
        :param pulumi.Input[int] key_size: Specifies the Size of the RSA key to create in bytes. For example, 1024 or 2048. *Note*: This field is required if `key_type` is `RSA-HSM`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] key_type: Specifies the Key Type to use for this Key Vault Managed Hardware Security Module Key. Possible values are `EC-HSM` and `RSA-HSM`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] managed_hsm_id: Specifies the ID of the Key Vault Managed Hardware Security Module that they key will be owned by. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Key Vault Managed Hardware Security Module Key. Changing this forces a new resource to be created.
        :param pulumi.Input[str] not_before_date: Key not usable before the provided UTC datetime (Y-m-d'T'H:M:S'Z').
               
               > **Note:** Once `expiration_date` is set, it's not possible to unset the key even if it is deleted & recreated as underlying Azure API uses the restore of the purged key.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] versioned_id: The versioned Key Vault Secret Managed Hardware Security Module Key ID.
        """
        if curve is not None:
            pulumi.set(__self__, "curve", curve)
        if expiration_date is not None:
            pulumi.set(__self__, "expiration_date", expiration_date)
        if key_opts is not None:
            pulumi.set(__self__, "key_opts", key_opts)
        if key_size is not None:
            pulumi.set(__self__, "key_size", key_size)
        if key_type is not None:
            pulumi.set(__self__, "key_type", key_type)
        if managed_hsm_id is not None:
            pulumi.set(__self__, "managed_hsm_id", managed_hsm_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if not_before_date is not None:
            pulumi.set(__self__, "not_before_date", not_before_date)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if versioned_id is not None:
            pulumi.set(__self__, "versioned_id", versioned_id)

    @property
    @pulumi.getter
    def curve(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the curve to use when creating an `EC-HSM` key. Possible values are `P-256`, `P-256K`, `P-384`, and `P-521`. This field is required if `key_type` is `EC-HSM`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "curve")

    @curve.setter
    def curve(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "curve", value)

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> Optional[pulumi.Input[str]]:
        """
        Expiration UTC datetime (Y-m-d'T'H:M:S'Z'). When this parameter gets changed on reruns, if newer date is ahead of current date, an update is performed. If the newer date is before the current date, resource will be force created.
        """
        return pulumi.get(self, "expiration_date")

    @expiration_date.setter
    def expiration_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expiration_date", value)

    @property
    @pulumi.getter(name="keyOpts")
    def key_opts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of JSON web key operations. Possible values include: `decrypt`, `encrypt`, `sign`, `unwrapKey`, `verify` and `wrapKey`. Please note these values are case-sensitive.
        """
        return pulumi.get(self, "key_opts")

    @key_opts.setter
    def key_opts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "key_opts", value)

    @property
    @pulumi.getter(name="keySize")
    def key_size(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the Size of the RSA key to create in bytes. For example, 1024 or 2048. *Note*: This field is required if `key_type` is `RSA-HSM`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "key_size")

    @key_size.setter
    def key_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "key_size", value)

    @property
    @pulumi.getter(name="keyType")
    def key_type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Key Type to use for this Key Vault Managed Hardware Security Module Key. Possible values are `EC-HSM` and `RSA-HSM`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "key_type")

    @key_type.setter
    def key_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_type", value)

    @property
    @pulumi.getter(name="managedHsmId")
    def managed_hsm_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of the Key Vault Managed Hardware Security Module that they key will be owned by. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "managed_hsm_id")

    @managed_hsm_id.setter
    def managed_hsm_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "managed_hsm_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Key Vault Managed Hardware Security Module Key. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="notBeforeDate")
    def not_before_date(self) -> Optional[pulumi.Input[str]]:
        """
        Key not usable before the provided UTC datetime (Y-m-d'T'H:M:S'Z').

        > **Note:** Once `expiration_date` is set, it's not possible to unset the key even if it is deleted & recreated as underlying Azure API uses the restore of the purged key.
        """
        return pulumi.get(self, "not_before_date")

    @not_before_date.setter
    def not_before_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "not_before_date", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="versionedId")
    def versioned_id(self) -> Optional[pulumi.Input[str]]:
        """
        The versioned Key Vault Secret Managed Hardware Security Module Key ID.
        """
        return pulumi.get(self, "versioned_id")

    @versioned_id.setter
    def versioned_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "versioned_id", value)


class ManagedHardwareSecurityModuleKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 curve: Optional[pulumi.Input[str]] = None,
                 expiration_date: Optional[pulumi.Input[str]] = None,
                 key_opts: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 key_size: Optional[pulumi.Input[int]] = None,
                 key_type: Optional[pulumi.Input[str]] = None,
                 managed_hsm_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_before_date: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a Key Vault Managed Hardware Security Module Key.

        > **Note:** The Azure Provider includes a Feature Toggle which will purge a Key Vault Managed Hardware Security Module Key resource on destroy, rather than the default soft-delete. See `purge_soft_deleted_hardware_security_modules_on_destroy` for more information.

        ## Import

        Key Vault Managed Hardware Security Module Key can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:keyvault/managedHardwareSecurityModuleKey:ManagedHardwareSecurityModuleKey example https://exampleHSM.managedhsm.azure.net/keys/exampleKey
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] curve: Specifies the curve to use when creating an `EC-HSM` key. Possible values are `P-256`, `P-256K`, `P-384`, and `P-521`. This field is required if `key_type` is `EC-HSM`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] expiration_date: Expiration UTC datetime (Y-m-d'T'H:M:S'Z'). When this parameter gets changed on reruns, if newer date is ahead of current date, an update is performed. If the newer date is before the current date, resource will be force created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] key_opts: A list of JSON web key operations. Possible values include: `decrypt`, `encrypt`, `sign`, `unwrapKey`, `verify` and `wrapKey`. Please note these values are case-sensitive.
        :param pulumi.Input[int] key_size: Specifies the Size of the RSA key to create in bytes. For example, 1024 or 2048. *Note*: This field is required if `key_type` is `RSA-HSM`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] key_type: Specifies the Key Type to use for this Key Vault Managed Hardware Security Module Key. Possible values are `EC-HSM` and `RSA-HSM`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] managed_hsm_id: Specifies the ID of the Key Vault Managed Hardware Security Module that they key will be owned by. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Key Vault Managed Hardware Security Module Key. Changing this forces a new resource to be created.
        :param pulumi.Input[str] not_before_date: Key not usable before the provided UTC datetime (Y-m-d'T'H:M:S'Z').
               
               > **Note:** Once `expiration_date` is set, it's not possible to unset the key even if it is deleted & recreated as underlying Azure API uses the restore of the purged key.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagedHardwareSecurityModuleKeyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Key Vault Managed Hardware Security Module Key.

        > **Note:** The Azure Provider includes a Feature Toggle which will purge a Key Vault Managed Hardware Security Module Key resource on destroy, rather than the default soft-delete. See `purge_soft_deleted_hardware_security_modules_on_destroy` for more information.

        ## Import

        Key Vault Managed Hardware Security Module Key can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:keyvault/managedHardwareSecurityModuleKey:ManagedHardwareSecurityModuleKey example https://exampleHSM.managedhsm.azure.net/keys/exampleKey
        ```

        :param str resource_name: The name of the resource.
        :param ManagedHardwareSecurityModuleKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedHardwareSecurityModuleKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 curve: Optional[pulumi.Input[str]] = None,
                 expiration_date: Optional[pulumi.Input[str]] = None,
                 key_opts: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 key_size: Optional[pulumi.Input[int]] = None,
                 key_type: Optional[pulumi.Input[str]] = None,
                 managed_hsm_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_before_date: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagedHardwareSecurityModuleKeyArgs.__new__(ManagedHardwareSecurityModuleKeyArgs)

            __props__.__dict__["curve"] = curve
            __props__.__dict__["expiration_date"] = expiration_date
            if key_opts is None and not opts.urn:
                raise TypeError("Missing required property 'key_opts'")
            __props__.__dict__["key_opts"] = key_opts
            __props__.__dict__["key_size"] = key_size
            if key_type is None and not opts.urn:
                raise TypeError("Missing required property 'key_type'")
            __props__.__dict__["key_type"] = key_type
            if managed_hsm_id is None and not opts.urn:
                raise TypeError("Missing required property 'managed_hsm_id'")
            __props__.__dict__["managed_hsm_id"] = managed_hsm_id
            __props__.__dict__["name"] = name
            __props__.__dict__["not_before_date"] = not_before_date
            __props__.__dict__["tags"] = tags
            __props__.__dict__["versioned_id"] = None
        super(ManagedHardwareSecurityModuleKey, __self__).__init__(
            'azure:keyvault/managedHardwareSecurityModuleKey:ManagedHardwareSecurityModuleKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            curve: Optional[pulumi.Input[str]] = None,
            expiration_date: Optional[pulumi.Input[str]] = None,
            key_opts: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            key_size: Optional[pulumi.Input[int]] = None,
            key_type: Optional[pulumi.Input[str]] = None,
            managed_hsm_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            not_before_date: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            versioned_id: Optional[pulumi.Input[str]] = None) -> 'ManagedHardwareSecurityModuleKey':
        """
        Get an existing ManagedHardwareSecurityModuleKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] curve: Specifies the curve to use when creating an `EC-HSM` key. Possible values are `P-256`, `P-256K`, `P-384`, and `P-521`. This field is required if `key_type` is `EC-HSM`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] expiration_date: Expiration UTC datetime (Y-m-d'T'H:M:S'Z'). When this parameter gets changed on reruns, if newer date is ahead of current date, an update is performed. If the newer date is before the current date, resource will be force created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] key_opts: A list of JSON web key operations. Possible values include: `decrypt`, `encrypt`, `sign`, `unwrapKey`, `verify` and `wrapKey`. Please note these values are case-sensitive.
        :param pulumi.Input[int] key_size: Specifies the Size of the RSA key to create in bytes. For example, 1024 or 2048. *Note*: This field is required if `key_type` is `RSA-HSM`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] key_type: Specifies the Key Type to use for this Key Vault Managed Hardware Security Module Key. Possible values are `EC-HSM` and `RSA-HSM`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] managed_hsm_id: Specifies the ID of the Key Vault Managed Hardware Security Module that they key will be owned by. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Key Vault Managed Hardware Security Module Key. Changing this forces a new resource to be created.
        :param pulumi.Input[str] not_before_date: Key not usable before the provided UTC datetime (Y-m-d'T'H:M:S'Z').
               
               > **Note:** Once `expiration_date` is set, it's not possible to unset the key even if it is deleted & recreated as underlying Azure API uses the restore of the purged key.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] versioned_id: The versioned Key Vault Secret Managed Hardware Security Module Key ID.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ManagedHardwareSecurityModuleKeyState.__new__(_ManagedHardwareSecurityModuleKeyState)

        __props__.__dict__["curve"] = curve
        __props__.__dict__["expiration_date"] = expiration_date
        __props__.__dict__["key_opts"] = key_opts
        __props__.__dict__["key_size"] = key_size
        __props__.__dict__["key_type"] = key_type
        __props__.__dict__["managed_hsm_id"] = managed_hsm_id
        __props__.__dict__["name"] = name
        __props__.__dict__["not_before_date"] = not_before_date
        __props__.__dict__["tags"] = tags
        __props__.__dict__["versioned_id"] = versioned_id
        return ManagedHardwareSecurityModuleKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def curve(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the curve to use when creating an `EC-HSM` key. Possible values are `P-256`, `P-256K`, `P-384`, and `P-521`. This field is required if `key_type` is `EC-HSM`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "curve")

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> pulumi.Output[Optional[str]]:
        """
        Expiration UTC datetime (Y-m-d'T'H:M:S'Z'). When this parameter gets changed on reruns, if newer date is ahead of current date, an update is performed. If the newer date is before the current date, resource will be force created.
        """
        return pulumi.get(self, "expiration_date")

    @property
    @pulumi.getter(name="keyOpts")
    def key_opts(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of JSON web key operations. Possible values include: `decrypt`, `encrypt`, `sign`, `unwrapKey`, `verify` and `wrapKey`. Please note these values are case-sensitive.
        """
        return pulumi.get(self, "key_opts")

    @property
    @pulumi.getter(name="keySize")
    def key_size(self) -> pulumi.Output[Optional[int]]:
        """
        Specifies the Size of the RSA key to create in bytes. For example, 1024 or 2048. *Note*: This field is required if `key_type` is `RSA-HSM`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "key_size")

    @property
    @pulumi.getter(name="keyType")
    def key_type(self) -> pulumi.Output[str]:
        """
        Specifies the Key Type to use for this Key Vault Managed Hardware Security Module Key. Possible values are `EC-HSM` and `RSA-HSM`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "key_type")

    @property
    @pulumi.getter(name="managedHsmId")
    def managed_hsm_id(self) -> pulumi.Output[str]:
        """
        Specifies the ID of the Key Vault Managed Hardware Security Module that they key will be owned by. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "managed_hsm_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Key Vault Managed Hardware Security Module Key. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="notBeforeDate")
    def not_before_date(self) -> pulumi.Output[Optional[str]]:
        """
        Key not usable before the provided UTC datetime (Y-m-d'T'H:M:S'Z').

        > **Note:** Once `expiration_date` is set, it's not possible to unset the key even if it is deleted & recreated as underlying Azure API uses the restore of the purged key.
        """
        return pulumi.get(self, "not_before_date")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="versionedId")
    def versioned_id(self) -> pulumi.Output[str]:
        """
        The versioned Key Vault Secret Managed Hardware Security Module Key ID.
        """
        return pulumi.get(self, "versioned_id")

