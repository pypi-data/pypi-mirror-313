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

__all__ = ['ElasticsearchArgs', 'Elasticsearch']

@pulumi.input_type
class ElasticsearchArgs:
    def __init__(__self__, *,
                 elastic_cloud_email_address: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 sku_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 logs: Optional[pulumi.Input['ElasticsearchLogsArgs']] = None,
                 monitoring_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Elasticsearch resource.
        :param pulumi.Input[str] elastic_cloud_email_address: Specifies the Email Address which should be associated with this Elasticsearch account. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] sku_name: Specifies the name of the SKU for this Elasticsearch. Changing this forces a new Elasticsearch to be created.
               
               > **NOTE:** The SKU depends on the Elasticsearch Plans available for your account and is a combination of PlanID_Term.
               Ex: If the plan ID is "planXYZ" and term is "Yearly", the SKU will be "planXYZ_Yearly".
               You may find your eligible plans [here](https://portal.azure.com/#view/Microsoft_Azure_Marketplace/GalleryItemDetailsBladeNopdl/id/elastic.ec-azure-pp) or in the online documentation [here](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/elastic.ec-azure-pp?tab=PlansAndPrice) for more details or in case of any issues with the SKU.
        :param pulumi.Input[str] location: The Azure Region where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input['ElasticsearchLogsArgs'] logs: A `logs` block as defined below.
        :param pulumi.Input[bool] monitoring_enabled: Specifies if the Elasticsearch should have monitoring configured? Defaults to `true`. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] name: The name which should be used for this Elasticsearch resource. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Elasticsearch resource.
        """
        pulumi.set(__self__, "elastic_cloud_email_address", elastic_cloud_email_address)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "sku_name", sku_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if logs is not None:
            pulumi.set(__self__, "logs", logs)
        if monitoring_enabled is not None:
            pulumi.set(__self__, "monitoring_enabled", monitoring_enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="elasticCloudEmailAddress")
    def elastic_cloud_email_address(self) -> pulumi.Input[str]:
        """
        Specifies the Email Address which should be associated with this Elasticsearch account. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "elastic_cloud_email_address")

    @elastic_cloud_email_address.setter
    def elastic_cloud_email_address(self, value: pulumi.Input[str]):
        pulumi.set(self, "elastic_cloud_email_address", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="skuName")
    def sku_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the SKU for this Elasticsearch. Changing this forces a new Elasticsearch to be created.

        > **NOTE:** The SKU depends on the Elasticsearch Plans available for your account and is a combination of PlanID_Term.
        Ex: If the plan ID is "planXYZ" and term is "Yearly", the SKU will be "planXYZ_Yearly".
        You may find your eligible plans [here](https://portal.azure.com/#view/Microsoft_Azure_Marketplace/GalleryItemDetailsBladeNopdl/id/elastic.ec-azure-pp) or in the online documentation [here](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/elastic.ec-azure-pp?tab=PlansAndPrice) for more details or in case of any issues with the SKU.
        """
        return pulumi.get(self, "sku_name")

    @sku_name.setter
    def sku_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "sku_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def logs(self) -> Optional[pulumi.Input['ElasticsearchLogsArgs']]:
        """
        A `logs` block as defined below.
        """
        return pulumi.get(self, "logs")

    @logs.setter
    def logs(self, value: Optional[pulumi.Input['ElasticsearchLogsArgs']]):
        pulumi.set(self, "logs", value)

    @property
    @pulumi.getter(name="monitoringEnabled")
    def monitoring_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if the Elasticsearch should have monitoring configured? Defaults to `true`. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "monitoring_enabled")

    @monitoring_enabled.setter
    def monitoring_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "monitoring_enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Elasticsearch resource. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Elasticsearch resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ElasticsearchState:
    def __init__(__self__, *,
                 elastic_cloud_deployment_id: Optional[pulumi.Input[str]] = None,
                 elastic_cloud_email_address: Optional[pulumi.Input[str]] = None,
                 elastic_cloud_sso_default_url: Optional[pulumi.Input[str]] = None,
                 elastic_cloud_user_id: Optional[pulumi.Input[str]] = None,
                 elasticsearch_service_url: Optional[pulumi.Input[str]] = None,
                 kibana_service_url: Optional[pulumi.Input[str]] = None,
                 kibana_sso_uri: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 logs: Optional[pulumi.Input['ElasticsearchLogsArgs']] = None,
                 monitoring_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Elasticsearch resources.
        :param pulumi.Input[str] elastic_cloud_deployment_id: The ID of the Deployment within Elastic Cloud.
        :param pulumi.Input[str] elastic_cloud_email_address: Specifies the Email Address which should be associated with this Elasticsearch account. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] elastic_cloud_sso_default_url: The Default URL used for Single Sign On (SSO) to Elastic Cloud.
        :param pulumi.Input[str] elastic_cloud_user_id: The ID of the User Account within Elastic Cloud.
        :param pulumi.Input[str] elasticsearch_service_url: The URL to the Elasticsearch Service associated with this Elasticsearch.
        :param pulumi.Input[str] kibana_service_url: The URL to the Kibana Dashboard associated with this Elasticsearch.
        :param pulumi.Input[str] kibana_sso_uri: The URI used for SSO to the Kibana Dashboard associated with this Elasticsearch.
        :param pulumi.Input[str] location: The Azure Region where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input['ElasticsearchLogsArgs'] logs: A `logs` block as defined below.
        :param pulumi.Input[bool] monitoring_enabled: Specifies if the Elasticsearch should have monitoring configured? Defaults to `true`. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] name: The name which should be used for this Elasticsearch resource. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] sku_name: Specifies the name of the SKU for this Elasticsearch. Changing this forces a new Elasticsearch to be created.
               
               > **NOTE:** The SKU depends on the Elasticsearch Plans available for your account and is a combination of PlanID_Term.
               Ex: If the plan ID is "planXYZ" and term is "Yearly", the SKU will be "planXYZ_Yearly".
               You may find your eligible plans [here](https://portal.azure.com/#view/Microsoft_Azure_Marketplace/GalleryItemDetailsBladeNopdl/id/elastic.ec-azure-pp) or in the online documentation [here](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/elastic.ec-azure-pp?tab=PlansAndPrice) for more details or in case of any issues with the SKU.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Elasticsearch resource.
        """
        if elastic_cloud_deployment_id is not None:
            pulumi.set(__self__, "elastic_cloud_deployment_id", elastic_cloud_deployment_id)
        if elastic_cloud_email_address is not None:
            pulumi.set(__self__, "elastic_cloud_email_address", elastic_cloud_email_address)
        if elastic_cloud_sso_default_url is not None:
            pulumi.set(__self__, "elastic_cloud_sso_default_url", elastic_cloud_sso_default_url)
        if elastic_cloud_user_id is not None:
            pulumi.set(__self__, "elastic_cloud_user_id", elastic_cloud_user_id)
        if elasticsearch_service_url is not None:
            pulumi.set(__self__, "elasticsearch_service_url", elasticsearch_service_url)
        if kibana_service_url is not None:
            pulumi.set(__self__, "kibana_service_url", kibana_service_url)
        if kibana_sso_uri is not None:
            pulumi.set(__self__, "kibana_sso_uri", kibana_sso_uri)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if logs is not None:
            pulumi.set(__self__, "logs", logs)
        if monitoring_enabled is not None:
            pulumi.set(__self__, "monitoring_enabled", monitoring_enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if sku_name is not None:
            pulumi.set(__self__, "sku_name", sku_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="elasticCloudDeploymentId")
    def elastic_cloud_deployment_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Deployment within Elastic Cloud.
        """
        return pulumi.get(self, "elastic_cloud_deployment_id")

    @elastic_cloud_deployment_id.setter
    def elastic_cloud_deployment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "elastic_cloud_deployment_id", value)

    @property
    @pulumi.getter(name="elasticCloudEmailAddress")
    def elastic_cloud_email_address(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Email Address which should be associated with this Elasticsearch account. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "elastic_cloud_email_address")

    @elastic_cloud_email_address.setter
    def elastic_cloud_email_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "elastic_cloud_email_address", value)

    @property
    @pulumi.getter(name="elasticCloudSsoDefaultUrl")
    def elastic_cloud_sso_default_url(self) -> Optional[pulumi.Input[str]]:
        """
        The Default URL used for Single Sign On (SSO) to Elastic Cloud.
        """
        return pulumi.get(self, "elastic_cloud_sso_default_url")

    @elastic_cloud_sso_default_url.setter
    def elastic_cloud_sso_default_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "elastic_cloud_sso_default_url", value)

    @property
    @pulumi.getter(name="elasticCloudUserId")
    def elastic_cloud_user_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the User Account within Elastic Cloud.
        """
        return pulumi.get(self, "elastic_cloud_user_id")

    @elastic_cloud_user_id.setter
    def elastic_cloud_user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "elastic_cloud_user_id", value)

    @property
    @pulumi.getter(name="elasticsearchServiceUrl")
    def elasticsearch_service_url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL to the Elasticsearch Service associated with this Elasticsearch.
        """
        return pulumi.get(self, "elasticsearch_service_url")

    @elasticsearch_service_url.setter
    def elasticsearch_service_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "elasticsearch_service_url", value)

    @property
    @pulumi.getter(name="kibanaServiceUrl")
    def kibana_service_url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL to the Kibana Dashboard associated with this Elasticsearch.
        """
        return pulumi.get(self, "kibana_service_url")

    @kibana_service_url.setter
    def kibana_service_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kibana_service_url", value)

    @property
    @pulumi.getter(name="kibanaSsoUri")
    def kibana_sso_uri(self) -> Optional[pulumi.Input[str]]:
        """
        The URI used for SSO to the Kibana Dashboard associated with this Elasticsearch.
        """
        return pulumi.get(self, "kibana_sso_uri")

    @kibana_sso_uri.setter
    def kibana_sso_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kibana_sso_uri", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def logs(self) -> Optional[pulumi.Input['ElasticsearchLogsArgs']]:
        """
        A `logs` block as defined below.
        """
        return pulumi.get(self, "logs")

    @logs.setter
    def logs(self, value: Optional[pulumi.Input['ElasticsearchLogsArgs']]):
        pulumi.set(self, "logs", value)

    @property
    @pulumi.getter(name="monitoringEnabled")
    def monitoring_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if the Elasticsearch should have monitoring configured? Defaults to `true`. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "monitoring_enabled")

    @monitoring_enabled.setter
    def monitoring_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "monitoring_enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Elasticsearch resource. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="skuName")
    def sku_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the SKU for this Elasticsearch. Changing this forces a new Elasticsearch to be created.

        > **NOTE:** The SKU depends on the Elasticsearch Plans available for your account and is a combination of PlanID_Term.
        Ex: If the plan ID is "planXYZ" and term is "Yearly", the SKU will be "planXYZ_Yearly".
        You may find your eligible plans [here](https://portal.azure.com/#view/Microsoft_Azure_Marketplace/GalleryItemDetailsBladeNopdl/id/elastic.ec-azure-pp) or in the online documentation [here](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/elastic.ec-azure-pp?tab=PlansAndPrice) for more details or in case of any issues with the SKU.
        """
        return pulumi.get(self, "sku_name")

    @sku_name.setter
    def sku_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Elasticsearch resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class Elasticsearch(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 elastic_cloud_email_address: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 logs: Optional[pulumi.Input[Union['ElasticsearchLogsArgs', 'ElasticsearchLogsArgsDict']]] = None,
                 monitoring_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages an Elasticsearch in Elastic Cloud.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        test = azure.core.ResourceGroup("test",
            name="example-resources",
            location="West Europe")
        test_elasticsearch = azure.elasticcloud.Elasticsearch("test",
            name="example-elasticsearch",
            resource_group_name=test.name,
            location=test.location,
            sku_name="ess-consumption-2024_Monthly",
            elastic_cloud_email_address="user@example.com")
        ```

        ## Import

        Elasticsearch's can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:elasticcloud/elasticsearch:Elasticsearch example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Elastic/monitors/monitor1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] elastic_cloud_email_address: Specifies the Email Address which should be associated with this Elasticsearch account. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] location: The Azure Region where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[Union['ElasticsearchLogsArgs', 'ElasticsearchLogsArgsDict']] logs: A `logs` block as defined below.
        :param pulumi.Input[bool] monitoring_enabled: Specifies if the Elasticsearch should have monitoring configured? Defaults to `true`. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] name: The name which should be used for this Elasticsearch resource. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] sku_name: Specifies the name of the SKU for this Elasticsearch. Changing this forces a new Elasticsearch to be created.
               
               > **NOTE:** The SKU depends on the Elasticsearch Plans available for your account and is a combination of PlanID_Term.
               Ex: If the plan ID is "planXYZ" and term is "Yearly", the SKU will be "planXYZ_Yearly".
               You may find your eligible plans [here](https://portal.azure.com/#view/Microsoft_Azure_Marketplace/GalleryItemDetailsBladeNopdl/id/elastic.ec-azure-pp) or in the online documentation [here](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/elastic.ec-azure-pp?tab=PlansAndPrice) for more details or in case of any issues with the SKU.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Elasticsearch resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ElasticsearchArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an Elasticsearch in Elastic Cloud.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        test = azure.core.ResourceGroup("test",
            name="example-resources",
            location="West Europe")
        test_elasticsearch = azure.elasticcloud.Elasticsearch("test",
            name="example-elasticsearch",
            resource_group_name=test.name,
            location=test.location,
            sku_name="ess-consumption-2024_Monthly",
            elastic_cloud_email_address="user@example.com")
        ```

        ## Import

        Elasticsearch's can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:elasticcloud/elasticsearch:Elasticsearch example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Elastic/monitors/monitor1
        ```

        :param str resource_name: The name of the resource.
        :param ElasticsearchArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ElasticsearchArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 elastic_cloud_email_address: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 logs: Optional[pulumi.Input[Union['ElasticsearchLogsArgs', 'ElasticsearchLogsArgsDict']]] = None,
                 monitoring_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ElasticsearchArgs.__new__(ElasticsearchArgs)

            if elastic_cloud_email_address is None and not opts.urn:
                raise TypeError("Missing required property 'elastic_cloud_email_address'")
            __props__.__dict__["elastic_cloud_email_address"] = elastic_cloud_email_address
            __props__.__dict__["location"] = location
            __props__.__dict__["logs"] = logs
            __props__.__dict__["monitoring_enabled"] = monitoring_enabled
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if sku_name is None and not opts.urn:
                raise TypeError("Missing required property 'sku_name'")
            __props__.__dict__["sku_name"] = sku_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["elastic_cloud_deployment_id"] = None
            __props__.__dict__["elastic_cloud_sso_default_url"] = None
            __props__.__dict__["elastic_cloud_user_id"] = None
            __props__.__dict__["elasticsearch_service_url"] = None
            __props__.__dict__["kibana_service_url"] = None
            __props__.__dict__["kibana_sso_uri"] = None
        super(Elasticsearch, __self__).__init__(
            'azure:elasticcloud/elasticsearch:Elasticsearch',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            elastic_cloud_deployment_id: Optional[pulumi.Input[str]] = None,
            elastic_cloud_email_address: Optional[pulumi.Input[str]] = None,
            elastic_cloud_sso_default_url: Optional[pulumi.Input[str]] = None,
            elastic_cloud_user_id: Optional[pulumi.Input[str]] = None,
            elasticsearch_service_url: Optional[pulumi.Input[str]] = None,
            kibana_service_url: Optional[pulumi.Input[str]] = None,
            kibana_sso_uri: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            logs: Optional[pulumi.Input[Union['ElasticsearchLogsArgs', 'ElasticsearchLogsArgsDict']]] = None,
            monitoring_enabled: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            sku_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Elasticsearch':
        """
        Get an existing Elasticsearch resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] elastic_cloud_deployment_id: The ID of the Deployment within Elastic Cloud.
        :param pulumi.Input[str] elastic_cloud_email_address: Specifies the Email Address which should be associated with this Elasticsearch account. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] elastic_cloud_sso_default_url: The Default URL used for Single Sign On (SSO) to Elastic Cloud.
        :param pulumi.Input[str] elastic_cloud_user_id: The ID of the User Account within Elastic Cloud.
        :param pulumi.Input[str] elasticsearch_service_url: The URL to the Elasticsearch Service associated with this Elasticsearch.
        :param pulumi.Input[str] kibana_service_url: The URL to the Kibana Dashboard associated with this Elasticsearch.
        :param pulumi.Input[str] kibana_sso_uri: The URI used for SSO to the Kibana Dashboard associated with this Elasticsearch.
        :param pulumi.Input[str] location: The Azure Region where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[Union['ElasticsearchLogsArgs', 'ElasticsearchLogsArgsDict']] logs: A `logs` block as defined below.
        :param pulumi.Input[bool] monitoring_enabled: Specifies if the Elasticsearch should have monitoring configured? Defaults to `true`. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] name: The name which should be used for this Elasticsearch resource. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        :param pulumi.Input[str] sku_name: Specifies the name of the SKU for this Elasticsearch. Changing this forces a new Elasticsearch to be created.
               
               > **NOTE:** The SKU depends on the Elasticsearch Plans available for your account and is a combination of PlanID_Term.
               Ex: If the plan ID is "planXYZ" and term is "Yearly", the SKU will be "planXYZ_Yearly".
               You may find your eligible plans [here](https://portal.azure.com/#view/Microsoft_Azure_Marketplace/GalleryItemDetailsBladeNopdl/id/elastic.ec-azure-pp) or in the online documentation [here](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/elastic.ec-azure-pp?tab=PlansAndPrice) for more details or in case of any issues with the SKU.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Elasticsearch resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ElasticsearchState.__new__(_ElasticsearchState)

        __props__.__dict__["elastic_cloud_deployment_id"] = elastic_cloud_deployment_id
        __props__.__dict__["elastic_cloud_email_address"] = elastic_cloud_email_address
        __props__.__dict__["elastic_cloud_sso_default_url"] = elastic_cloud_sso_default_url
        __props__.__dict__["elastic_cloud_user_id"] = elastic_cloud_user_id
        __props__.__dict__["elasticsearch_service_url"] = elasticsearch_service_url
        __props__.__dict__["kibana_service_url"] = kibana_service_url
        __props__.__dict__["kibana_sso_uri"] = kibana_sso_uri
        __props__.__dict__["location"] = location
        __props__.__dict__["logs"] = logs
        __props__.__dict__["monitoring_enabled"] = monitoring_enabled
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["sku_name"] = sku_name
        __props__.__dict__["tags"] = tags
        return Elasticsearch(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="elasticCloudDeploymentId")
    def elastic_cloud_deployment_id(self) -> pulumi.Output[str]:
        """
        The ID of the Deployment within Elastic Cloud.
        """
        return pulumi.get(self, "elastic_cloud_deployment_id")

    @property
    @pulumi.getter(name="elasticCloudEmailAddress")
    def elastic_cloud_email_address(self) -> pulumi.Output[str]:
        """
        Specifies the Email Address which should be associated with this Elasticsearch account. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "elastic_cloud_email_address")

    @property
    @pulumi.getter(name="elasticCloudSsoDefaultUrl")
    def elastic_cloud_sso_default_url(self) -> pulumi.Output[str]:
        """
        The Default URL used for Single Sign On (SSO) to Elastic Cloud.
        """
        return pulumi.get(self, "elastic_cloud_sso_default_url")

    @property
    @pulumi.getter(name="elasticCloudUserId")
    def elastic_cloud_user_id(self) -> pulumi.Output[str]:
        """
        The ID of the User Account within Elastic Cloud.
        """
        return pulumi.get(self, "elastic_cloud_user_id")

    @property
    @pulumi.getter(name="elasticsearchServiceUrl")
    def elasticsearch_service_url(self) -> pulumi.Output[str]:
        """
        The URL to the Elasticsearch Service associated with this Elasticsearch.
        """
        return pulumi.get(self, "elasticsearch_service_url")

    @property
    @pulumi.getter(name="kibanaServiceUrl")
    def kibana_service_url(self) -> pulumi.Output[str]:
        """
        The URL to the Kibana Dashboard associated with this Elasticsearch.
        """
        return pulumi.get(self, "kibana_service_url")

    @property
    @pulumi.getter(name="kibanaSsoUri")
    def kibana_sso_uri(self) -> pulumi.Output[str]:
        """
        The URI used for SSO to the Kibana Dashboard associated with this Elasticsearch.
        """
        return pulumi.get(self, "kibana_sso_uri")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure Region where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def logs(self) -> pulumi.Output[Optional['outputs.ElasticsearchLogs']]:
        """
        A `logs` block as defined below.
        """
        return pulumi.get(self, "logs")

    @property
    @pulumi.getter(name="monitoringEnabled")
    def monitoring_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies if the Elasticsearch should have monitoring configured? Defaults to `true`. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "monitoring_enabled")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Elasticsearch resource. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Elasticsearch resource should exist. Changing this forces a new Elasticsearch to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="skuName")
    def sku_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the SKU for this Elasticsearch. Changing this forces a new Elasticsearch to be created.

        > **NOTE:** The SKU depends on the Elasticsearch Plans available for your account and is a combination of PlanID_Term.
        Ex: If the plan ID is "planXYZ" and term is "Yearly", the SKU will be "planXYZ_Yearly".
        You may find your eligible plans [here](https://portal.azure.com/#view/Microsoft_Azure_Marketplace/GalleryItemDetailsBladeNopdl/id/elastic.ec-azure-pp) or in the online documentation [here](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/elastic.ec-azure-pp?tab=PlansAndPrice) for more details or in case of any issues with the SKU.
        """
        return pulumi.get(self, "sku_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to the Elasticsearch resource.
        """
        return pulumi.get(self, "tags")

