#!/usr/bin/env python3

# CORTX-Py-Utils: CORTX Python common library.
# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.

from cortx.utils.message_bus import MessageBus


class MessageBusClient:
    """ common infrastruture for producer and consumer """

    def __init__(self, message_bus: MessageBus, **client_conf: dict):
        self._message_bus = message_bus
        self._message_bus.init_client(**client_conf)
        self._client_conf = client_conf

    def _get_conf(self, key):
        if key not in self._client_conf.keys():
            raise MessageBusError(errno.EINVAL, "Invalid entry %s", key) 
        return self._client_conf[key]

    def send(self, messages: str):
        message_type = self._get_conf('message_type')
        method = self._get_conf('method')
        self._message_bus.send(messages, message_type, method)

    def receive(self) -> list:
        return self._message_bus.receive()

    def ack(self):
        self._message_bus.ack()


class MessageProducer(MessageBusClient):
    """ A client that publishes messages """

    def __init__(self, message_bus: MessageBus, producer_id: str, \
        message_type: str, method: str = None):
        """ Initialize a Message Producer

        Parameters:
        message_bus     An instance of message bus class.
        producer_id     A String that represents Producer client ID.
        message_type    This is essentially equivalent to the
                        queue/topic name. For e.g. ["Alert"]
        """
        super().__init__(message_bus, client_type='producer', \
            client_id=producer_id, message_type=message_type, method=method)


class MessageConsumer(MessageBusClient):
    """ A client that consumes messages """

    def __init__(self, message_bus: MessageBus, consumer_id: str, \
        consumer_group: str, message_type: str, auto_ack: str, offset: str):
        """ Initialize a Message Consumer

        Parameters:
        message_bus     An instance of message bus class.
        consumer_id     A String that represents Consumer client ID.
        consumer_group  A String that represents Consumer Group ID.
                        Group of consumers can process messages
        message_type    This is essentially equivalent to the queue/topic name.
                        For e.g. ["Alert"]
        offset          Can be set to "earliest" (default) or "latest".
                        ("earliest" will cause messages to be read from the beginning)
        """
        super().__init__(message_bus, client_type='consumer', \
            client_id=consumer_id, consumer_group=consumer_group, \
            message_type=message_type, offset=offset)