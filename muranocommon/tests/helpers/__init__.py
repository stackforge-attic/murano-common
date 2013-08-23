# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import types


class TokenCleaner():
    def __init__(self, tokens=('token', 'pass'), filler='<SANITIZED>'):
        self._tokens = tokens
        self._filler = filler

    @property
    def tokens(self):
        return self._tokens

    @property
    def filler(self):
        return self._filler

    def contains_token(self, value):
        for token in self.tokens:
            if token in value.lower():
                return True
        return False

    def clean(self, obj):
        if isinstance(obj, types.DictType):
            return dict([self.clean(item) for item in obj.iteritems()])
        elif isinstance(obj, types.ListType):
            return [self.clean(item) for item in obj]
        elif isinstance(obj, types.TupleType):
            k, v = obj
            if self.contains_token(k) and isinstance(v, types.StringTypes):
                return k, self.filler
            return k, self.clean(v)
        else:
            return obj