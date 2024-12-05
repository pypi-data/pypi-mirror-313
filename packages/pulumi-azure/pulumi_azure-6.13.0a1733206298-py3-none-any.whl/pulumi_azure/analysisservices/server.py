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

__all__ = ['ServerArgs', 'Server']

@pulumi.input_type
class ServerArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 sku: pulumi.Input[str],
                 admin_users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 backup_blob_container_uri: Optional[pulumi.Input[str]] = None,
                 ipv4_firewall_rules: Optional[pulumi.Input[Sequence[pulumi.Input['ServerIpv4FirewallRuleArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 power_bi_service_enabled: Optional[pulumi.Input[bool]] = None,
                 querypool_connection_mode: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Server resource.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the Analysis Services Server should be exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sku: SKU for the Analysis Services Server. Possible values are: `D1`, `B1`, `B2`, `S0`, `S1`, `S2`, `S4`, `S8`, `S9`, `S8v2` and `S9v2`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] admin_users: List of email addresses of admin users.
        :param pulumi.Input[str] backup_blob_container_uri: URI and SAS token for a blob container to store backups.
        :param pulumi.Input[Sequence[pulumi.Input['ServerIpv4FirewallRuleArgs']]] ipv4_firewall_rules: One or more `ipv4_firewall_rule` block(s) as defined below.
        :param pulumi.Input[str] location: The Azure location where the Analysis Services Server exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Analysis Services Server. Only lowercase Alphanumeric characters allowed, starting with a letter. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] power_bi_service_enabled: Indicates if the Power BI service is allowed to access or not.
        :param pulumi.Input[str] querypool_connection_mode: Controls how the read-write server is used in the query pool. If this value is set to `All` then read-write servers are also used for queries. Otherwise with `ReadOnly` these servers do not participate in query operations. Defaults to `All`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "sku", sku)
        if admin_users is not None:
            pulumi.set(__self__, "admin_users", admin_users)
        if backup_blob_container_uri is not None:
            pulumi.set(__self__, "backup_blob_container_uri", backup_blob_container_uri)
        if ipv4_firewall_rules is not None:
            pulumi.set(__self__, "ipv4_firewall_rules", ipv4_firewall_rules)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if power_bi_service_enabled is not None:
            pulumi.set(__self__, "power_bi_service_enabled", power_bi_service_enabled)
        if querypool_connection_mode is not None:
            pulumi.set(__self__, "querypool_connection_mode", querypool_connection_mode)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group in which the Analysis Services Server should be exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Input[str]:
        """
        SKU for the Analysis Services Server. Possible values are: `D1`, `B1`, `B2`, `S0`, `S1`, `S2`, `S4`, `S8`, `S9`, `S8v2` and `S9v2`.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: pulumi.Input[str]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="adminUsers")
    def admin_users(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of email addresses of admin users.
        """
        return pulumi.get(self, "admin_users")

    @admin_users.setter
    def admin_users(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "admin_users", value)

    @property
    @pulumi.getter(name="backupBlobContainerUri")
    def backup_blob_container_uri(self) -> Optional[pulumi.Input[str]]:
        """
        URI and SAS token for a blob container to store backups.
        """
        return pulumi.get(self, "backup_blob_container_uri")

    @backup_blob_container_uri.setter
    def backup_blob_container_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backup_blob_container_uri", value)

    @property
    @pulumi.getter(name="ipv4FirewallRules")
    def ipv4_firewall_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServerIpv4FirewallRuleArgs']]]]:
        """
        One or more `ipv4_firewall_rule` block(s) as defined below.
        """
        return pulumi.get(self, "ipv4_firewall_rules")

    @ipv4_firewall_rules.setter
    def ipv4_firewall_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServerIpv4FirewallRuleArgs']]]]):
        pulumi.set(self, "ipv4_firewall_rules", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure location where the Analysis Services Server exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Analysis Services Server. Only lowercase Alphanumeric characters allowed, starting with a letter. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="powerBiServiceEnabled")
    def power_bi_service_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates if the Power BI service is allowed to access or not.
        """
        return pulumi.get(self, "power_bi_service_enabled")

    @power_bi_service_enabled.setter
    def power_bi_service_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "power_bi_service_enabled", value)

    @property
    @pulumi.getter(name="querypoolConnectionMode")
    def querypool_connection_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Controls how the read-write server is used in the query pool. If this value is set to `All` then read-write servers are also used for queries. Otherwise with `ReadOnly` these servers do not participate in query operations. Defaults to `All`.
        """
        return pulumi.get(self, "querypool_connection_mode")

    @querypool_connection_mode.setter
    def querypool_connection_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "querypool_connection_mode", value)

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
class _ServerState:
    def __init__(__self__, *,
                 admin_users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 backup_blob_container_uri: Optional[pulumi.Input[str]] = None,
                 ipv4_firewall_rules: Optional[pulumi.Input[Sequence[pulumi.Input['ServerIpv4FirewallRuleArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 power_bi_service_enabled: Optional[pulumi.Input[bool]] = None,
                 querypool_connection_mode: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_full_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Server resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] admin_users: List of email addresses of admin users.
        :param pulumi.Input[str] backup_blob_container_uri: URI and SAS token for a blob container to store backups.
        :param pulumi.Input[Sequence[pulumi.Input['ServerIpv4FirewallRuleArgs']]] ipv4_firewall_rules: One or more `ipv4_firewall_rule` block(s) as defined below.
        :param pulumi.Input[str] location: The Azure location where the Analysis Services Server exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Analysis Services Server. Only lowercase Alphanumeric characters allowed, starting with a letter. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] power_bi_service_enabled: Indicates if the Power BI service is allowed to access or not.
        :param pulumi.Input[str] querypool_connection_mode: Controls how the read-write server is used in the query pool. If this value is set to `All` then read-write servers are also used for queries. Otherwise with `ReadOnly` these servers do not participate in query operations. Defaults to `All`.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the Analysis Services Server should be exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] server_full_name: The full name of the Analysis Services Server.
        :param pulumi.Input[str] sku: SKU for the Analysis Services Server. Possible values are: `D1`, `B1`, `B2`, `S0`, `S1`, `S2`, `S4`, `S8`, `S9`, `S8v2` and `S9v2`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        if admin_users is not None:
            pulumi.set(__self__, "admin_users", admin_users)
        if backup_blob_container_uri is not None:
            pulumi.set(__self__, "backup_blob_container_uri", backup_blob_container_uri)
        if ipv4_firewall_rules is not None:
            pulumi.set(__self__, "ipv4_firewall_rules", ipv4_firewall_rules)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if power_bi_service_enabled is not None:
            pulumi.set(__self__, "power_bi_service_enabled", power_bi_service_enabled)
        if querypool_connection_mode is not None:
            pulumi.set(__self__, "querypool_connection_mode", querypool_connection_mode)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if server_full_name is not None:
            pulumi.set(__self__, "server_full_name", server_full_name)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="adminUsers")
    def admin_users(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of email addresses of admin users.
        """
        return pulumi.get(self, "admin_users")

    @admin_users.setter
    def admin_users(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "admin_users", value)

    @property
    @pulumi.getter(name="backupBlobContainerUri")
    def backup_blob_container_uri(self) -> Optional[pulumi.Input[str]]:
        """
        URI and SAS token for a blob container to store backups.
        """
        return pulumi.get(self, "backup_blob_container_uri")

    @backup_blob_container_uri.setter
    def backup_blob_container_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backup_blob_container_uri", value)

    @property
    @pulumi.getter(name="ipv4FirewallRules")
    def ipv4_firewall_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServerIpv4FirewallRuleArgs']]]]:
        """
        One or more `ipv4_firewall_rule` block(s) as defined below.
        """
        return pulumi.get(self, "ipv4_firewall_rules")

    @ipv4_firewall_rules.setter
    def ipv4_firewall_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServerIpv4FirewallRuleArgs']]]]):
        pulumi.set(self, "ipv4_firewall_rules", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure location where the Analysis Services Server exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Analysis Services Server. Only lowercase Alphanumeric characters allowed, starting with a letter. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="powerBiServiceEnabled")
    def power_bi_service_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates if the Power BI service is allowed to access or not.
        """
        return pulumi.get(self, "power_bi_service_enabled")

    @power_bi_service_enabled.setter
    def power_bi_service_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "power_bi_service_enabled", value)

    @property
    @pulumi.getter(name="querypoolConnectionMode")
    def querypool_connection_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Controls how the read-write server is used in the query pool. If this value is set to `All` then read-write servers are also used for queries. Otherwise with `ReadOnly` these servers do not participate in query operations. Defaults to `All`.
        """
        return pulumi.get(self, "querypool_connection_mode")

    @querypool_connection_mode.setter
    def querypool_connection_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "querypool_connection_mode", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group in which the Analysis Services Server should be exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="serverFullName")
    def server_full_name(self) -> Optional[pulumi.Input[str]]:
        """
        The full name of the Analysis Services Server.
        """
        return pulumi.get(self, "server_full_name")

    @server_full_name.setter
    def server_full_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_full_name", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input[str]]:
        """
        SKU for the Analysis Services Server. Possible values are: `D1`, `B1`, `B2`, `S0`, `S1`, `S2`, `S4`, `S8`, `S9`, `S8v2` and `S9v2`.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku", value)

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


class Server(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin_users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 backup_blob_container_uri: Optional[pulumi.Input[str]] = None,
                 ipv4_firewall_rules: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ServerIpv4FirewallRuleArgs', 'ServerIpv4FirewallRuleArgsDict']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 power_bi_service_enabled: Optional[pulumi.Input[bool]] = None,
                 querypool_connection_mode: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages an Analysis Services Server.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="analysis-services-server-test",
            location="West Europe")
        server = azure.analysisservices.Server("server",
            name="analysisservicesserver",
            location=example.location,
            resource_group_name=example.name,
            sku="S0",
            admin_users=["myuser@domain.tld"],
            power_bi_service_enabled=True,
            ipv4_firewall_rules=[{
                "name": "myRule1",
                "range_start": "210.117.252.0",
                "range_end": "210.117.252.255",
            }],
            tags={
                "abc": "123",
            })
        ```

        > **NOTE:** The server resource will automatically be started and stopped during an update if it is in `paused` state.

        ## Import

        Analysis Services Server can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:analysisservices/server:Server server /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourcegroup1/providers/Microsoft.AnalysisServices/servers/server1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] admin_users: List of email addresses of admin users.
        :param pulumi.Input[str] backup_blob_container_uri: URI and SAS token for a blob container to store backups.
        :param pulumi.Input[Sequence[pulumi.Input[Union['ServerIpv4FirewallRuleArgs', 'ServerIpv4FirewallRuleArgsDict']]]] ipv4_firewall_rules: One or more `ipv4_firewall_rule` block(s) as defined below.
        :param pulumi.Input[str] location: The Azure location where the Analysis Services Server exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Analysis Services Server. Only lowercase Alphanumeric characters allowed, starting with a letter. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] power_bi_service_enabled: Indicates if the Power BI service is allowed to access or not.
        :param pulumi.Input[str] querypool_connection_mode: Controls how the read-write server is used in the query pool. If this value is set to `All` then read-write servers are also used for queries. Otherwise with `ReadOnly` these servers do not participate in query operations. Defaults to `All`.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the Analysis Services Server should be exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sku: SKU for the Analysis Services Server. Possible values are: `D1`, `B1`, `B2`, `S0`, `S1`, `S2`, `S4`, `S8`, `S9`, `S8v2` and `S9v2`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an Analysis Services Server.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="analysis-services-server-test",
            location="West Europe")
        server = azure.analysisservices.Server("server",
            name="analysisservicesserver",
            location=example.location,
            resource_group_name=example.name,
            sku="S0",
            admin_users=["myuser@domain.tld"],
            power_bi_service_enabled=True,
            ipv4_firewall_rules=[{
                "name": "myRule1",
                "range_start": "210.117.252.0",
                "range_end": "210.117.252.255",
            }],
            tags={
                "abc": "123",
            })
        ```

        > **NOTE:** The server resource will automatically be started and stopped during an update if it is in `paused` state.

        ## Import

        Analysis Services Server can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:analysisservices/server:Server server /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourcegroup1/providers/Microsoft.AnalysisServices/servers/server1
        ```

        :param str resource_name: The name of the resource.
        :param ServerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin_users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 backup_blob_container_uri: Optional[pulumi.Input[str]] = None,
                 ipv4_firewall_rules: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ServerIpv4FirewallRuleArgs', 'ServerIpv4FirewallRuleArgsDict']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 power_bi_service_enabled: Optional[pulumi.Input[bool]] = None,
                 querypool_connection_mode: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServerArgs.__new__(ServerArgs)

            __props__.__dict__["admin_users"] = admin_users
            __props__.__dict__["backup_blob_container_uri"] = None if backup_blob_container_uri is None else pulumi.Output.secret(backup_blob_container_uri)
            __props__.__dict__["ipv4_firewall_rules"] = ipv4_firewall_rules
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["power_bi_service_enabled"] = power_bi_service_enabled
            __props__.__dict__["querypool_connection_mode"] = querypool_connection_mode
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if sku is None and not opts.urn:
                raise TypeError("Missing required property 'sku'")
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["server_full_name"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["backupBlobContainerUri"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Server, __self__).__init__(
            'azure:analysisservices/server:Server',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            admin_users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            backup_blob_container_uri: Optional[pulumi.Input[str]] = None,
            ipv4_firewall_rules: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ServerIpv4FirewallRuleArgs', 'ServerIpv4FirewallRuleArgsDict']]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            power_bi_service_enabled: Optional[pulumi.Input[bool]] = None,
            querypool_connection_mode: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            server_full_name: Optional[pulumi.Input[str]] = None,
            sku: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Server':
        """
        Get an existing Server resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] admin_users: List of email addresses of admin users.
        :param pulumi.Input[str] backup_blob_container_uri: URI and SAS token for a blob container to store backups.
        :param pulumi.Input[Sequence[pulumi.Input[Union['ServerIpv4FirewallRuleArgs', 'ServerIpv4FirewallRuleArgsDict']]]] ipv4_firewall_rules: One or more `ipv4_firewall_rule` block(s) as defined below.
        :param pulumi.Input[str] location: The Azure location where the Analysis Services Server exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Analysis Services Server. Only lowercase Alphanumeric characters allowed, starting with a letter. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] power_bi_service_enabled: Indicates if the Power BI service is allowed to access or not.
        :param pulumi.Input[str] querypool_connection_mode: Controls how the read-write server is used in the query pool. If this value is set to `All` then read-write servers are also used for queries. Otherwise with `ReadOnly` these servers do not participate in query operations. Defaults to `All`.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the Analysis Services Server should be exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] server_full_name: The full name of the Analysis Services Server.
        :param pulumi.Input[str] sku: SKU for the Analysis Services Server. Possible values are: `D1`, `B1`, `B2`, `S0`, `S1`, `S2`, `S4`, `S8`, `S9`, `S8v2` and `S9v2`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServerState.__new__(_ServerState)

        __props__.__dict__["admin_users"] = admin_users
        __props__.__dict__["backup_blob_container_uri"] = backup_blob_container_uri
        __props__.__dict__["ipv4_firewall_rules"] = ipv4_firewall_rules
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["power_bi_service_enabled"] = power_bi_service_enabled
        __props__.__dict__["querypool_connection_mode"] = querypool_connection_mode
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["server_full_name"] = server_full_name
        __props__.__dict__["sku"] = sku
        __props__.__dict__["tags"] = tags
        return Server(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="adminUsers")
    def admin_users(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of email addresses of admin users.
        """
        return pulumi.get(self, "admin_users")

    @property
    @pulumi.getter(name="backupBlobContainerUri")
    def backup_blob_container_uri(self) -> pulumi.Output[Optional[str]]:
        """
        URI and SAS token for a blob container to store backups.
        """
        return pulumi.get(self, "backup_blob_container_uri")

    @property
    @pulumi.getter(name="ipv4FirewallRules")
    def ipv4_firewall_rules(self) -> pulumi.Output[Optional[Sequence['outputs.ServerIpv4FirewallRule']]]:
        """
        One or more `ipv4_firewall_rule` block(s) as defined below.
        """
        return pulumi.get(self, "ipv4_firewall_rules")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure location where the Analysis Services Server exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Analysis Services Server. Only lowercase Alphanumeric characters allowed, starting with a letter. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="powerBiServiceEnabled")
    def power_bi_service_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates if the Power BI service is allowed to access or not.
        """
        return pulumi.get(self, "power_bi_service_enabled")

    @property
    @pulumi.getter(name="querypoolConnectionMode")
    def querypool_connection_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Controls how the read-write server is used in the query pool. If this value is set to `All` then read-write servers are also used for queries. Otherwise with `ReadOnly` these servers do not participate in query operations. Defaults to `All`.
        """
        return pulumi.get(self, "querypool_connection_mode")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group in which the Analysis Services Server should be exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="serverFullName")
    def server_full_name(self) -> pulumi.Output[str]:
        """
        The full name of the Analysis Services Server.
        """
        return pulumi.get(self, "server_full_name")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[str]:
        """
        SKU for the Analysis Services Server. Possible values are: `D1`, `B1`, `B2`, `S0`, `S1`, `S2`, `S4`, `S8`, `S9`, `S8v2` and `S9v2`.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

