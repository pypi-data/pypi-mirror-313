# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer Organizations service."""

import logging
import tldextract

from datalayer_solr.organizations import (
    add_organization_member,
    create_organization,
    get_organization_by_handle,
    get_organization_by_uid,
    get_organization_member,
    get_organization_with_children_by_uid,
    get_organizations_by_type,
    get_organizations_for_user,
    update_organization,
    update_organization_member,
)
from datalayer_solr.utils import new_ulid, new_uuid
from datalayer_solr.models.roles import (
    OrganizationRoles,
    SchoolRoles,
)


logger = logging.getLogger("__name__")


def create_organization_service(user, form):
    """Create an organization."""
    organization_handle = str(form["handle"]).lower()
    organization = {
        "id": new_uuid(),
        "uid": new_ulid(),
        "type_s": "organization",
        "handle_s": organization_handle,
        "name_t": form["name"],
        "description_t": form["description"],
        "public_b": False,
        "members": [
            {
                "id": new_uuid(),
                "type_s": "organization_member",
                "uid": user["uid"],
                "handle_s": user["handle"],
                "email_s": user["email"],
                "first_name_t": user["firstName"],
                "last_name_t": user["lastName"],
                "roles_ss": [
                    OrganizationRoles.OWNER.value,
                    OrganizationRoles.MEMBER.value,
                ],
            }
        ],
    }
    create_organization(organization)
    """
    # TODO Do we want to create a space by default?
    create_space_service(
        user,
        {
            "variant": "default",
            "organizationHandle": organization_handle,
            "spaceHandle": "library",
            "name": "Library",
            "description": "Library",
            "public": False,
        },
    )
    """
    return organization


def get_organization_member_service(organization_uid, user_uid, public=True):
    """Get organization member."""
    return get_organization_member(organization_uid, user_uid, deep=False, public=public)


def get_organization_with_children_by_uid_service(organization_handle):
    """Get organization with children by handle."""
    return get_organization_with_children_by_uid(organization_handle)


def get_organizations_by_type_service(organization_type, load_children):
    """Get organizations by type."""
    return get_organizations_by_type(organization_type, load_children)


def get_organizations_for_user_service(user_handle):
    """Get organizations for user."""
    return get_organizations_for_user(user_handle)


def create_school_service(user, form):
    """Create a school."""
    school = {
        "id": new_uuid(),
        "uid": new_ulid(),
        "type_s": "school",
        "handle_s": user["handle"],
        "first_name_t": user["firstName"],
        "last_name_t": user["lastName"],
        "email_s": user["email"],
        "name_t": form["name"],
        "description_t": form["description"],
        "public_b": form["public"],
        "members": [
            {
                "id": new_uuid(),
                "type_s": "organization_member",
                "uid": user["uid"],
                "handle_s": user["handle"],
                "email_s": user["email"],
                "first_name_t": user["firstName"],
                "last_name_t": user["lastName"],
                "roles_ss": [
                    SchoolRoles.DEAN.value,
                ],
            }
        ],
    }
    create_organization(school)
    return school


def create_school_service_for_user(user):
    """Create a school for the given user."""
    tld = tldextract.extract(user["email_s"])
    school_uid = tld.domain + "-" + tld.suffix
    school = get_organization_by_uid(school_uid)
    if not school:
        school = {
            "id": new_uuid(),
            "uid": school_uid,
            "type_s": "school",
            "name_t": f"{school_uid} school",
            "description_t": f"The {school_uid} school on Datalayer.",
            "members": [],
            "groups": [],
        }
        create_organization(school)
        dean = {
            "id": new_uuid(),
            "uid": user["uid"],
            "handle_s": user["handle_s"],
            "first_name_t": user["first_name_t"],
            "last_name_t": user["last_name_t"],
            "roles_ss": [
                SchoolRoles.DEAN.value,
            ],
        }
        add_organization_member(school["id"], dean)


def update_organization_service(organization_uid, form):
    """Update an organization."""
    organization = get_organization_by_uid(organization_uid, public=False)
    organization["name_t"] = {"set": form["name"]}
    organization["description_t"] = {"set": form["description"]}
    update_organization(organization)


def update_school_service(school_update):
    """Update a school."""
    school = get_organization_by_uid(school_update["uid"], public=False)
    school["name_t"] = {"set": school_update["name"]}
    school["description_t"] = {"set": school_update["description"]}
    update_organization(school)


def get_organization_by_uid_service(organization_uid):
    """Get an organization by uid."""
    return get_organization_by_uid(organization_uid)


def get_organization_by_handle_service(organization_handle):
    """Get an organization by handle."""
    return get_organization_by_handle(organization_handle)


def add_member_to_organization_service(organization_uid, user):
    """Add a member to an organization."""
    organization = get_organization_by_uid(organization_uid, public=False)
    member = {
        "id": new_uuid(),
        "type_s": "organization_member",
        "uid": user["uid"],
        "handle_s": user["handle_s"],
        "first_name_t": user["first_name_t"],
        "last_name_t": user["last_name_t"],
        "roles_ss": [
            OrganizationRoles.MEMBER.value,
        ],
    }
    organization_update = {
        "id": organization["id"],
        "members": {"add": [member]},
    }
    update_organization(organization_update)


def remove_member_from_organization_service(member):
    """Remove a member from an organization."""
    organization_update = {
        "id": member["_root_"],
        "members": {
            "remove": [
                {
                    "id": member["id"],
                    "_root_": member["_root_"],
                    "_nest_parent_": member["_nest_parent_"],
                }
            ]
        },
    }
    update_organization(organization_update)


def add_member_role_to_organization_service(member, role):
    """Add a role to a member of an organization."""
    member_update = {
        "id": member["id"],
        "_root_": member["_root_"],
        "_nest_parent_": member["_nest_parent_"],
        "roles_ss": {"add": [role]},
    }
    update_organization_member(member_update)


def remove_member_role_from_organization_service(member, role):
    """Remove a role from an organization member."""
    member_update = {
        "id": member["id"],
        "_root_": member["_root_"],
        "_nest_parent_": member["_nest_parent_"],
        "roles_ss": {"remove": [role]},
    }
    update_organization_member(member_update)
