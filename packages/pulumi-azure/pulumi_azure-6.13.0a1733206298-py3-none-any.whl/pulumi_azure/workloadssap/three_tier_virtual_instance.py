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

__all__ = ['ThreeTierVirtualInstanceArgs', 'ThreeTierVirtualInstance']

@pulumi.input_type
class ThreeTierVirtualInstanceArgs:
    def __init__(__self__, *,
                 app_location: pulumi.Input[str],
                 environment: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 sap_fqdn: pulumi.Input[str],
                 sap_product: pulumi.Input[str],
                 three_tier_configuration: pulumi.Input['ThreeTierVirtualInstanceThreeTierConfigurationArgs'],
                 identity: Optional[pulumi.Input['ThreeTierVirtualInstanceIdentityArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 managed_resource_group_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ThreeTierVirtualInstance resource.
        :param pulumi.Input[str] app_location: The Geo-Location where the SAP system is to be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] environment: The environment type for the SAP Three Tier Virtual Instance. Possible values are `NonProd` and `Prod`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sap_fqdn: The FQDN of the SAP system. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sap_product: The SAP Product type for the SAP Three Tier Virtual Instance. Possible values are `ECC`, `Other` and `S4HANA`. Changing this forces a new resource to be created.
        :param pulumi.Input['ThreeTierVirtualInstanceThreeTierConfigurationArgs'] three_tier_configuration: A `three_tier_configuration` block as defined below. Changing this forces a new resource to be created.
        :param pulumi.Input['ThreeTierVirtualInstanceIdentityArgs'] identity: An `identity` block as defined below.
        :param pulumi.Input[str] location: The Azure Region where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] managed_resource_group_name: The name of the managed Resource Group for the SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of this SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the SAP Three Tier Virtual Instance.
        """
        pulumi.set(__self__, "app_location", app_location)
        pulumi.set(__self__, "environment", environment)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "sap_fqdn", sap_fqdn)
        pulumi.set(__self__, "sap_product", sap_product)
        pulumi.set(__self__, "three_tier_configuration", three_tier_configuration)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if managed_resource_group_name is not None:
            pulumi.set(__self__, "managed_resource_group_name", managed_resource_group_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="appLocation")
    def app_location(self) -> pulumi.Input[str]:
        """
        The Geo-Location where the SAP system is to be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "app_location")

    @app_location.setter
    def app_location(self, value: pulumi.Input[str]):
        pulumi.set(self, "app_location", value)

    @property
    @pulumi.getter
    def environment(self) -> pulumi.Input[str]:
        """
        The environment type for the SAP Three Tier Virtual Instance. Possible values are `NonProd` and `Prod`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "environment")

    @environment.setter
    def environment(self, value: pulumi.Input[str]):
        pulumi.set(self, "environment", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="sapFqdn")
    def sap_fqdn(self) -> pulumi.Input[str]:
        """
        The FQDN of the SAP system. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "sap_fqdn")

    @sap_fqdn.setter
    def sap_fqdn(self, value: pulumi.Input[str]):
        pulumi.set(self, "sap_fqdn", value)

    @property
    @pulumi.getter(name="sapProduct")
    def sap_product(self) -> pulumi.Input[str]:
        """
        The SAP Product type for the SAP Three Tier Virtual Instance. Possible values are `ECC`, `Other` and `S4HANA`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "sap_product")

    @sap_product.setter
    def sap_product(self, value: pulumi.Input[str]):
        pulumi.set(self, "sap_product", value)

    @property
    @pulumi.getter(name="threeTierConfiguration")
    def three_tier_configuration(self) -> pulumi.Input['ThreeTierVirtualInstanceThreeTierConfigurationArgs']:
        """
        A `three_tier_configuration` block as defined below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "three_tier_configuration")

    @three_tier_configuration.setter
    def three_tier_configuration(self, value: pulumi.Input['ThreeTierVirtualInstanceThreeTierConfigurationArgs']):
        pulumi.set(self, "three_tier_configuration", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ThreeTierVirtualInstanceIdentityArgs']]:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ThreeTierVirtualInstanceIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="managedResourceGroupName")
    def managed_resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the managed Resource Group for the SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "managed_resource_group_name")

    @managed_resource_group_name.setter
    def managed_resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "managed_resource_group_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of this SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the SAP Three Tier Virtual Instance.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ThreeTierVirtualInstanceState:
    def __init__(__self__, *,
                 app_location: Optional[pulumi.Input[str]] = None,
                 environment: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input['ThreeTierVirtualInstanceIdentityArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 managed_resource_group_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sap_fqdn: Optional[pulumi.Input[str]] = None,
                 sap_product: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 three_tier_configuration: Optional[pulumi.Input['ThreeTierVirtualInstanceThreeTierConfigurationArgs']] = None):
        """
        Input properties used for looking up and filtering ThreeTierVirtualInstance resources.
        :param pulumi.Input[str] app_location: The Geo-Location where the SAP system is to be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] environment: The environment type for the SAP Three Tier Virtual Instance. Possible values are `NonProd` and `Prod`. Changing this forces a new resource to be created.
        :param pulumi.Input['ThreeTierVirtualInstanceIdentityArgs'] identity: An `identity` block as defined below.
        :param pulumi.Input[str] location: The Azure Region where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] managed_resource_group_name: The name of the managed Resource Group for the SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of this SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sap_fqdn: The FQDN of the SAP system. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sap_product: The SAP Product type for the SAP Three Tier Virtual Instance. Possible values are `ECC`, `Other` and `S4HANA`. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the SAP Three Tier Virtual Instance.
        :param pulumi.Input['ThreeTierVirtualInstanceThreeTierConfigurationArgs'] three_tier_configuration: A `three_tier_configuration` block as defined below. Changing this forces a new resource to be created.
        """
        if app_location is not None:
            pulumi.set(__self__, "app_location", app_location)
        if environment is not None:
            pulumi.set(__self__, "environment", environment)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if managed_resource_group_name is not None:
            pulumi.set(__self__, "managed_resource_group_name", managed_resource_group_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if sap_fqdn is not None:
            pulumi.set(__self__, "sap_fqdn", sap_fqdn)
        if sap_product is not None:
            pulumi.set(__self__, "sap_product", sap_product)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if three_tier_configuration is not None:
            pulumi.set(__self__, "three_tier_configuration", three_tier_configuration)

    @property
    @pulumi.getter(name="appLocation")
    def app_location(self) -> Optional[pulumi.Input[str]]:
        """
        The Geo-Location where the SAP system is to be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "app_location")

    @app_location.setter
    def app_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "app_location", value)

    @property
    @pulumi.getter
    def environment(self) -> Optional[pulumi.Input[str]]:
        """
        The environment type for the SAP Three Tier Virtual Instance. Possible values are `NonProd` and `Prod`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "environment")

    @environment.setter
    def environment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "environment", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ThreeTierVirtualInstanceIdentityArgs']]:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ThreeTierVirtualInstanceIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="managedResourceGroupName")
    def managed_resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the managed Resource Group for the SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "managed_resource_group_name")

    @managed_resource_group_name.setter
    def managed_resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "managed_resource_group_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of this SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="sapFqdn")
    def sap_fqdn(self) -> Optional[pulumi.Input[str]]:
        """
        The FQDN of the SAP system. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "sap_fqdn")

    @sap_fqdn.setter
    def sap_fqdn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sap_fqdn", value)

    @property
    @pulumi.getter(name="sapProduct")
    def sap_product(self) -> Optional[pulumi.Input[str]]:
        """
        The SAP Product type for the SAP Three Tier Virtual Instance. Possible values are `ECC`, `Other` and `S4HANA`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "sap_product")

    @sap_product.setter
    def sap_product(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sap_product", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the SAP Three Tier Virtual Instance.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="threeTierConfiguration")
    def three_tier_configuration(self) -> Optional[pulumi.Input['ThreeTierVirtualInstanceThreeTierConfigurationArgs']]:
        """
        A `three_tier_configuration` block as defined below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "three_tier_configuration")

    @three_tier_configuration.setter
    def three_tier_configuration(self, value: Optional[pulumi.Input['ThreeTierVirtualInstanceThreeTierConfigurationArgs']]):
        pulumi.set(self, "three_tier_configuration", value)


class ThreeTierVirtualInstance(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_location: Optional[pulumi.Input[str]] = None,
                 environment: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[Union['ThreeTierVirtualInstanceIdentityArgs', 'ThreeTierVirtualInstanceIdentityArgsDict']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 managed_resource_group_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sap_fqdn: Optional[pulumi.Input[str]] = None,
                 sap_product: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 three_tier_configuration: Optional[pulumi.Input[Union['ThreeTierVirtualInstanceThreeTierConfigurationArgs', 'ThreeTierVirtualInstanceThreeTierConfigurationArgsDict']]] = None,
                 __props__=None):
        """
        Manages an SAP Three Tier Virtual Instance with a new SAP System.

        > **Note:** Before using this resource, it's required to submit the request of registering the Resource Provider with Azure CLI `az provider register --namespace "Microsoft.Workloads"`. The Resource Provider can take a while to register, you can check the status by running `az provider show --namespace "Microsoft.Workloads" --query "registrationState"`. Once this outputs "Registered" the Resource Provider is available for use.

        ## Import

        SAP Three Tier Virtual Instances with new SAP Systems can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:workloadssap/threeTierVirtualInstance:ThreeTierVirtualInstance example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Workloads/sapVirtualInstances/vis1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_location: The Geo-Location where the SAP system is to be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] environment: The environment type for the SAP Three Tier Virtual Instance. Possible values are `NonProd` and `Prod`. Changing this forces a new resource to be created.
        :param pulumi.Input[Union['ThreeTierVirtualInstanceIdentityArgs', 'ThreeTierVirtualInstanceIdentityArgsDict']] identity: An `identity` block as defined below.
        :param pulumi.Input[str] location: The Azure Region where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] managed_resource_group_name: The name of the managed Resource Group for the SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of this SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sap_fqdn: The FQDN of the SAP system. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sap_product: The SAP Product type for the SAP Three Tier Virtual Instance. Possible values are `ECC`, `Other` and `S4HANA`. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the SAP Three Tier Virtual Instance.
        :param pulumi.Input[Union['ThreeTierVirtualInstanceThreeTierConfigurationArgs', 'ThreeTierVirtualInstanceThreeTierConfigurationArgsDict']] three_tier_configuration: A `three_tier_configuration` block as defined below. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ThreeTierVirtualInstanceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an SAP Three Tier Virtual Instance with a new SAP System.

        > **Note:** Before using this resource, it's required to submit the request of registering the Resource Provider with Azure CLI `az provider register --namespace "Microsoft.Workloads"`. The Resource Provider can take a while to register, you can check the status by running `az provider show --namespace "Microsoft.Workloads" --query "registrationState"`. Once this outputs "Registered" the Resource Provider is available for use.

        ## Import

        SAP Three Tier Virtual Instances with new SAP Systems can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:workloadssap/threeTierVirtualInstance:ThreeTierVirtualInstance example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Workloads/sapVirtualInstances/vis1
        ```

        :param str resource_name: The name of the resource.
        :param ThreeTierVirtualInstanceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ThreeTierVirtualInstanceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_location: Optional[pulumi.Input[str]] = None,
                 environment: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[Union['ThreeTierVirtualInstanceIdentityArgs', 'ThreeTierVirtualInstanceIdentityArgsDict']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 managed_resource_group_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sap_fqdn: Optional[pulumi.Input[str]] = None,
                 sap_product: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 three_tier_configuration: Optional[pulumi.Input[Union['ThreeTierVirtualInstanceThreeTierConfigurationArgs', 'ThreeTierVirtualInstanceThreeTierConfigurationArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ThreeTierVirtualInstanceArgs.__new__(ThreeTierVirtualInstanceArgs)

            if app_location is None and not opts.urn:
                raise TypeError("Missing required property 'app_location'")
            __props__.__dict__["app_location"] = app_location
            if environment is None and not opts.urn:
                raise TypeError("Missing required property 'environment'")
            __props__.__dict__["environment"] = environment
            __props__.__dict__["identity"] = identity
            __props__.__dict__["location"] = location
            __props__.__dict__["managed_resource_group_name"] = managed_resource_group_name
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if sap_fqdn is None and not opts.urn:
                raise TypeError("Missing required property 'sap_fqdn'")
            __props__.__dict__["sap_fqdn"] = sap_fqdn
            if sap_product is None and not opts.urn:
                raise TypeError("Missing required property 'sap_product'")
            __props__.__dict__["sap_product"] = sap_product
            __props__.__dict__["tags"] = tags
            if three_tier_configuration is None and not opts.urn:
                raise TypeError("Missing required property 'three_tier_configuration'")
            __props__.__dict__["three_tier_configuration"] = three_tier_configuration
        super(ThreeTierVirtualInstance, __self__).__init__(
            'azure:workloadssap/threeTierVirtualInstance:ThreeTierVirtualInstance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            app_location: Optional[pulumi.Input[str]] = None,
            environment: Optional[pulumi.Input[str]] = None,
            identity: Optional[pulumi.Input[Union['ThreeTierVirtualInstanceIdentityArgs', 'ThreeTierVirtualInstanceIdentityArgsDict']]] = None,
            location: Optional[pulumi.Input[str]] = None,
            managed_resource_group_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            sap_fqdn: Optional[pulumi.Input[str]] = None,
            sap_product: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            three_tier_configuration: Optional[pulumi.Input[Union['ThreeTierVirtualInstanceThreeTierConfigurationArgs', 'ThreeTierVirtualInstanceThreeTierConfigurationArgsDict']]] = None) -> 'ThreeTierVirtualInstance':
        """
        Get an existing ThreeTierVirtualInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_location: The Geo-Location where the SAP system is to be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] environment: The environment type for the SAP Three Tier Virtual Instance. Possible values are `NonProd` and `Prod`. Changing this forces a new resource to be created.
        :param pulumi.Input[Union['ThreeTierVirtualInstanceIdentityArgs', 'ThreeTierVirtualInstanceIdentityArgsDict']] identity: An `identity` block as defined below.
        :param pulumi.Input[str] location: The Azure Region where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] managed_resource_group_name: The name of the managed Resource Group for the SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of this SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sap_fqdn: The FQDN of the SAP system. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sap_product: The SAP Product type for the SAP Three Tier Virtual Instance. Possible values are `ECC`, `Other` and `S4HANA`. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the SAP Three Tier Virtual Instance.
        :param pulumi.Input[Union['ThreeTierVirtualInstanceThreeTierConfigurationArgs', 'ThreeTierVirtualInstanceThreeTierConfigurationArgsDict']] three_tier_configuration: A `three_tier_configuration` block as defined below. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ThreeTierVirtualInstanceState.__new__(_ThreeTierVirtualInstanceState)

        __props__.__dict__["app_location"] = app_location
        __props__.__dict__["environment"] = environment
        __props__.__dict__["identity"] = identity
        __props__.__dict__["location"] = location
        __props__.__dict__["managed_resource_group_name"] = managed_resource_group_name
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["sap_fqdn"] = sap_fqdn
        __props__.__dict__["sap_product"] = sap_product
        __props__.__dict__["tags"] = tags
        __props__.__dict__["three_tier_configuration"] = three_tier_configuration
        return ThreeTierVirtualInstance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appLocation")
    def app_location(self) -> pulumi.Output[str]:
        """
        The Geo-Location where the SAP system is to be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "app_location")

    @property
    @pulumi.getter
    def environment(self) -> pulumi.Output[str]:
        """
        The environment type for the SAP Three Tier Virtual Instance. Possible values are `NonProd` and `Prod`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "environment")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ThreeTierVirtualInstanceIdentity']]:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure Region where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedResourceGroupName")
    def managed_resource_group_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the managed Resource Group for the SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "managed_resource_group_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of this SAP Three Tier Virtual Instance. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the SAP Three Tier Virtual Instance should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="sapFqdn")
    def sap_fqdn(self) -> pulumi.Output[str]:
        """
        The FQDN of the SAP system. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "sap_fqdn")

    @property
    @pulumi.getter(name="sapProduct")
    def sap_product(self) -> pulumi.Output[str]:
        """
        The SAP Product type for the SAP Three Tier Virtual Instance. Possible values are `ECC`, `Other` and `S4HANA`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "sap_product")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to the SAP Three Tier Virtual Instance.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="threeTierConfiguration")
    def three_tier_configuration(self) -> pulumi.Output['outputs.ThreeTierVirtualInstanceThreeTierConfiguration']:
        """
        A `three_tier_configuration` block as defined below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "three_tier_configuration")

