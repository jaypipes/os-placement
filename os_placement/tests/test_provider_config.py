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

from os_placement.provider import config
from os_placement.tests import base


TEST_DIR = os.path.dirname(os.path.realpath(__file__))
SCHEMA_V1_0_PATH = os.path.join(TEST_DIR, 'provider-1.0.yaml')


class TestFromFile(base.TestCase):

    def test_schema_v1_0(self):
        cfg = config.from_file(SCHEMA_V1_0_PATH)
        self.assertEqual('1.0', cfg.schema_version)
        self.assertIsNotNone(cfg.uuid)
        self.assertEqual('b0d8feb1-1389-4c61-b8a8-52030847da27', cfg.uuid)
        self.assertIsNotNone(cfg.name)
        self.assertEqual('zoneA.row1.rack13.compute26', cfg.name)
        self.assertIsNone(cfg.parent)

        self.assertIsNotNone(cfg.inventories)
        self.assertEqual(3, len(cfg.inventories))

        cpu_inv = cfg.inventories['VCPU']
        self.assertIsInstance(cpu_inv, config.ProviderInventoryConfig)
        self.assertEqual('1.0', cpu_inv.schema_version)
        self.assertEqual('VCPU', cpu_inv.resource_class)
        self.assertIsNone(cpu_inv.total)
        self.assertIsNotNone(cpu_inv.max_unit)
        self.assertEqual(12, cpu_inv.max_unit)

        ram_inv = cfg.inventories['MEMORY_MB']
        self.assertIsInstance(ram_inv, config.ProviderInventoryConfig)
        self.assertEqual('1.0', ram_inv.schema_version)
        self.assertEqual('MEMORY_MB', ram_inv.resource_class)
        self.assertIsNone(ram_inv.total)
        self.assertIsNotNone(ram_inv.reserved)
        self.assertEqual(256, ram_inv.reserved)
        self.assertIsNotNone(ram_inv.min_unit)
        self.assertEqual(64, ram_inv.min_unit)
        self.assertIsNotNone(ram_inv.max_unit)
        self.assertEqual(16384, ram_inv.max_unit)
        self.assertIsNotNone(ram_inv.step_size)
        self.assertEqual(64, ram_inv.step_size)
        self.assertIsNone(ram_inv.allocation_ratio)

        disk_inv = cfg.inventories['DISK_GB']
        self.assertIsInstance(disk_inv, config.ProviderInventoryConfig)
        self.assertEqual('1.0', disk_inv.schema_version)
        self.assertEqual('DISK_GB', disk_inv.resource_class)
        self.assertIsNotNone(disk_inv.total)
        self.assertEqual(2000, disk_inv.total)
        self.assertIsNotNone(disk_inv.reserved)
        self.assertEqual(100, disk_inv.reserved)
        self.assertIsNotNone(disk_inv.min_unit)
        self.assertEqual(100, disk_inv.min_unit)
        self.assertIsNotNone(disk_inv.max_unit)
        self.assertEqual(1000, disk_inv.max_unit)
        self.assertIsNotNone(disk_inv.step_size)
        self.assertEqual(100, disk_inv.step_size)
        self.assertIsNotNone(disk_inv.allocation_ratio)
        self.assertEqual(1.0, disk_inv.allocation_ratio)

    def test_file_not_found(self):
        self.assertRaises(ValueError, config.from_file,
                          '/garbage/filepath/xaqlojalas')
