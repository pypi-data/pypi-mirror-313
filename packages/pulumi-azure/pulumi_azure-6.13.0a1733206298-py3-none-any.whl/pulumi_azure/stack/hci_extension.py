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

__all__ = ['HciExtensionArgs', 'HciExtension']

@pulumi.input_type
class HciExtensionArgs:
    def __init__(__self__, *,
                 arc_setting_id: pulumi.Input[str],
                 publisher: pulumi.Input[str],
                 type: pulumi.Input[str],
                 auto_upgrade_minor_version_enabled: Optional[pulumi.Input[bool]] = None,
                 automatic_upgrade_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 protected_settings: Optional[pulumi.Input[str]] = None,
                 settings: Optional[pulumi.Input[str]] = None,
                 type_handler_version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a HciExtension resource.
        :param pulumi.Input[str] arc_setting_id: The ID of the Azure Stack HCI Cluster Arc Setting. Changing this forces a new resource to be created.
        :param pulumi.Input[str] publisher: The name of the extension handler publisher, such as `Microsoft.Azure.Monitor`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] type: Specifies the type of the extension. For example `CustomScriptExtension` or `AzureMonitorLinuxAgent`. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] auto_upgrade_minor_version_enabled: Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true. Changing this forces a new resource to be created. Possible values are `true` and `false`. Defaults to `true`.
        :param pulumi.Input[bool] automatic_upgrade_enabled: Indicates whether the extension should be automatically upgraded by the platform if there is a newer version available. Possible values are `true` and `false`. Defaults to `true`.
        :param pulumi.Input[str] name: The name which should be used for this Azure Stack HCI Extension. Changing this forces a new resource to be created.
        :param pulumi.Input[str] protected_settings: The json formatted protected settings for the extension.
        :param pulumi.Input[str] settings: The json formatted public settings for the extension.
        :param pulumi.Input[str] type_handler_version: Specifies the version of the script handler.
               
               > **NOTE:** `type_handler_version` cannot be set when `automatic_upgrade_enabled` is set to `true`.
        """
        pulumi.set(__self__, "arc_setting_id", arc_setting_id)
        pulumi.set(__self__, "publisher", publisher)
        pulumi.set(__self__, "type", type)
        if auto_upgrade_minor_version_enabled is not None:
            pulumi.set(__self__, "auto_upgrade_minor_version_enabled", auto_upgrade_minor_version_enabled)
        if automatic_upgrade_enabled is not None:
            pulumi.set(__self__, "automatic_upgrade_enabled", automatic_upgrade_enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if protected_settings is not None:
            pulumi.set(__self__, "protected_settings", protected_settings)
        if settings is not None:
            pulumi.set(__self__, "settings", settings)
        if type_handler_version is not None:
            pulumi.set(__self__, "type_handler_version", type_handler_version)

    @property
    @pulumi.getter(name="arcSettingId")
    def arc_setting_id(self) -> pulumi.Input[str]:
        """
        The ID of the Azure Stack HCI Cluster Arc Setting. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "arc_setting_id")

    @arc_setting_id.setter
    def arc_setting_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "arc_setting_id", value)

    @property
    @pulumi.getter
    def publisher(self) -> pulumi.Input[str]:
        """
        The name of the extension handler publisher, such as `Microsoft.Azure.Monitor`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "publisher")

    @publisher.setter
    def publisher(self, value: pulumi.Input[str]):
        pulumi.set(self, "publisher", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Specifies the type of the extension. For example `CustomScriptExtension` or `AzureMonitorLinuxAgent`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="autoUpgradeMinorVersionEnabled")
    def auto_upgrade_minor_version_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true. Changing this forces a new resource to be created. Possible values are `true` and `false`. Defaults to `true`.
        """
        return pulumi.get(self, "auto_upgrade_minor_version_enabled")

    @auto_upgrade_minor_version_enabled.setter
    def auto_upgrade_minor_version_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_upgrade_minor_version_enabled", value)

    @property
    @pulumi.getter(name="automaticUpgradeEnabled")
    def automatic_upgrade_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether the extension should be automatically upgraded by the platform if there is a newer version available. Possible values are `true` and `false`. Defaults to `true`.
        """
        return pulumi.get(self, "automatic_upgrade_enabled")

    @automatic_upgrade_enabled.setter
    def automatic_upgrade_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "automatic_upgrade_enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Azure Stack HCI Extension. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="protectedSettings")
    def protected_settings(self) -> Optional[pulumi.Input[str]]:
        """
        The json formatted protected settings for the extension.
        """
        return pulumi.get(self, "protected_settings")

    @protected_settings.setter
    def protected_settings(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protected_settings", value)

    @property
    @pulumi.getter
    def settings(self) -> Optional[pulumi.Input[str]]:
        """
        The json formatted public settings for the extension.
        """
        return pulumi.get(self, "settings")

    @settings.setter
    def settings(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "settings", value)

    @property
    @pulumi.getter(name="typeHandlerVersion")
    def type_handler_version(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the version of the script handler.

        > **NOTE:** `type_handler_version` cannot be set when `automatic_upgrade_enabled` is set to `true`.
        """
        return pulumi.get(self, "type_handler_version")

    @type_handler_version.setter
    def type_handler_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type_handler_version", value)


