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
    'FlexibleServerAuthentication',
    'FlexibleServerCustomerManagedKey',
    'FlexibleServerHighAvailability',
    'FlexibleServerIdentity',
    'FlexibleServerMaintenanceWindow',
    'ServerIdentity',
    'ServerThreatDetectionPolicy',
    'GetServerIdentityResult',
]

@pulumi.output_type
class FlexibleServerAuthentication(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "activeDirectoryAuthEnabled":
            suggest = "active_directory_auth_enabled"
        elif key == "passwordAuthEnabled":
            suggest = "password_auth_enabled"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FlexibleServerAuthentication. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FlexibleServerAuthentication.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FlexibleServerAuthentication.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 active_directory_auth_enabled: Optional[bool] = None,
                 password_auth_enabled: Optional[bool] = None,
                 tenant_id: Optional[str] = None):
        """
        :param bool active_directory_auth_enabled: Whether or not Active Directory authentication is allowed to access the PostgreSQL Flexible Server. Defaults to `false`.
        :param bool password_auth_enabled: Whether or not password authentication is allowed to access the PostgreSQL Flexible Server. Defaults to `true`.
        :param str tenant_id: The Tenant ID of the Azure Active Directory which is used by the Active Directory authentication. `active_directory_auth_enabled` must be set to `true`.
               
               > **Note:** Setting `active_directory_auth_enabled` to `true` requires a Service Principal for the Postgres Flexible Server. For more details see [this document](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/how-to-configure-sign-in-azure-ad-authentication).
               
               > **Note:** `tenant_id` is required when `active_directory_auth_enabled` is set to `true`. And it should not be specified when `active_directory_auth_enabled` is set to `false`
        """
        if active_directory_auth_enabled is not None:
            pulumi.set(__self__, "active_directory_auth_enabled", active_directory_auth_enabled)
        if password_auth_enabled is not None:
            pulumi.set(__self__, "password_auth_enabled", password_auth_enabled)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="activeDirectoryAuthEnabled")
    def active_directory_auth_enabled(self) -> Optional[bool]:
        """
        Whether or not Active Directory authentication is allowed to access the PostgreSQL Flexible Server. Defaults to `false`.
        """
        return pulumi.get(self, "active_directory_auth_enabled")

    @property
    @pulumi.getter(name="passwordAuthEnabled")
    def password_auth_enabled(self) -> Optional[bool]:
        """
        Whether or not password authentication is allowed to access the PostgreSQL Flexible Server. Defaults to `true`.
        """
        return pulumi.get(self, "password_auth_enabled")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        """
        The Tenant ID of the Azure Active Directory which is used by the Active Directory authentication. `active_directory_auth_enabled` must be set to `true`.

        > **Note:** Setting `active_directory_auth_enabled` to `true` requires a Service Principal for the Postgres Flexible Server. For more details see [this document](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/how-to-configure-sign-in-azure-ad-authentication).

        > **Note:** `tenant_id` is required when `active_directory_auth_enabled` is set to `true`. And it should not be specified when `active_directory_auth_enabled` is set to `false`
        """
        return pulumi.get(self, "tenant_id")


