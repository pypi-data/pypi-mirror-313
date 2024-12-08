# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer Teams service."""

import logging

from datalayer_solr.teams import (
    create_team,
    get_organization_teams,
    get_team_by_handle,
    get_team_by_uid,
    get_team_member,
    get_team_with_children_by_uid,
    update_team,
    update_team_member,
)
from datalayer_solr.utils import new_ulid, new_uuid
from datalayer_solr.models.roles import (
    TeamRoles,
)


logger = logging.getLogger("__name__")


def create_team_service(user, form):
    """Create a team."""
    team_handle = str(form["handle"]).lower()
    organization_uid = form["organizationId"]
    team = {
        "id": new_uuid(),
        "uid": new_ulid(),
        "type_s": "team",
        "handle_s": team_handle,
        "organization_uid": organization_uid,
        "name_t": form["name"],
        "description_t": form["description"],
        "public_b": False,
        "members": [
            {
                "id": new_uuid(),
                "type_s": "team_member",
                "uid": user["uid"],
                "handle_s": user["handle"],
                "email_s": user["email"],
                "first_name_t": user["firstName"],
                "last_name_t": user["lastName"],
                "roles_ss": [
                    TeamRoles.OWNER.value,
                    TeamRoles.MEMBER.value,
                ],
            }
        ],
    }
    create_team(team)
    return team


def get_team_member_service(team_uid, user_uid, public=True):
    """Get team member."""
    return get_team_member(team_uid, user_uid, deep=False, public=public)


def get_team_with_children_by_uid_service(team_handle):
    """Get team with children by handle."""
    return get_team_with_children_by_uid(team_handle)


def get_organization_teams_service(organization_uid):
    """Get teams for an organization."""
    return get_organization_teams(organization_uid)


def update_team_service(team_uid, form):
    """Update a team."""
    team = get_team_by_uid(team_uid, public=False)
    team["name_t"] = {"set": form["name"]}
    team["description_t"] = {"set": form["description"]}
    update_team(team)


def get_team_by_uid_service(organization_uid, team_handle):
    """Get a team by handle."""
    return get_team_by_handle(organization_uid, team_handle)


def add_member_to_team_service(team_uid, user):
    """Add a member to a team."""
    team = get_team_by_uid(team_uid, public=False)
    member = {
        "id": new_uuid(),
        "type_s": "team_member",
        "uid": user["uid"],
        "handle_s": user["handle_s"],
        "first_name_t": user["first_name_t"],
        "last_name_t": user["last_name_t"],
        "roles_ss": [
            TeamRoles.MEMBER.value,
        ],
    }
    team_update = {
        "id": team["id"],
        "members": {"add": [member]},
    }
    update_team(team_update)


def remove_member_from_team_service(member):
    """Remove a member from a team."""
    team_update = {
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
    update_team(team_update)


def add_member_role_to_team_service(member, role):
    """Add a role to a member of a team."""
    member_update = {
        "id": member["id"],
        "_root_": member["_root_"],
        "_nest_parent_": member["_nest_parent_"],
        "roles_ss": {"add": [role]},
    }
    update_team_member(member_update)


def remove_member_role_from_team_service(member, role):
    """Remove a role from a team member."""
    member_update = {
        "id": member["id"],
        "_root_": member["_root_"],
        "_nest_parent_": member["_nest_parent_"],
        "roles_ss": {"remove": [role]},
    }
    update_team_member(member_update)
