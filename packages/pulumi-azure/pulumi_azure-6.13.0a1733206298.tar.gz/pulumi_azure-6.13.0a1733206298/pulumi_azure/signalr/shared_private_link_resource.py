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

__all__ = ['SharedPrivateLinkResourceArgs', 'SharedPrivateLinkResource']

@pulumi.input_type
class SharedPrivateLinkResourceArgs:
    def __init__(__self__, *,
                 signalr_service_id: pulumi.Input[str],
                 sub_resource_name: pulumi.Input[str],
                 target_resource_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 request_message: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SharedPrivateLinkResource resource.
        :param pulumi.Input[str] signalr_service_id: The id of the Signalr Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sub_resource_name: The sub resource name which the Signalr Private Endpoint can connect to. Possible values are `sites`, `vault`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_resource_id: The ID of the Shared Private Link Enabled Remote Resource which this Signalr Private Endpoint should be connected to. Changing this forces a new resource to be created.
               
               > **NOTE:** The `sub_resource_name` should match with the type of the `target_resource_id` that's being specified.
        :param pulumi.Input[str] name: The name of the Signalr Shared Private Link Resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] request_message: The request message for requesting approval of the Shared Private Link Enabled Remote Resource.
        """
        pulumi.set(__self__, "signalr_service_id", signalr_service_id)
        pulumi.set(__self__, "sub_resource_name", sub_resource_name)
        pulumi.set(__self__, "target_resource_id", target_resource_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if request_message is not None:
            pulumi.set(__self__, "request_message", request_message)

    @property
    @pulumi.getter(name="signalrServiceId")
    def signalr_service_id(self) -> pulumi.Input[str]:
        """
        The id of the Signalr Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "signalr_service_id")

    @signalr_service_id.setter
    def signalr_service_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "signalr_service_id", value)

    @property
    @pulumi.getter(name="subResourceName")
    def sub_resource_name(self) -> pulumi.Input[str]:
        """
        The sub resource name which the Signalr Private Endpoint can connect to. Possible values are `sites`, `vault`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "sub_resource_name")

    @sub_resource_name.setter
    def sub_resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "sub_resource_name", value)

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> pulumi.Input[str]:
        """
        The ID of the Shared Private Link Enabled Remote Resource which this Signalr Private Endpoint should be connected to. Changing this forces a new resource to be created.

        > **NOTE:** The `sub_resource_name` should match with the type of the `target_resource_id` that's being specified.
        """
        return pulumi.get(self, "target_resource_id")

    @target_resource_id.setter
    def target_resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_resource_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Signalr Shared Private Link Resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="requestMessage")
    def request_message(self) -> Optional[pulumi.Input[str]]:
        """
        The request message for requesting approval of the Shared Private Link Enabled Remote Resource.
        """
        return pulumi.get(self, "request_message")

    @request_message.setter
    def request_message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "request_message", value)


@pulumi.input_type
class _SharedPrivateLinkResourceState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 request_message: Optional[pulumi.Input[str]] = None,
                 signalr_service_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 sub_resource_name: Optional[pulumi.Input[str]] = None,
                 target_resource_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SharedPrivateLinkResource resources.
        :param pulumi.Input[str] name: The name of the Signalr Shared Private Link Resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] request_message: The request message for requesting approval of the Shared Private Link Enabled Remote Resource.
        :param pulumi.Input[str] signalr_service_id: The id of the Signalr Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] status: The status of a private endpoint connection. Possible values are `Pending`, `Approved`, `Rejected` or `Disconnected`.
        :param pulumi.Input[str] sub_resource_name: The sub resource name which the Signalr Private Endpoint can connect to. Possible values are `sites`, `vault`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_resource_id: The ID of the Shared Private Link Enabled Remote Resource which this Signalr Private Endpoint should be connected to. Changing this forces a new resource to be created.
               
               > **NOTE:** The `sub_resource_name` should match with the type of the `target_resource_id` that's being specified.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if request_message is not None:
            pulumi.set(__self__, "request_message", request_message)
        if signalr_service_id is not None:
            pulumi.set(__self__, "signalr_service_id", signalr_service_id)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if sub_resource_name is not None:
            pulumi.set(__self__, "sub_resource_name", sub_resource_name)
        if target_resource_id is not None:
            pulumi.set(__self__, "target_resource_id", target_resource_id)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Signalr Shared Private Link Resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="requestMessage")
    def request_message(self) -> Optional[pulumi.Input[str]]:
        """
        The request message for requesting approval of the Shared Private Link Enabled Remote Resource.
        """
        return pulumi.get(self, "request_message")

    @request_message.setter
    def request_message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "request_message", value)

    @property
    @pulumi.getter(name="signalrServiceId")
    def signalr_service_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the Signalr Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "signalr_service_id")

    @signalr_service_id.setter
    def signalr_service_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "signalr_service_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of a private endpoint connection. Possible values are `Pending`, `Approved`, `Rejected` or `Disconnected`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="subResourceName")
    def sub_resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        The sub resource name which the Signalr Private Endpoint can connect to. Possible values are `sites`, `vault`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "sub_resource_name")

    @sub_resource_name.setter
    def sub_resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sub_resource_name", value)

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Shared Private Link Enabled Remote Resource which this Signalr Private Endpoint should be connected to. Changing this forces a new resource to be created.

        > **NOTE:** The `sub_resource_name` should match with the type of the `target_resource_id` that's being specified.
        """
        return pulumi.get(self, "target_resource_id")

    @target_resource_id.setter
    def target_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_resource_id", value)


