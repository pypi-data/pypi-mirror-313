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
    'ServiceCorArgs',
    'ServiceCorArgsDict',
    'ServiceIdentityArgs',
    'ServiceIdentityArgsDict',
    'ServiceLiveTraceArgs',
    'ServiceLiveTraceArgsDict',
    'ServiceNetworkAclPrivateEndpointArgs',
    'ServiceNetworkAclPrivateEndpointArgsDict',
    'ServiceNetworkAclPublicNetworkArgs',
    'ServiceNetworkAclPublicNetworkArgsDict',
    'ServiceSkuArgs',
    'ServiceSkuArgsDict',
    'ServiceUpstreamEndpointArgs',
    'ServiceUpstreamEndpointArgsDict',
]

MYPY = False

if not MYPY:
    class ServiceCorArgsDict(TypedDict):
        allowed_origins: pulumi.Input[Sequence[pulumi.Input[str]]]
        """
        A list of origins which should be able to make cross-origin calls. `*` can be used to allow all calls.
        """
elif False:
    ServiceCorArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ServiceCorArgs:
    def __init__(__self__, *,
                 allowed_origins: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_origins: A list of origins which should be able to make cross-origin calls. `*` can be used to allow all calls.
        """
        pulumi.set(__self__, "allowed_origins", allowed_origins)

    @property
    @pulumi.getter(name="allowedOrigins")
    def allowed_origins(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of origins which should be able to make cross-origin calls. `*` can be used to allow all calls.
        """
        return pulumi.get(self, "allowed_origins")

    @allowed_origins.setter
    def allowed_origins(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "allowed_origins", value)


if not MYPY:
    class ServiceIdentityArgsDict(TypedDict):
        type: pulumi.Input[str]
        """
        Specifies the type of Managed Service Identity that should be configured on this signalR. Possible values are `SystemAssigned`, `UserAssigned`.
        """
        identity_ids: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        Specifies a list of User Assigned Managed Identity IDs to be assigned to this signalR.

        > **NOTE:** This is required when `type` is set to `UserAssigned`
        """
        principal_id: NotRequired[pulumi.Input[str]]
        tenant_id: NotRequired[pulumi.Input[str]]
elif False:
    ServiceIdentityArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ServiceIdentityArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 identity_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] type: Specifies the type of Managed Service Identity that should be configured on this signalR. Possible values are `SystemAssigned`, `UserAssigned`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] identity_ids: Specifies a list of User Assigned Managed Identity IDs to be assigned to this signalR.
               
               > **NOTE:** This is required when `type` is set to `UserAssigned`
        """
        pulumi.set(__self__, "type", type)
        if identity_ids is not None:
            pulumi.set(__self__, "identity_ids", identity_ids)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Specifies the type of Managed Service Identity that should be configured on this signalR. Possible values are `SystemAssigned`, `UserAssigned`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="identityIds")
    def identity_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies a list of User Assigned Managed Identity IDs to be assigned to this signalR.

        > **NOTE:** This is required when `type` is set to `UserAssigned`
        """
        return pulumi.get(self, "identity_ids")

    @identity_ids.setter
    def identity_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "identity_ids", value)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)


if not MYPY:
    class ServiceLiveTraceArgsDict(TypedDict):
        connectivity_logs_enabled: NotRequired[pulumi.Input[bool]]
        """
        Whether the log category `ConnectivityLogs` is enabled? Defaults to `true`
        """
        enabled: NotRequired[pulumi.Input[bool]]
        """
        Whether the live trace is enabled? Defaults to `true`.
        """
        http_request_logs_enabled: NotRequired[pulumi.Input[bool]]
        """
        Whether the log category `HttpRequestLogs` is enabled? Defaults to `true`
        """
        messaging_logs_enabled: NotRequired[pulumi.Input[bool]]
        """
        Whether the log category `MessagingLogs` is enabled? Defaults to `true`
        """
elif False:
    ServiceLiveTraceArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ServiceLiveTraceArgs:
    def __init__(__self__, *,
                 connectivity_logs_enabled: Optional[pulumi.Input[bool]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 http_request_logs_enabled: Optional[pulumi.Input[bool]] = None,
                 messaging_logs_enabled: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[bool] connectivity_logs_enabled: Whether the log category `ConnectivityLogs` is enabled? Defaults to `true`
        :param pulumi.Input[bool] enabled: Whether the live trace is enabled? Defaults to `true`.
        :param pulumi.Input[bool] http_request_logs_enabled: Whether the log category `HttpRequestLogs` is enabled? Defaults to `true`
        :param pulumi.Input[bool] messaging_logs_enabled: Whether the log category `MessagingLogs` is enabled? Defaults to `true`
        """
        if connectivity_logs_enabled is not None:
            pulumi.set(__self__, "connectivity_logs_enabled", connectivity_logs_enabled)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if http_request_logs_enabled is not None:
            pulumi.set(__self__, "http_request_logs_enabled", http_request_logs_enabled)
        if messaging_logs_enabled is not None:
            pulumi.set(__self__, "messaging_logs_enabled", messaging_logs_enabled)

    @property
    @pulumi.getter(name="connectivityLogsEnabled")
    def connectivity_logs_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the log category `ConnectivityLogs` is enabled? Defaults to `true`
        """
        return pulumi.get(self, "connectivity_logs_enabled")

    @connectivity_logs_enabled.setter
    def connectivity_logs_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "connectivity_logs_enabled", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the live trace is enabled? Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="httpRequestLogsEnabled")
    def http_request_logs_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the log category `HttpRequestLogs` is enabled? Defaults to `true`
        """
        return pulumi.get(self, "http_request_logs_enabled")

    @http_request_logs_enabled.setter
    def http_request_logs_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "http_request_logs_enabled", value)

    @property
    @pulumi.getter(name="messagingLogsEnabled")
    def messaging_logs_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the log category `MessagingLogs` is enabled? Defaults to `true`
        """
        return pulumi.get(self, "messaging_logs_enabled")

    @messaging_logs_enabled.setter
    def messaging_logs_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "messaging_logs_enabled", value)


if not MYPY:
    class ServiceNetworkAclPrivateEndpointArgsDict(TypedDict):
        id: pulumi.Input[str]
        """
        The ID of the Private Endpoint which is based on the SignalR service.
        """
        allowed_request_types: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        The allowed request types for the Private Endpoint Connection. Possible values are `ClientConnection`, `ServerConnection`, `RESTAPI` and `Trace`.

        > **Note:** When `default_action` is `Allow`, `allowed_request_types`cannot be set.
        """
        denied_request_types: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        The denied request types for the Private Endpoint Connection. Possible values are `ClientConnection`, `ServerConnection`, `RESTAPI` and `Trace`.

        > **Note:** When `default_action` is `Deny`, `denied_request_types`cannot be set.

        > **Note:** `allowed_request_types` - (Optional) and `denied_request_types` cannot be set together.
        """
elif False:
    ServiceNetworkAclPrivateEndpointArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ServiceNetworkAclPrivateEndpointArgs:
    def __init__(__self__, *,
                 id: pulumi.Input[str],
                 allowed_request_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 denied_request_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] id: The ID of the Private Endpoint which is based on the SignalR service.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_request_types: The allowed request types for the Private Endpoint Connection. Possible values are `ClientConnection`, `ServerConnection`, `RESTAPI` and `Trace`.
               
               > **Note:** When `default_action` is `Allow`, `allowed_request_types`cannot be set.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] denied_request_types: The denied request types for the Private Endpoint Connection. Possible values are `ClientConnection`, `ServerConnection`, `RESTAPI` and `Trace`.
               
               > **Note:** When `default_action` is `Deny`, `denied_request_types`cannot be set.
               
               > **Note:** `allowed_request_types` - (Optional) and `denied_request_types` cannot be set together.
        """
        pulumi.set(__self__, "id", id)
        if allowed_request_types is not None:
            pulumi.set(__self__, "allowed_request_types", allowed_request_types)
        if denied_request_types is not None:
            pulumi.set(__self__, "denied_request_types", denied_request_types)

    @property
    @pulumi.getter
    def id(self) -> pulumi.Input[str]:
        """
        The ID of the Private Endpoint which is based on the SignalR service.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: pulumi.Input[str]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter(name="allowedRequestTypes")
    def allowed_request_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The allowed request types for the Private Endpoint Connection. Possible values are `ClientConnection`, `ServerConnection`, `RESTAPI` and `Trace`.

        > **Note:** When `default_action` is `Allow`, `allowed_request_types`cannot be set.
        """
        return pulumi.get(self, "allowed_request_types")

    @allowed_request_types.setter
    def allowed_request_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allowed_request_types", value)

    @property
    @pulumi.getter(name="deniedRequestTypes")
    def denied_request_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The denied request types for the Private Endpoint Connection. Possible values are `ClientConnection`, `ServerConnection`, `RESTAPI` and `Trace`.

        > **Note:** When `default_action` is `Deny`, `denied_request_types`cannot be set.

        > **Note:** `allowed_request_types` - (Optional) and `denied_request_types` cannot be set together.
        """
        return pulumi.get(self, "denied_request_types")

    @denied_request_types.setter
    def denied_request_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "denied_request_types", value)


if not MYPY:
    class ServiceNetworkAclPublicNetworkArgsDict(TypedDict):
        allowed_request_types: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        The allowed request types for the public network. Possible values are `ClientConnection`, `ServerConnection`, `RESTAPI` and `Trace`.

        > **Note:** When `default_action` is `Allow`, `allowed_request_types`cannot be set.
        """
        denied_request_types: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        The denied request types for the public network. Possible values are `ClientConnection`, `ServerConnection`, `RESTAPI` and `Trace`.

        > **Note:** When `default_action` is `Deny`, `denied_request_types`cannot be set.

        > **Note:** `allowed_request_types` - (Optional) and `denied_request_types` cannot be set together.
        """
elif False:
    ServiceNetworkAclPublicNetworkArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ServiceNetworkAclPublicNetworkArgs:
    def __init__(__self__, *,
                 allowed_request_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 denied_request_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_request_types: The allowed request types for the public network. Possible values are `ClientConnection`, `ServerConnection`, `RESTAPI` and `Trace`.
               
               > **Note:** When `default_action` is `Allow`, `allowed_request_types`cannot be set.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] denied_request_types: The denied request types for the public network. Possible values are `ClientConnection`, `ServerConnection`, `RESTAPI` and `Trace`.
               
               > **Note:** When `default_action` is `Deny`, `denied_request_types`cannot be set.
               
               > **Note:** `allowed_request_types` - (Optional) and `denied_request_types` cannot be set together.
        """
        if allowed_request_types is not None:
            pulumi.set(__self__, "allowed_request_types", allowed_request_types)
        if denied_request_types is not None:
            pulumi.set(__self__, "denied_request_types", denied_request_types)

    @property
    @pulumi.getter(name="allowedRequestTypes")
    def allowed_request_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The allowed request types for the public network. Possible values are `ClientConnection`, `ServerConnection`, `RESTAPI` and `Trace`.

        > **Note:** When `default_action` is `Allow`, `allowed_request_types`cannot be set.
        """
        return pulumi.get(self, "allowed_request_types")

    @allowed_request_types.setter
    def allowed_request_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allowed_request_types", value)

    @property
    @pulumi.getter(name="deniedRequestTypes")
    def denied_request_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The denied request types for the public network. Possible values are `ClientConnection`, `ServerConnection`, `RESTAPI` and `Trace`.

        > **Note:** When `default_action` is `Deny`, `denied_request_types`cannot be set.

        > **Note:** `allowed_request_types` - (Optional) and `denied_request_types` cannot be set together.
        """
        return pulumi.get(self, "denied_request_types")

    @denied_request_types.setter
    def denied_request_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "denied_request_types", value)


