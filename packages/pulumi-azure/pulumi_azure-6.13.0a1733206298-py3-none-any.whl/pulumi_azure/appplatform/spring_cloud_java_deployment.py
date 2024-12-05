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

__all__ = ['SpringCloudJavaDeploymentArgs', 'SpringCloudJavaDeployment']

@pulumi.input_type
class SpringCloudJavaDeploymentArgs:
    def __init__(__self__, *,
                 spring_cloud_app_id: pulumi.Input[str],
                 environment_variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 instance_count: Optional[pulumi.Input[int]] = None,
                 jvm_options: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 quota: Optional[pulumi.Input['SpringCloudJavaDeploymentQuotaArgs']] = None,
                 runtime_version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SpringCloudJavaDeployment resource.
        :param pulumi.Input[str] spring_cloud_app_id: Specifies the id of the Spring Cloud Application in which to create the Deployment. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] environment_variables: Specifies the environment variables of the Spring Cloud Deployment as a map of key-value pairs.
        :param pulumi.Input[int] instance_count: Specifies the required instance count of the Spring Cloud Deployment. Possible Values are between `1` and `500`. Defaults to `1` if not specified.
        :param pulumi.Input[str] jvm_options: Specifies the jvm option of the Spring Cloud Deployment.
        :param pulumi.Input[str] name: Specifies the name of the Spring Cloud Deployment. Changing this forces a new resource to be created.
        :param pulumi.Input['SpringCloudJavaDeploymentQuotaArgs'] quota: A `quota` block as defined below.
        :param pulumi.Input[str] runtime_version: Specifies the runtime version of the Spring Cloud Deployment. Possible Values are `Java_8`, `Java_11` and `Java_17`. Defaults to `Java_8`.
        """
        pulumi.set(__self__, "spring_cloud_app_id", spring_cloud_app_id)
        if environment_variables is not None:
            pulumi.set(__self__, "environment_variables", environment_variables)
        if instance_count is not None:
            pulumi.set(__self__, "instance_count", instance_count)
        if jvm_options is not None:
            pulumi.set(__self__, "jvm_options", jvm_options)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if quota is not None:
            pulumi.set(__self__, "quota", quota)
        if runtime_version is not None:
            pulumi.set(__self__, "runtime_version", runtime_version)

    @property
    @pulumi.getter(name="springCloudAppId")
    def spring_cloud_app_id(self) -> pulumi.Input[str]:
        """
        Specifies the id of the Spring Cloud Application in which to create the Deployment. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "spring_cloud_app_id")

    @spring_cloud_app_id.setter
    def spring_cloud_app_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "spring_cloud_app_id", value)

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Specifies the environment variables of the Spring Cloud Deployment as a map of key-value pairs.
        """
        return pulumi.get(self, "environment_variables")

    @environment_variables.setter
    def environment_variables(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "environment_variables", value)

    @property
    @pulumi.getter(name="instanceCount")
    def instance_count(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the required instance count of the Spring Cloud Deployment. Possible Values are between `1` and `500`. Defaults to `1` if not specified.
        """
        return pulumi.get(self, "instance_count")

    @instance_count.setter
    def instance_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "instance_count", value)

    @property
    @pulumi.getter(name="jvmOptions")
    def jvm_options(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the jvm option of the Spring Cloud Deployment.
        """
        return pulumi.get(self, "jvm_options")

    @jvm_options.setter
    def jvm_options(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "jvm_options", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Spring Cloud Deployment. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def quota(self) -> Optional[pulumi.Input['SpringCloudJavaDeploymentQuotaArgs']]:
        """
        A `quota` block as defined below.
        """
        return pulumi.get(self, "quota")

    @quota.setter
    def quota(self, value: Optional[pulumi.Input['SpringCloudJavaDeploymentQuotaArgs']]):
        pulumi.set(self, "quota", value)

    @property
    @pulumi.getter(name="runtimeVersion")
    def runtime_version(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the runtime version of the Spring Cloud Deployment. Possible Values are `Java_8`, `Java_11` and `Java_17`. Defaults to `Java_8`.
        """
        return pulumi.get(self, "runtime_version")

    @runtime_version.setter
    def runtime_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "runtime_version", value)


