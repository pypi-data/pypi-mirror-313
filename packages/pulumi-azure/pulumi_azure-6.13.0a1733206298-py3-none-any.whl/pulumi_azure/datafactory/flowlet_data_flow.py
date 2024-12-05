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

__all__ = ['FlowletDataFlowArgs', 'FlowletDataFlow']

@pulumi.input_type
class FlowletDataFlowArgs:
    def __init__(__self__, *,
                 data_factory_id: pulumi.Input[str],
                 annotations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 folder: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 script: Optional[pulumi.Input[str]] = None,
                 script_lines: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 sinks: Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSinkArgs']]]] = None,
                 sources: Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSourceArgs']]]] = None,
                 transformations: Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowTransformationArgs']]]] = None):
        """
        The set of arguments for constructing a FlowletDataFlow resource.
        :param pulumi.Input[str] data_factory_id: The ID of Data Factory in which to associate the Data Flow with. Changing this forces a new resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] annotations: List of tags that can be used for describing the Data Factory Flowlet Data Flow.
        :param pulumi.Input[str] description: The description for the Data Factory Flowlet Data Flow.
        :param pulumi.Input[str] folder: The folder that this Data Flow is in. If not specified, the Data Flow will appear at the root level.
        :param pulumi.Input[str] name: Specifies the name of the Data Factory Flowlet Data Flow. Changing this forces a new resource to be created.
        :param pulumi.Input[str] script: The script for the Data Factory Flowlet Data Flow.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] script_lines: The script lines for the Data Factory Flowlet Data Flow.
        :param pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSinkArgs']]] sinks: One or more `sink` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSourceArgs']]] sources: One or more `source` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowTransformationArgs']]] transformations: One or more `transformation` blocks as defined below.
        """
        pulumi.set(__self__, "data_factory_id", data_factory_id)
        if annotations is not None:
            pulumi.set(__self__, "annotations", annotations)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if folder is not None:
            pulumi.set(__self__, "folder", folder)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if script is not None:
            pulumi.set(__self__, "script", script)
        if script_lines is not None:
            pulumi.set(__self__, "script_lines", script_lines)
        if sinks is not None:
            pulumi.set(__self__, "sinks", sinks)
        if sources is not None:
            pulumi.set(__self__, "sources", sources)
        if transformations is not None:
            pulumi.set(__self__, "transformations", transformations)

    @property
    @pulumi.getter(name="dataFactoryId")
    def data_factory_id(self) -> pulumi.Input[str]:
        """
        The ID of Data Factory in which to associate the Data Flow with. Changing this forces a new resource.
        """
        return pulumi.get(self, "data_factory_id")

    @data_factory_id.setter
    def data_factory_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "data_factory_id", value)

    @property
    @pulumi.getter
    def annotations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of tags that can be used for describing the Data Factory Flowlet Data Flow.
        """
        return pulumi.get(self, "annotations")

    @annotations.setter
    def annotations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "annotations", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description for the Data Factory Flowlet Data Flow.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def folder(self) -> Optional[pulumi.Input[str]]:
        """
        The folder that this Data Flow is in. If not specified, the Data Flow will appear at the root level.
        """
        return pulumi.get(self, "folder")

    @folder.setter
    def folder(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "folder", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Data Factory Flowlet Data Flow. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def script(self) -> Optional[pulumi.Input[str]]:
        """
        The script for the Data Factory Flowlet Data Flow.
        """
        return pulumi.get(self, "script")

    @script.setter
    def script(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "script", value)

    @property
    @pulumi.getter(name="scriptLines")
    def script_lines(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The script lines for the Data Factory Flowlet Data Flow.
        """
        return pulumi.get(self, "script_lines")

    @script_lines.setter
    def script_lines(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "script_lines", value)

    @property
    @pulumi.getter
    def sinks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSinkArgs']]]]:
        """
        One or more `sink` blocks as defined below.
        """
        return pulumi.get(self, "sinks")

    @sinks.setter
    def sinks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSinkArgs']]]]):
        pulumi.set(self, "sinks", value)

    @property
    @pulumi.getter
    def sources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSourceArgs']]]]:
        """
        One or more `source` blocks as defined below.
        """
        return pulumi.get(self, "sources")

    @sources.setter
    def sources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSourceArgs']]]]):
        pulumi.set(self, "sources", value)

    @property
    @pulumi.getter
    def transformations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowTransformationArgs']]]]:
        """
        One or more `transformation` blocks as defined below.
        """
        return pulumi.get(self, "transformations")

    @transformations.setter
    def transformations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowTransformationArgs']]]]):
        pulumi.set(self, "transformations", value)


