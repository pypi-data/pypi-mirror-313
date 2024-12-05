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
    'StandardWebTestRequestArgs',
    'StandardWebTestRequestArgsDict',
    'StandardWebTestRequestHeaderArgs',
    'StandardWebTestRequestHeaderArgsDict',
    'StandardWebTestValidationRulesArgs',
    'StandardWebTestValidationRulesArgsDict',
    'StandardWebTestValidationRulesContentArgs',
    'StandardWebTestValidationRulesContentArgsDict',
    'WorkbookIdentityArgs',
    'WorkbookIdentityArgsDict',
    'WorkbookTemplateGalleryArgs',
    'WorkbookTemplateGalleryArgsDict',
]

MYPY = False

if not MYPY:
    class StandardWebTestRequestArgsDict(TypedDict):
        url: pulumi.Input[str]
        """
        The WebTest request URL.
        """
        body: NotRequired[pulumi.Input[str]]
        """
        The WebTest request body.
        """
        follow_redirects_enabled: NotRequired[pulumi.Input[bool]]
        """
        Should the following of redirects be enabled? Defaults to `true`.
        """
        headers: NotRequired[pulumi.Input[Sequence[pulumi.Input['StandardWebTestRequestHeaderArgsDict']]]]
        """
        One or more `header` blocks as defined above.
        """
        http_verb: NotRequired[pulumi.Input[str]]
        """
        Which HTTP verb to use for the call. Options are 'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', and 'OPTIONS'. Defaults to `GET`.
        """
        parse_dependent_requests_enabled: NotRequired[pulumi.Input[bool]]
        """
        Should the parsing of dependend requests be enabled? Defaults to `true`.
        """
elif False:
    StandardWebTestRequestArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class StandardWebTestRequestArgs:
    def __init__(__self__, *,
                 url: pulumi.Input[str],
                 body: Optional[pulumi.Input[str]] = None,
                 follow_redirects_enabled: Optional[pulumi.Input[bool]] = None,
                 headers: Optional[pulumi.Input[Sequence[pulumi.Input['StandardWebTestRequestHeaderArgs']]]] = None,
                 http_verb: Optional[pulumi.Input[str]] = None,
                 parse_dependent_requests_enabled: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] url: The WebTest request URL.
        :param pulumi.Input[str] body: The WebTest request body.
        :param pulumi.Input[bool] follow_redirects_enabled: Should the following of redirects be enabled? Defaults to `true`.
        :param pulumi.Input[Sequence[pulumi.Input['StandardWebTestRequestHeaderArgs']]] headers: One or more `header` blocks as defined above.
        :param pulumi.Input[str] http_verb: Which HTTP verb to use for the call. Options are 'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', and 'OPTIONS'. Defaults to `GET`.
        :param pulumi.Input[bool] parse_dependent_requests_enabled: Should the parsing of dependend requests be enabled? Defaults to `true`.
        """
        pulumi.set(__self__, "url", url)
        if body is not None:
            pulumi.set(__self__, "body", body)
        if follow_redirects_enabled is not None:
            pulumi.set(__self__, "follow_redirects_enabled", follow_redirects_enabled)
        if headers is not None:
            pulumi.set(__self__, "headers", headers)
        if http_verb is not None:
            pulumi.set(__self__, "http_verb", http_verb)
        if parse_dependent_requests_enabled is not None:
            pulumi.set(__self__, "parse_dependent_requests_enabled", parse_dependent_requests_enabled)

    @property
    @pulumi.getter
    def url(self) -> pulumi.Input[str]:
        """
        The WebTest request URL.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: pulumi.Input[str]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter
    def body(self) -> Optional[pulumi.Input[str]]:
        """
        The WebTest request body.
        """
        return pulumi.get(self, "body")

    @body.setter
    def body(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "body", value)

    @property
    @pulumi.getter(name="followRedirectsEnabled")
    def follow_redirects_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the following of redirects be enabled? Defaults to `true`.
        """
        return pulumi.get(self, "follow_redirects_enabled")

    @follow_redirects_enabled.setter
    def follow_redirects_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "follow_redirects_enabled", value)

    @property
    @pulumi.getter
    def headers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['StandardWebTestRequestHeaderArgs']]]]:
        """
        One or more `header` blocks as defined above.
        """
        return pulumi.get(self, "headers")

    @headers.setter
    def headers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['StandardWebTestRequestHeaderArgs']]]]):
        pulumi.set(self, "headers", value)

    @property
    @pulumi.getter(name="httpVerb")
    def http_verb(self) -> Optional[pulumi.Input[str]]:
        """
        Which HTTP verb to use for the call. Options are 'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', and 'OPTIONS'. Defaults to `GET`.
        """
        return pulumi.get(self, "http_verb")

    @http_verb.setter
    def http_verb(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "http_verb", value)

    @property
    @pulumi.getter(name="parseDependentRequestsEnabled")
    def parse_dependent_requests_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the parsing of dependend requests be enabled? Defaults to `true`.
        """
        return pulumi.get(self, "parse_dependent_requests_enabled")

    @parse_dependent_requests_enabled.setter
    def parse_dependent_requests_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "parse_dependent_requests_enabled", value)