@pulumi.input_type
class _HciExtensionState:
    def __init__(__self__, *,
                 arc_setting_id: Optional[pulumi.Input[str]] = None,
                 auto_upgrade_minor_version_enabled: Optional[pulumi.Input[bool]] = None,
                 automatic_upgrade_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 protected_settings: Optional[pulumi.Input[str]] = None,
                 publisher: Optional[pulumi.Input[str]] = None,
                 settings: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 type_handler_version: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering HciExtension resources.
        :param pulumi.Input[str] arc_setting_id: The ID of the Azure Stack HCI Cluster Arc Setting. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] auto_upgrade_minor_version_enabled: Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true. Changing this forces a new resource to be created. Possible values are `true` and `false`. Defaults to `true`.
        :param pulumi.Input[bool] automatic_upgrade_enabled: Indicates whether the extension should be automatically upgraded by the platform if there is a newer version available. Possible values are `true` and `false`. Defaults to `true`.
        :param pulumi.Input[str] name: The name which should be used for this Azure Stack HCI Extension. Changing this forces a new resource to be created.
        :param pulumi.Input[str] protected_settings: The json formatted protected settings for the extension.
        :param pulumi.Input[str] publisher: The name of the extension handler publisher, such as `Microsoft.Azure.Monitor`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] settings: The json formatted public settings for the extension.
        :param pulumi.Input[str] type: Specifies the type of the extension. For example `CustomScriptExtension` or `AzureMonitorLinuxAgent`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] type_handler_version: Specifies the version of the script handler.
               
               > **NOTE:** `type_handler_version` cannot be set when `automatic_upgrade_enabled` is set to `true`.
        """
        if arc_setting_id is not None:
            pulumi.set(__self__, "arc_setting_id", arc_setting_id)
        if auto_upgrade_minor_version_enabled is not None:
            pulumi.set(__self__, "auto_upgrade_minor_version_enabled", auto_upgrade_minor_version_enabled)
        if automatic_upgrade_enabled is not None:
            pulumi.set(__self__, "automatic_upgrade_enabled", automatic_upgrade_enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if protected_settings is not None:
            pulumi.set(__self__, "protected_settings", protected_settings)
        if publisher is not None:
            pulumi.set(__self__, "publisher", publisher)
        if settings is not None:
            pulumi.set(__self__, "settings", settings)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if type_handler_version is not None:
            pulumi.set(__self__, "type_handler_version", type_handler_version)

    @property
    @pulumi.getter(name="arcSettingId")
    def arc_setting_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Azure Stack HCI Cluster Arc Setting. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "arc_setting_id")

    @arc_setting_id.setter
    def arc_setting_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arc_setting_id", value)

    @property
    @pulumi.getter(name="autoUpgradeMinorVersionEnabled")
    def auto_upgrade_minor_version_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true. Changing this forces a new resource to be created. Possible values are `true` and `false`. Defaults to `true`.
        """
        return pulumi.get(self, "auto_upgrade_minor_version_enabled")

    @auto_upgrade_minor_version_enabled.setter
    def auto_upgrade_minor_version_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_upgrade_minor_version_enabled", value)

    @property
    @pulumi.getter(name="automaticUpgradeEnabled")
    def automatic_upgrade_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether the extension should be automatically upgraded by the platform if there is a newer version available. Possible values are `true` and `false`. Defaults to `true`.
        """
        return pulumi.get(self, "automatic_upgrade_enabled")

    @automatic_upgrade_enabled.setter
    def automatic_upgrade_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "automatic_upgrade_enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Azure Stack HCI Extension. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="protectedSettings")
    def protected_settings(self) -> Optional[pulumi.Input[str]]:
        """
        The json formatted protected settings for the extension.
        """
        return pulumi.get(self, "protected_settings")

    @protected_settings.setter
    def protected_settings(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protected_settings", value)

    @property
    @pulumi.getter
    def publisher(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the extension handler publisher, such as `Microsoft.Azure.Monitor`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "publisher")

    @publisher.setter
    def publisher(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "publisher", value)

    @property
    @pulumi.getter
    def settings(self) -> Optional[pulumi.Input[str]]:
        """
        The json formatted public settings for the extension.
        """
        return pulumi.get(self, "settings")

    @settings.setter
    def settings(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "settings", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of the extension. For example `CustomScriptExtension` or `AzureMonitorLinuxAgent`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="typeHandlerVersion")
    def type_handler_version(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the version of the script handler.

        > **NOTE:** `type_handler_version` cannot be set when `automatic_upgrade_enabled` is set to `true`.
        """
        return pulumi.get(self, "type_handler_version")

    @type_handler_version.setter
    def type_handler_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type_handler_version", value)