@pulumi.input_type
class _FlowletDataFlowState:
    def __init__(__self__, *,
                 annotations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_factory_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 folder: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 script: Optional[pulumi.Input[str]] = None,
                 script_lines: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 sinks: Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSinkArgs']]]] = None,
                 sources: Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSourceArgs']]]] = None,
                 transformations: Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowTransformationArgs']]]] = None):
        """
        Input properties used for looking up and filtering FlowletDataFlow resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] annotations: List of tags that can be used for describing the Data Factory Flowlet Data Flow.
        :param pulumi.Input[str] data_factory_id: The ID of Data Factory in which to associate the Data Flow with. Changing this forces a new resource.
        :param pulumi.Input[str] description: The description for the Data Factory Flowlet Data Flow.
        :param pulumi.Input[str] folder: The folder that this Data Flow is in. If not specified, the Data Flow will appear at the root level.
        :param pulumi.Input[str] name: Specifies the name of the Data Factory Flowlet Data Flow. Changing this forces a new resource to be created.
        :param pulumi.Input[str] script: The script for the Data Factory Flowlet Data Flow.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] script_lines: The script lines for the Data Factory Flowlet Data Flow.
        :param pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSinkArgs']]] sinks: One or more `sink` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSourceArgs']]] sources: One or more `source` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowTransformationArgs']]] transformations: One or more `transformation` blocks as defined below.
        """
        if annotations is not None:
            pulumi.set(__self__, "annotations", annotations)
        if data_factory_id is not None:
            pulumi.set(__self__, "data_factory_id", data_factory_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if folder is not None:
            pulumi.set(__self__, "folder", folder)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if script is not None:
            pulumi.set(__self__, "script", script)
        if script_lines is not None:
            pulumi.set(__self__, "script_lines", script_lines)
        if sinks is not None:
            pulumi.set(__self__, "sinks", sinks)
        if sources is not None:
            pulumi.set(__self__, "sources", sources)
        if transformations is not None:
            pulumi.set(__self__, "transformations", transformations)

    @property
    @pulumi.getter
    def annotations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of tags that can be used for describing the Data Factory Flowlet Data Flow.
        """
        return pulumi.get(self, "annotations")

    @annotations.setter
    def annotations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "annotations", value)

    @property
    @pulumi.getter(name="dataFactoryId")
    def data_factory_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of Data Factory in which to associate the Data Flow with. Changing this forces a new resource.
        """
        return pulumi.get(self, "data_factory_id")

    @data_factory_id.setter
    def data_factory_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_factory_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description for the Data Factory Flowlet Data Flow.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def folder(self) -> Optional[pulumi.Input[str]]:
        """
        The folder that this Data Flow is in. If not specified, the Data Flow will appear at the root level.
        """
        return pulumi.get(self, "folder")

    @folder.setter
    def folder(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "folder", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Data Factory Flowlet Data Flow. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def script(self) -> Optional[pulumi.Input[str]]:
        """
        The script for the Data Factory Flowlet Data Flow.
        """
        return pulumi.get(self, "script")

    @script.setter
    def script(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "script", value)

    @property
    @pulumi.getter(name="scriptLines")
    def script_lines(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The script lines for the Data Factory Flowlet Data Flow.
        """
        return pulumi.get(self, "script_lines")

    @script_lines.setter
    def script_lines(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "script_lines", value)

    @property
    @pulumi.getter
    def sinks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSinkArgs']]]]:
        """
        One or more `sink` blocks as defined below.
        """
        return pulumi.get(self, "sinks")

    @sinks.setter
    def sinks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSinkArgs']]]]):
        pulumi.set(self, "sinks", value)

    @property
    @pulumi.getter
    def sources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSourceArgs']]]]:
        """
        One or more `source` blocks as defined below.
        """
        return pulumi.get(self, "sources")

    @sources.setter
    def sources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowSourceArgs']]]]):
        pulumi.set(self, "sources", value)

    @property
    @pulumi.getter
    def transformations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowTransformationArgs']]]]:
        """
        One or more `transformation` blocks as defined below.
        """
        return pulumi.get(self, "transformations")

    @transformations.setter
    def transformations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FlowletDataFlowTransformationArgs']]]]):
        pulumi.set(self, "transformations", value)


class FlowletDataFlow(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 annotations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_factory_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 folder: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 script: Optional[pulumi.Input[str]] = None,
                 script_lines: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 sinks: Optional[pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowSinkArgs', 'FlowletDataFlowSinkArgsDict']]]]] = None,
                 sources: Optional[pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowSourceArgs', 'FlowletDataFlowSourceArgsDict']]]]] = None,
                 transformations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowTransformationArgs', 'FlowletDataFlowTransformationArgsDict']]]]] = None,
                 __props__=None):
        """
        Manages a Flowlet Data Flow inside an Azure Data Factory.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_account = azure.storage.Account("example",
            name="example",
            location=example.location,
            resource_group_name=example.name,
            account_tier="Standard",
            account_replication_type="LRS")
        example_factory = azure.datafactory.Factory("example",
            name="example",
            location=example.location,
            resource_group_name=example.name)
        example_linked_custom_service = azure.datafactory.LinkedCustomService("example",
            name="linked_service",
            data_factory_id=example_factory.id,
            type="AzureBlobStorage",
            type_properties_json=example_account.primary_connection_string.apply(lambda primary_connection_string: f\"\"\"{{
          "connectionString": "{primary_connection_string}"
        }}
        \"\"\"))
        example1 = azure.datafactory.DatasetJson("example1",
            name="dataset1",
            data_factory_id=example_factory.id,
            linked_service_name=example_linked_custom_service.name,
            azure_blob_storage_location={
                "container": "container",
                "path": "foo/bar/",
                "filename": "foo.txt",
            },
            encoding="UTF-8")
        example2 = azure.datafactory.DatasetJson("example2",
            name="dataset2",
            data_factory_id=example_factory.id,
            linked_service_name=example_linked_custom_service.name,
            azure_blob_storage_location={
                "container": "container",
                "path": "foo/bar/",
                "filename": "bar.txt",
            },
            encoding="UTF-8")
        example1_flowlet_data_flow = azure.datafactory.FlowletDataFlow("example1",
            name="example",
            data_factory_id=example_factory.id,
            sources=[{
                "name": "source1",
                "linked_service": {
                    "name": example_linked_custom_service.name,
                },
            }],
            sinks=[{
                "name": "sink1",
                "linked_service": {
                    "name": example_linked_custom_service.name,
                },
            }],
            script=\"\"\"source(
          allowSchemaDrift: true, 
          validateSchema: false, 
          limit: 100, 
          ignoreNoFilesFound: false, 
          documentForm: 'documentPerLine') ~> source1 
        source1 sink(
          allowSchemaDrift: true, 
          validateSchema: false, 
          skipDuplicateMapInputs: true, 
          skipDuplicateMapOutputs: true) ~> sink1
        \"\"\")
        example2_flowlet_data_flow = azure.datafactory.FlowletDataFlow("example2",
            name="example",
            data_factory_id=example_factory.id,
            sources=[{
                "name": "source1",
                "linked_service": {
                    "name": example_linked_custom_service.name,
                },
            }],
            sinks=[{
                "name": "sink1",
                "linked_service": {
                    "name": example_linked_custom_service.name,
                },
            }],
            script=\"\"\"source(
          allowSchemaDrift: true, 
          validateSchema: false, 
          limit: 100, 
          ignoreNoFilesFound: false, 
          documentForm: 'documentPerLine') ~> source1 
        source1 sink(
          allowSchemaDrift: true, 
          validateSchema: false, 
          skipDuplicateMapInputs: true, 
          skipDuplicateMapOutputs: true) ~> sink1
        \"\"\")
        example_flowlet_data_flow = azure.datafactory.FlowletDataFlow("example",
            name="example",
            data_factory_id=example_factory.id,
            sources=[{
                "name": "source1",
                "flowlet": {
                    "name": example1_flowlet_data_flow.name,
                },
                "linked_service": {
                    "name": example_linked_custom_service.name,
                },
            }],
            sinks=[{
                "name": "sink1",
                "flowlet": {
                    "name": example2_flowlet_data_flow.name,
                },
                "linked_service": {
                    "name": example_linked_custom_service.name,
                },
            }],
            script=\"\"\"source(
          allowSchemaDrift: true, 
          validateSchema: false, 
          limit: 100, 
          ignoreNoFilesFound: false, 
          documentForm: 'documentPerLine') ~> source1 
        source1 sink(
          allowSchemaDrift: true, 
          validateSchema: false, 
          skipDuplicateMapInputs: true, 
          skipDuplicateMapOutputs: true) ~> sink1
        \"\"\")
        ```

        ## Import

        Data Factory Flowlet Data Flow can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:datafactory/flowletDataFlow:FlowletDataFlow example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example/providers/Microsoft.DataFactory/factories/example/dataflows/example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] annotations: List of tags that can be used for describing the Data Factory Flowlet Data Flow.
        :param pulumi.Input[str] data_factory_id: The ID of Data Factory in which to associate the Data Flow with. Changing this forces a new resource.
        :param pulumi.Input[str] description: The description for the Data Factory Flowlet Data Flow.
        :param pulumi.Input[str] folder: The folder that this Data Flow is in. If not specified, the Data Flow will appear at the root level.
        :param pulumi.Input[str] name: Specifies the name of the Data Factory Flowlet Data Flow. Changing this forces a new resource to be created.
        :param pulumi.Input[str] script: The script for the Data Factory Flowlet Data Flow.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] script_lines: The script lines for the Data Factory Flowlet Data Flow.
        :param pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowSinkArgs', 'FlowletDataFlowSinkArgsDict']]]] sinks: One or more `sink` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowSourceArgs', 'FlowletDataFlowSourceArgsDict']]]] sources: One or more `source` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowTransformationArgs', 'FlowletDataFlowTransformationArgsDict']]]] transformations: One or more `transformation` blocks as defined below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FlowletDataFlowArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Flowlet Data Flow inside an Azure Data Factory.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_account = azure.storage.Account("example",
            name="example",
            location=example.location,
            resource_group_name=example.name,
            account_tier="Standard",
            account_replication_type="LRS")
        example_factory = azure.datafactory.Factory("example",
            name="example",
            location=example.location,
            resource_group_name=example.name)
        example_linked_custom_service = azure.datafactory.LinkedCustomService("example",
            name="linked_service",
            data_factory_id=example_factory.id,
            type="AzureBlobStorage",
            type_properties_json=example_account.primary_connection_string.apply(lambda primary_connection_string: f\"\"\"{{
          "connectionString": "{primary_connection_string}"
        }}
        \"\"\"))
        example1 = azure.datafactory.DatasetJson("example1",
            name="dataset1",
            data_factory_id=example_factory.id,
            linked_service_name=example_linked_custom_service.name,
            azure_blob_storage_location={
                "container": "container",
                "path": "foo/bar/",
                "filename": "foo.txt",
            },
            encoding="UTF-8")
        example2 = azure.datafactory.DatasetJson("example2",
            name="dataset2",
            data_factory_id=example_factory.id,
            linked_service_name=example_linked_custom_service.name,
            azure_blob_storage_location={
                "container": "container",
                "path": "foo/bar/",
                "filename": "bar.txt",
            },
            encoding="UTF-8")
        example1_flowlet_data_flow = azure.datafactory.FlowletDataFlow("example1",
            name="example",
            data_factory_id=example_factory.id,
            sources=[{
                "name": "source1",
                "linked_service": {
                    "name": example_linked_custom_service.name,
                },
            }],
            sinks=[{
                "name": "sink1",
                "linked_service": {
                    "name": example_linked_custom_service.name,
                },
            }],
            script=\"\"\"source(
          allowSchemaDrift: true, 
          validateSchema: false, 
          limit: 100, 
          ignoreNoFilesFound: false, 
          documentForm: 'documentPerLine') ~> source1 
        source1 sink(
          allowSchemaDrift: true, 
          validateSchema: false, 
          skipDuplicateMapInputs: true, 
          skipDuplicateMapOutputs: true) ~> sink1
        \"\"\")
        example2_flowlet_data_flow = azure.datafactory.FlowletDataFlow("example2",
            name="example",
            data_factory_id=example_factory.id,
            sources=[{
                "name": "source1",
                "linked_service": {
                    "name": example_linked_custom_service.name,
                },
            }],
            sinks=[{
                "name": "sink1",
                "linked_service": {
                    "name": example_linked_custom_service.name,
                },
            }],
            script=\"\"\"source(
          allowSchemaDrift: true, 
          validateSchema: false, 
          limit: 100, 
          ignoreNoFilesFound: false, 
          documentForm: 'documentPerLine') ~> source1 
        source1 sink(
          allowSchemaDrift: true, 
          validateSchema: false, 
          skipDuplicateMapInputs: true, 
          skipDuplicateMapOutputs: true) ~> sink1
        \"\"\")
        example_flowlet_data_flow = azure.datafactory.FlowletDataFlow("example",
            name="example",
            data_factory_id=example_factory.id,
            sources=[{
                "name": "source1",
                "flowlet": {
                    "name": example1_flowlet_data_flow.name,
                },
                "linked_service": {
                    "name": example_linked_custom_service.name,
                },
            }],
            sinks=[{
                "name": "sink1",
                "flowlet": {
                    "name": example2_flowlet_data_flow.name,
                },
                "linked_service": {
                    "name": example_linked_custom_service.name,
                },
            }],
            script=\"\"\"source(
          allowSchemaDrift: true, 
          validateSchema: false, 
          limit: 100, 
          ignoreNoFilesFound: false, 
          documentForm: 'documentPerLine') ~> source1 
        source1 sink(
          allowSchemaDrift: true, 
          validateSchema: false, 
          skipDuplicateMapInputs: true, 
          skipDuplicateMapOutputs: true) ~> sink1
        \"\"\")
        ```

        ## Import

        Data Factory Flowlet Data Flow can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:datafactory/flowletDataFlow:FlowletDataFlow example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example/providers/Microsoft.DataFactory/factories/example/dataflows/example
        ```

        :param str resource_name: The name of the resource.
        :param FlowletDataFlowArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FlowletDataFlowArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 annotations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_factory_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 folder: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 script: Optional[pulumi.Input[str]] = None,
                 script_lines: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 sinks: Optional[pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowSinkArgs', 'FlowletDataFlowSinkArgsDict']]]]] = None,
                 sources: Optional[pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowSourceArgs', 'FlowletDataFlowSourceArgsDict']]]]] = None,
                 transformations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowTransformationArgs', 'FlowletDataFlowTransformationArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FlowletDataFlowArgs.__new__(FlowletDataFlowArgs)

            __props__.__dict__["annotations"] = annotations
            if data_factory_id is None and not opts.urn:
                raise TypeError("Missing required property 'data_factory_id'")
            __props__.__dict__["data_factory_id"] = data_factory_id
            __props__.__dict__["description"] = description
            __props__.__dict__["folder"] = folder
            __props__.__dict__["name"] = name
            __props__.__dict__["script"] = script
            __props__.__dict__["script_lines"] = script_lines
            __props__.__dict__["sinks"] = sinks
            __props__.__dict__["sources"] = sources
            __props__.__dict__["transformations"] = transformations
        super(FlowletDataFlow, __self__).__init__(
            'azure:datafactory/flowletDataFlow:FlowletDataFlow',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            annotations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            data_factory_id: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            folder: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            script: Optional[pulumi.Input[str]] = None,
            script_lines: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            sinks: Optional[pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowSinkArgs', 'FlowletDataFlowSinkArgsDict']]]]] = None,
            sources: Optional[pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowSourceArgs', 'FlowletDataFlowSourceArgsDict']]]]] = None,
            transformations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowTransformationArgs', 'FlowletDataFlowTransformationArgsDict']]]]] = None) -> 'FlowletDataFlow':
        """
        Get an existing FlowletDataFlow resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] annotations: List of tags that can be used for describing the Data Factory Flowlet Data Flow.
        :param pulumi.Input[str] data_factory_id: The ID of Data Factory in which to associate the Data Flow with. Changing this forces a new resource.
        :param pulumi.Input[str] description: The description for the Data Factory Flowlet Data Flow.
        :param pulumi.Input[str] folder: The folder that this Data Flow is in. If not specified, the Data Flow will appear at the root level.
        :param pulumi.Input[str] name: Specifies the name of the Data Factory Flowlet Data Flow. Changing this forces a new resource to be created.
        :param pulumi.Input[str] script: The script for the Data Factory Flowlet Data Flow.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] script_lines: The script lines for the Data Factory Flowlet Data Flow.
        :param pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowSinkArgs', 'FlowletDataFlowSinkArgsDict']]]] sinks: One or more `sink` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowSourceArgs', 'FlowletDataFlowSourceArgsDict']]]] sources: One or more `source` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[Union['FlowletDataFlowTransformationArgs', 'FlowletDataFlowTransformationArgsDict']]]] transformations: One or more `transformation` blocks as defined below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FlowletDataFlowState.__new__(_FlowletDataFlowState)

        __props__.__dict__["annotations"] = annotations
        __props__.__dict__["data_factory_id"] = data_factory_id
        __props__.__dict__["description"] = description
        __props__.__dict__["folder"] = folder
        __props__.__dict__["name"] = name
        __props__.__dict__["script"] = script
        __props__.__dict__["script_lines"] = script_lines
        __props__.__dict__["sinks"] = sinks
        __props__.__dict__["sources"] = sources
        __props__.__dict__["transformations"] = transformations
        return FlowletDataFlow(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def annotations(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of tags that can be used for describing the Data Factory Flowlet Data Flow.
        """
        return pulumi.get(self, "annotations")

    @property
    @pulumi.getter(name="dataFactoryId")
    def data_factory_id(self) -> pulumi.Output[str]:
        """
        The ID of Data Factory in which to associate the Data Flow with. Changing this forces a new resource.
        """
        return pulumi.get(self, "data_factory_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description for the Data Factory Flowlet Data Flow.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def folder(self) -> pulumi.Output[Optional[str]]:
        """
        The folder that this Data Flow is in. If not specified, the Data Flow will appear at the root level.
        """
        return pulumi.get(self, "folder")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Data Factory Flowlet Data Flow. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def script(self) -> pulumi.Output[Optional[str]]:
        """
        The script for the Data Factory Flowlet Data Flow.
        """
        return pulumi.get(self, "script")

    @property
    @pulumi.getter(name="scriptLines")
    def script_lines(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The script lines for the Data Factory Flowlet Data Flow.
        """
        return pulumi.get(self, "script_lines")

    @property
    @pulumi.getter
    def sinks(self) -> pulumi.Output[Optional[Sequence['outputs.FlowletDataFlowSink']]]:
        """
        One or more `sink` blocks as defined below.
        """
        return pulumi.get(self, "sinks")

    @property
    @pulumi.getter
    def sources(self) -> pulumi.Output[Optional[Sequence['outputs.FlowletDataFlowSource']]]:
        """
        One or more `source` blocks as defined below.
        """
        return pulumi.get(self, "sources")

    @property
    @pulumi.getter
    def transformations(self) -> pulumi.Output[Optional[Sequence['outputs.FlowletDataFlowTransformation']]]:
        """
        One or more `transformation` blocks as defined below.
        """
        return pulumi.get(self, "transformations")