if not MYPY:
    class StandardWebTestRequestHeaderArgsDict(TypedDict):
        name: pulumi.Input[str]
        """
        The name which should be used for a header in the request.
        """
        value: pulumi.Input[str]
        """
        The value which should be used for a header in the request.
        """
elif False:
    StandardWebTestRequestHeaderArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class StandardWebTestRequestHeaderArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] name: The name which should be used for a header in the request.
        :param pulumi.Input[str] value: The value which should be used for a header in the request.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name which should be used for a header in the request.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value which should be used for a header in the request.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


if not MYPY:
    class StandardWebTestValidationRulesArgsDict(TypedDict):
        content: NotRequired[pulumi.Input['StandardWebTestValidationRulesContentArgsDict']]
        """
        A `content` block as defined above.
        """
        expected_status_code: NotRequired[pulumi.Input[int]]
        """
        The expected status code of the response. Default is '200', '0' means 'response code < 400'
        """
        ssl_cert_remaining_lifetime: NotRequired[pulumi.Input[int]]
        """
        The number of days of SSL certificate validity remaining for the checked endpoint. If the certificate has a shorter remaining lifetime left, the test will fail. This number should be between 1 and 365.
        """
        ssl_check_enabled: NotRequired[pulumi.Input[bool]]
        """
        Should the SSL check be enabled?
        """
