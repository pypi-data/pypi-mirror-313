from typing import List, Optional

from pydantic import BaseModel

import app.settings as settings
from app.model.alert_model import AlertBaseModel


class BasicAuthUser(AlertBaseModel):
    username: str
    password: str
    modifier: Optional[str] = None


class TokenData(BaseModel):
    sub: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    # for backward compatibility of keycloak
    realm_roles: Optional[List[str]] = None
    """
    {realm_access: [role1, role2, ...]}
    """
    realm_access: Optional[dict] = None
    """
    {realm_access: {roles: [role1, role2, ...]}}
    """
    resource_access: Optional[dict] = None

    def is_platform_admin(self) -> bool:
        if self._validate_realm_roles():
            _realm_roles = (
                self.realm_roles
                if self.realm_roles is not None
                else self.realm_access.get("roles")
            )
            return settings.PLATFORM_ADMIN_ROLE in _realm_roles
        else:
            return False

    def is_alert_admin(self) -> bool:
        if self._validate_realm_roles():
            _realm_roles = (
                self.realm_roles
                if self.realm_roles is not None
                else self.realm_access.get("roles")
            )
            return settings.ALERT_ADMIN_ROLE in _realm_roles
        else:
            return False

    def has_realm_role(self, role: str) -> bool:
        if self._validate_realm_roles():
            _realm_roles = (
                self.realm_roles
                if self.realm_roles is not None
                else self.realm_access.get("roles")
            )
            return role in _realm_roles
        else:
            return False

    def has_client_role(self, client_id: str, role: str) -> bool:
        if self.resource_access is None or len(self.resource_access) == 0:
            return False
        if client_id in self.resource_access.keys():
            return role in self.resource_access.get(client_id).get("roles")
        return False

    def _validate_realm_roles(self) -> bool:
        if (self.realm_roles is None or len(self.realm_roles) == 0) and (
            self.realm_access is None
        ):
            return False

        if self.realm_roles and len(self.realm_roles) == 0:
            return False

        if self.realm_access:
            if self.realm_access.get("roles") is None:
                return False
            else:
                if len(self.realm_access.get("roles")) == 0:
                    return False

        return True