@pulumi.output_type
class FlexibleServerCustomerManagedKey(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyVaultKeyId":
            suggest = "key_vault_key_id"
        elif key == "geoBackupKeyVaultKeyId":
            suggest = "geo_backup_key_vault_key_id"
        elif key == "geoBackupUserAssignedIdentityId":
            suggest = "geo_backup_user_assigned_identity_id"
        elif key == "primaryUserAssignedIdentityId":
            suggest = "primary_user_assigned_identity_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FlexibleServerCustomerManagedKey. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FlexibleServerCustomerManagedKey.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FlexibleServerCustomerManagedKey.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 key_vault_key_id: str,
                 geo_backup_key_vault_key_id: Optional[str] = None,
                 geo_backup_user_assigned_identity_id: Optional[str] = None,
                 primary_user_assigned_identity_id: Optional[str] = None):
        """
        :param str key_vault_key_id: The ID of the Key Vault Key.
        :param str geo_backup_key_vault_key_id: The ID of the geo backup Key Vault Key. It can't cross region and need Customer Managed Key in same region as geo backup.
        :param str geo_backup_user_assigned_identity_id: The geo backup user managed identity id for a Customer Managed Key. Should be added with `identity_ids`. It can't cross region and need identity in same region as geo backup.
               
               > **Note:** `primary_user_assigned_identity_id` or `geo_backup_user_assigned_identity_id` is required when `type` is set to `UserAssigned`.
        :param str primary_user_assigned_identity_id: Specifies the primary user managed identity id for a Customer Managed Key. Should be added with `identity_ids`.
        """
        pulumi.set(__self__, "key_vault_key_id", key_vault_key_id)
        if geo_backup_key_vault_key_id is not None:
            pulumi.set(__self__, "geo_backup_key_vault_key_id", geo_backup_key_vault_key_id)
        if geo_backup_user_assigned_identity_id is not None:
            pulumi.set(__self__, "geo_backup_user_assigned_identity_id", geo_backup_user_assigned_identity_id)
        if primary_user_assigned_identity_id is not None:
            pulumi.set(__self__, "primary_user_assigned_identity_id", primary_user_assigned_identity_id)

    @property
    @pulumi.getter(name="keyVaultKeyId")
    def key_vault_key_id(self) -> str:
        """
        The ID of the Key Vault Key.
        """
        return pulumi.get(self, "key_vault_key_id")

    @property
    @pulumi.getter(name="geoBackupKeyVaultKeyId")
    def geo_backup_key_vault_key_id(self) -> Optional[str]:
        """
        The ID of the geo backup Key Vault Key. It can't cross region and need Customer Managed Key in same region as geo backup.
        """
        return pulumi.get(self, "geo_backup_key_vault_key_id")

    @property
    @pulumi.getter(name="geoBackupUserAssignedIdentityId")
    def geo_backup_user_assigned_identity_id(self) -> Optional[str]:
        """
        The geo backup user managed identity id for a Customer Managed Key. Should be added with `identity_ids`. It can't cross region and need identity in same region as geo backup.

        > **Note:** `primary_user_assigned_identity_id` or `geo_backup_user_assigned_identity_id` is required when `type` is set to `UserAssigned`.
        """
        return pulumi.get(self, "geo_backup_user_assigned_identity_id")

    @property
    @pulumi.getter(name="primaryUserAssignedIdentityId")
    def primary_user_assigned_identity_id(self) -> Optional[str]:
        """
        Specifies the primary user managed identity id for a Customer Managed Key. Should be added with `identity_ids`.
        """
        return pulumi.get(self, "primary_user_assigned_identity_id")


@pulumi.output_type
class FlexibleServerHighAvailability(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "standbyAvailabilityZone":
            suggest = "standby_availability_zone"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FlexibleServerHighAvailability. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FlexibleServerHighAvailability.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FlexibleServerHighAvailability.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 mode: str,
                 standby_availability_zone: Optional[str] = None):
        """
        :param str mode: The high availability mode for the PostgreSQL Flexible Server. Possible value are `SameZone` or `ZoneRedundant`.
        """
        pulumi.set(__self__, "mode", mode)
        if standby_availability_zone is not None:
            pulumi.set(__self__, "standby_availability_zone", standby_availability_zone)

    @property
    @pulumi.getter
    def mode(self) -> str:
        """
        The high availability mode for the PostgreSQL Flexible Server. Possible value are `SameZone` or `ZoneRedundant`.
        """
        return pulumi.get(self, "mode")

    @property
    @pulumi.getter(name="standbyAvailabilityZone")
    def standby_availability_zone(self) -> Optional[str]:
        return pulumi.get(self, "standby_availability_zone")


