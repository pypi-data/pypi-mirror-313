#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale User """

# standard python imports
import random
import string
from typing import cast, Optional, List

from pydantic import Field, ConfigDict

from regscale.core.app.utils.app_utils import get_current_datetime
from .regscale_model import RegScaleModel, T


def generate_password() -> str:
    """
    Generates a random string that is 12-20 characters long

    :return: random string 12-20 characters long
    :rtype: str
    """
    # select a random password length between 12-20 characters
    length = random.randint(12, 20)

    # get all possible strings to create a password
    all_string_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

    # randomly select characters matching the random length
    temp = random.sample(all_string_chars, length)
    # return a string from the temp list of samples
    return "".join(temp)


class User(RegScaleModel):
    """User Model"""

    model_config = ConfigDict(populate_by_name=True)
    _module_slug = "accounts"
    _unique_fields = [
        ["userName", "email"],
    ]
    _exclude_graphql_fields = ["extra_data", "tenantsId", "password"]

    userName: str = Field(alias="username")
    email: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    tenantId: int = 1
    initials: Optional[str] = None
    id: Optional[str] = None
    password: str = Field(default_factory=generate_password)
    name: Optional[str] = None
    workPhone: Optional[str] = None
    mobilePhone: Optional[str] = None
    avatar: Optional[bytes] = None
    jobTitle: Optional[str] = None
    orgId: Optional[int] = None
    pictureURL: Optional[str] = None
    activated: bool = False
    emailNotifications: bool = True
    ldapUser: bool = False
    externalId: Optional[str] = None
    dateCreated: Optional[str] = Field(default_factory=get_current_datetime)
    lastLogin: Optional[str] = None
    readOnly: bool = True
    roles: Optional[List[str]] = None

    @classmethod
    def _get_additional_endpoints(cls) -> ConfigDict:
        """
        Get additional endpoints for the Accounts model, using {model_slug} as a placeholder for the model slug.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_all="/api/{model_slug}",
            create_account=cls._module_slug_url,
            update_account=cls._module_slug_url,
            get_accounts=cls._module_slug_url,
            register_questionnaire_user="/api/{model_slug}/registerQuestionnaireUser",
            cache_reset="/api/{model_slug}/cacheReset",
            create_ldap_accounts="/api/{model_slug}/ldap",
            create_azuread_accounts="/api/{model_slug}/azureAD",
            assign_role="/api/{model_slug}/assignRole",
            check_role="/api/{model_slug}/checkRole/{strUserId}/{strRoleId}",
            delete_role="/api/{model_slug}/deleteRole/{strUserId}/{strRoleId}",
            get_my_manager="/api/{model_slug}/getMyManager",
            get_manager_by_user_id="/api/{model_slug}/getManagerByUserId/{strUserId}",
            list="/api/{model_slug}/getList",
            get_inactive_users="/api/{model_slug}/getInactiveUsers",
            get_accounts_by_tenant="/api/{model_slug}/{tenantId}",
            get_accounts_by_email_flag="/api/{model_slug}/{intTenantId}/{bEmailFlag}",
            get_all_by_tenant="/api/{model_slug}/getAllByTenant/{intTenantId}",
            filter_users="/api/{model_slug}/filterUsers/{intTenant}/{strSearch}/{bActive}/{strSortBy}/{strDirection}/{intPage}/{intPageSize}",
            filter_user_roles="/api/{model_slug}/filterUserRoles/{intId}/{strRole}/{strSortBy}/{strDirection}/{intPage}/{intPageSize}",
            change_user_status="/api/{model_slug}/changeUserStatus/{strId}/{bStatus}",
            get_user_by_username="/api/{model_slug}/getUserByUsername/{strUsername}",
            get="/api/{model_slug}/find/{id}",
            get_roles="/api/{model_slug}/getRoles",
            get_roles_by_user="/api/{model_slug}/getRolesByUser/{strUser}",
            is_delegate="/api/{model_slug}/isDelegate/{strUser}",
            get_delegates="/api/{model_slug}/getDelegates/{userId}",
            change_avatar="/api/{model_slug}/changeAvatar/{strUsername}",
        )

    @classmethod
    def get_user_by_id(cls, user_id: str) -> "User":
        """
        Get a user by their ID

        :param str user_id: The user's ID
        :return: The user object
        :rtype: User
        """
        response = cls._api_handler.get(
            endpoint=cls.get_endpoint("get").format(model_slug=cls._module_slug, id=user_id)
        )
        return cls._handle_response(response)

    @classmethod
    def get_all(cls) -> List["User"]:
        """
        Get all users from RegScale

        :return: List of RegScale users
        :rtype: List[User]
        """
        response = cls._api_handler.get(endpoint=cls.get_endpoint("get_all"))
        return cast(List[T], cls._handle_list_response(response))

    def assign_role(self, role_id: str) -> bool:
        """
        Assign a role to a user

        :return: Whether the role was assigned
        :rtype: bool
        """
        response = self._api_handler.post(
            data={"roleId": role_id, "userId": self.id}, endpoint=self.get_endpoint("assign_role")
        )
        return response.ok
