# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""
Helper to extract endpoints of all services to a data JSON file
for rego policies evaluation.

The script lists the removed and added policies."""

import argparse
import itertools
import json
import sys
from pathlib import Path
from typing import Optional

import yaml
from starlette.routing import compile_path

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from datalayer_solr.models.roles import PlatformRoles


HERE = Path(__file__).parent


def _to_cedar(output: Path, defined_operations: dict) -> None:
    # Policies
    output_cedar = output / "cedar" / "policy.cedar"
    operations = itertools.chain.from_iterable(
        grp for grp in defined_operations.values()
    )

    groupby_roles = {None: []}
    for op in operations:
        for role in op.get("roles", [None]):
            if role not in groupby_roles:
                groupby_roles[role] = []
            groupby_roles[role].append(op["action"])

    # Format JSON don't allow multiple policies in the same file !?
    # policies = []
    # for role, actions in groupby_roles.items():
    #     principal = (
    #         {"op": "All"}
    #         if role is None
    #         else {"op": "in", "entity": {"type": "UserRole", "id": role}}
    #     )
    #     policies.append(
    #         {
    #             "effect": "permit",
    #             "principal": principal,
    #             "action": {
    #                 "op": "in",
    #                 "entities": [
    #                     {"type": "Action", "id": action} for action in actions
    #                 ],
    #             },
    #             "resource": {"op": "All"},
    #             "conditions": []
    #         }
    #     )

    # output_cedar.write_text(json.dumps(policies))

    content = ""
    for role, actions in groupby_roles.items():
        content += """
permit (
    principal{},
    action in [
        {}
    ],
    resource
);
""".format(
            "" if role is None else f' in UserRole::"{role}"',
            ",\n        ".join(map(lambda a: f'Action::"{a}"', actions)),
        )

    output_cedar.write_text(content)

    # Partial entities
    entities = []
    for role in PlatformRoles:
        entities.append(
            {"uid": {"type": "UserRole", "id": role.value}, "attrs": {}, "parents": []}
        )
    (output / "cedar" / "entities.json").write_text(json.dumps(entities))


def _data_to_rego(operation: dict) -> dict:
    rego = {"method": operation["method"], "path": operation["path"]}
    if "roles" in operation:
        rego["roles"] = operation["roles"]
    return rego


def _to_rego(output: Path, defined_operations: dict) -> None:
    output_rego = output / "rego" / "endpoints.json"
    operations = [
        map(
            _data_to_rego,
            itertools.chain(grp for grp in defined_operations.values()),
        )
    ]
    output_rego.write_text(json.dumps({"allowed_operations": operations}))


def update_policies_data(
    output_folder: Path,
    format: str,
    selector: str,
    check: bool = False,
    exclude: Optional[frozenset[str]] = None,
) -> None:
    print(f"Extracting routes from '{selector}' in {output_folder!s}")

    orig = dict()
    output = output_folder / "endpoints.json"
    if output.exists():
        orig = json.loads(output.read_text())

    defined_operations = {}
    for spec_file in HERE.parent.parent.rglob(selector):
        if exclude is not None and not exclude.isdisjoint(spec_file.parts):
            print(f"Ignoring file '{spec_file!s}'.")
            continue
        with spec_file.open() as s:
            spec = yaml.load(s, Loader=Loader)
        base_url = next(filter(lambda u: u["url"].startswith("/"), spec["servers"]))[
            "url"
        ]
        defined_operations[base_url] = []
        for path, operations in spec.get("paths").items():
            full_path = base_url + path
            regex_path, _, _ = compile_path(full_path)
            defined_operations[base_url].extend(
                map(
                    lambda o: {
                        "method": o.upper(),
                        "path": regex_path.pattern,
                        "action": "{} {}".format(o.lower(), full_path.lower()),
                    },
                    operations,
                )
            )

    orig_operations = orig
    new = {}
    errors = []
    for category, ops in defined_operations.items():
        new[category] = []
        orig_ops = orig_operations.get(category)
        for op in ops:
            found = False
            for orig_op in orig_ops.copy():
                if orig_op["method"] == op["method"] and orig_op["path"] == op["path"]:
                    # Check all defined roles are valid
                    invalid_roles = []
                    for role in orig_op.get("roles", []):
                        try:
                            PlatformRoles(role)
                        except ValueError:
                            invalid_roles.append(role)
                    if invalid_roles:
                        errors.append(
                            "Rule for {method} {path} has unknown roles: ".format(**op)
                            + ", ".join(invalid_roles)
                        )
                    op.update(orig_op)
                    orig_ops.remove(orig_op)
                    found = True
                    break
            if not found:
                new[category].append(op)

    print("Removed operations:\n", json.dumps(orig_operations, indent=2))
    print("Added operations:\n", json.dumps(new, indent=2))
    if errors:
        print("Some errors occurs:\n" + "\n".join(errors))

    if check:
        if orig_operations or new:
            print("Operations listed for policies are not up to date.")
            sys.exit(1)
    output.write_text(json.dumps(defined_operations, indent=2))

    match format:
        case "cedar":
            _to_cedar(output_folder, defined_operations)

        case "rego":
            _to_rego(output_folder, defined_operations)


def main():
    parser = argparse.ArgumentParser(
        prog="openAPIExtractor",
        description="Update the policies data file with the open API endpoints.",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="cedar",
        choices=["cedar", "rego"],
        help="Policies file format.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=str(HERE.parent.joinpath("datalayer_iam", "policies")),
        help="Folder to update with the policies.",
        type=Path,
    )
    parser.add_argument(
        "-p",
        "--policies",
        default="openapi.yml",
        help="Shell selector for listing openAPI spec files.",
    )
    parser.add_argument(
        "-e", "--exclude", default=["companion", "operator"], help="Path to exclude"
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="If set the file won't be changed but the command will exist with code error if it would have changed.",
    )

    args = parser.parse_args()

    update_policies_data(
        args.output, args.format, args.policies, args.check, frozenset(args.exclude)
    )


if __name__ == "__main__":
    main()
