# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

import warnings
import asyncio

from getpass import getpass
from pathlib import Path
from traitlets import Set, Unicode

from datalayer_core.application import NoStart

from datalayer_iam import __version__
from datalayer_iam.application_base import DatalayerIAMBaseApp
from datalayer_iam.reserved.handles import RESERVED_HANDLES
from datalayer_iam.services.accounts import (
    get_account_by_handle,
)
from datalayer_iam.services.users import (
    add_user_role_service,
    add_user_role_by_handle_service,
    create_user_service,
    delete_user_service,
    remove_user_role_service,
    remove_user_role_by_handle_service,
)
from datalayer_solr.models.roles import PlatformRoles


HERE = Path(__file__).parent


class ConfigExportApp(DatalayerIAMBaseApp):
    """An application to export the configuration."""

    description = """
      An application to export the configuration
    """

    def initialize(self, *args, **kwargs):
        """Initialize the app."""
        super().initialize(*args, **kwargs)

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for workspace export.")
            self.exit(1)
        self.log.info("ConfigApp %s", self.version)


class ConfigApp(DatalayerIAMBaseApp):
    """A config app."""

    description = """
    Manage the configuration.
    """

    subcommands = {}
    subcommands["export"] = (
        ConfigExportApp,
        ConfigExportApp.description.splitlines()[0],
    )

    def start(self):
        try:
            super().start()
            self.log.info(
                f"One of `{'`, `'.join(ConfigApp.subcommands.keys())}` must be specified."
            )
            self.exit(1)
        except NoStart:
            pass
        self.exit(0)


class UserAddRoleApp(DatalayerIAMBaseApp):
    """An application to add roles to a user."""

    description = """
      An application to add roles to a user
    """

    handle = Unicode(config=True, help="User Handle")

    uid = Unicode(config=True, help="User UID")

    roles = Set(
        trait=Unicode, default_value={PlatformRoles.GUEST.value}, config=True, help="User roles"
    )

    aliases = {
        "handle": "UserAddRoleApp.handle",
        "uid": "UserAddRoleApp.uid",
        "roles": "UserAddRoleApp.roles",
    }

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for user creation.")
            self.exit(1)
        if not self.uid and not self.handle:
            raise ValueError(f"Provide a uid or a handle, not both at the same time")
        if self.uid and self.handle:
            raise ValueError(f"Please provide a uid or a handle")

        for role in self.roles:
            if self.uid:
                add_user_role_service(self.uid, role)
                print(f"Role {role} added to user uid {self.uid}")
            elif self.handle:
                add_user_role_by_handle_service(self.handle, role)
                print(f"Role {role} added to user handle {self.handle}")


class UserRemoveRoleApp(DatalayerIAMBaseApp):
    """An application to remove roles to a user."""

    description = """
      An application to remove roles to a user
    """

    handle = Unicode(config=True, help="User Handle")

    uid = Unicode(config=True, help="User UID")

    roles = Set(
        trait=Unicode, default_value={PlatformRoles.GUEST.value}, config=True, help="User roles"
    )

    aliases = {
        "handle": "UserRemoveRoleApp.handle",
        "uid": "UserRemoveRoleApp.uid",
        "roles": "UserRemoveRoleApp.roles",
    }

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for user creation.")
            self.exit(1)
        if not self.uid and not self.handle:
            raise ValueError(f"Provide a uid or a handle")
        if self.uid and self.handle:
            raise ValueError(f"Please provide a uid or a handle, not both at the same time")

        for role in self.roles:
            if self.uid:
                remove_user_role_service(self.uid, role)
                print(f"Role {role} added to user uid {self.uid}")
            elif self.handle:
                remove_user_role_by_handle_service(self.handle, role)
                print(f"Role {role} removed from user handle {self.handle}")


class UserCreateApp(DatalayerIAMBaseApp):
    """An application to create a user."""

    description = """
      An application to create a user
    """

    handle = Unicode(config=True, help="User handle")

    email = Unicode(default_value="", config=True, help="User email")

    roles = Set(
        trait=Unicode, default_value={PlatformRoles.GUEST.value}, config=True, help="User roles"
    )

    aliases = {
        "handle": "UserCreateApp.handle",
        "email": "UserCreateApp.email",
        "roles": "UserCreateApp.roles",
    }

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for user creation.")
            self.exit(1)
        if not self.handle:
            raise ValueError(f"User handle cannot be empty")

        password = getpass("User password: ")
        confirm_password = getpass("User password confirmation: ")

        if password != confirm_password:
            print(f"Passwords do not match.")
            self.exit(1)
        
        account = get_account_by_handle(self.handle)
        if account is not None:
            print(f"Handle {self.handle} is not available.")
            self.exit(1)

        if self.handle in RESERVED_HANDLES or self.handle + "s" in RESERVED_HANDLES:
            print(f"Handle {self.handle} is reserved.")
            self.exit(1)

        asyncio.run(
             create_user_service(
                self.handle,
                "",
                "",
                self.email,
                password,
                origin="cli",
                roles=[r.lower() for r in self.roles],
            )
        )
        print(f"User {self.handle} is created")


class UserDeleteApp(DatalayerIAMBaseApp):
    """An application to delete a user."""

    description = """
      An application to delete a user
    """

    def start(self):
        """Start the app."""
        if len(self.extra_args) != 1:  # pragma: no cover
            warnings.warn("Only the user handle must be specified to delete a user.")
            self.exit(1)
        handle = self.extra_args[0]
        if not self.answer_yes:
            confirm = input(f"Are you sure you want to remove user '{handle}'? [y/N] ")
            if not confirm.lower().startswith("y"):
                self.exit(0)
                return

        delete_user_service(handle)
        print(f"User {handle} removed.")


class UserApp(DatalayerIAMBaseApp):
    """User management CLI."""

    description = "Manage Datalayer through CLI."

    subcommands = {
        "add-role": (
            UserAddRoleApp,
            UserAddRoleApp.description.splitlines()[0],
        ),
        "create": (
            UserCreateApp,
            UserCreateApp.description.splitlines()[0],
        ),
        "delete": (
            UserDeleteApp,
            UserDeleteApp.description.splitlines()[0],
        ),
        "remove-role": (
            UserRemoveRoleApp,
            UserRemoveRoleApp.description.splitlines()[0],
        ),
    }

    def start(self):
        try:
            super().start()
            self.log.info(
                f"One of `{'`, `'.join(UserApp.subcommands.keys())}` must be specified."
            )
            self.exit(1)
        except NoStart:
            pass
        self.exit(0)


class DatalayerIAMApp(DatalayerIAMBaseApp):
    description = """
      The Datalayer IAM application.
    """

    subcommands = {
        "config": (ConfigApp, ConfigApp.description.splitlines()[0]),
        "user": (UserApp, UserApp.description.splitlines()[0]),
        "users": (UserApp, UserApp.description.splitlines()[0]),
    }

    def initialize(self, argv=None):
        """Subclass because the ExtensionApp.initialize() method does not take arguments."""
        super().initialize()

    def start(self):
        super(DatalayerIAMApp, self).start()
        self.log.info("Datalayer IAM - Version [%s] - Cloud [%s] ", self.version, self.cloud)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = DatalayerIAMApp.launch_instance

if __name__ == "__main__":
    main()
