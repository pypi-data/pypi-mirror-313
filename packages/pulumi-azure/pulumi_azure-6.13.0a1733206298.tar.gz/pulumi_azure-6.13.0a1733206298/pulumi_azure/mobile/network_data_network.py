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

__all__ = ['NetworkDataNetworkArgs', 'NetworkDataNetwork']

@pulumi.input_type
class NetworkDataNetworkArgs:
    def __init__(__self__, *,
                 mobile_network_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a NetworkDataNetwork resource.
        :param pulumi.Input[str] mobile_network_id: Specifies the ID of the Mobile Network. Changing this forces a new Mobile Network Data Network to be created.
        :param pulumi.Input[str] description: A description of this Mobile Network Data Network.
        :param pulumi.Input[str] location: Specifies the Azure Region where the Mobile Network Data Network should exist. Changing this forces a new Mobile Network Data Network to be created.
        :param pulumi.Input[str] name: Specifies the name which should be used for this Mobile Network Data Network. Changing this forces a new Mobile Network Data Network to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Mobile Network Data Network.
        """
        pulumi.set(__self__, "mobile_network_id", mobile_network_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="mobileNetworkId")
    def mobile_network_id(self) -> pulumi.Input[str]:
        """
        Specifies the ID of the Mobile Network. Changing this forces a new Mobile Network Data Network to be created.
        """
        return pulumi.get(self, "mobile_network_id")

    @mobile_network_id.setter
    def mobile_network_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "mobile_network_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of this Mobile Network Data Network.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Azure Region where the Mobile Network Data Network should exist. Changing this forces a new Mobile Network Data Network to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name which should be used for this Mobile Network Data Network. Changing this forces a new Mobile Network Data Network to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Mobile Network Data Network.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _NetworkDataNetworkState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mobile_network_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering NetworkDataNetwork resources.
        :param pulumi.Input[str] description: A description of this Mobile Network Data Network.
        :param pulumi.Input[str] location: Specifies the Azure Region where the Mobile Network Data Network should exist. Changing this forces a new Mobile Network Data Network to be created.
        :param pulumi.Input[str] mobile_network_id: Specifies the ID of the Mobile Network. Changing this forces a new Mobile Network Data Network to be created.
        :param pulumi.Input[str] name: Specifies the name which should be used for this Mobile Network Data Network. Changing this forces a new Mobile Network Data Network to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Mobile Network Data Network.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if mobile_network_id is not None:
            pulumi.set(__self__, "mobile_network_id", mobile_network_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of this Mobile Network Data Network.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Azure Region where the Mobile Network Data Network should exist. Changing this forces a new Mobile Network Data Network to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="mobileNetworkId")
    def mobile_network_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of the Mobile Network. Changing this forces a new Mobile Network Data Network to be created.
        """
        return pulumi.get(self, "mobile_network_id")

    @mobile_network_id.setter
    def mobile_network_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mobile_network_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name which should be used for this Mobile Network Data Network. Changing this forces a new Mobile Network Data Network to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Mobile Network Data Network.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class NetworkDataNetwork(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mobile_network_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a Mobile Network Data Network.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="East Us")
        example_network = azure.mobile.Network("example",
            name="example-mn",
            location=example.location,
            resource_group_name=example.name,
            mobile_country_code="001",
            mobile_network_code="01")
        example_network_data_network = azure.mobile.NetworkDataNetwork("example",
            name="example-mndn",
            mobile_network_id=example_network.id,
            location=example.location,
            description="example description",
            tags={
                "key": "value",
            })
        ```

        ## Import

        Mobile Network Data Network can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:mobile/networkDataNetwork:NetworkDataNetwork example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourceGroup1/providers/Microsoft.MobileNetwork/mobileNetworks/mobileNetwork1/dataNetworks/dataNetwork1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description of this Mobile Network Data Network.
        :param pulumi.Input[str] location: Specifies the Azure Region where the Mobile Network Data Network should exist. Changing this forces a new Mobile Network Data Network to be created.
        :param pulumi.Input[str] mobile_network_id: Specifies the ID of the Mobile Network. Changing this forces a new Mobile Network Data Network to be created.
        :param pulumi.Input[str] name: Specifies the name which should be used for this Mobile Network Data Network. Changing this forces a new Mobile Network Data Network to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Mobile Network Data Network.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkDataNetworkArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Mobile Network Data Network.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="East Us")
        example_network = azure.mobile.Network("example",
            name="example-mn",
            location=example.location,
            resource_group_name=example.name,
            mobile_country_code="001",
            mobile_network_code="01")
        example_network_data_network = azure.mobile.NetworkDataNetwork("example",
            name="example-mndn",
            mobile_network_id=example_network.id,
            location=example.location,
            description="example description",
            tags={
                "key": "value",
            })
        ```

        ## Import

        Mobile Network Data Network can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:mobile/networkDataNetwork:NetworkDataNetwork example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourceGroup1/providers/Microsoft.MobileNetwork/mobileNetworks/mobileNetwork1/dataNetworks/dataNetwork1
        ```

        :param str resource_name: The name of the resource.
        :param NetworkDataNetworkArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkDataNetworkArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mobile_network_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkDataNetworkArgs.__new__(NetworkDataNetworkArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["location"] = location
            if mobile_network_id is None and not opts.urn:
                raise TypeError("Missing required property 'mobile_network_id'")
            __props__.__dict__["mobile_network_id"] = mobile_network_id
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
        super(NetworkDataNetwork, __self__).__init__(
            'azure:mobile/networkDataNetwork:NetworkDataNetwork',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            mobile_network_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'NetworkDataNetwork':
        """
        Get an existing NetworkDataNetwork resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description of this Mobile Network Data Network.
        :param pulumi.Input[str] location: Specifies the Azure Region where the Mobile Network Data Network should exist. Changing this forces a new Mobile Network Data Network to be created.
        :param pulumi.Input[str] mobile_network_id: Specifies the ID of the Mobile Network. Changing this forces a new Mobile Network Data Network to be created.
        :param pulumi.Input[str] name: Specifies the name which should be used for this Mobile Network Data Network. Changing this forces a new Mobile Network Data Network to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Mobile Network Data Network.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkDataNetworkState.__new__(_NetworkDataNetworkState)

        __props__.__dict__["description"] = description
        __props__.__dict__["location"] = location
        __props__.__dict__["mobile_network_id"] = mobile_network_id
        __props__.__dict__["name"] = name
        __props__.__dict__["tags"] = tags
        return NetworkDataNetwork(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of this Mobile Network Data Network.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the Azure Region where the Mobile Network Data Network should exist. Changing this forces a new Mobile Network Data Network to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="mobileNetworkId")
    def mobile_network_id(self) -> pulumi.Output[str]:
        """
        Specifies the ID of the Mobile Network. Changing this forces a new Mobile Network Data Network to be created.
        """
        return pulumi.get(self, "mobile_network_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name which should be used for this Mobile Network Data Network. Changing this forces a new Mobile Network Data Network to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to the Mobile Network Data Network.
        """
        return pulumi.get(self, "tags")

