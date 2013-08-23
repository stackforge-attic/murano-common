#    Copyright (c) 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import unittest2 as unittest

from muranocommon.tests.helpers import TokenCleaner


class SecureDescriptionTests(unittest.TestCase):
    cleaner = TokenCleaner()

    def test_dict_with_one_value(self):
        source = {'token': 'value'}
        value = self.cleaner.clean(source)
        self.assertEqual(value['token'], self.cleaner.filler)

    def test_dict_with_few_value(self):
        source = {'token': 'value', 'pass': 'value'}
        value = self.cleaner.clean(source)
        self.assertEqual(value['token'], self.cleaner.filler)
        self.assertEqual(value['pass'], self.cleaner.filler)

    def test_dict_with_nested_dict(self):
        source = {'obj': {'pass': 'value'}}
        value = self.cleaner.clean(source)
        self.assertEqual(value['obj']['pass'], self.cleaner.filler)

    def test_dict_with_nested_list(self):
        source = {'obj': [{'pass': 'value'}]}
        value = self.cleaner.clean(source)
        self.assertEqual(value['obj'][0]['pass'], self.cleaner.filler)

    def test_leave_out_other_values(self):
        source = {'obj': ['value']}
        value = self.cleaner.clean(source)
        self.assertEqual(value['obj'][0], 'value')