class HciExtension(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 arc_setting_id: Optional[pulumi.Input[str]] = None,
                 auto_upgrade_minor_version_enabled: Optional[pulumi.Input[bool]] = None,
                 automatic_upgrade_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 protected_settings: Optional[pulumi.Input[str]] = None,
                 publisher: Optional[pulumi.Input[str]] = None,
                 settings: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 type_handler_version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an Azure Stack HCI Extension.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-hci-ext",
            location="West Europe")
        example_hci_extension = azure.stack.HciExtension("example",
            name="AzureMonitorWindowsAgent",
            arc_setting_id="/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example-hci/providers/Microsoft.AzureStackHCI/clusters/hci-cl/arcSettings/default",
            publisher="Microsoft.Azure.Monitor",
            type="MicrosoftMonitoringAgent",
            auto_upgrade_minor_version_enabled=True,
            automatic_upgrade_enabled=True,
            type_handler_version="1.22.0")
        ```

        ## Import

        Azure Stack HCI Extension can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:stack/hciExtension:HciExtension example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.AzureStackHCI/clusters/cluster1/arcSettings/default/extensions/extension1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arc_setting_id: The ID of the Azure Stack HCI Cluster Arc Setting. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] auto_upgrade_minor_version_enabled: Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true. Changing this forces a new resource to be created. Possible values are `true` and `false`. Defaults to `true`.
        :param pulumi.Input[bool] automatic_upgrade_enabled: Indicates whether the extension should be automatically upgraded by the platform if there is a newer version available. Possible values are `true` and `false`. Defaults to `true`.
        :param pulumi.Input[str] name: The name which should be used for this Azure Stack HCI Extension. Changing this forces a new resource to be created.
        :param pulumi.Input[str] protected_settings: The json formatted protected settings for the extension.
        :param pulumi.Input[str] publisher: The name of the extension handler publisher, such as `Microsoft.Azure.Monitor`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] settings: The json formatted public settings for the extension.
        :param pulumi.Input[str] type: Specifies the type of the extension. For example `CustomScriptExtension` or `AzureMonitorLinuxAgent`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] type_handler_version: Specifies the version of the script handler.
               
               > **NOTE:** `type_handler_version` cannot be set when `automatic_upgrade_enabled` is set to `true`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: HciExtensionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an Azure Stack HCI Extension.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-hci-ext",
            location="West Europe")
        example_hci_extension = azure.stack.HciExtension("example",
            name="AzureMonitorWindowsAgent",
            arc_setting_id="/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example-hci/providers/Microsoft.AzureStackHCI/clusters/hci-cl/arcSettings/default",
            publisher="Microsoft.Azure.Monitor",
            type="MicrosoftMonitoringAgent",
            auto_upgrade_minor_version_enabled=True,
            automatic_upgrade_enabled=True,
            type_handler_version="1.22.0")
        ```

        ## Import

        Azure Stack HCI Extension can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:stack/hciExtension:HciExtension example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.AzureStackHCI/clusters/cluster1/arcSettings/default/extensions/extension1
        ```

        :param str resource_name: The name of the resource.
        :param HciExtensionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(HciExtensionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 arc_setting_id: Optional[pulumi.Input[str]] = None,
                 auto_upgrade_minor_version_enabled: Optional[pulumi.Input[bool]] = None,
                 automatic_upgrade_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 protected_settings: Optional[pulumi.Input[str]] = None,
                 publisher: Optional[pulumi.Input[str]] = None,
                 settings: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 type_handler_version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = HciExtensionArgs.__new__(HciExtensionArgs)

            if arc_setting_id is None and not opts.urn:
                raise TypeError("Missing required property 'arc_setting_id'")
            __props__.__dict__["arc_setting_id"] = arc_setting_id
            __props__.__dict__["auto_upgrade_minor_version_enabled"] = auto_upgrade_minor_version_enabled
            __props__.__dict__["automatic_upgrade_enabled"] = automatic_upgrade_enabled
            __props__.__dict__["name"] = name
            __props__.__dict__["protected_settings"] = None if protected_settings is None else pulumi.Output.secret(protected_settings)
            if publisher is None and not opts.urn:
                raise TypeError("Missing required property 'publisher'")
            __props__.__dict__["publisher"] = publisher
            __props__.__dict__["settings"] = settings
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["type_handler_version"] = type_handler_version
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["protectedSettings"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(HciExtension, __self__).__init__(
            'azure:stack/hciExtension:HciExtension',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arc_setting_id: Optional[pulumi.Input[str]] = None,
            auto_upgrade_minor_version_enabled: Optional[pulumi.Input[bool]] = None,
            automatic_upgrade_enabled: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            protected_settings: Optional[pulumi.Input[str]] = None,
            publisher: Optional[pulumi.Input[str]] = None,
            settings: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            type_handler_version: Optional[pulumi.Input[str]] = None) -> 'HciExtension':
        """
        Get an existing HciExtension resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arc_setting_id: The ID of the Azure Stack HCI Cluster Arc Setting. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] auto_upgrade_minor_version_enabled: Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true. Changing this forces a new resource to be created. Possible values are `true` and `false`. Defaults to `true`.
        :param pulumi.Input[bool] automatic_upgrade_enabled: Indicates whether the extension should be automatically upgraded by the platform if there is a newer version available. Possible values are `true` and `false`. Defaults to `true`.
        :param pulumi.Input[str] name: The name which should be used for this Azure Stack HCI Extension. Changing this forces a new resource to be created.
        :param pulumi.Input[str] protected_settings: The json formatted protected settings for the extension.
        :param pulumi.Input[str] publisher: The name of the extension handler publisher, such as `Microsoft.Azure.Monitor`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] settings: The json formatted public settings for the extension.
        :param pulumi.Input[str] type: Specifies the type of the extension. For example `CustomScriptExtension` or `AzureMonitorLinuxAgent`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] type_handler_version: Specifies the version of the script handler.
               
               > **NOTE:** `type_handler_version` cannot be set when `automatic_upgrade_enabled` is set to `true`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _HciExtensionState.__new__(_HciExtensionState)

        __props__.__dict__["arc_setting_id"] = arc_setting_id
        __props__.__dict__["auto_upgrade_minor_version_enabled"] = auto_upgrade_minor_version_enabled
        __props__.__dict__["automatic_upgrade_enabled"] = automatic_upgrade_enabled
        __props__.__dict__["name"] = name
        __props__.__dict__["protected_settings"] = protected_settings
        __props__.__dict__["publisher"] = publisher
        __props__.__dict__["settings"] = settings
        __props__.__dict__["type"] = type
        __props__.__dict__["type_handler_version"] = type_handler_version
        return HciExtension(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="arcSettingId")
    def arc_setting_id(self) -> pulumi.Output[str]:
        """
        The ID of the Azure Stack HCI Cluster Arc Setting. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "arc_setting_id")

    @property
    @pulumi.getter(name="autoUpgradeMinorVersionEnabled")
    def auto_upgrade_minor_version_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true. Changing this forces a new resource to be created. Possible values are `true` and `false`. Defaults to `true`.
        """
        return pulumi.get(self, "auto_upgrade_minor_version_enabled")

    @property
    @pulumi.getter(name="automaticUpgradeEnabled")
    def automatic_upgrade_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether the extension should be automatically upgraded by the platform if there is a newer version available. Possible values are `true` and `false`. Defaults to `true`.
        """
        return pulumi.get(self, "automatic_upgrade_enabled")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Azure Stack HCI Extension. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="protectedSettings")
    def protected_settings(self) -> pulumi.Output[Optional[str]]:
        """
        The json formatted protected settings for the extension.
        """
        return pulumi.get(self, "protected_settings")

    @property
    @pulumi.getter
    def publisher(self) -> pulumi.Output[str]:
        """
        The name of the extension handler publisher, such as `Microsoft.Azure.Monitor`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "publisher")

    @property
    @pulumi.getter
    def settings(self) -> pulumi.Output[Optional[str]]:
        """
        The json formatted public settings for the extension.
        """
        return pulumi.get(self, "settings")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Specifies the type of the extension. For example `CustomScriptExtension` or `AzureMonitorLinuxAgent`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="typeHandlerVersion")
    def type_handler_version(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the version of the script handler.

        > **NOTE:** `type_handler_version` cannot be set when `automatic_upgrade_enabled` is set to `true`.
        """
        return pulumi.get(self, "type_handler_version")

