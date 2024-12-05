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

__all__ = [
    'ClusterExtensionIdentity',
    'ClusterIdentity',
    'FluxConfigurationBlobStorage',
    'FluxConfigurationBlobStorageServicePrincipal',
    'FluxConfigurationBucket',
    'FluxConfigurationGitRepository',
    'FluxConfigurationKustomization',
]

@pulumi.output_type
class ClusterExtensionIdentity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ClusterExtensionIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ClusterExtensionIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ClusterExtensionIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: str,
                 principal_id: Optional[str] = None,
                 tenant_id: Optional[str] = None):
        """
        :param str type: Specifies the type of Managed Service Identity. The only possible value is `SystemAssigned`. Changing this forces a new resource to be created.
        :param str principal_id: The Principal ID associated with this Managed Service Identity.
        :param str tenant_id: The Tenant ID associated with this Managed Service Identity.
        """
        pulumi.set(__self__, "type", type)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies the type of Managed Service Identity. The only possible value is `SystemAssigned`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[str]:
        """
        The Principal ID associated with this Managed Service Identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        """
        The Tenant ID associated with this Managed Service Identity.
        """
        return pulumi.get(self, "tenant_id")


@pulumi.output_type
class ClusterIdentity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ClusterIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ClusterIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ClusterIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: str,
                 principal_id: Optional[str] = None,
                 tenant_id: Optional[str] = None):
        """
        :param str type: Specifies the type of Managed Service Identity assigned to this Arc Kubernetes Cluster. At this time the only possible value is `SystemAssigned`. Changing this forces a new resource to be created.
        :param str principal_id: The Principal ID associated with this Managed Service Identity.
        :param str tenant_id: The Tenant ID associated with this Managed Service Identity.
        """
        pulumi.set(__self__, "type", type)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies the type of Managed Service Identity assigned to this Arc Kubernetes Cluster. At this time the only possible value is `SystemAssigned`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[str]:
        """
        The Principal ID associated with this Managed Service Identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        """
        The Tenant ID associated with this Managed Service Identity.
        """
        return pulumi.get(self, "tenant_id")


