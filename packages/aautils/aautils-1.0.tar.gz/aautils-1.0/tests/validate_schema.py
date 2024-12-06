#!/usr/bin/env python3
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: Red Hat Inc. 2022
# Author: Beraldo Leal <bleal@redhat.com>
"""
Validates autil YAML files against our schema.

For now, JSON Schemas are being used to validate YAML documents.
"""

import glob
import sys

import yaml
from jsonschema import exceptions, validate


def validate_yaml(filename, schema):
    """Validate a yaml file against a specific schema."""
    print(f"Validating {filename}...")
    with open(filename, "rb") as fp_data, open(schema, "rb") as fp_schema:
        data = fp_data.read()
        schema = fp_schema.read()

    validate(
        yaml.load(data, Loader=yaml.SafeLoader),
        yaml.load(schema, Loader=yaml.SafeLoader),
    )


def validate_yamls():
    """Validates all yamls in the repo against the autils schema."""
    print("Starting validation...")
    failed = False
    for file in glob.glob("./metadata/autils/*/*.yml"):
        try:
            validate_yaml(file, "./schemas/autils.schema")
        except exceptions.ValidationError as err:
            print(file, err.message)
            failed = True

    if failed:
        print("ERROR: Failed to validate all files.")
        return 1

    print("All files passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(validate_yamls())