if not MYPY:
    class ServiceSkuArgsDict(TypedDict):
        capacity: pulumi.Input[int]
        """
        Specifies the number of units associated with this SignalR service. Valid values are `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `20`, `30`, `40`, `50`, `60`, `70`, `80`, `90`, `100`, `200`, `300`, `400`, `500`, `600`, `700`, `800`, `900` and `1000`.

        > **NOTE:** The valid capacity range for sku `Free_F1` is `1`, for sku `Premium_P2` is from `100` to `1000`, and from `1` to `100` for sku `Standard_S1` and `Premium_P1`.
        """
        name: pulumi.Input[str]
        """
        Specifies which tier to use. Valid values are `Free_F1`, `Standard_S1`, `Premium_P1` and `Premium_P2`.
        """
elif False:
    ServiceSkuArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ServiceSkuArgs:
    def __init__(__self__, *,
                 capacity: pulumi.Input[int],
                 name: pulumi.Input[str]):
        """
        :param pulumi.Input[int] capacity: Specifies the number of units associated with this SignalR service. Valid values are `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `20`, `30`, `40`, `50`, `60`, `70`, `80`, `90`, `100`, `200`, `300`, `400`, `500`, `600`, `700`, `800`, `900` and `1000`.
               
               > **NOTE:** The valid capacity range for sku `Free_F1` is `1`, for sku `Premium_P2` is from `100` to `1000`, and from `1` to `100` for sku `Standard_S1` and `Premium_P1`.
        :param pulumi.Input[str] name: Specifies which tier to use. Valid values are `Free_F1`, `Standard_S1`, `Premium_P1` and `Premium_P2`.
        """
        pulumi.set(__self__, "capacity", capacity)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def capacity(self) -> pulumi.Input[int]:
        """
        Specifies the number of units associated with this SignalR service. Valid values are `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `20`, `30`, `40`, `50`, `60`, `70`, `80`, `90`, `100`, `200`, `300`, `400`, `500`, `600`, `700`, `800`, `900` and `1000`.

        > **NOTE:** The valid capacity range for sku `Free_F1` is `1`, for sku `Premium_P2` is from `100` to `1000`, and from `1` to `100` for sku `Standard_S1` and `Premium_P1`.
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: pulumi.Input[int]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Specifies which tier to use. Valid values are `Free_F1`, `Standard_S1`, `Premium_P1` and `Premium_P2`.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)


if not MYPY:
    class ServiceUpstreamEndpointArgsDict(TypedDict):
        category_patterns: pulumi.Input[Sequence[pulumi.Input[str]]]
        """
        The categories to match on, or `*` for all.
        """
        event_patterns: pulumi.Input[Sequence[pulumi.Input[str]]]
        """
        The events to match on, or `*` for all.
        """
        hub_patterns: pulumi.Input[Sequence[pulumi.Input[str]]]
        """
        The hubs to match on, or `*` for all.
        """
        url_template: pulumi.Input[str]
        """
        The upstream URL Template. This can be a url or a template such as `http://host.com/{hub}/api/{category}/{event}`.
        """
        user_assigned_identity_id: NotRequired[pulumi.Input[str]]
        """
        Specifies the Managed Identity IDs to be assigned to this signalR upstream setting by using resource uuid as both system assigned and user assigned identity is supported.
        """
elif False:
    ServiceUpstreamEndpointArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ServiceUpstreamEndpointArgs:
    def __init__(__self__, *,
                 category_patterns: pulumi.Input[Sequence[pulumi.Input[str]]],
                 event_patterns: pulumi.Input[Sequence[pulumi.Input[str]]],
                 hub_patterns: pulumi.Input[Sequence[pulumi.Input[str]]],
                 url_template: pulumi.Input[str],
                 user_assigned_identity_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] category_patterns: The categories to match on, or `*` for all.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] event_patterns: The events to match on, or `*` for all.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] hub_patterns: The hubs to match on, or `*` for all.
        :param pulumi.Input[str] url_template: The upstream URL Template. This can be a url or a template such as `http://host.com/{hub}/api/{category}/{event}`.
        :param pulumi.Input[str] user_assigned_identity_id: Specifies the Managed Identity IDs to be assigned to this signalR upstream setting by using resource uuid as both system assigned and user assigned identity is supported.
        """
        pulumi.set(__self__, "category_patterns", category_patterns)
        pulumi.set(__self__, "event_patterns", event_patterns)
        pulumi.set(__self__, "hub_patterns", hub_patterns)
        pulumi.set(__self__, "url_template", url_template)
        if user_assigned_identity_id is not None:
            pulumi.set(__self__, "user_assigned_identity_id", user_assigned_identity_id)

    @property
    @pulumi.getter(name="categoryPatterns")
    def category_patterns(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The categories to match on, or `*` for all.
        """
        return pulumi.get(self, "category_patterns")

    @category_patterns.setter
    def category_patterns(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "category_patterns", value)

    @property
    @pulumi.getter(name="eventPatterns")
    def event_patterns(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The events to match on, or `*` for all.
        """
        return pulumi.get(self, "event_patterns")

    @event_patterns.setter
    def event_patterns(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "event_patterns", value)

    @property
    @pulumi.getter(name="hubPatterns")
    def hub_patterns(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The hubs to match on, or `*` for all.
        """
        return pulumi.get(self, "hub_patterns")

    @hub_patterns.setter
    def hub_patterns(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "hub_patterns", value)

    @property
    @pulumi.getter(name="urlTemplate")
    def url_template(self) -> pulumi.Input[str]:
        """
        The upstream URL Template. This can be a url or a template such as `http://host.com/{hub}/api/{category}/{event}`.
        """
        return pulumi.get(self, "url_template")

    @url_template.setter
    def url_template(self, value: pulumi.Input[str]):
        pulumi.set(self, "url_template", value)

    @property
    @pulumi.getter(name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Managed Identity IDs to be assigned to this signalR upstream setting by using resource uuid as both system assigned and user assigned identity is supported.
        """
        return pulumi.get(self, "user_assigned_identity_id")

    @user_assigned_identity_id.setter
    def user_assigned_identity_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_assigned_identity_id", value)


