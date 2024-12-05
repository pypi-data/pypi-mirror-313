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

__all__ = [
    'ProfileDnsConfigArgs',
    'ProfileDnsConfigArgsDict',
    'ProfileMonitorConfigArgs',
    'ProfileMonitorConfigArgsDict',
    'ProfileMonitorConfigCustomHeaderArgs',
    'ProfileMonitorConfigCustomHeaderArgsDict',
]

MYPY = False

if not MYPY:
    class ProfileDnsConfigArgsDict(TypedDict):
        relative_name: pulumi.Input[str]
        """
        The relative domain name, this is combined with the domain name used by Traffic Manager to form the FQDN which is exported as documented below. Changing this forces a new resource to be created.
        """
        ttl: pulumi.Input[int]
        """
        The TTL value of the Profile used by Local DNS resolvers and clients.
        """
elif False:
    ProfileDnsConfigArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ProfileDnsConfigArgs:
    def __init__(__self__, *,
                 relative_name: pulumi.Input[str],
                 ttl: pulumi.Input[int]):
        """
        :param pulumi.Input[str] relative_name: The relative domain name, this is combined with the domain name used by Traffic Manager to form the FQDN which is exported as documented below. Changing this forces a new resource to be created.
        :param pulumi.Input[int] ttl: The TTL value of the Profile used by Local DNS resolvers and clients.
        """
        pulumi.set(__self__, "relative_name", relative_name)
        pulumi.set(__self__, "ttl", ttl)

    @property
    @pulumi.getter(name="relativeName")
    def relative_name(self) -> pulumi.Input[str]:
        """
        The relative domain name, this is combined with the domain name used by Traffic Manager to form the FQDN which is exported as documented below. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "relative_name")

    @relative_name.setter
    def relative_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "relative_name", value)

    @property
    @pulumi.getter
    def ttl(self) -> pulumi.Input[int]:
        """
        The TTL value of the Profile used by Local DNS resolvers and clients.
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: pulumi.Input[int]):
        pulumi.set(self, "ttl", value)


