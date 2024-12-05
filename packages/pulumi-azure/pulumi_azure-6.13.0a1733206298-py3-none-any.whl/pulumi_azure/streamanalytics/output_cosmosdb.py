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

__all__ = ['OutputCosmosdbArgs', 'OutputCosmosdb']

@pulumi.input_type
class OutputCosmosdbArgs:
    def __init__(__self__, *,
                 container_name: pulumi.Input[str],
                 cosmosdb_account_key: pulumi.Input[str],
                 cosmosdb_sql_database_id: pulumi.Input[str],
                 stream_analytics_job_id: pulumi.Input[str],
                 document_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 partition_key: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a OutputCosmosdb resource.
        :param pulumi.Input[str] container_name: The name of the CosmosDB container.
        :param pulumi.Input[str] cosmosdb_account_key: The account key for the CosmosDB database.
        :param pulumi.Input[str] cosmosdb_sql_database_id: The ID of the CosmosDB database.
        :param pulumi.Input[str] stream_analytics_job_id: The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        :param pulumi.Input[str] document_id: The name of the field in output events used to specify the primary key which insert or update operations are based on.
        :param pulumi.Input[str] name: The name of the Stream Analytics Output. Changing this forces a new resource to be created.
        :param pulumi.Input[str] partition_key: The name of the field in output events used to specify the key for partitioning output across collections. If `container_name` contains `{partition}` token, this property is required to be specified.
        """
        pulumi.set(__self__, "container_name", container_name)
        pulumi.set(__self__, "cosmosdb_account_key", cosmosdb_account_key)
        pulumi.set(__self__, "cosmosdb_sql_database_id", cosmosdb_sql_database_id)
        pulumi.set(__self__, "stream_analytics_job_id", stream_analytics_job_id)
        if document_id is not None:
            pulumi.set(__self__, "document_id", document_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if partition_key is not None:
            pulumi.set(__self__, "partition_key", partition_key)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> pulumi.Input[str]:
        """
        The name of the CosmosDB container.
        """
        return pulumi.get(self, "container_name")

    @container_name.setter
    def container_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "container_name", value)

    @property
    @pulumi.getter(name="cosmosdbAccountKey")
    def cosmosdb_account_key(self) -> pulumi.Input[str]:
        """
        The account key for the CosmosDB database.
        """
        return pulumi.get(self, "cosmosdb_account_key")

    @cosmosdb_account_key.setter
    def cosmosdb_account_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "cosmosdb_account_key", value)

    @property
    @pulumi.getter(name="cosmosdbSqlDatabaseId")
    def cosmosdb_sql_database_id(self) -> pulumi.Input[str]:
        """
        The ID of the CosmosDB database.
        """
        return pulumi.get(self, "cosmosdb_sql_database_id")

    @cosmosdb_sql_database_id.setter
    def cosmosdb_sql_database_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "cosmosdb_sql_database_id", value)

    @property
    @pulumi.getter(name="streamAnalyticsJobId")
    def stream_analytics_job_id(self) -> pulumi.Input[str]:
        """
        The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "stream_analytics_job_id")

    @stream_analytics_job_id.setter
    def stream_analytics_job_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "stream_analytics_job_id", value)

    @property
    @pulumi.getter(name="documentId")
    def document_id(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the field in output events used to specify the primary key which insert or update operations are based on.
        """
        return pulumi.get(self, "document_id")

    @document_id.setter
    def document_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "document_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Stream Analytics Output. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="partitionKey")
    def partition_key(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the field in output events used to specify the key for partitioning output across collections. If `container_name` contains `{partition}` token, this property is required to be specified.
        """
        return pulumi.get(self, "partition_key")

    @partition_key.setter
    def partition_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "partition_key", value)