@pulumi.output_type
class FlexibleServerIdentity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "identityIds":
            suggest = "identity_ids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FlexibleServerIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FlexibleServerIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FlexibleServerIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 identity_ids: Sequence[str],
                 type: str):
        """
        :param Sequence[str] identity_ids: A list of User Assigned Managed Identity IDs to be assigned to this PostgreSQL Flexible Server. Required if used together with `customer_managed_key` block.
        :param str type: Specifies the type of Managed Service Identity that should be configured on this PostgreSQL Flexible Server. The only possible value is `UserAssigned`.
        """
        pulumi.set(__self__, "identity_ids", identity_ids)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="identityIds")
    def identity_ids(self) -> Sequence[str]:
        """
        A list of User Assigned Managed Identity IDs to be assigned to this PostgreSQL Flexible Server. Required if used together with `customer_managed_key` block.
        """
        return pulumi.get(self, "identity_ids")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies the type of Managed Service Identity that should be configured on this PostgreSQL Flexible Server. The only possible value is `UserAssigned`.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class FlexibleServerMaintenanceWindow(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dayOfWeek":
            suggest = "day_of_week"
        elif key == "startHour":
            suggest = "start_hour"
        elif key == "startMinute":
            suggest = "start_minute"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FlexibleServerMaintenanceWindow. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FlexibleServerMaintenanceWindow.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FlexibleServerMaintenanceWindow.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 day_of_week: Optional[int] = None,
                 start_hour: Optional[int] = None,
                 start_minute: Optional[int] = None):
        """
        :param int day_of_week: The day of week for maintenance window, where the week starts on a Sunday, i.e. Sunday = `0`, Monday = `1`. Defaults to `0`.
        :param int start_hour: The start hour for maintenance window. Defaults to `0`.
        :param int start_minute: The start minute for maintenance window. Defaults to `0`.
               
               > **NOTE** The specified `maintenance_window` is always defined in UTC time. When unspecified, the maintenance window falls back to the default [system-managed](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/how-to-maintenance-portal#specify-maintenance-schedule-options).
        """
        if day_of_week is not None:
            pulumi.set(__self__, "day_of_week", day_of_week)
        if start_hour is not None:
            pulumi.set(__self__, "start_hour", start_hour)
        if start_minute is not None:
            pulumi.set(__self__, "start_minute", start_minute)

    @property
    @pulumi.getter(name="dayOfWeek")
    def day_of_week(self) -> Optional[int]:
        """
        The day of week for maintenance window, where the week starts on a Sunday, i.e. Sunday = `0`, Monday = `1`. Defaults to `0`.
        """
        return pulumi.get(self, "day_of_week")

    @property
    @pulumi.getter(name="startHour")
    def start_hour(self) -> Optional[int]:
        """
        The start hour for maintenance window. Defaults to `0`.
        """
        return pulumi.get(self, "start_hour")

    @property
    @pulumi.getter(name="startMinute")
    def start_minute(self) -> Optional[int]:
        """
        The start minute for maintenance window. Defaults to `0`.

        > **NOTE** The specified `maintenance_window` is always defined in UTC time. When unspecified, the maintenance window falls back to the default [system-managed](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/how-to-maintenance-portal#specify-maintenance-schedule-options).
        """
        return pulumi.get(self, "start_minute")