@pulumi.output_type
class FluxConfigurationBlobStorage(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "containerId":
            suggest = "container_id"
        elif key == "accountKey":
            suggest = "account_key"
        elif key == "localAuthReference":
            suggest = "local_auth_reference"
        elif key == "sasToken":
            suggest = "sas_token"
        elif key == "servicePrincipal":
            suggest = "service_principal"
        elif key == "syncIntervalInSeconds":
            suggest = "sync_interval_in_seconds"
        elif key == "timeoutInSeconds":
            suggest = "timeout_in_seconds"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FluxConfigurationBlobStorage. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FluxConfigurationBlobStorage.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FluxConfigurationBlobStorage.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 container_id: str,
                 account_key: Optional[str] = None,
                 local_auth_reference: Optional[str] = None,
                 sas_token: Optional[str] = None,
                 service_principal: Optional['outputs.FluxConfigurationBlobStorageServicePrincipal'] = None,
                 sync_interval_in_seconds: Optional[int] = None,
                 timeout_in_seconds: Optional[int] = None):
        """
        :param str container_id: Specifies the Azure Blob container ID.
        :param str account_key: Specifies the account key (shared key) to access the storage account.
        :param str local_auth_reference: Specifies the name of a local secret on the Kubernetes cluster to use as the authentication secret rather than the managed or user-provided configuration secrets.
        :param str sas_token: Specifies the shared access token to access the storage container.
        :param 'FluxConfigurationBlobStorageServicePrincipalArgs' service_principal: A `service_principal` block as defined below.
        :param int sync_interval_in_seconds: Specifies the interval at which to re-reconcile the cluster Azure Blob source with the remote.
        :param int timeout_in_seconds: Specifies the maximum time to attempt to reconcile the cluster Azure Blob source with the remote.
        """
        pulumi.set(__self__, "container_id", container_id)
        if account_key is not None:
            pulumi.set(__self__, "account_key", account_key)
        if local_auth_reference is not None:
            pulumi.set(__self__, "local_auth_reference", local_auth_reference)
        if sas_token is not None:
            pulumi.set(__self__, "sas_token", sas_token)
        if service_principal is not None:
            pulumi.set(__self__, "service_principal", service_principal)
        if sync_interval_in_seconds is not None:
            pulumi.set(__self__, "sync_interval_in_seconds", sync_interval_in_seconds)
        if timeout_in_seconds is not None:
            pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)

    @property
    @pulumi.getter(name="containerId")
    def container_id(self) -> str:
        """
        Specifies the Azure Blob container ID.
        """
        return pulumi.get(self, "container_id")

    @property
    @pulumi.getter(name="accountKey")
    def account_key(self) -> Optional[str]:
        """
        Specifies the account key (shared key) to access the storage account.
        """
        return pulumi.get(self, "account_key")

    @property
    @pulumi.getter(name="localAuthReference")
    def local_auth_reference(self) -> Optional[str]:
        """
        Specifies the name of a local secret on the Kubernetes cluster to use as the authentication secret rather than the managed or user-provided configuration secrets.
        """
        return pulumi.get(self, "local_auth_reference")

    @property
    @pulumi.getter(name="sasToken")
    def sas_token(self) -> Optional[str]:
        """
        Specifies the shared access token to access the storage container.
        """
        return pulumi.get(self, "sas_token")

    @property
    @pulumi.getter(name="servicePrincipal")
    def service_principal(self) -> Optional['outputs.FluxConfigurationBlobStorageServicePrincipal']:
        """
        A `service_principal` block as defined below.
        """
        return pulumi.get(self, "service_principal")

    @property
    @pulumi.getter(name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> Optional[int]:
        """
        Specifies the interval at which to re-reconcile the cluster Azure Blob source with the remote.
        """
        return pulumi.get(self, "sync_interval_in_seconds")

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> Optional[int]:
        """
        Specifies the maximum time to attempt to reconcile the cluster Azure Blob source with the remote.
        """
        return pulumi.get(self, "timeout_in_seconds")


@pulumi.output_type
class FluxConfigurationBlobStorageServicePrincipal(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientId":
            suggest = "client_id"
        elif key == "tenantId":
            suggest = "tenant_id"
        elif key == "clientCertificateBase64":
            suggest = "client_certificate_base64"
        elif key == "clientCertificatePassword":
            suggest = "client_certificate_password"
        elif key == "clientCertificateSendChain":
            suggest = "client_certificate_send_chain"
        elif key == "clientSecret":
            suggest = "client_secret"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FluxConfigurationBlobStorageServicePrincipal. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FluxConfigurationBlobStorageServicePrincipal.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FluxConfigurationBlobStorageServicePrincipal.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id: str,
                 tenant_id: str,
                 client_certificate_base64: Optional[str] = None,
                 client_certificate_password: Optional[str] = None,
                 client_certificate_send_chain: Optional[bool] = None,
                 client_secret: Optional[str] = None):
        """
        :param str client_id: Specifies the client ID for authenticating a Service Principal.
        :param str tenant_id: Specifies the tenant ID for authenticating a Service Principal.
        :param str client_certificate_base64: Base64-encoded certificate used to authenticate a Service Principal .
        :param str client_certificate_password: Specifies the password for the certificate used to authenticate a Service Principal .
        :param bool client_certificate_send_chain: Specifies whether to include x5c header in client claims when acquiring a token to enable subject name / issuer based authentication for the client certificate.
        :param str client_secret: Specifies the client secret for authenticating a Service Principal.
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        if client_certificate_base64 is not None:
            pulumi.set(__self__, "client_certificate_base64", client_certificate_base64)
        if client_certificate_password is not None:
            pulumi.set(__self__, "client_certificate_password", client_certificate_password)
        if client_certificate_send_chain is not None:
            pulumi.set(__self__, "client_certificate_send_chain", client_certificate_send_chain)
        if client_secret is not None:
            pulumi.set(__self__, "client_secret", client_secret)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        Specifies the client ID for authenticating a Service Principal.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        Specifies the tenant ID for authenticating a Service Principal.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter(name="clientCertificateBase64")
    def client_certificate_base64(self) -> Optional[str]:
        """
        Base64-encoded certificate used to authenticate a Service Principal .
        """
        return pulumi.get(self, "client_certificate_base64")

    @property
    @pulumi.getter(name="clientCertificatePassword")
    def client_certificate_password(self) -> Optional[str]:
        """
        Specifies the password for the certificate used to authenticate a Service Principal .
        """
        return pulumi.get(self, "client_certificate_password")

    @property
    @pulumi.getter(name="clientCertificateSendChain")
    def client_certificate_send_chain(self) -> Optional[bool]:
        """
        Specifies whether to include x5c header in client claims when acquiring a token to enable subject name / issuer based authentication for the client certificate.
        """
        return pulumi.get(self, "client_certificate_send_chain")

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> Optional[str]:
        """
        Specifies the client secret for authenticating a Service Principal.
        """
        return pulumi.get(self, "client_secret")


@pulumi.output_type
class FluxConfigurationBucket(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketName":
            suggest = "bucket_name"
        elif key == "accessKey":
            suggest = "access_key"
        elif key == "localAuthReference":
            suggest = "local_auth_reference"
        elif key == "secretKeyBase64":
            suggest = "secret_key_base64"
        elif key == "syncIntervalInSeconds":
            suggest = "sync_interval_in_seconds"
        elif key == "timeoutInSeconds":
            suggest = "timeout_in_seconds"
        elif key == "tlsEnabled":
            suggest = "tls_enabled"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FluxConfigurationBucket. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FluxConfigurationBucket.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FluxConfigurationBucket.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket_name: str,
                 url: str,
                 access_key: Optional[str] = None,
                 local_auth_reference: Optional[str] = None,
                 secret_key_base64: Optional[str] = None,
                 sync_interval_in_seconds: Optional[int] = None,
                 timeout_in_seconds: Optional[int] = None,
                 tls_enabled: Optional[bool] = None):
        """
        :param str bucket_name: Specifies the bucket name to sync from the url endpoint for the flux configuration.
        :param str url: Specifies the URL to sync for the flux configuration S3 bucket. It must start with `http://` or `https://`.
        :param str access_key: Specifies the plaintext access key used to securely access the S3 bucket.
        :param str local_auth_reference: Specifies the name of a local secret on the Kubernetes cluster to use as the authentication secret rather than the managed or user-provided configuration secrets.
        :param str secret_key_base64: Specifies the Base64-encoded secret key used to authenticate with the bucket source.
        :param int sync_interval_in_seconds: Specifies the interval at which to re-reconcile the cluster git repository source with the remote. Defaults to `600`.
        :param int timeout_in_seconds: Specifies the maximum time to attempt to reconcile the cluster git repository source with the remote. Defaults to `600`.
        :param bool tls_enabled: Specify whether to communicate with a bucket using TLS is enabled. Defaults to `true`.
        """
        pulumi.set(__self__, "bucket_name", bucket_name)
        pulumi.set(__self__, "url", url)
        if access_key is not None:
            pulumi.set(__self__, "access_key", access_key)
        if local_auth_reference is not None:
            pulumi.set(__self__, "local_auth_reference", local_auth_reference)
        if secret_key_base64 is not None:
            pulumi.set(__self__, "secret_key_base64", secret_key_base64)
        if sync_interval_in_seconds is not None:
            pulumi.set(__self__, "sync_interval_in_seconds", sync_interval_in_seconds)
        if timeout_in_seconds is not None:
            pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)
        if tls_enabled is not None:
            pulumi.set(__self__, "tls_enabled", tls_enabled)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> str:
        """
        Specifies the bucket name to sync from the url endpoint for the flux configuration.
        """
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter
    def url(self) -> str:
        """
        Specifies the URL to sync for the flux configuration S3 bucket. It must start with `http://` or `https://`.
        """
        return pulumi.get(self, "url")

    @property
    @pulumi.getter(name="accessKey")
    def access_key(self) -> Optional[str]:
        """
        Specifies the plaintext access key used to securely access the S3 bucket.
        """
        return pulumi.get(self, "access_key")

    @property
    @pulumi.getter(name="localAuthReference")
    def local_auth_reference(self) -> Optional[str]:
        """
        Specifies the name of a local secret on the Kubernetes cluster to use as the authentication secret rather than the managed or user-provided configuration secrets.
        """
        return pulumi.get(self, "local_auth_reference")

    @property
    @pulumi.getter(name="secretKeyBase64")
    def secret_key_base64(self) -> Optional[str]:
        """
        Specifies the Base64-encoded secret key used to authenticate with the bucket source.
        """
        return pulumi.get(self, "secret_key_base64")

    @property
    @pulumi.getter(name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> Optional[int]:
        """
        Specifies the interval at which to re-reconcile the cluster git repository source with the remote. Defaults to `600`.
        """
        return pulumi.get(self, "sync_interval_in_seconds")

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> Optional[int]:
        """
        Specifies the maximum time to attempt to reconcile the cluster git repository source with the remote. Defaults to `600`.
        """
        return pulumi.get(self, "timeout_in_seconds")

    @property
    @pulumi.getter(name="tlsEnabled")
    def tls_enabled(self) -> Optional[bool]:
        """
        Specify whether to communicate with a bucket using TLS is enabled. Defaults to `true`.
        """
        return pulumi.get(self, "tls_enabled")


@pulumi.output_type
class FluxConfigurationGitRepository(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "referenceType":
            suggest = "reference_type"
        elif key == "referenceValue":
            suggest = "reference_value"
        elif key == "httpsCaCertBase64":
            suggest = "https_ca_cert_base64"
        elif key == "httpsKeyBase64":
            suggest = "https_key_base64"
        elif key == "httpsUser":
            suggest = "https_user"
        elif key == "localAuthReference":
            suggest = "local_auth_reference"
        elif key == "sshKnownHostsBase64":
            suggest = "ssh_known_hosts_base64"
        elif key == "sshPrivateKeyBase64":
            suggest = "ssh_private_key_base64"
        elif key == "syncIntervalInSeconds":
            suggest = "sync_interval_in_seconds"
        elif key == "timeoutInSeconds":
            suggest = "timeout_in_seconds"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FluxConfigurationGitRepository. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FluxConfigurationGitRepository.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FluxConfigurationGitRepository.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 reference_type: str,
                 reference_value: str,
                 url: str,
                 https_ca_cert_base64: Optional[str] = None,
                 https_key_base64: Optional[str] = None,
                 https_user: Optional[str] = None,
                 local_auth_reference: Optional[str] = None,
                 ssh_known_hosts_base64: Optional[str] = None,
                 ssh_private_key_base64: Optional[str] = None,
                 sync_interval_in_seconds: Optional[int] = None,
                 timeout_in_seconds: Optional[int] = None):
        """
        :param str reference_type: Specifies the source reference type for the GitRepository object. Possible values are `branch`, `commit`, `semver` and `tag`.
        :param str reference_value: Specifies the source reference value for the GitRepository object.
        :param str url: Specifies the URL to sync for the flux configuration git repository. It must start with `http://`, `https://`, `git@` or `ssh://`.
        :param str https_ca_cert_base64: Specifies the Base64-encoded HTTPS certificate authority contents used to access git private git repositories over HTTPS.
        :param str https_key_base64: Specifies the Base64-encoded HTTPS personal access token or password that will be used to access the repository.
        :param str https_user: Specifies the plaintext HTTPS username used to access private git repositories over HTTPS.
        :param str local_auth_reference: Specifies the name of a local secret on the Kubernetes cluster to use as the authentication secret rather than the managed or user-provided configuration secrets. It must be between 1 and 63 characters. It can contain only lowercase letters, numbers, and hyphens (-). It must start and end with a lowercase letter or number.
        :param str ssh_known_hosts_base64: Specifies the Base64-encoded known_hosts value containing public SSH keys required to access private git repositories over SSH.
        :param str ssh_private_key_base64: Specifies the Base64-encoded SSH private key in PEM format.
        :param int sync_interval_in_seconds: Specifies the interval at which to re-reconcile the cluster git repository source with the remote. Defaults to `600`.
        :param int timeout_in_seconds: Specifies the maximum time to attempt to reconcile the cluster git repository source with the remote. Defaults to `600`.
        """
        pulumi.set(__self__, "reference_type", reference_type)
        pulumi.set(__self__, "reference_value", reference_value)
        pulumi.set(__self__, "url", url)
        if https_ca_cert_base64 is not None:
            pulumi.set(__self__, "https_ca_cert_base64", https_ca_cert_base64)
        if https_key_base64 is not None:
            pulumi.set(__self__, "https_key_base64", https_key_base64)
        if https_user is not None:
            pulumi.set(__self__, "https_user", https_user)
        if local_auth_reference is not None:
            pulumi.set(__self__, "local_auth_reference", local_auth_reference)
        if ssh_known_hosts_base64 is not None:
            pulumi.set(__self__, "ssh_known_hosts_base64", ssh_known_hosts_base64)
        if ssh_private_key_base64 is not None:
            pulumi.set(__self__, "ssh_private_key_base64", ssh_private_key_base64)
        if sync_interval_in_seconds is not None:
            pulumi.set(__self__, "sync_interval_in_seconds", sync_interval_in_seconds)
        if timeout_in_seconds is not None:
            pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)

    @property
    @pulumi.getter(name="referenceType")
    def reference_type(self) -> str:
        """
        Specifies the source reference type for the GitRepository object. Possible values are `branch`, `commit`, `semver` and `tag`.
        """
        return pulumi.get(self, "reference_type")

    @property
    @pulumi.getter(name="referenceValue")
    def reference_value(self) -> str:
        """
        Specifies the source reference value for the GitRepository object.
        """
        return pulumi.get(self, "reference_value")

    @property
    @pulumi.getter
    def url(self) -> str:
        """
        Specifies the URL to sync for the flux configuration git repository. It must start with `http://`, `https://`, `git@` or `ssh://`.
        """
        return pulumi.get(self, "url")

    @property
    @pulumi.getter(name="httpsCaCertBase64")
    def https_ca_cert_base64(self) -> Optional[str]:
        """
        Specifies the Base64-encoded HTTPS certificate authority contents used to access git private git repositories over HTTPS.
        """
        return pulumi.get(self, "https_ca_cert_base64")

    @property
    @pulumi.getter(name="httpsKeyBase64")
    def https_key_base64(self) -> Optional[str]:
        """
        Specifies the Base64-encoded HTTPS personal access token or password that will be used to access the repository.
        """
        return pulumi.get(self, "https_key_base64")

    @property
    @pulumi.getter(name="httpsUser")
    def https_user(self) -> Optional[str]:
        """
        Specifies the plaintext HTTPS username used to access private git repositories over HTTPS.
        """
        return pulumi.get(self, "https_user")

    @property
    @pulumi.getter(name="localAuthReference")
    def local_auth_reference(self) -> Optional[str]:
        """
        Specifies the name of a local secret on the Kubernetes cluster to use as the authentication secret rather than the managed or user-provided configuration secrets. It must be between 1 and 63 characters. It can contain only lowercase letters, numbers, and hyphens (-). It must start and end with a lowercase letter or number.
        """
        return pulumi.get(self, "local_auth_reference")

    @property
    @pulumi.getter(name="sshKnownHostsBase64")
    def ssh_known_hosts_base64(self) -> Optional[str]:
        """
        Specifies the Base64-encoded known_hosts value containing public SSH keys required to access private git repositories over SSH.
        """
        return pulumi.get(self, "ssh_known_hosts_base64")

    @property
    @pulumi.getter(name="sshPrivateKeyBase64")
    def ssh_private_key_base64(self) -> Optional[str]:
        """
        Specifies the Base64-encoded SSH private key in PEM format.
        """
        return pulumi.get(self, "ssh_private_key_base64")

    @property
    @pulumi.getter(name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> Optional[int]:
        """
        Specifies the interval at which to re-reconcile the cluster git repository source with the remote. Defaults to `600`.
        """
        return pulumi.get(self, "sync_interval_in_seconds")

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> Optional[int]:
        """
        Specifies the maximum time to attempt to reconcile the cluster git repository source with the remote. Defaults to `600`.
        """
        return pulumi.get(self, "timeout_in_seconds")


@pulumi.output_type
class FluxConfigurationKustomization(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dependsOns":
            suggest = "depends_ons"
        elif key == "garbageCollectionEnabled":
            suggest = "garbage_collection_enabled"
        elif key == "recreatingEnabled":
            suggest = "recreating_enabled"
        elif key == "retryIntervalInSeconds":
            suggest = "retry_interval_in_seconds"
        elif key == "syncIntervalInSeconds":
            suggest = "sync_interval_in_seconds"
        elif key == "timeoutInSeconds":
            suggest = "timeout_in_seconds"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FluxConfigurationKustomization. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FluxConfigurationKustomization.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FluxConfigurationKustomization.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: str,
                 depends_ons: Optional[Sequence[str]] = None,
                 garbage_collection_enabled: Optional[bool] = None,
                 path: Optional[str] = None,
                 recreating_enabled: Optional[bool] = None,
                 retry_interval_in_seconds: Optional[int] = None,
                 sync_interval_in_seconds: Optional[int] = None,
                 timeout_in_seconds: Optional[int] = None):
        """
        :param str name: Specifies the name of the kustomization.
        :param Sequence[str] depends_ons: Specifies other kustomizations that this kustomization depends on. This kustomization will not reconcile until all dependencies have completed their reconciliation.
        :param bool garbage_collection_enabled: Whether garbage collections of Kubernetes objects created by this kustomization is enabled. Defaults to `false`.
        :param str path: Specifies the path in the source reference to reconcile on the cluster.
        :param bool recreating_enabled: Whether re-creating Kubernetes resources on the cluster is enabled when patching fails due to an immutable field change. Defaults to `false`.
        :param int retry_interval_in_seconds: The interval at which to re-reconcile the kustomization on the cluster in the event of failure on reconciliation. Defaults to `600`.
        :param int sync_interval_in_seconds: The interval at which to re-reconcile the kustomization on the cluster. Defaults to `600`.
        :param int timeout_in_seconds: The maximum time to attempt to reconcile the kustomization on the cluster. Defaults to `600`.
        """
        pulumi.set(__self__, "name", name)
        if depends_ons is not None:
            pulumi.set(__self__, "depends_ons", depends_ons)
        if garbage_collection_enabled is not None:
            pulumi.set(__self__, "garbage_collection_enabled", garbage_collection_enabled)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if recreating_enabled is not None:
            pulumi.set(__self__, "recreating_enabled", recreating_enabled)
        if retry_interval_in_seconds is not None:
            pulumi.set(__self__, "retry_interval_in_seconds", retry_interval_in_seconds)
        if sync_interval_in_seconds is not None:
            pulumi.set(__self__, "sync_interval_in_seconds", sync_interval_in_seconds)
        if timeout_in_seconds is not None:
            pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the name of the kustomization.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="dependsOns")
    def depends_ons(self) -> Optional[Sequence[str]]:
        """
        Specifies other kustomizations that this kustomization depends on. This kustomization will not reconcile until all dependencies have completed their reconciliation.
        """
        return pulumi.get(self, "depends_ons")

    @property
    @pulumi.getter(name="garbageCollectionEnabled")
    def garbage_collection_enabled(self) -> Optional[bool]:
        """
        Whether garbage collections of Kubernetes objects created by this kustomization is enabled. Defaults to `false`.
        """
        return pulumi.get(self, "garbage_collection_enabled")

    @property
    @pulumi.getter
    def path(self) -> Optional[str]:
        """
        Specifies the path in the source reference to reconcile on the cluster.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter(name="recreatingEnabled")
    def recreating_enabled(self) -> Optional[bool]:
        """
        Whether re-creating Kubernetes resources on the cluster is enabled when patching fails due to an immutable field change. Defaults to `false`.
        """
        return pulumi.get(self, "recreating_enabled")

    @property
    @pulumi.getter(name="retryIntervalInSeconds")
    def retry_interval_in_seconds(self) -> Optional[int]:
        """
        The interval at which to re-reconcile the kustomization on the cluster in the event of failure on reconciliation. Defaults to `600`.
        """
        return pulumi.get(self, "retry_interval_in_seconds")

    @property
    @pulumi.getter(name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> Optional[int]:
        """
        The interval at which to re-reconcile the kustomization on the cluster. Defaults to `600`.
        """
        return pulumi.get(self, "sync_interval_in_seconds")

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> Optional[int]:
        """
        The maximum time to attempt to reconcile the kustomization on the cluster. Defaults to `600`.
        """
        return pulumi.get(self, "timeout_in_seconds")


