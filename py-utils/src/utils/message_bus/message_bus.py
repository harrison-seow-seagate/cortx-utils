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

from cortx.utils.message_bus.message_broker import MessageBrokerFactory
from cortx.utils.message_bus.error import MessageBusError
from cortx.utils.schema import Conf
from cortx.utils.schema.payload import *
import errno


class MessageBus:
    """ Message Bus Framework over various types of Message Brokers """

    conf_file = "/etc/cortx/message_bus.conf"

    def __init__(self):
        """ Initialize a MessageBus and load its configurations """
        try:
            Conf.load('message_bus', Json(self.conf_file))
            self._broker_conf = Conf.get("message_bus", "message_broker")
            broker_type = self._broker_conf['type']

        except Exception as e:
            raise MessageBusError(errno.EINVAL, "Invalid conf in %s. %s",
                self.conf_file, e) 

        self._broker = MessageBrokerFactory.get_instance(broker_type, \
            self._broker_conf)

    def get_client(self, client: str, **client_config):
        """ To create producer/consumer client based on the configurations """
        self._message_broker.get_client(client, **client_config)

    def send(self, messages: list):
        """ Sends list of messages to the configured message broker """
        self._message_broker.send(messages)

    def receive(self) -> list:
        """ Receives messages from the configured message broker """
        return self._message_broker.receive()

    def ack(self):
        """ Provides acknowledgement on offset """
        self._message_broker.ack()
