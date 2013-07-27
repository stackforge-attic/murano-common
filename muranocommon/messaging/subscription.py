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

from message import Message


class Subscription(object):
    def __init__(self, client, queue, prefetch_count=1):
        self._client = client
        self._queue = queue
        self._promise = None
        self._prefetch_count = prefetch_count

    def __enter__(self):
        self._promise = self._client.basic_consume(
            queue=self._queue,
            prefetch_count=self._prefetch_count)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        promise = self._client.basic_cancel(self._promise)
        self._client.wait(promise)
        return False

    def get_message(self, timeout=None):
        if not self._promise:
            raise RuntimeError(
                "Subscription object must be used within 'with' block")
        msg_handle = self._client.wait(self._promise, timeout=timeout)
        if msg_handle is None:
            return None
        msg = Message(self._client, msg_handle)
        return msg
