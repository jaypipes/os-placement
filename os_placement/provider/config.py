# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

import yaml

MIN_SCHEMA_VERSION = "1.0"

class ProviderInventoryConfig(object):
    def __init__(schema_version, resource_class, data):
        self.schema_version = schema_version
        self.resource_class = resource_class
        self.total = data.get("total")
        self.reserved = data.get("reserved")
        self.min_unit = data.get("min_unit")
        self.max_unit = data.get("max_unit")
        self.step_size = data.get("step_size")
        self.allocation_ratio = data.get("allocation_ratio")


class ProviderTraitsConfig(object):
    def __init__(schema_version, data):
        self.schema_version = schema_version
        self.always = data.get("always")
        self.ignore = data.get("ignore")


class ProviderConfig(object):
    def __init__(data):
        schema_version = data.get("schema_version", MIN_SCHEMA_VERSION)
        self.schema_version = schema_version
        self.uuid = data.get("uuid")
        self.name = data.get("name")
        self.parent = data.get("parent")
        inventories = data.get("inventories")
        if inventories:
            self.inventories = {
                resource_class: ProviderInventoryConfig(
                    schema_version, resource_class, inv_data)
                for resource_class, inv_data in inventories.items()
            }
        traits = data.get("traits")
        if traits:
            self.traits = ProviderTraitsConfig(schema_version, traits)


def from_file(path):
    """Loads a provider.yaml file and returns a `ProviderConfig` object
    representing the resource provider's configuration information.

    :param path: string path to the filename to load

    :raises ValueError: if the file could not be found or could not be read
                        properly
    """
    if not os.path.exists(path):
        raise ValueError("Provider configuration file %s not found." % path)

    with open(path, 'rb') as f:
        try:
            data = yaml.load(f)
        except yaml.YAMLError as e:
            msg = "failed to read configuration file %s. Got error: %s"
            msg = msg % (path, str(e))
            raise ValueError(msg)

    return ProviderConfig(data)
