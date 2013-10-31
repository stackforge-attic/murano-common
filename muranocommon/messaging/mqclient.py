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

from eventlet import patcher
puka = patcher.import_patched('puka')
import anyjson
from subscription import Subscription


class MqClient(object):
    def __init__(self, login, password, host, port, virtual_host,
                 ssl=False, ca_certs=None):
        scheme = 'amqp:' if not ssl else 'amqps:'

        ssl_parameters = None
        if ssl:
            ssl_parameters = puka.SslConnectionParameters()
            ssl_parameters.ca_certs = ca_certs

        self._client = puka.Client('{0}//{1}:{2}@{3}:{4}/{5}'.format(
            scheme,
            login,
            password,
            host,
            port,
            virtual_host
        ), ssl_parameters=ssl_parameters)
        self._connected = False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def connect(self):
        if not self._connected:
            promise = self._client.connect()
            if self._client.wait(promise, timeout=10) is not None:
                self._connected = True

    def close(self):
        if self._connected:
            promise = self._client.close()
            self._client.wait(promise)
            self._connected = False

    def declare(self, queue, exchange=None):
        promise = self._client.queue_declare(
            str(queue), durable=True, arguments={'x-ha-policy': 'all'}
        )
        self._client.wait(promise)

        if exchange:
            promise = self._client.exchange_declare(
                str(exchange),
                durable=True)
            self._client.wait(promise)
            promise = self._client.queue_bind(
                str(queue), str(exchange), routing_key=str(queue))
            self._client.wait(promise)

    def send(self, message, key, exchange='', timeout=None):
        if not self._connected:
            raise RuntimeError('Not connected to RabbitMQ')

        headers = {'message_id': str(message.id)}

        promise = self._client.basic_publish(
            exchange=str(exchange),
            routing_key=str(key),
            body=anyjson.dumps(message.body),
            headers=headers)
        self._client.wait(promise, timeout=timeout)

    def open(self, queue, prefetch_count=1):
        if not self._connected:
            raise RuntimeError('Not connected to RabbitMQ')

        return Subscription(self._client, queue, prefetch_count)