@pulumi.output_type
class ServerIdentity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServerIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServerIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServerIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: str,
                 principal_id: Optional[str] = None,
                 tenant_id: Optional[str] = None):
        """
        :param str type: Specifies the type of Managed Service Identity that should be configured on this PostgreSQL Server. The only possible value is `SystemAssigned`.
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
        Specifies the type of Managed Service Identity that should be configured on this PostgreSQL Server. The only possible value is `SystemAssigned`.
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
class ServerThreatDetectionPolicy(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "disabledAlerts":
            suggest = "disabled_alerts"
        elif key == "emailAccountAdmins":
            suggest = "email_account_admins"
        elif key == "emailAddresses":
            suggest = "email_addresses"
        elif key == "retentionDays":
            suggest = "retention_days"
        elif key == "storageAccountAccessKey":
            suggest = "storage_account_access_key"
        elif key == "storageEndpoint":
            suggest = "storage_endpoint"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServerThreatDetectionPolicy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServerThreatDetectionPolicy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServerThreatDetectionPolicy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 disabled_alerts: Optional[Sequence[str]] = None,
                 email_account_admins: Optional[bool] = None,
                 email_addresses: Optional[Sequence[str]] = None,
                 enabled: Optional[bool] = None,
                 retention_days: Optional[int] = None,
                 storage_account_access_key: Optional[str] = None,
                 storage_endpoint: Optional[str] = None):
        """
        :param Sequence[str] disabled_alerts: Specifies a list of alerts which should be disabled. Possible values are `Sql_Injection`, `Sql_Injection_Vulnerability`, `Access_Anomaly`, `Data_Exfiltration` and `Unsafe_Action`.
        :param bool email_account_admins: Should the account administrators be emailed when this alert is triggered?
        :param Sequence[str] email_addresses: A list of email addresses which alerts should be sent to.
        :param bool enabled: Is the policy enabled?
        :param int retention_days: Specifies the number of days to keep in the Threat Detection audit logs.
        :param str storage_account_access_key: Specifies the identifier key of the Threat Detection audit storage account.
        :param str storage_endpoint: Specifies the blob storage endpoint (e.g. <https://example.blob.core.windows.net>). This blob storage will hold all Threat Detection audit logs.
        """
        if disabled_alerts is not None:
            pulumi.set(__self__, "disabled_alerts", disabled_alerts)
        if email_account_admins is not None:
            pulumi.set(__self__, "email_account_admins", email_account_admins)
        if email_addresses is not None:
            pulumi.set(__self__, "email_addresses", email_addresses)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if retention_days is not None:
            pulumi.set(__self__, "retention_days", retention_days)
        if storage_account_access_key is not None:
            pulumi.set(__self__, "storage_account_access_key", storage_account_access_key)
        if storage_endpoint is not None:
            pulumi.set(__self__, "storage_endpoint", storage_endpoint)

    @property
    @pulumi.getter(name="disabledAlerts")
    def disabled_alerts(self) -> Optional[Sequence[str]]:
        """
        Specifies a list of alerts which should be disabled. Possible values are `Sql_Injection`, `Sql_Injection_Vulnerability`, `Access_Anomaly`, `Data_Exfiltration` and `Unsafe_Action`.
        """
        return pulumi.get(self, "disabled_alerts")

    @property
    @pulumi.getter(name="emailAccountAdmins")
    def email_account_admins(self) -> Optional[bool]:
        """
        Should the account administrators be emailed when this alert is triggered?
        """
        return pulumi.get(self, "email_account_admins")

    @property
    @pulumi.getter(name="emailAddresses")
    def email_addresses(self) -> Optional[Sequence[str]]:
        """
        A list of email addresses which alerts should be sent to.
        """
        return pulumi.get(self, "email_addresses")

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Is the policy enabled?
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="retentionDays")
    def retention_days(self) -> Optional[int]:
        """
        Specifies the number of days to keep in the Threat Detection audit logs.
        """
        return pulumi.get(self, "retention_days")

    @property
    @pulumi.getter(name="storageAccountAccessKey")
    def storage_account_access_key(self) -> Optional[str]:
        """
        Specifies the identifier key of the Threat Detection audit storage account.
        """
        return pulumi.get(self, "storage_account_access_key")

    @property
    @pulumi.getter(name="storageEndpoint")
    def storage_endpoint(self) -> Optional[str]:
        """
        Specifies the blob storage endpoint (e.g. <https://example.blob.core.windows.net>). This blob storage will hold all Threat Detection audit logs.
        """
        return pulumi.get(self, "storage_endpoint")


@pulumi.output_type
class GetServerIdentityResult(dict):
    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: str):
        """
        :param str principal_id: The ID of the System Managed Service Principal assigned to the PostgreSQL Server.
        :param str tenant_id: The ID of the Tenant of the System Managed Service Principal assigned to the PostgreSQL Server.
        :param str type: The identity type of the Managed Identity assigned to the PostgreSQL Server.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The ID of the System Managed Service Principal assigned to the PostgreSQL Server.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The ID of the Tenant of the System Managed Service Principal assigned to the PostgreSQL Server.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The identity type of the Managed Identity assigned to the PostgreSQL Server.
        """
        return pulumi.get(self, "type")