@pulumi.input_type
class _SpringCloudJavaDeploymentState:
    def __init__(__self__, *,
                 environment_variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 instance_count: Optional[pulumi.Input[int]] = None,
                 jvm_options: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 quota: Optional[pulumi.Input['SpringCloudJavaDeploymentQuotaArgs']] = None,
                 runtime_version: Optional[pulumi.Input[str]] = None,
                 spring_cloud_app_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SpringCloudJavaDeployment resources.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] environment_variables: Specifies the environment variables of the Spring Cloud Deployment as a map of key-value pairs.
        :param pulumi.Input[int] instance_count: Specifies the required instance count of the Spring Cloud Deployment. Possible Values are between `1` and `500`. Defaults to `1` if not specified.
        :param pulumi.Input[str] jvm_options: Specifies the jvm option of the Spring Cloud Deployment.
        :param pulumi.Input[str] name: Specifies the name of the Spring Cloud Deployment. Changing this forces a new resource to be created.
        :param pulumi.Input['SpringCloudJavaDeploymentQuotaArgs'] quota: A `quota` block as defined below.
        :param pulumi.Input[str] runtime_version: Specifies the runtime version of the Spring Cloud Deployment. Possible Values are `Java_8`, `Java_11` and `Java_17`. Defaults to `Java_8`.
        :param pulumi.Input[str] spring_cloud_app_id: Specifies the id of the Spring Cloud Application in which to create the Deployment. Changing this forces a new resource to be created.
        """
        if environment_variables is not None:
            pulumi.set(__self__, "environment_variables", environment_variables)
        if instance_count is not None:
            pulumi.set(__self__, "instance_count", instance_count)
        if jvm_options is not None:
            pulumi.set(__self__, "jvm_options", jvm_options)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if quota is not None:
            pulumi.set(__self__, "quota", quota)
        if runtime_version is not None:
            pulumi.set(__self__, "runtime_version", runtime_version)
        if spring_cloud_app_id is not None:
            pulumi.set(__self__, "spring_cloud_app_id", spring_cloud_app_id)

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Specifies the environment variables of the Spring Cloud Deployment as a map of key-value pairs.
        """
        return pulumi.get(self, "environment_variables")

    @environment_variables.setter
    def environment_variables(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "environment_variables", value)

    @property
    @pulumi.getter(name="instanceCount")
    def instance_count(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the required instance count of the Spring Cloud Deployment. Possible Values are between `1` and `500`. Defaults to `1` if not specified.
        """
        return pulumi.get(self, "instance_count")

    @instance_count.setter
    def instance_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "instance_count", value)

    @property
    @pulumi.getter(name="jvmOptions")
    def jvm_options(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the jvm option of the Spring Cloud Deployment.
        """
        return pulumi.get(self, "jvm_options")

    @jvm_options.setter
    def jvm_options(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "jvm_options", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Spring Cloud Deployment. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def quota(self) -> Optional[pulumi.Input['SpringCloudJavaDeploymentQuotaArgs']]:
        """
        A `quota` block as defined below.
        """
        return pulumi.get(self, "quota")

    @quota.setter
    def quota(self, value: Optional[pulumi.Input['SpringCloudJavaDeploymentQuotaArgs']]):
        pulumi.set(self, "quota", value)

    @property
    @pulumi.getter(name="runtimeVersion")
    def runtime_version(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the runtime version of the Spring Cloud Deployment. Possible Values are `Java_8`, `Java_11` and `Java_17`. Defaults to `Java_8`.
        """
        return pulumi.get(self, "runtime_version")

    @runtime_version.setter
    def runtime_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "runtime_version", value)

    @property
    @pulumi.getter(name="springCloudAppId")
    def spring_cloud_app_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the id of the Spring Cloud Application in which to create the Deployment. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "spring_cloud_app_id")

    @spring_cloud_app_id.setter
    def spring_cloud_app_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "spring_cloud_app_id", value)


class SpringCloudJavaDeployment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 environment_variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 instance_count: Optional[pulumi.Input[int]] = None,
                 jvm_options: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 quota: Optional[pulumi.Input[Union['SpringCloudJavaDeploymentQuotaArgs', 'SpringCloudJavaDeploymentQuotaArgsDict']]] = None,
                 runtime_version: Optional[pulumi.Input[str]] = None,
                 spring_cloud_app_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an Azure Spring Cloud Deployment with a Java runtime.

        > **NOTE:** This resource is applicable only for Spring Cloud Service with basic and standard tier.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_spring_cloud_service = azure.appplatform.SpringCloudService("example",
            name="example-springcloud",
            resource_group_name=example.name,
            location=example.location)
        example_spring_cloud_app = azure.appplatform.SpringCloudApp("example",
            name="example-springcloudapp",
            resource_group_name=example.name,
            service_name=example_spring_cloud_service.name,
            identity={
                "type": "SystemAssigned",
            })
        example_spring_cloud_java_deployment = azure.appplatform.SpringCloudJavaDeployment("example",
            name="deploy1",
            spring_cloud_app_id=example_spring_cloud_app.id,
            instance_count=2,
            jvm_options="-XX:+PrintGC",
            quota={
                "cpu": "2",
                "memory": "4Gi",
            },
            runtime_version="Java_11",
            environment_variables={
                "Foo": "Bar",
                "Env": "Staging",
            })
        ```

        ## Import

        Spring Cloud Deployment can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:appplatform/springCloudJavaDeployment:SpringCloudJavaDeployment example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourcegroup1/providers/Microsoft.AppPlatform/spring/service1/apps/app1/deployments/deploy1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] environment_variables: Specifies the environment variables of the Spring Cloud Deployment as a map of key-value pairs.
        :param pulumi.Input[int] instance_count: Specifies the required instance count of the Spring Cloud Deployment. Possible Values are between `1` and `500`. Defaults to `1` if not specified.
        :param pulumi.Input[str] jvm_options: Specifies the jvm option of the Spring Cloud Deployment.
        :param pulumi.Input[str] name: Specifies the name of the Spring Cloud Deployment. Changing this forces a new resource to be created.
        :param pulumi.Input[Union['SpringCloudJavaDeploymentQuotaArgs', 'SpringCloudJavaDeploymentQuotaArgsDict']] quota: A `quota` block as defined below.
        :param pulumi.Input[str] runtime_version: Specifies the runtime version of the Spring Cloud Deployment. Possible Values are `Java_8`, `Java_11` and `Java_17`. Defaults to `Java_8`.
        :param pulumi.Input[str] spring_cloud_app_id: Specifies the id of the Spring Cloud Application in which to create the Deployment. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SpringCloudJavaDeploymentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an Azure Spring Cloud Deployment with a Java runtime.

        > **NOTE:** This resource is applicable only for Spring Cloud Service with basic and standard tier.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        example_spring_cloud_service = azure.appplatform.SpringCloudService("example",
            name="example-springcloud",
            resource_group_name=example.name,
            location=example.location)
        example_spring_cloud_app = azure.appplatform.SpringCloudApp("example",
            name="example-springcloudapp",
            resource_group_name=example.name,
            service_name=example_spring_cloud_service.name,
            identity={
                "type": "SystemAssigned",
            })
        example_spring_cloud_java_deployment = azure.appplatform.SpringCloudJavaDeployment("example",
            name="deploy1",
            spring_cloud_app_id=example_spring_cloud_app.id,
            instance_count=2,
            jvm_options="-XX:+PrintGC",
            quota={
                "cpu": "2",
                "memory": "4Gi",
            },
            runtime_version="Java_11",
            environment_variables={
                "Foo": "Bar",
                "Env": "Staging",
            })
        ```

        ## Import

        Spring Cloud Deployment can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:appplatform/springCloudJavaDeployment:SpringCloudJavaDeployment example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourcegroup1/providers/Microsoft.AppPlatform/spring/service1/apps/app1/deployments/deploy1
        ```

        :param str resource_name: The name of the resource.
        :param SpringCloudJavaDeploymentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SpringCloudJavaDeploymentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 environment_variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 instance_count: Optional[pulumi.Input[int]] = None,
                 jvm_options: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 quota: Optional[pulumi.Input[Union['SpringCloudJavaDeploymentQuotaArgs', 'SpringCloudJavaDeploymentQuotaArgsDict']]] = None,
                 runtime_version: Optional[pulumi.Input[str]] = None,
                 spring_cloud_app_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SpringCloudJavaDeploymentArgs.__new__(SpringCloudJavaDeploymentArgs)

            __props__.__dict__["environment_variables"] = environment_variables
            __props__.__dict__["instance_count"] = instance_count
            __props__.__dict__["jvm_options"] = jvm_options
            __props__.__dict__["name"] = name
            __props__.__dict__["quota"] = quota
            __props__.__dict__["runtime_version"] = runtime_version
            if spring_cloud_app_id is None and not opts.urn:
                raise TypeError("Missing required property 'spring_cloud_app_id'")
            __props__.__dict__["spring_cloud_app_id"] = spring_cloud_app_id
        super(SpringCloudJavaDeployment, __self__).__init__(
            'azure:appplatform/springCloudJavaDeployment:SpringCloudJavaDeployment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            environment_variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            instance_count: Optional[pulumi.Input[int]] = None,
            jvm_options: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            quota: Optional[pulumi.Input[Union['SpringCloudJavaDeploymentQuotaArgs', 'SpringCloudJavaDeploymentQuotaArgsDict']]] = None,
            runtime_version: Optional[pulumi.Input[str]] = None,
            spring_cloud_app_id: Optional[pulumi.Input[str]] = None) -> 'SpringCloudJavaDeployment':
        """
        Get an existing SpringCloudJavaDeployment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] environment_variables: Specifies the environment variables of the Spring Cloud Deployment as a map of key-value pairs.
        :param pulumi.Input[int] instance_count: Specifies the required instance count of the Spring Cloud Deployment. Possible Values are between `1` and `500`. Defaults to `1` if not specified.
        :param pulumi.Input[str] jvm_options: Specifies the jvm option of the Spring Cloud Deployment.
        :param pulumi.Input[str] name: Specifies the name of the Spring Cloud Deployment. Changing this forces a new resource to be created.
        :param pulumi.Input[Union['SpringCloudJavaDeploymentQuotaArgs', 'SpringCloudJavaDeploymentQuotaArgsDict']] quota: A `quota` block as defined below.
        :param pulumi.Input[str] runtime_version: Specifies the runtime version of the Spring Cloud Deployment. Possible Values are `Java_8`, `Java_11` and `Java_17`. Defaults to `Java_8`.
        :param pulumi.Input[str] spring_cloud_app_id: Specifies the id of the Spring Cloud Application in which to create the Deployment. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SpringCloudJavaDeploymentState.__new__(_SpringCloudJavaDeploymentState)

        __props__.__dict__["environment_variables"] = environment_variables
        __props__.__dict__["instance_count"] = instance_count
        __props__.__dict__["jvm_options"] = jvm_options
        __props__.__dict__["name"] = name
        __props__.__dict__["quota"] = quota
        __props__.__dict__["runtime_version"] = runtime_version
        __props__.__dict__["spring_cloud_app_id"] = spring_cloud_app_id
        return SpringCloudJavaDeployment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Specifies the environment variables of the Spring Cloud Deployment as a map of key-value pairs.
        """
        return pulumi.get(self, "environment_variables")

    @property
    @pulumi.getter(name="instanceCount")
    def instance_count(self) -> pulumi.Output[Optional[int]]:
        """
        Specifies the required instance count of the Spring Cloud Deployment. Possible Values are between `1` and `500`. Defaults to `1` if not specified.
        """
        return pulumi.get(self, "instance_count")

    @property
    @pulumi.getter(name="jvmOptions")
    def jvm_options(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the jvm option of the Spring Cloud Deployment.
        """
        return pulumi.get(self, "jvm_options")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Spring Cloud Deployment. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def quota(self) -> pulumi.Output['outputs.SpringCloudJavaDeploymentQuota']:
        """
        A `quota` block as defined below.
        """
        return pulumi.get(self, "quota")

    @property
    @pulumi.getter(name="runtimeVersion")
    def runtime_version(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the runtime version of the Spring Cloud Deployment. Possible Values are `Java_8`, `Java_11` and `Java_17`. Defaults to `Java_8`.
        """
        return pulumi.get(self, "runtime_version")

    @property
    @pulumi.getter(name="springCloudAppId")
    def spring_cloud_app_id(self) -> pulumi.Output[str]:
        """
        Specifies the id of the Spring Cloud Application in which to create the Deployment. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "spring_cloud_app_id")