elif False:
    StandardWebTestValidationRulesArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class StandardWebTestValidationRulesArgs:
    def __init__(__self__, *,
                 content: Optional[pulumi.Input['StandardWebTestValidationRulesContentArgs']] = None,
                 expected_status_code: Optional[pulumi.Input[int]] = None,
                 ssl_cert_remaining_lifetime: Optional[pulumi.Input[int]] = None,
                 ssl_check_enabled: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input['StandardWebTestValidationRulesContentArgs'] content: A `content` block as defined above.
        :param pulumi.Input[int] expected_status_code: The expected status code of the response. Default is '200', '0' means 'response code < 400'
        :param pulumi.Input[int] ssl_cert_remaining_lifetime: The number of days of SSL certificate validity remaining for the checked endpoint. If the certificate has a shorter remaining lifetime left, the test will fail. This number should be between 1 and 365.
        :param pulumi.Input[bool] ssl_check_enabled: Should the SSL check be enabled?
        """
        if content is not None:
            pulumi.set(__self__, "content", content)
        if expected_status_code is not None:
            pulumi.set(__self__, "expected_status_code", expected_status_code)
        if ssl_cert_remaining_lifetime is not None:
            pulumi.set(__self__, "ssl_cert_remaining_lifetime", ssl_cert_remaining_lifetime)
        if ssl_check_enabled is not None:
            pulumi.set(__self__, "ssl_check_enabled", ssl_check_enabled)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input['StandardWebTestValidationRulesContentArgs']]:
        """
        A `content` block as defined above.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input['StandardWebTestValidationRulesContentArgs']]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter(name="expectedStatusCode")
    def expected_status_code(self) -> Optional[pulumi.Input[int]]:
        """
        The expected status code of the response. Default is '200', '0' means 'response code < 400'
        """
        return pulumi.get(self, "expected_status_code")

    @expected_status_code.setter
    def expected_status_code(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "expected_status_code", value)

    @property
    @pulumi.getter(name="sslCertRemainingLifetime")
    def ssl_cert_remaining_lifetime(self) -> Optional[pulumi.Input[int]]:
        """
        The number of days of SSL certificate validity remaining for the checked endpoint. If the certificate has a shorter remaining lifetime left, the test will fail. This number should be between 1 and 365.
        """
        return pulumi.get(self, "ssl_cert_remaining_lifetime")

    @ssl_cert_remaining_lifetime.setter
    def ssl_cert_remaining_lifetime(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ssl_cert_remaining_lifetime", value)

    @property
    @pulumi.getter(name="sslCheckEnabled")
    def ssl_check_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the SSL check be enabled?
        """
        return pulumi.get(self, "ssl_check_enabled")

    @ssl_check_enabled.setter
    def ssl_check_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ssl_check_enabled", value)


if not MYPY:
    class StandardWebTestValidationRulesContentArgsDict(TypedDict):
        content_match: pulumi.Input[str]
        """
        A string value containing the content to match on.
        """
        ignore_case: NotRequired[pulumi.Input[bool]]
        """
        Ignore the casing in the `content_match` value.
        """
        pass_if_text_found: NotRequired[pulumi.Input[bool]]
        """
        If the content of `content_match` is found, pass the test. If set to `false`, the WebTest is failing if the content of `content_match` is found.
        """
elif False:
    StandardWebTestValidationRulesContentArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class StandardWebTestValidationRulesContentArgs:
    def __init__(__self__, *,
                 content_match: pulumi.Input[str],
                 ignore_case: Optional[pulumi.Input[bool]] = None,
                 pass_if_text_found: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] content_match: A string value containing the content to match on.
        :param pulumi.Input[bool] ignore_case: Ignore the casing in the `content_match` value.
        :param pulumi.Input[bool] pass_if_text_found: If the content of `content_match` is found, pass the test. If set to `false`, the WebTest is failing if the content of `content_match` is found.
        """
        pulumi.set(__self__, "content_match", content_match)
        if ignore_case is not None:
            pulumi.set(__self__, "ignore_case", ignore_case)
        if pass_if_text_found is not None:
            pulumi.set(__self__, "pass_if_text_found", pass_if_text_found)

    @property
    @pulumi.getter(name="contentMatch")
    def content_match(self) -> pulumi.Input[str]:
        """
        A string value containing the content to match on.
        """
        return pulumi.get(self, "content_match")

    @content_match.setter
    def content_match(self, value: pulumi.Input[str]):
        pulumi.set(self, "content_match", value)

    @property
    @pulumi.getter(name="ignoreCase")
    def ignore_case(self) -> Optional[pulumi.Input[bool]]:
        """
        Ignore the casing in the `content_match` value.
        """
        return pulumi.get(self, "ignore_case")

    @ignore_case.setter
    def ignore_case(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ignore_case", value)

    @property
    @pulumi.getter(name="passIfTextFound")
    def pass_if_text_found(self) -> Optional[pulumi.Input[bool]]:
        """
        If the content of `content_match` is found, pass the test. If set to `false`, the WebTest is failing if the content of `content_match` is found.
        """
        return pulumi.get(self, "pass_if_text_found")

    @pass_if_text_found.setter
    def pass_if_text_found(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "pass_if_text_found", value)


if not MYPY:
    class WorkbookIdentityArgsDict(TypedDict):
        type: pulumi.Input[str]
        """
        The type of Managed Service Identity that is configured on this Workbook. Possible values are `UserAssigned`, `SystemAssigned` and `SystemAssigned, UserAssigned`. Changing this forces a new resource to be created.
        """
        identity_ids: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        The list of User Assigned Managed Identity IDs assigned to this Workbook. Changing this forces a new resource to be created.
        """
        principal_id: NotRequired[pulumi.Input[str]]
        """
        The Principal ID of the System Assigned Managed Service Identity that is configured on this Workbook.
        """
        tenant_id: NotRequired[pulumi.Input[str]]
        """
        The Tenant ID of the System Assigned Managed Service Identity that is configured on this Workbook.
        """
elif False:
    WorkbookIdentityArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class WorkbookIdentityArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 identity_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] type: The type of Managed Service Identity that is configured on this Workbook. Possible values are `UserAssigned`, `SystemAssigned` and `SystemAssigned, UserAssigned`. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] identity_ids: The list of User Assigned Managed Identity IDs assigned to this Workbook. Changing this forces a new resource to be created.
        :param pulumi.Input[str] principal_id: The Principal ID of the System Assigned Managed Service Identity that is configured on this Workbook.
        :param pulumi.Input[str] tenant_id: The Tenant ID of the System Assigned Managed Service Identity that is configured on this Workbook.
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
        The type of Managed Service Identity that is configured on this Workbook. Possible values are `UserAssigned`, `SystemAssigned` and `SystemAssigned, UserAssigned`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="identityIds")
    def identity_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of User Assigned Managed Identity IDs assigned to this Workbook. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "identity_ids")

    @identity_ids.setter
    def identity_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "identity_ids", value)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Principal ID of the System Assigned Managed Service Identity that is configured on this Workbook.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Tenant ID of the System Assigned Managed Service Identity that is configured on this Workbook.
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)


if not MYPY:
    class WorkbookTemplateGalleryArgsDict(TypedDict):
        category: pulumi.Input[str]
        """
        Category for the gallery.
        """
        name: pulumi.Input[str]
        """
        Name of the workbook template in the gallery.
        """
        order: NotRequired[pulumi.Input[int]]
        """
        Order of the template within the gallery. Defaults to `0`.
        """
        resource_type: NotRequired[pulumi.Input[str]]
        """
        Azure resource type supported by the gallery. Defaults to `Azure Monitor`.
        """
        type: NotRequired[pulumi.Input[str]]
        """
        Type of workbook supported by the workbook template. Defaults to `workbook`.

        > **Note:** See [documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-automate#galleries) for more information of `resource_type` and `type`.
        """
elif False:
    WorkbookTemplateGalleryArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class WorkbookTemplateGalleryArgs:
    def __init__(__self__, *,
                 category: pulumi.Input[str],
                 name: pulumi.Input[str],
                 order: Optional[pulumi.Input[int]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] category: Category for the gallery.
        :param pulumi.Input[str] name: Name of the workbook template in the gallery.
        :param pulumi.Input[int] order: Order of the template within the gallery. Defaults to `0`.
        :param pulumi.Input[str] resource_type: Azure resource type supported by the gallery. Defaults to `Azure Monitor`.
        :param pulumi.Input[str] type: Type of workbook supported by the workbook template. Defaults to `workbook`.
               
               > **Note:** See [documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-automate#galleries) for more information of `resource_type` and `type`.
        """
        pulumi.set(__self__, "category", category)
        pulumi.set(__self__, "name", name)
        if order is not None:
            pulumi.set(__self__, "order", order)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def category(self) -> pulumi.Input[str]:
        """
        Category for the gallery.
        """
        return pulumi.get(self, "category")

    @category.setter
    def category(self, value: pulumi.Input[str]):
        pulumi.set(self, "category", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the workbook template in the gallery.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def order(self) -> Optional[pulumi.Input[int]]:
        """
        Order of the template within the gallery. Defaults to `0`.
        """
        return pulumi.get(self, "order")

    @order.setter
    def order(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "order", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[pulumi.Input[str]]:
        """
        Azure resource type supported by the gallery. Defaults to `Azure Monitor`.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_type", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of workbook supported by the workbook template. Defaults to `workbook`.

        > **Note:** See [documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-automate#galleries) for more information of `resource_type` and `type`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