class SharedPrivateLinkResource(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 request_message: Optional[pulumi.Input[str]] = None,
                 signalr_service_id: Optional[pulumi.Input[str]] = None,
                 sub_resource_name: Optional[pulumi.Input[str]] = None,
                 target_resource_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages the Shared Private Link Resource for a Signalr service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example = azure.core.ResourceGroup("example",
            name="terraform-signalr",
            location="east us")
        example_key_vault = azure.keyvault.KeyVault("example",
            name="examplekeyvault",
            location=example.location,
            resource_group_name=example.name,
            tenant_id=current.tenant_id,
            sku_name="standard",
            soft_delete_retention_days=7,
            access_policies=[{
                "tenant_id": current.tenant_id,
                "object_id": current.object_id,
                "certificate_permissions": ["ManageContacts"],
                "key_permissions": ["Create"],
                "secret_permissions": ["Set"],
            }])
        test = azure.signalr.Service("test",
            name="tfex-signalr",
            location=test_azurerm_resource_group["location"],
            resource_group_name=test_azurerm_resource_group["name"],
            sku={
                "name": "Standard_S1",
                "capacity": 1,
            })
        example_shared_private_link_resource = azure.signalr.SharedPrivateLinkResource("example",
            name="tfex-signalr-splr",
            signalr_service_id=example_azurerm_signalr_service["id"],
            sub_resource_name="vault",
            target_resource_id=example_key_vault.id)
        ```

        ## Import

        Signalr Shared Private Link Resource can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:signalr/sharedPrivateLinkResource:SharedPrivateLinkResource example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.SignalRService/signalR/signalr1/sharedPrivateLinkResources/resource1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the Signalr Shared Private Link Resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] request_message: The request message for requesting approval of the Shared Private Link Enabled Remote Resource.
        :param pulumi.Input[str] signalr_service_id: The id of the Signalr Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sub_resource_name: The sub resource name which the Signalr Private Endpoint can connect to. Possible values are `sites`, `vault`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_resource_id: The ID of the Shared Private Link Enabled Remote Resource which this Signalr Private Endpoint should be connected to. Changing this forces a new resource to be created.
               
               > **NOTE:** The `sub_resource_name` should match with the type of the `target_resource_id` that's being specified.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SharedPrivateLinkResourceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages the Shared Private Link Resource for a Signalr service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example = azure.core.ResourceGroup("example",
            name="terraform-signalr",
            location="east us")
        example_key_vault = azure.keyvault.KeyVault("example",
            name="examplekeyvault",
            location=example.location,
            resource_group_name=example.name,
            tenant_id=current.tenant_id,
            sku_name="standard",
            soft_delete_retention_days=7,
            access_policies=[{
                "tenant_id": current.tenant_id,
                "object_id": current.object_id,
                "certificate_permissions": ["ManageContacts"],
                "key_permissions": ["Create"],
                "secret_permissions": ["Set"],
            }])
        test = azure.signalr.Service("test",
            name="tfex-signalr",
            location=test_azurerm_resource_group["location"],
            resource_group_name=test_azurerm_resource_group["name"],
            sku={
                "name": "Standard_S1",
                "capacity": 1,
            })
        example_shared_private_link_resource = azure.signalr.SharedPrivateLinkResource("example",
            name="tfex-signalr-splr",
            signalr_service_id=example_azurerm_signalr_service["id"],
            sub_resource_name="vault",
            target_resource_id=example_key_vault.id)
        ```

        ## Import

        Signalr Shared Private Link Resource can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:signalr/sharedPrivateLinkResource:SharedPrivateLinkResource example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.SignalRService/signalR/signalr1/sharedPrivateLinkResources/resource1
        ```

        :param str resource_name: The name of the resource.
        :param SharedPrivateLinkResourceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SharedPrivateLinkResourceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 request_message: Optional[pulumi.Input[str]] = None,
                 signalr_service_id: Optional[pulumi.Input[str]] = None,
                 sub_resource_name: Optional[pulumi.Input[str]] = None,
                 target_resource_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SharedPrivateLinkResourceArgs.__new__(SharedPrivateLinkResourceArgs)

            __props__.__dict__["name"] = name
            __props__.__dict__["request_message"] = request_message
            if signalr_service_id is None and not opts.urn:
                raise TypeError("Missing required property 'signalr_service_id'")
            __props__.__dict__["signalr_service_id"] = signalr_service_id
            if sub_resource_name is None and not opts.urn:
                raise TypeError("Missing required property 'sub_resource_name'")
            __props__.__dict__["sub_resource_name"] = sub_resource_name
            if target_resource_id is None and not opts.urn:
                raise TypeError("Missing required property 'target_resource_id'")
            __props__.__dict__["target_resource_id"] = target_resource_id
            __props__.__dict__["status"] = None
        super(SharedPrivateLinkResource, __self__).__init__(
            'azure:signalr/sharedPrivateLinkResource:SharedPrivateLinkResource',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            request_message: Optional[pulumi.Input[str]] = None,
            signalr_service_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            sub_resource_name: Optional[pulumi.Input[str]] = None,
            target_resource_id: Optional[pulumi.Input[str]] = None) -> 'SharedPrivateLinkResource':
        """
        Get an existing SharedPrivateLinkResource resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the Signalr Shared Private Link Resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] request_message: The request message for requesting approval of the Shared Private Link Enabled Remote Resource.
        :param pulumi.Input[str] signalr_service_id: The id of the Signalr Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] status: The status of a private endpoint connection. Possible values are `Pending`, `Approved`, `Rejected` or `Disconnected`.
        :param pulumi.Input[str] sub_resource_name: The sub resource name which the Signalr Private Endpoint can connect to. Possible values are `sites`, `vault`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_resource_id: The ID of the Shared Private Link Enabled Remote Resource which this Signalr Private Endpoint should be connected to. Changing this forces a new resource to be created.
               
               > **NOTE:** The `sub_resource_name` should match with the type of the `target_resource_id` that's being specified.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SharedPrivateLinkResourceState.__new__(_SharedPrivateLinkResourceState)

        __props__.__dict__["name"] = name
        __props__.__dict__["request_message"] = request_message
        __props__.__dict__["signalr_service_id"] = signalr_service_id
        __props__.__dict__["status"] = status
        __props__.__dict__["sub_resource_name"] = sub_resource_name
        __props__.__dict__["target_resource_id"] = target_resource_id
        return SharedPrivateLinkResource(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Signalr Shared Private Link Resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="requestMessage")
    def request_message(self) -> pulumi.Output[Optional[str]]:
        """
        The request message for requesting approval of the Shared Private Link Enabled Remote Resource.
        """
        return pulumi.get(self, "request_message")

    @property
    @pulumi.getter(name="signalrServiceId")
    def signalr_service_id(self) -> pulumi.Output[str]:
        """
        The id of the Signalr Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "signalr_service_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of a private endpoint connection. Possible values are `Pending`, `Approved`, `Rejected` or `Disconnected`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="subResourceName")
    def sub_resource_name(self) -> pulumi.Output[str]:
        """
        The sub resource name which the Signalr Private Endpoint can connect to. Possible values are `sites`, `vault`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "sub_resource_name")

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> pulumi.Output[str]:
        """
        The ID of the Shared Private Link Enabled Remote Resource which this Signalr Private Endpoint should be connected to. Changing this forces a new resource to be created.

        > **NOTE:** The `sub_resource_name` should match with the type of the `target_resource_id` that's being specified.
        """
        return pulumi.get(self, "target_resource_id")