@pulumi.input_type
class _OutputCosmosdbState:
    def __init__(__self__, *,
                 container_name: Optional[pulumi.Input[str]] = None,
                 cosmosdb_account_key: Optional[pulumi.Input[str]] = None,
                 cosmosdb_sql_database_id: Optional[pulumi.Input[str]] = None,
                 document_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 partition_key: Optional[pulumi.Input[str]] = None,
                 stream_analytics_job_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering OutputCosmosdb resources.
        :param pulumi.Input[str] container_name: The name of the CosmosDB container.
        :param pulumi.Input[str] cosmosdb_account_key: The account key for the CosmosDB database.
        :param pulumi.Input[str] cosmosdb_sql_database_id: The ID of the CosmosDB database.
        :param pulumi.Input[str] document_id: The name of the field in output events used to specify the primary key which insert or update operations are based on.
        :param pulumi.Input[str] name: The name of the Stream Analytics Output. Changing this forces a new resource to be created.
        :param pulumi.Input[str] partition_key: The name of the field in output events used to specify the key for partitioning output across collections. If `container_name` contains `{partition}` token, this property is required to be specified.
        :param pulumi.Input[str] stream_analytics_job_id: The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        """
        if container_name is not None:
            pulumi.set(__self__, "container_name", container_name)
        if cosmosdb_account_key is not None:
            pulumi.set(__self__, "cosmosdb_account_key", cosmosdb_account_key)
        if cosmosdb_sql_database_id is not None:
            pulumi.set(__self__, "cosmosdb_sql_database_id", cosmosdb_sql_database_id)
        if document_id is not None:
            pulumi.set(__self__, "document_id", document_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if partition_key is not None:
            pulumi.set(__self__, "partition_key", partition_key)
        if stream_analytics_job_id is not None:
            pulumi.set(__self__, "stream_analytics_job_id", stream_analytics_job_id)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the CosmosDB container.
        """
        return pulumi.get(self, "container_name")

    @container_name.setter
    def container_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "container_name", value)

    @property
    @pulumi.getter(name="cosmosdbAccountKey")
    def cosmosdb_account_key(self) -> Optional[pulumi.Input[str]]:
        """
        The account key for the CosmosDB database.
        """
        return pulumi.get(self, "cosmosdb_account_key")

    @cosmosdb_account_key.setter
    def cosmosdb_account_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cosmosdb_account_key", value)

    @property
    @pulumi.getter(name="cosmosdbSqlDatabaseId")
    def cosmosdb_sql_database_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the CosmosDB database.
        """
        return pulumi.get(self, "cosmosdb_sql_database_id")

    @cosmosdb_sql_database_id.setter
    def cosmosdb_sql_database_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cosmosdb_sql_database_id", value)

    @property
    @pulumi.getter(name="documentId")
    def document_id(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the field in output events used to specify the primary key which insert or update operations are based on.
        """
        return pulumi.get(self, "document_id")

    @document_id.setter
    def document_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "document_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Stream Analytics Output. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="partitionKey")
    def partition_key(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the field in output events used to specify the key for partitioning output across collections. If `container_name` contains `{partition}` token, this property is required to be specified.
        """
        return pulumi.get(self, "partition_key")

    @partition_key.setter
    def partition_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "partition_key", value)

    @property
    @pulumi.getter(name="streamAnalyticsJobId")
    def stream_analytics_job_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "stream_analytics_job_id")

    @stream_analytics_job_id.setter
    def stream_analytics_job_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stream_analytics_job_id", value)


class OutputCosmosdb(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 cosmosdb_account_key: Optional[pulumi.Input[str]] = None,
                 cosmosdb_sql_database_id: Optional[pulumi.Input[str]] = None,
                 document_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 partition_key: Optional[pulumi.Input[str]] = None,
                 stream_analytics_job_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Stream Analytics Output to CosmosDB.

        ## Import

        Stream Analytics Outputs for CosmosDB can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:streamanalytics/outputCosmosdb:OutputCosmosdb example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.StreamAnalytics/streamingJobs/job1/outputs/output1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] container_name: The name of the CosmosDB container.
        :param pulumi.Input[str] cosmosdb_account_key: The account key for the CosmosDB database.
        :param pulumi.Input[str] cosmosdb_sql_database_id: The ID of the CosmosDB database.
        :param pulumi.Input[str] document_id: The name of the field in output events used to specify the primary key which insert or update operations are based on.
        :param pulumi.Input[str] name: The name of the Stream Analytics Output. Changing this forces a new resource to be created.
        :param pulumi.Input[str] partition_key: The name of the field in output events used to specify the key for partitioning output across collections. If `container_name` contains `{partition}` token, this property is required to be specified.
        :param pulumi.Input[str] stream_analytics_job_id: The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OutputCosmosdbArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Stream Analytics Output to CosmosDB.

        ## Import

        Stream Analytics Outputs for CosmosDB can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:streamanalytics/outputCosmosdb:OutputCosmosdb example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.StreamAnalytics/streamingJobs/job1/outputs/output1
        ```

        :param str resource_name: The name of the resource.
        :param OutputCosmosdbArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OutputCosmosdbArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 cosmosdb_account_key: Optional[pulumi.Input[str]] = None,
                 cosmosdb_sql_database_id: Optional[pulumi.Input[str]] = None,
                 document_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 partition_key: Optional[pulumi.Input[str]] = None,
                 stream_analytics_job_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OutputCosmosdbArgs.__new__(OutputCosmosdbArgs)

            if container_name is None and not opts.urn:
                raise TypeError("Missing required property 'container_name'")
            __props__.__dict__["container_name"] = container_name
            if cosmosdb_account_key is None and not opts.urn:
                raise TypeError("Missing required property 'cosmosdb_account_key'")
            __props__.__dict__["cosmosdb_account_key"] = None if cosmosdb_account_key is None else pulumi.Output.secret(cosmosdb_account_key)
            if cosmosdb_sql_database_id is None and not opts.urn:
                raise TypeError("Missing required property 'cosmosdb_sql_database_id'")
            __props__.__dict__["cosmosdb_sql_database_id"] = cosmosdb_sql_database_id
            __props__.__dict__["document_id"] = document_id
            __props__.__dict__["name"] = name
            __props__.__dict__["partition_key"] = partition_key
            if stream_analytics_job_id is None and not opts.urn:
                raise TypeError("Missing required property 'stream_analytics_job_id'")
            __props__.__dict__["stream_analytics_job_id"] = stream_analytics_job_id
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["cosmosdbAccountKey"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(OutputCosmosdb, __self__).__init__(
            'azure:streamanalytics/outputCosmosdb:OutputCosmosdb',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            container_name: Optional[pulumi.Input[str]] = None,
            cosmosdb_account_key: Optional[pulumi.Input[str]] = None,
            cosmosdb_sql_database_id: Optional[pulumi.Input[str]] = None,
            document_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            partition_key: Optional[pulumi.Input[str]] = None,
            stream_analytics_job_id: Optional[pulumi.Input[str]] = None) -> 'OutputCosmosdb':
        """
        Get an existing OutputCosmosdb resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] container_name: The name of the CosmosDB container.
        :param pulumi.Input[str] cosmosdb_account_key: The account key for the CosmosDB database.
        :param pulumi.Input[str] cosmosdb_sql_database_id: The ID of the CosmosDB database.
        :param pulumi.Input[str] document_id: The name of the field in output events used to specify the primary key which insert or update operations are based on.
        :param pulumi.Input[str] name: The name of the Stream Analytics Output. Changing this forces a new resource to be created.
        :param pulumi.Input[str] partition_key: The name of the field in output events used to specify the key for partitioning output across collections. If `container_name` contains `{partition}` token, this property is required to be specified.
        :param pulumi.Input[str] stream_analytics_job_id: The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OutputCosmosdbState.__new__(_OutputCosmosdbState)

        __props__.__dict__["container_name"] = container_name
        __props__.__dict__["cosmosdb_account_key"] = cosmosdb_account_key
        __props__.__dict__["cosmosdb_sql_database_id"] = cosmosdb_sql_database_id
        __props__.__dict__["document_id"] = document_id
        __props__.__dict__["name"] = name
        __props__.__dict__["partition_key"] = partition_key
        __props__.__dict__["stream_analytics_job_id"] = stream_analytics_job_id
        return OutputCosmosdb(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> pulumi.Output[str]:
        """
        The name of the CosmosDB container.
        """
        return pulumi.get(self, "container_name")

    @property
    @pulumi.getter(name="cosmosdbAccountKey")
    def cosmosdb_account_key(self) -> pulumi.Output[str]:
        """
        The account key for the CosmosDB database.
        """
        return pulumi.get(self, "cosmosdb_account_key")

    @property
    @pulumi.getter(name="cosmosdbSqlDatabaseId")
    def cosmosdb_sql_database_id(self) -> pulumi.Output[str]:
        """
        The ID of the CosmosDB database.
        """
        return pulumi.get(self, "cosmosdb_sql_database_id")

    @property
    @pulumi.getter(name="documentId")
    def document_id(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the field in output events used to specify the primary key which insert or update operations are based on.
        """
        return pulumi.get(self, "document_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Stream Analytics Output. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="partitionKey")
    def partition_key(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the field in output events used to specify the key for partitioning output across collections. If `container_name` contains `{partition}` token, this property is required to be specified.
        """
        return pulumi.get(self, "partition_key")

    @property
    @pulumi.getter(name="streamAnalyticsJobId")
    def stream_analytics_job_id(self) -> pulumi.Output[str]:
        """
        The ID of the Stream Analytics Job. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "stream_analytics_job_id")