if not MYPY:
    class ProfileMonitorConfigArgsDict(TypedDict):
        port: pulumi.Input[int]
        """
        The port number used by the monitoring checks.
        """
        protocol: pulumi.Input[str]
        """
        The protocol used by the monitoring checks, supported values are `HTTP`, `HTTPS` and `TCP`.
        """
        custom_headers: NotRequired[pulumi.Input[Sequence[pulumi.Input['ProfileMonitorConfigCustomHeaderArgsDict']]]]
        """
        One or more `custom_header` blocks as defined below.
        """
        expected_status_code_ranges: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        A list of status code ranges in the format of `100-101`.
        """
        interval_in_seconds: NotRequired[pulumi.Input[int]]
        """
        The interval used to check the endpoint health from a Traffic Manager probing agent. You can specify two values here: `30` (normal probing) and `10` (fast probing). The default value is `30`.
        """
        path: NotRequired[pulumi.Input[str]]
        """
        The path used by the monitoring checks. Required when `protocol` is set to `HTTP` or `HTTPS` - cannot be set when `protocol` is set to `TCP`.
        """
        timeout_in_seconds: NotRequired[pulumi.Input[int]]
        """
        The amount of time the Traffic Manager probing agent should wait before considering that check a failure when a health check probe is sent to the endpoint. If `interval_in_seconds` is set to `30`, then `timeout_in_seconds` can be between `5` and `10`. The default value is `10`. If `interval_in_seconds` is set to `10`, then valid values are between `5` and `9` and `timeout_in_seconds` is required.
        """
        tolerated_number_of_failures: NotRequired[pulumi.Input[int]]
        """
        The number of failures a Traffic Manager probing agent tolerates before marking that endpoint as unhealthy. Valid values are between `0` and `9`. The default value is `3`
        """
elif False:
    ProfileMonitorConfigArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ProfileMonitorConfigArgs:
    def __init__(__self__, *,
                 port: pulumi.Input[int],
                 protocol: pulumi.Input[str],
                 custom_headers: Optional[pulumi.Input[Sequence[pulumi.Input['ProfileMonitorConfigCustomHeaderArgs']]]] = None,
                 expected_status_code_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 interval_in_seconds: Optional[pulumi.Input[int]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 timeout_in_seconds: Optional[pulumi.Input[int]] = None,
                 tolerated_number_of_failures: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] port: The port number used by the monitoring checks.
        :param pulumi.Input[str] protocol: The protocol used by the monitoring checks, supported values are `HTTP`, `HTTPS` and `TCP`.
        :param pulumi.Input[Sequence[pulumi.Input['ProfileMonitorConfigCustomHeaderArgs']]] custom_headers: One or more `custom_header` blocks as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] expected_status_code_ranges: A list of status code ranges in the format of `100-101`.
        :param pulumi.Input[int] interval_in_seconds: The interval used to check the endpoint health from a Traffic Manager probing agent. You can specify two values here: `30` (normal probing) and `10` (fast probing). The default value is `30`.
        :param pulumi.Input[str] path: The path used by the monitoring checks. Required when `protocol` is set to `HTTP` or `HTTPS` - cannot be set when `protocol` is set to `TCP`.
        :param pulumi.Input[int] timeout_in_seconds: The amount of time the Traffic Manager probing agent should wait before considering that check a failure when a health check probe is sent to the endpoint. If `interval_in_seconds` is set to `30`, then `timeout_in_seconds` can be between `5` and `10`. The default value is `10`. If `interval_in_seconds` is set to `10`, then valid values are between `5` and `9` and `timeout_in_seconds` is required.
        :param pulumi.Input[int] tolerated_number_of_failures: The number of failures a Traffic Manager probing agent tolerates before marking that endpoint as unhealthy. Valid values are between `0` and `9`. The default value is `3`
        """
        pulumi.set(__self__, "port", port)
        pulumi.set(__self__, "protocol", protocol)
        if custom_headers is not None:
            pulumi.set(__self__, "custom_headers", custom_headers)
        if expected_status_code_ranges is not None:
            pulumi.set(__self__, "expected_status_code_ranges", expected_status_code_ranges)
        if interval_in_seconds is not None:
            pulumi.set(__self__, "interval_in_seconds", interval_in_seconds)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if timeout_in_seconds is not None:
            pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)
        if tolerated_number_of_failures is not None:
            pulumi.set(__self__, "tolerated_number_of_failures", tolerated_number_of_failures)

    @property
    @pulumi.getter
    def port(self) -> pulumi.Input[int]:
        """
        The port number used by the monitoring checks.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: pulumi.Input[int]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Input[str]:
        """
        The protocol used by the monitoring checks, supported values are `HTTP`, `HTTPS` and `TCP`.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: pulumi.Input[str]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="customHeaders")
    def custom_headers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ProfileMonitorConfigCustomHeaderArgs']]]]:
        """
        One or more `custom_header` blocks as defined below.
        """
        return pulumi.get(self, "custom_headers")

    @custom_headers.setter
    def custom_headers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ProfileMonitorConfigCustomHeaderArgs']]]]):
        pulumi.set(self, "custom_headers", value)

    @property
    @pulumi.getter(name="expectedStatusCodeRanges")
    def expected_status_code_ranges(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of status code ranges in the format of `100-101`.
        """
        return pulumi.get(self, "expected_status_code_ranges")

    @expected_status_code_ranges.setter
    def expected_status_code_ranges(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "expected_status_code_ranges", value)

    @property
    @pulumi.getter(name="intervalInSeconds")
    def interval_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        The interval used to check the endpoint health from a Traffic Manager probing agent. You can specify two values here: `30` (normal probing) and `10` (fast probing). The default value is `30`.
        """
        return pulumi.get(self, "interval_in_seconds")

    @interval_in_seconds.setter
    def interval_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "interval_in_seconds", value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        """
        The path used by the monitoring checks. Required when `protocol` is set to `HTTP` or `HTTPS` - cannot be set when `protocol` is set to `TCP`.
        """
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path", value)

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        The amount of time the Traffic Manager probing agent should wait before considering that check a failure when a health check probe is sent to the endpoint. If `interval_in_seconds` is set to `30`, then `timeout_in_seconds` can be between `5` and `10`. The default value is `10`. If `interval_in_seconds` is set to `10`, then valid values are between `5` and `9` and `timeout_in_seconds` is required.
        """
        return pulumi.get(self, "timeout_in_seconds")

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout_in_seconds", value)

    @property
    @pulumi.getter(name="toleratedNumberOfFailures")
    def tolerated_number_of_failures(self) -> Optional[pulumi.Input[int]]:
        """
        The number of failures a Traffic Manager probing agent tolerates before marking that endpoint as unhealthy. Valid values are between `0` and `9`. The default value is `3`
        """
        return pulumi.get(self, "tolerated_number_of_failures")

    @tolerated_number_of_failures.setter
    def tolerated_number_of_failures(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "tolerated_number_of_failures", value)


if not MYPY:
    class ProfileMonitorConfigCustomHeaderArgsDict(TypedDict):
        name: pulumi.Input[str]
        """
        The name of the custom header.
        """
        value: pulumi.Input[str]
        """
        The value of custom header. Applicable for HTTP and HTTPS protocol.
        """
elif False:
    ProfileMonitorConfigCustomHeaderArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ProfileMonitorConfigCustomHeaderArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] name: The name of the custom header.
        :param pulumi.Input[str] value: The value of custom header. Applicable for HTTP and HTTPS protocol.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the custom header.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of custom header. Applicable for HTTP and HTTPS protocol.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


