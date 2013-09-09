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

import anyjson
import logging

log = logging.getLogger("murano-common.messaging")


class Message(object):
    def __init__(self, client=None, message_handle=None):
        self._client = client
        self._message_handle = message_handle
        self.id = None if message_handle is None else \
            message_handle['headers'].get('message_id')
        try:
            self.body = None if message_handle is None else \
                anyjson.loads(message_handle['body'])
        except ValueError as e:
            self.body = None
            log.exception(e)

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value or ''

    def ack(self):
        self._client.basic_ack(self._message_handle)
