# Copyright 2019 Red Hat
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import logging

from proton import SSLDomain
from proton.handlers import MessagingHandler
from proton.reactor import Container
from proton import Message


logger = logging.getLogger(__name__)


class Sender(MessagingHandler):
    def __init__(self, params):
        super(Sender, self).__init__()
        self.crt_file = params.get("crt_file")
        self.key_file = params.get("key_file")
        self.ca_file = params.get("ca_file")
        self.brokers = params.get("brokers")
        self.target = params.get("target")
        self.message = params.get("message")

    def on_start(self, event):
        logger.debug("on_start")
        domain = SSLDomain(SSLDomain.MODE_CLIENT)
        domain.set_credentials(self.crt_file, self.key_file, None)
        domain.set_trusted_ca_db(self.ca_file)
        domain.set_peer_authentication(SSLDomain.VERIFY_PEER)
        conn = event.container.connect(urls=self.brokers, ssl_domain=domain)
        event.container.create_sender(conn, target=self.target)

    def on_sendable(self, event):
        logger.debug("on_sendable: send message")
        logger.debug(self.message)
        event.sender.send(Message(body=self.message))
        event.sender.close()

    def on_accepted(self, event):
        logger.debug("on_accepted: message accepted")
        event.connection.close()


def send(params):
    Container(Sender(params)).run()
