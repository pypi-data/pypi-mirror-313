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

__all__ = ['NetworkManagerDeploymentArgs', 'NetworkManagerDeployment']

@pulumi.input_type
class NetworkManagerDeploymentArgs:
    def __init__(__self__, *,
                 configuration_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 network_manager_id: pulumi.Input[str],
                 scope_access: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a NetworkManagerDeployment resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] configuration_ids: A list of Network Manager Configuration IDs which should be aligned with `scope_access`.
        :param pulumi.Input[str] network_manager_id: Specifies the ID of the Network Manager. Changing this forces a new Network Manager Deployment to be created.
        :param pulumi.Input[str] scope_access: Specifies the configuration deployment type. Possible values are `Connectivity` and `SecurityAdmin`. Changing this forces a new Network Manager Deployment to be created.
        :param pulumi.Input[str] location: Specifies the location which the configurations will be deployed to. Changing this forces a new Network Manager Deployment to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: A mapping of key values pairs that can be used to keep the deployment up with the Network Manager configurations and rules.
        """
        pulumi.set(__self__, "configuration_ids", configuration_ids)
        pulumi.set(__self__, "network_manager_id", network_manager_id)
        pulumi.set(__self__, "scope_access", scope_access)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if triggers is not None:
            pulumi.set(__self__, "triggers", triggers)

    @property
    @pulumi.getter(name="configurationIds")
    def configuration_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of Network Manager Configuration IDs which should be aligned with `scope_access`.
        """
        return pulumi.get(self, "configuration_ids")

    @configuration_ids.setter
    def configuration_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "configuration_ids", value)

    @property
    @pulumi.getter(name="networkManagerId")
    def network_manager_id(self) -> pulumi.Input[str]:
        """
        Specifies the ID of the Network Manager. Changing this forces a new Network Manager Deployment to be created.
        """
        return pulumi.get(self, "network_manager_id")

    @network_manager_id.setter
    def network_manager_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "network_manager_id", value)

    @property
    @pulumi.getter(name="scopeAccess")
    def scope_access(self) -> pulumi.Input[str]:
        """
        Specifies the configuration deployment type. Possible values are `Connectivity` and `SecurityAdmin`. Changing this forces a new Network Manager Deployment to be created.
        """
        return pulumi.get(self, "scope_access")

    @scope_access.setter
    def scope_access(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope_access", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the location which the configurations will be deployed to. Changing this forces a new Network Manager Deployment to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def triggers(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of key values pairs that can be used to keep the deployment up with the Network Manager configurations and rules.
        """
        return pulumi.get(self, "triggers")

    @triggers.setter
    def triggers(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "triggers", value)


@pulumi.input_type
class _NetworkManagerDeploymentState:
    def __init__(__self__, *,
                 configuration_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_manager_id: Optional[pulumi.Input[str]] = None,
                 scope_access: Optional[pulumi.Input[str]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering NetworkManagerDeployment resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] configuration_ids: A list of Network Manager Configuration IDs which should be aligned with `scope_access`.
        :param pulumi.Input[str] location: Specifies the location which the configurations will be deployed to. Changing this forces a new Network Manager Deployment to be created.
        :param pulumi.Input[str] network_manager_id: Specifies the ID of the Network Manager. Changing this forces a new Network Manager Deployment to be created.
        :param pulumi.Input[str] scope_access: Specifies the configuration deployment type. Possible values are `Connectivity` and `SecurityAdmin`. Changing this forces a new Network Manager Deployment to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: A mapping of key values pairs that can be used to keep the deployment up with the Network Manager configurations and rules.
        """
        if configuration_ids is not None:
            pulumi.set(__self__, "configuration_ids", configuration_ids)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if network_manager_id is not None:
            pulumi.set(__self__, "network_manager_id", network_manager_id)
        if scope_access is not None:
            pulumi.set(__self__, "scope_access", scope_access)
        if triggers is not None:
            pulumi.set(__self__, "triggers", triggers)

    @property
    @pulumi.getter(name="configurationIds")
    def configuration_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of Network Manager Configuration IDs which should be aligned with `scope_access`.
        """
        return pulumi.get(self, "configuration_ids")

    @configuration_ids.setter
    def configuration_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "configuration_ids", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the location which the configurations will be deployed to. Changing this forces a new Network Manager Deployment to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="networkManagerId")
    def network_manager_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of the Network Manager. Changing this forces a new Network Manager Deployment to be created.
        """
        return pulumi.get(self, "network_manager_id")

    @network_manager_id.setter
    def network_manager_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_manager_id", value)

    @property
    @pulumi.getter(name="scopeAccess")
    def scope_access(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the configuration deployment type. Possible values are `Connectivity` and `SecurityAdmin`. Changing this forces a new Network Manager Deployment to be created.
        """
        return pulumi.get(self, "scope_access")

    @scope_access.setter
    def scope_access(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scope_access", value)

    @property
    @pulumi.getter
    def triggers(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of key values pairs that can be used to keep the deployment up with the Network Manager configurations and rules.
        """
        return pulumi.get(self, "triggers")

    @triggers.setter
    def triggers(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "triggers", value)


class NetworkManagerDeployment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_manager_id: Optional[pulumi.Input[str]] = None,
                 scope_access: Optional[pulumi.Input[str]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a Network Manager Deployment.

        > **NOTE on Virtual Network Peering:** Using Network Manager Deployment to deploy Connectivity Configuration may modify or delete existing Virtual Network Peering. At this time you should not use Network Peering resource in conjunction with Network Manager Deployment. Doing so may cause a conflict of Peering configurations.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        current = azure.core.get_subscription()
        example_network_manager = azure.network.NetworkManager("example",
            name="example-network-manager",
            location=example.location,
            resource_group_name=example.name,
            scope={
                "subscription_ids": [current.id],
            },
            scope_accesses=[
                "Connectivity",
                "SecurityAdmin",
            ],
            description="example network manager")
        example_network_manager_network_group = azure.network.NetworkManagerNetworkGroup("example",
            name="example-group",
            network_manager_id=example_network_manager.id)
        example_virtual_network = azure.network.VirtualNetwork("example",
            name="example-net",
            location=example.location,
            resource_group_name=example.name,
            address_spaces=["10.0.0.0/16"],
            flow_timeout_in_minutes=10)
        example_network_manager_connectivity_configuration = azure.network.NetworkManagerConnectivityConfiguration("example",
            name="example-connectivity-conf",
            network_manager_id=example_network_manager.id,
            connectivity_topology="HubAndSpoke",
            applies_to_groups=[{
                "group_connectivity": "None",
                "network_group_id": example_network_manager_network_group.id,
            }],
            hub={
                "resource_id": example_virtual_network.id,
                "resource_type": "Microsoft.Network/virtualNetworks",
            })
        example_network_manager_deployment = azure.network.NetworkManagerDeployment("example",
            network_manager_id=example_network_manager.id,
            location="eastus",
            scope_access="Connectivity",
            configuration_ids=[example_network_manager_connectivity_configuration.id])
        ```

        ### Triggers)

        ```python
        import pulumi
        import pulumi_azure as azure
        import pulumi_std as std

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        current = azure.core.get_subscription()
        example_network_manager = azure.network.NetworkManager("example",
            name="example-network-manager",
            location=example.location,
            resource_group_name=example.name,
            scope={
                "subscription_ids": [current.id],
            },
            scope_accesses=[
                "Connectivity",
                "SecurityAdmin",
            ],
            description="example network manager")
        example_network_manager_network_group = azure.network.NetworkManagerNetworkGroup("example",
            name="example-group",
            network_manager_id=example_network_manager.id)
        example_virtual_network = azure.network.VirtualNetwork("example",
            name="example-net",
            location=example.location,
            resource_group_name=example.name,
            address_spaces=["10.0.0.0/16"],
            flow_timeout_in_minutes=10)
        example_network_manager_security_admin_configuration = azure.network.NetworkManagerSecurityAdminConfiguration("example",
            name="example-nmsac",
            network_manager_id=example_network_manager.id)
        example_network_manager_admin_rule_collection = azure.network.NetworkManagerAdminRuleCollection("example",
            name="example-nmarc",
            security_admin_configuration_id=example_network_manager_security_admin_configuration.id,
            network_group_ids=[example_network_manager_network_group.id])
        example_network_manager_admin_rule = azure.network.NetworkManagerAdminRule("example",
            name="example-nmar",
            admin_rule_collection_id=example_network_manager_admin_rule_collection.id,
            action="Deny",
            description="example",
            direction="Inbound",
            priority=1,
            protocol="Tcp",
            source_port_ranges=["80"],
            destination_port_ranges=["80"],
            sources=[{
                "address_prefix_type": "ServiceTag",
                "address_prefix": "Internet",
            }],
            destinations=[{
                "address_prefix_type": "IPPrefix",
                "address_prefix": "*",
            }])
        example_network_manager_deployment = azure.network.NetworkManagerDeployment("example",
            network_manager_id=example_network_manager.id,
            location="eastus",
            scope_access="SecurityAdmin",
            configuration_ids=[example_network_manager_security_admin_configuration.id],
            triggers={
                "source_port_ranges": example_network_manager_admin_rule.source_port_ranges.apply(lambda source_port_ranges: std.join_output(separator=",",
                    input=source_port_ranges)).apply(lambda invoke: invoke.result),
            },
            opts = pulumi.ResourceOptions(depends_on=[example_network_manager_admin_rule]))
        ```

        ## Import

        Network Manager Deployment can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:network/networkManagerDeployment:NetworkManagerDeployment example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourceGroup1/providers/Microsoft.Network/networkManagers/networkManager1/commit|eastus|Connectivity
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] configuration_ids: A list of Network Manager Configuration IDs which should be aligned with `scope_access`.
        :param pulumi.Input[str] location: Specifies the location which the configurations will be deployed to. Changing this forces a new Network Manager Deployment to be created.
        :param pulumi.Input[str] network_manager_id: Specifies the ID of the Network Manager. Changing this forces a new Network Manager Deployment to be created.
        :param pulumi.Input[str] scope_access: Specifies the configuration deployment type. Possible values are `Connectivity` and `SecurityAdmin`. Changing this forces a new Network Manager Deployment to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: A mapping of key values pairs that can be used to keep the deployment up with the Network Manager configurations and rules.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkManagerDeploymentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Network Manager Deployment.

        > **NOTE on Virtual Network Peering:** Using Network Manager Deployment to deploy Connectivity Configuration may modify or delete existing Virtual Network Peering. At this time you should not use Network Peering resource in conjunction with Network Manager Deployment. Doing so may cause a conflict of Peering configurations.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        current = azure.core.get_subscription()
        example_network_manager = azure.network.NetworkManager("example",
            name="example-network-manager",
            location=example.location,
            resource_group_name=example.name,
            scope={
                "subscription_ids": [current.id],
            },
            scope_accesses=[
                "Connectivity",
                "SecurityAdmin",
            ],
            description="example network manager")
        example_network_manager_network_group = azure.network.NetworkManagerNetworkGroup("example",
            name="example-group",
            network_manager_id=example_network_manager.id)
        example_virtual_network = azure.network.VirtualNetwork("example",
            name="example-net",
            location=example.location,
            resource_group_name=example.name,
            address_spaces=["10.0.0.0/16"],
            flow_timeout_in_minutes=10)
        example_network_manager_connectivity_configuration = azure.network.NetworkManagerConnectivityConfiguration("example",
            name="example-connectivity-conf",
            network_manager_id=example_network_manager.id,
            connectivity_topology="HubAndSpoke",
            applies_to_groups=[{
                "group_connectivity": "None",
                "network_group_id": example_network_manager_network_group.id,
            }],
            hub={
                "resource_id": example_virtual_network.id,
                "resource_type": "Microsoft.Network/virtualNetworks",
            })
        example_network_manager_deployment = azure.network.NetworkManagerDeployment("example",
            network_manager_id=example_network_manager.id,
            location="eastus",
            scope_access="Connectivity",
            configuration_ids=[example_network_manager_connectivity_configuration.id])
        ```

        ### Triggers)

        ```python
        import pulumi
        import pulumi_azure as azure
        import pulumi_std as std

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="West Europe")
        current = azure.core.get_subscription()
        example_network_manager = azure.network.NetworkManager("example",
            name="example-network-manager",
            location=example.location,
            resource_group_name=example.name,
            scope={
                "subscription_ids": [current.id],
            },
            scope_accesses=[
                "Connectivity",
                "SecurityAdmin",
            ],
            description="example network manager")
        example_network_manager_network_group = azure.network.NetworkManagerNetworkGroup("example",
            name="example-group",
            network_manager_id=example_network_manager.id)
        example_virtual_network = azure.network.VirtualNetwork("example",
            name="example-net",
            location=example.location,
            resource_group_name=example.name,
            address_spaces=["10.0.0.0/16"],
            flow_timeout_in_minutes=10)
        example_network_manager_security_admin_configuration = azure.network.NetworkManagerSecurityAdminConfiguration("example",
            name="example-nmsac",
            network_manager_id=example_network_manager.id)
        example_network_manager_admin_rule_collection = azure.network.NetworkManagerAdminRuleCollection("example",
            name="example-nmarc",
            security_admin_configuration_id=example_network_manager_security_admin_configuration.id,
            network_group_ids=[example_network_manager_network_group.id])
        example_network_manager_admin_rule = azure.network.NetworkManagerAdminRule("example",
            name="example-nmar",
            admin_rule_collection_id=example_network_manager_admin_rule_collection.id,
            action="Deny",
            description="example",
            direction="Inbound",
            priority=1,
            protocol="Tcp",
            source_port_ranges=["80"],
            destination_port_ranges=["80"],
            sources=[{
                "address_prefix_type": "ServiceTag",
                "address_prefix": "Internet",
            }],
            destinations=[{
                "address_prefix_type": "IPPrefix",
                "address_prefix": "*",
            }])
        example_network_manager_deployment = azure.network.NetworkManagerDeployment("example",
            network_manager_id=example_network_manager.id,
            location="eastus",
            scope_access="SecurityAdmin",
            configuration_ids=[example_network_manager_security_admin_configuration.id],
            triggers={
                "source_port_ranges": example_network_manager_admin_rule.source_port_ranges.apply(lambda source_port_ranges: std.join_output(separator=",",
                    input=source_port_ranges)).apply(lambda invoke: invoke.result),
            },
            opts = pulumi.ResourceOptions(depends_on=[example_network_manager_admin_rule]))
        ```

        ## Import

        Network Manager Deployment can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:network/networkManagerDeployment:NetworkManagerDeployment example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourceGroup1/providers/Microsoft.Network/networkManagers/networkManager1/commit|eastus|Connectivity
        ```

        :param str resource_name: The name of the resource.
        :param NetworkManagerDeploymentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkManagerDeploymentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_manager_id: Optional[pulumi.Input[str]] = None,
                 scope_access: Optional[pulumi.Input[str]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkManagerDeploymentArgs.__new__(NetworkManagerDeploymentArgs)

            if configuration_ids is None and not opts.urn:
                raise TypeError("Missing required property 'configuration_ids'")
            __props__.__dict__["configuration_ids"] = configuration_ids
            __props__.__dict__["location"] = location
            if network_manager_id is None and not opts.urn:
                raise TypeError("Missing required property 'network_manager_id'")
            __props__.__dict__["network_manager_id"] = network_manager_id
            if scope_access is None and not opts.urn:
                raise TypeError("Missing required property 'scope_access'")
            __props__.__dict__["scope_access"] = scope_access
            __props__.__dict__["triggers"] = triggers
        super(NetworkManagerDeployment, __self__).__init__(
            'azure:network/networkManagerDeployment:NetworkManagerDeployment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            configuration_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            network_manager_id: Optional[pulumi.Input[str]] = None,
            scope_access: Optional[pulumi.Input[str]] = None,
            triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'NetworkManagerDeployment':
        """
        Get an existing NetworkManagerDeployment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] configuration_ids: A list of Network Manager Configuration IDs which should be aligned with `scope_access`.
        :param pulumi.Input[str] location: Specifies the location which the configurations will be deployed to. Changing this forces a new Network Manager Deployment to be created.
        :param pulumi.Input[str] network_manager_id: Specifies the ID of the Network Manager. Changing this forces a new Network Manager Deployment to be created.
        :param pulumi.Input[str] scope_access: Specifies the configuration deployment type. Possible values are `Connectivity` and `SecurityAdmin`. Changing this forces a new Network Manager Deployment to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: A mapping of key values pairs that can be used to keep the deployment up with the Network Manager configurations and rules.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkManagerDeploymentState.__new__(_NetworkManagerDeploymentState)

        __props__.__dict__["configuration_ids"] = configuration_ids
        __props__.__dict__["location"] = location
        __props__.__dict__["network_manager_id"] = network_manager_id
        __props__.__dict__["scope_access"] = scope_access
        __props__.__dict__["triggers"] = triggers
        return NetworkManagerDeployment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="configurationIds")
    def configuration_ids(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of Network Manager Configuration IDs which should be aligned with `scope_access`.
        """
        return pulumi.get(self, "configuration_ids")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the location which the configurations will be deployed to. Changing this forces a new Network Manager Deployment to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="networkManagerId")
    def network_manager_id(self) -> pulumi.Output[str]:
        """
        Specifies the ID of the Network Manager. Changing this forces a new Network Manager Deployment to be created.
        """
        return pulumi.get(self, "network_manager_id")

    @property
    @pulumi.getter(name="scopeAccess")
    def scope_access(self) -> pulumi.Output[str]:
        """
        Specifies the configuration deployment type. Possible values are `Connectivity` and `SecurityAdmin`. Changing this forces a new Network Manager Deployment to be created.
        """
        return pulumi.get(self, "scope_access")

    @property
    @pulumi.getter
    def triggers(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of key values pairs that can be used to keep the deployment up with the Network Manager configurations and rules.
        """
        return pulumi.get(self, "triggers")

