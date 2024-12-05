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

__all__ = ['ManagedPrivateEndpointArgs', 'ManagedPrivateEndpoint']

@pulumi.input_type
class ManagedPrivateEndpointArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 stream_analytics_cluster_name: pulumi.Input[str],
                 subresource_name: pulumi.Input[str],
                 target_resource_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ManagedPrivateEndpoint resource.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Stream Analytics Managed Private Endpoint should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] stream_analytics_cluster_name: The name of the Stream Analytics Cluster where the Managed Private Endpoint should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] subresource_name: Specifies the sub resource name which the Stream Analytics Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_resource_id: The ID of the Private Link Enabled Remote Resource which this Stream Analytics Private endpoint should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name which should be used for this Stream Analytics Managed Private Endpoint. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "stream_analytics_cluster_name", stream_analytics_cluster_name)
        pulumi.set(__self__, "subresource_name", subresource_name)
        pulumi.set(__self__, "target_resource_id", target_resource_id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Stream Analytics Managed Private Endpoint should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="streamAnalyticsClusterName")
    def stream_analytics_cluster_name(self) -> pulumi.Input[str]:
        """
        The name of the Stream Analytics Cluster where the Managed Private Endpoint should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "stream_analytics_cluster_name")

    @stream_analytics_cluster_name.setter
    def stream_analytics_cluster_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "stream_analytics_cluster_name", value)

    @property
    @pulumi.getter(name="subresourceName")
    def subresource_name(self) -> pulumi.Input[str]:
        """
        Specifies the sub resource name which the Stream Analytics Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "subresource_name")

    @subresource_name.setter
    def subresource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "subresource_name", value)

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> pulumi.Input[str]:
        """
        The ID of the Private Link Enabled Remote Resource which this Stream Analytics Private endpoint should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "target_resource_id")

    @target_resource_id.setter
    def target_resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_resource_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Stream Analytics Managed Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ManagedPrivateEndpointState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 stream_analytics_cluster_name: Optional[pulumi.Input[str]] = None,
                 subresource_name: Optional[pulumi.Input[str]] = None,
                 target_resource_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ManagedPrivateEndpoint resources.
        :param pulumi.Input[str] name: The name which should be used for this Stream Analytics Managed Private Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Stream Analytics Managed Private Endpoint should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] stream_analytics_cluster_name: The name of the Stream Analytics Cluster where the Managed Private Endpoint should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] subresource_name: Specifies the sub resource name which the Stream Analytics Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_resource_id: The ID of the Private Link Enabled Remote Resource which this Stream Analytics Private endpoint should be connected to. Changing this forces a new resource to be created.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if stream_analytics_cluster_name is not None:
            pulumi.set(__self__, "stream_analytics_cluster_name", stream_analytics_cluster_name)
        if subresource_name is not None:
            pulumi.set(__self__, "subresource_name", subresource_name)
        if target_resource_id is not None:
            pulumi.set(__self__, "target_resource_id", target_resource_id)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Stream Analytics Managed Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Stream Analytics Managed Private Endpoint should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="streamAnalyticsClusterName")
    def stream_analytics_cluster_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Stream Analytics Cluster where the Managed Private Endpoint should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "stream_analytics_cluster_name")

    @stream_analytics_cluster_name.setter
    def stream_analytics_cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stream_analytics_cluster_name", value)

    @property
    @pulumi.getter(name="subresourceName")
    def subresource_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the sub resource name which the Stream Analytics Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "subresource_name")

    @subresource_name.setter
    def subresource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subresource_name", value)

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Private Link Enabled Remote Resource which this Stream Analytics Private endpoint should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "target_resource_id")

    @target_resource_id.setter
    def target_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_resource_id", value)


class ManagedPrivateEndpoint(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 stream_analytics_cluster_name: Optional[pulumi.Input[str]] = None,
                 subresource_name: Optional[pulumi.Input[str]] = None,
                 target_resource_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Stream Analytics Managed Private Endpoint.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_account = azure.storage.Account("example",
            name="examplestorageacc",
            resource_group_name=example.name,
            location=example.location,
            account_tier="Standard",
            account_replication_type="LRS",
            account_kind="StorageV2",
            is_hns_enabled=True)
        example_cluster = azure.streamanalytics.Cluster("example",
            name="examplestreamanalyticscluster",
            resource_group_name=example.name,
            location=example.location,
            streaming_capacity=36)
        example_managed_private_endpoint = azure.streamanalytics.ManagedPrivateEndpoint("example",
            name="exampleprivateendpoint",
            resource_group_name=example.name,
            stream_analytics_cluster_name=example_cluster.name,
            target_resource_id=example_account.id,
            subresource_name="blob")
        ```

        ## Import

        Stream Analytics Private Endpoints can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:streamanalytics/managedPrivateEndpoint:ManagedPrivateEndpoint example /subscriptions/12345678-1234-9876-4563-123456789012/resourceGroups/resGroup1/providers/Microsoft.StreamAnalytics/clusters/cluster1/privateEndpoints/endpoint1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name which should be used for this Stream Analytics Managed Private Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Stream Analytics Managed Private Endpoint should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] stream_analytics_cluster_name: The name of the Stream Analytics Cluster where the Managed Private Endpoint should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] subresource_name: Specifies the sub resource name which the Stream Analytics Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_resource_id: The ID of the Private Link Enabled Remote Resource which this Stream Analytics Private endpoint should be connected to. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagedPrivateEndpointArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Stream Analytics Managed Private Endpoint.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_account = azure.storage.Account("example",
            name="examplestorageacc",
            resource_group_name=example.name,
            location=example.location,
            account_tier="Standard",
            account_replication_type="LRS",
            account_kind="StorageV2",
            is_hns_enabled=True)
        example_cluster = azure.streamanalytics.Cluster("example",
            name="examplestreamanalyticscluster",
            resource_group_name=example.name,
            location=example.location,
            streaming_capacity=36)
        example_managed_private_endpoint = azure.streamanalytics.ManagedPrivateEndpoint("example",
            name="exampleprivateendpoint",
            resource_group_name=example.name,
            stream_analytics_cluster_name=example_cluster.name,
            target_resource_id=example_account.id,
            subresource_name="blob")
        ```

        ## Import

        Stream Analytics Private Endpoints can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:streamanalytics/managedPrivateEndpoint:ManagedPrivateEndpoint example /subscriptions/12345678-1234-9876-4563-123456789012/resourceGroups/resGroup1/providers/Microsoft.StreamAnalytics/clusters/cluster1/privateEndpoints/endpoint1
        ```

        :param str resource_name: The name of the resource.
        :param ManagedPrivateEndpointArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedPrivateEndpointArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 stream_analytics_cluster_name: Optional[pulumi.Input[str]] = None,
                 subresource_name: Optional[pulumi.Input[str]] = None,
                 target_resource_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagedPrivateEndpointArgs.__new__(ManagedPrivateEndpointArgs)

            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if stream_analytics_cluster_name is None and not opts.urn:
                raise TypeError("Missing required property 'stream_analytics_cluster_name'")
            __props__.__dict__["stream_analytics_cluster_name"] = stream_analytics_cluster_name
            if subresource_name is None and not opts.urn:
                raise TypeError("Missing required property 'subresource_name'")
            __props__.__dict__["subresource_name"] = subresource_name
            if target_resource_id is None and not opts.urn:
                raise TypeError("Missing required property 'target_resource_id'")
            __props__.__dict__["target_resource_id"] = target_resource_id
        super(ManagedPrivateEndpoint, __self__).__init__(
            'azure:streamanalytics/managedPrivateEndpoint:ManagedPrivateEndpoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            stream_analytics_cluster_name: Optional[pulumi.Input[str]] = None,
            subresource_name: Optional[pulumi.Input[str]] = None,
            target_resource_id: Optional[pulumi.Input[str]] = None) -> 'ManagedPrivateEndpoint':
        """
        Get an existing ManagedPrivateEndpoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name which should be used for this Stream Analytics Managed Private Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Stream Analytics Managed Private Endpoint should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] stream_analytics_cluster_name: The name of the Stream Analytics Cluster where the Managed Private Endpoint should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] subresource_name: Specifies the sub resource name which the Stream Analytics Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_resource_id: The ID of the Private Link Enabled Remote Resource which this Stream Analytics Private endpoint should be connected to. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ManagedPrivateEndpointState.__new__(_ManagedPrivateEndpointState)

        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["stream_analytics_cluster_name"] = stream_analytics_cluster_name
        __props__.__dict__["subresource_name"] = subresource_name
        __props__.__dict__["target_resource_id"] = target_resource_id
        return ManagedPrivateEndpoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Stream Analytics Managed Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Stream Analytics Managed Private Endpoint should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="streamAnalyticsClusterName")
    def stream_analytics_cluster_name(self) -> pulumi.Output[str]:
        """
        The name of the Stream Analytics Cluster where the Managed Private Endpoint should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "stream_analytics_cluster_name")

    @property
    @pulumi.getter(name="subresourceName")
    def subresource_name(self) -> pulumi.Output[str]:
        """
        Specifies the sub resource name which the Stream Analytics Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "subresource_name")

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> pulumi.Output[str]:
        """
        The ID of the Private Link Enabled Remote Resource which this Stream Analytics Private endpoint should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "target_resource_id")

