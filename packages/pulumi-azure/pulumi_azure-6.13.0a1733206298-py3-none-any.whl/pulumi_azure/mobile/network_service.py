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

__all__ = ['NetworkServiceArgs', 'NetworkService']

@pulumi.input_type
class NetworkServiceArgs:
    def __init__(__self__, *,
                 mobile_network_id: pulumi.Input[str],
                 pcc_rules: pulumi.Input[Sequence[pulumi.Input['NetworkServicePccRuleArgs']]],
                 service_precedence: pulumi.Input[int],
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 service_qos_policy: Optional[pulumi.Input['NetworkServiceServiceQosPolicyArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a NetworkService resource.
        :param pulumi.Input[str] mobile_network_id: Specifies the ID of the Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkServicePccRuleArgs']]] pcc_rules: A `pcc_rule` block as defined below. The set of PCC Rules that make up this service.
        :param pulumi.Input[int] service_precedence: A precedence value that is used to decide between services when identifying the QoS values to use for a particular SIM. A lower value means a higher priority. This value should be unique among all services configured in the mobile network. Must be between `0` and `255`.
        :param pulumi.Input[str] location: Specifies the Azure Region where the Mobile Network Service should exist. Changing this forces a new Mobile Network Service to be created.
        :param pulumi.Input[str] name: Specifies the name which should be used for this Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        :param pulumi.Input['NetworkServiceServiceQosPolicyArgs'] service_qos_policy: A `service_qos_policy` block as defined below. The QoS policy to use for packets matching this service. This can be overridden for particular flows using the ruleQosPolicy field in a `pcc_rule`. If this field is not specified then the `sim_policy` of User Equipment (UE) will define the QoS settings.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Mobile Network Service.
        """
        pulumi.set(__self__, "mobile_network_id", mobile_network_id)
        pulumi.set(__self__, "pcc_rules", pcc_rules)
        pulumi.set(__self__, "service_precedence", service_precedence)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if service_qos_policy is not None:
            pulumi.set(__self__, "service_qos_policy", service_qos_policy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="mobileNetworkId")
    def mobile_network_id(self) -> pulumi.Input[str]:
        """
        Specifies the ID of the Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        """
        return pulumi.get(self, "mobile_network_id")

    @mobile_network_id.setter
    def mobile_network_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "mobile_network_id", value)

    @property
    @pulumi.getter(name="pccRules")
    def pcc_rules(self) -> pulumi.Input[Sequence[pulumi.Input['NetworkServicePccRuleArgs']]]:
        """
        A `pcc_rule` block as defined below. The set of PCC Rules that make up this service.
        """
        return pulumi.get(self, "pcc_rules")

    @pcc_rules.setter
    def pcc_rules(self, value: pulumi.Input[Sequence[pulumi.Input['NetworkServicePccRuleArgs']]]):
        pulumi.set(self, "pcc_rules", value)

    @property
    @pulumi.getter(name="servicePrecedence")
    def service_precedence(self) -> pulumi.Input[int]:
        """
        A precedence value that is used to decide between services when identifying the QoS values to use for a particular SIM. A lower value means a higher priority. This value should be unique among all services configured in the mobile network. Must be between `0` and `255`.
        """
        return pulumi.get(self, "service_precedence")

    @service_precedence.setter
    def service_precedence(self, value: pulumi.Input[int]):
        pulumi.set(self, "service_precedence", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Azure Region where the Mobile Network Service should exist. Changing this forces a new Mobile Network Service to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name which should be used for this Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="serviceQosPolicy")
    def service_qos_policy(self) -> Optional[pulumi.Input['NetworkServiceServiceQosPolicyArgs']]:
        """
        A `service_qos_policy` block as defined below. The QoS policy to use for packets matching this service. This can be overridden for particular flows using the ruleQosPolicy field in a `pcc_rule`. If this field is not specified then the `sim_policy` of User Equipment (UE) will define the QoS settings.
        """
        return pulumi.get(self, "service_qos_policy")

    @service_qos_policy.setter
    def service_qos_policy(self, value: Optional[pulumi.Input['NetworkServiceServiceQosPolicyArgs']]):
        pulumi.set(self, "service_qos_policy", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Mobile Network Service.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _NetworkServiceState:
    def __init__(__self__, *,
                 location: Optional[pulumi.Input[str]] = None,
                 mobile_network_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pcc_rules: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkServicePccRuleArgs']]]] = None,
                 service_precedence: Optional[pulumi.Input[int]] = None,
                 service_qos_policy: Optional[pulumi.Input['NetworkServiceServiceQosPolicyArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering NetworkService resources.
        :param pulumi.Input[str] location: Specifies the Azure Region where the Mobile Network Service should exist. Changing this forces a new Mobile Network Service to be created.
        :param pulumi.Input[str] mobile_network_id: Specifies the ID of the Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        :param pulumi.Input[str] name: Specifies the name which should be used for this Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkServicePccRuleArgs']]] pcc_rules: A `pcc_rule` block as defined below. The set of PCC Rules that make up this service.
        :param pulumi.Input[int] service_precedence: A precedence value that is used to decide between services when identifying the QoS values to use for a particular SIM. A lower value means a higher priority. This value should be unique among all services configured in the mobile network. Must be between `0` and `255`.
        :param pulumi.Input['NetworkServiceServiceQosPolicyArgs'] service_qos_policy: A `service_qos_policy` block as defined below. The QoS policy to use for packets matching this service. This can be overridden for particular flows using the ruleQosPolicy field in a `pcc_rule`. If this field is not specified then the `sim_policy` of User Equipment (UE) will define the QoS settings.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Mobile Network Service.
        """
        if location is not None:
            pulumi.set(__self__, "location", location)
        if mobile_network_id is not None:
            pulumi.set(__self__, "mobile_network_id", mobile_network_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if pcc_rules is not None:
            pulumi.set(__self__, "pcc_rules", pcc_rules)
        if service_precedence is not None:
            pulumi.set(__self__, "service_precedence", service_precedence)
        if service_qos_policy is not None:
            pulumi.set(__self__, "service_qos_policy", service_qos_policy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Azure Region where the Mobile Network Service should exist. Changing this forces a new Mobile Network Service to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="mobileNetworkId")
    def mobile_network_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of the Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        """
        return pulumi.get(self, "mobile_network_id")

    @mobile_network_id.setter
    def mobile_network_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mobile_network_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name which should be used for this Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="pccRules")
    def pcc_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkServicePccRuleArgs']]]]:
        """
        A `pcc_rule` block as defined below. The set of PCC Rules that make up this service.
        """
        return pulumi.get(self, "pcc_rules")

    @pcc_rules.setter
    def pcc_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkServicePccRuleArgs']]]]):
        pulumi.set(self, "pcc_rules", value)

    @property
    @pulumi.getter(name="servicePrecedence")
    def service_precedence(self) -> Optional[pulumi.Input[int]]:
        """
        A precedence value that is used to decide between services when identifying the QoS values to use for a particular SIM. A lower value means a higher priority. This value should be unique among all services configured in the mobile network. Must be between `0` and `255`.
        """
        return pulumi.get(self, "service_precedence")

    @service_precedence.setter
    def service_precedence(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "service_precedence", value)

    @property
    @pulumi.getter(name="serviceQosPolicy")
    def service_qos_policy(self) -> Optional[pulumi.Input['NetworkServiceServiceQosPolicyArgs']]:
        """
        A `service_qos_policy` block as defined below. The QoS policy to use for packets matching this service. This can be overridden for particular flows using the ruleQosPolicy field in a `pcc_rule`. If this field is not specified then the `sim_policy` of User Equipment (UE) will define the QoS settings.
        """
        return pulumi.get(self, "service_qos_policy")

    @service_qos_policy.setter
    def service_qos_policy(self, value: Optional[pulumi.Input['NetworkServiceServiceQosPolicyArgs']]):
        pulumi.set(self, "service_qos_policy", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Mobile Network Service.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class NetworkService(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mobile_network_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pcc_rules: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NetworkServicePccRuleArgs', 'NetworkServicePccRuleArgsDict']]]]] = None,
                 service_precedence: Optional[pulumi.Input[int]] = None,
                 service_qos_policy: Optional[pulumi.Input[Union['NetworkServiceServiceQosPolicyArgs', 'NetworkServiceServiceQosPolicyArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a Mobile Network Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="east us")
        example_network = azure.mobile.Network("example",
            name="example-mn",
            location=example.location,
            resource_group_name=example.name,
            mobile_country_code="001",
            mobile_network_code="01")
        example_network_service = azure.mobile.NetworkService("example",
            name="example-mns",
            mobile_network_id=example_network.id,
            location=example.location,
            service_precedence=0,
            pcc_rules=[{
                "name": "default-rule",
                "precedence": 1,
                "traffic_control_enabled": True,
                "qos_policy": {
                    "allocation_and_retention_priority_level": 9,
                    "qos_indicator": 9,
                    "preemption_capability": "NotPreempt",
                    "preemption_vulnerability": "Preemptable",
                    "guaranteed_bit_rate": {
                        "downlink": "100 Mbps",
                        "uplink": "10 Mbps",
                    },
                    "maximum_bit_rate": {
                        "downlink": "1 Gbps",
                        "uplink": "100 Mbps",
                    },
                },
                "service_data_flow_templates": [{
                    "direction": "Uplink",
                    "name": "IP-to-server",
                    "ports": [],
                    "protocols": ["ip"],
                    "remote_ip_lists": ["10.3.4.0/24"],
                }],
            }],
            service_qos_policy={
                "allocation_and_retention_priority_level": 9,
                "qos_indicator": 9,
                "preemption_capability": "NotPreempt",
                "preemption_vulnerability": "Preemptable",
                "maximum_bit_rate": {
                    "downlink": "1 Gbps",
                    "uplink": "100 Mbps",
                },
            },
            tags={
                "key": "value",
            })
        ```

        ## Import

        Mobile Network Service can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:mobile/networkService:NetworkService example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourceGroup1/providers/Microsoft.MobileNetwork/mobileNetworks/mobileNetwork1/services/service1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: Specifies the Azure Region where the Mobile Network Service should exist. Changing this forces a new Mobile Network Service to be created.
        :param pulumi.Input[str] mobile_network_id: Specifies the ID of the Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        :param pulumi.Input[str] name: Specifies the name which should be used for this Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        :param pulumi.Input[Sequence[pulumi.Input[Union['NetworkServicePccRuleArgs', 'NetworkServicePccRuleArgsDict']]]] pcc_rules: A `pcc_rule` block as defined below. The set of PCC Rules that make up this service.
        :param pulumi.Input[int] service_precedence: A precedence value that is used to decide between services when identifying the QoS values to use for a particular SIM. A lower value means a higher priority. This value should be unique among all services configured in the mobile network. Must be between `0` and `255`.
        :param pulumi.Input[Union['NetworkServiceServiceQosPolicyArgs', 'NetworkServiceServiceQosPolicyArgsDict']] service_qos_policy: A `service_qos_policy` block as defined below. The QoS policy to use for packets matching this service. This can be overridden for particular flows using the ruleQosPolicy field in a `pcc_rule`. If this field is not specified then the `sim_policy` of User Equipment (UE) will define the QoS settings.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Mobile Network Service.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Mobile Network Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.core.ResourceGroup("example",
            name="example-resources",
            location="east us")
        example_network = azure.mobile.Network("example",
            name="example-mn",
            location=example.location,
            resource_group_name=example.name,
            mobile_country_code="001",
            mobile_network_code="01")
        example_network_service = azure.mobile.NetworkService("example",
            name="example-mns",
            mobile_network_id=example_network.id,
            location=example.location,
            service_precedence=0,
            pcc_rules=[{
                "name": "default-rule",
                "precedence": 1,
                "traffic_control_enabled": True,
                "qos_policy": {
                    "allocation_and_retention_priority_level": 9,
                    "qos_indicator": 9,
                    "preemption_capability": "NotPreempt",
                    "preemption_vulnerability": "Preemptable",
                    "guaranteed_bit_rate": {
                        "downlink": "100 Mbps",
                        "uplink": "10 Mbps",
                    },
                    "maximum_bit_rate": {
                        "downlink": "1 Gbps",
                        "uplink": "100 Mbps",
                    },
                },
                "service_data_flow_templates": [{
                    "direction": "Uplink",
                    "name": "IP-to-server",
                    "ports": [],
                    "protocols": ["ip"],
                    "remote_ip_lists": ["10.3.4.0/24"],
                }],
            }],
            service_qos_policy={
                "allocation_and_retention_priority_level": 9,
                "qos_indicator": 9,
                "preemption_capability": "NotPreempt",
                "preemption_vulnerability": "Preemptable",
                "maximum_bit_rate": {
                    "downlink": "1 Gbps",
                    "uplink": "100 Mbps",
                },
            },
            tags={
                "key": "value",
            })
        ```

        ## Import

        Mobile Network Service can be imported using the `resource id`, e.g.

        ```sh
        $ pulumi import azure:mobile/networkService:NetworkService example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resourceGroup1/providers/Microsoft.MobileNetwork/mobileNetworks/mobileNetwork1/services/service1
        ```

        :param str resource_name: The name of the resource.
        :param NetworkServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mobile_network_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pcc_rules: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NetworkServicePccRuleArgs', 'NetworkServicePccRuleArgsDict']]]]] = None,
                 service_precedence: Optional[pulumi.Input[int]] = None,
                 service_qos_policy: Optional[pulumi.Input[Union['NetworkServiceServiceQosPolicyArgs', 'NetworkServiceServiceQosPolicyArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkServiceArgs.__new__(NetworkServiceArgs)

            __props__.__dict__["location"] = location
            if mobile_network_id is None and not opts.urn:
                raise TypeError("Missing required property 'mobile_network_id'")
            __props__.__dict__["mobile_network_id"] = mobile_network_id
            __props__.__dict__["name"] = name
            if pcc_rules is None and not opts.urn:
                raise TypeError("Missing required property 'pcc_rules'")
            __props__.__dict__["pcc_rules"] = pcc_rules
            if service_precedence is None and not opts.urn:
                raise TypeError("Missing required property 'service_precedence'")
            __props__.__dict__["service_precedence"] = service_precedence
            __props__.__dict__["service_qos_policy"] = service_qos_policy
            __props__.__dict__["tags"] = tags
        super(NetworkService, __self__).__init__(
            'azure:mobile/networkService:NetworkService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            location: Optional[pulumi.Input[str]] = None,
            mobile_network_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            pcc_rules: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NetworkServicePccRuleArgs', 'NetworkServicePccRuleArgsDict']]]]] = None,
            service_precedence: Optional[pulumi.Input[int]] = None,
            service_qos_policy: Optional[pulumi.Input[Union['NetworkServiceServiceQosPolicyArgs', 'NetworkServiceServiceQosPolicyArgsDict']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'NetworkService':
        """
        Get an existing NetworkService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: Specifies the Azure Region where the Mobile Network Service should exist. Changing this forces a new Mobile Network Service to be created.
        :param pulumi.Input[str] mobile_network_id: Specifies the ID of the Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        :param pulumi.Input[str] name: Specifies the name which should be used for this Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        :param pulumi.Input[Sequence[pulumi.Input[Union['NetworkServicePccRuleArgs', 'NetworkServicePccRuleArgsDict']]]] pcc_rules: A `pcc_rule` block as defined below. The set of PCC Rules that make up this service.
        :param pulumi.Input[int] service_precedence: A precedence value that is used to decide between services when identifying the QoS values to use for a particular SIM. A lower value means a higher priority. This value should be unique among all services configured in the mobile network. Must be between `0` and `255`.
        :param pulumi.Input[Union['NetworkServiceServiceQosPolicyArgs', 'NetworkServiceServiceQosPolicyArgsDict']] service_qos_policy: A `service_qos_policy` block as defined below. The QoS policy to use for packets matching this service. This can be overridden for particular flows using the ruleQosPolicy field in a `pcc_rule`. If this field is not specified then the `sim_policy` of User Equipment (UE) will define the QoS settings.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Mobile Network Service.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkServiceState.__new__(_NetworkServiceState)

        __props__.__dict__["location"] = location
        __props__.__dict__["mobile_network_id"] = mobile_network_id
        __props__.__dict__["name"] = name
        __props__.__dict__["pcc_rules"] = pcc_rules
        __props__.__dict__["service_precedence"] = service_precedence
        __props__.__dict__["service_qos_policy"] = service_qos_policy
        __props__.__dict__["tags"] = tags
        return NetworkService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the Azure Region where the Mobile Network Service should exist. Changing this forces a new Mobile Network Service to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="mobileNetworkId")
    def mobile_network_id(self) -> pulumi.Output[str]:
        """
        Specifies the ID of the Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        """
        return pulumi.get(self, "mobile_network_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name which should be used for this Mobile Network Service. Changing this forces a new Mobile Network Service to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pccRules")
    def pcc_rules(self) -> pulumi.Output[Sequence['outputs.NetworkServicePccRule']]:
        """
        A `pcc_rule` block as defined below. The set of PCC Rules that make up this service.
        """
        return pulumi.get(self, "pcc_rules")

    @property
    @pulumi.getter(name="servicePrecedence")
    def service_precedence(self) -> pulumi.Output[int]:
        """
        A precedence value that is used to decide between services when identifying the QoS values to use for a particular SIM. A lower value means a higher priority. This value should be unique among all services configured in the mobile network. Must be between `0` and `255`.
        """
        return pulumi.get(self, "service_precedence")

    @property
    @pulumi.getter(name="serviceQosPolicy")
    def service_qos_policy(self) -> pulumi.Output[Optional['outputs.NetworkServiceServiceQosPolicy']]:
        """
        A `service_qos_policy` block as defined below. The QoS policy to use for packets matching this service. This can be overridden for particular flows using the ruleQosPolicy field in a `pcc_rule`. If this field is not specified then the `sim_policy` of User Equipment (UE) will define the QoS settings.
        """
        return pulumi.get(self, "service_qos_policy")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to the Mobile Network Service.
        """
        return pulumi.get(self, "tags")

