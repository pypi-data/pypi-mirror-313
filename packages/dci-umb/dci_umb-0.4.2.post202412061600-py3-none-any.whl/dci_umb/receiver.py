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
from dci_umb.bus import Bus
from dci_umb.handler import HTTPBouncerMessageHandler


logger = logging.getLogger(__name__)


class Receiver(MessagingHandler):
    def __init__(self, params):
        super(Receiver, self).__init__()
        handlers = []
        for destination in params.get("destinations"):
            handlers.append(HTTPBouncerMessageHandler(destination=destination))
        self.bus = Bus(handlers=handlers)
        self.crt_file = params.get("crt_file")
        self.key_file = params.get("key_file")
        self.ca_file = params.get("ca_file")
        self.brokers = params.get("brokers")
        self.sources = params.get("sources")

    def on_start(self, event):
        logger.debug("on_start")
        domain = SSLDomain(SSLDomain.MODE_CLIENT)
        domain.set_credentials(self.crt_file, self.key_file, None)
        domain.set_trusted_ca_db(self.ca_file)
        domain.set_peer_authentication(SSLDomain.VERIFY_PEER)
        conn = event.container.connect(urls=self.brokers, ssl_domain=domain)
        for source in self.sources:
            event.container.create_receiver(conn, source=source)

    def on_message(self, event):
        self.bus.dispatch_event(event)

    def on_link_opened(self, event):
        logger.debug("on_link_opened")
        logger.debug("event.connection.hostname: %s" % event.connection.hostname)
        logger.debug(
            "event.receiver.source.address: %s" % event.receiver.source.address
        )

    def on_link_error(self, event):
        logger.debug("on_link_error")
        logger.debug("link error: %s" % event.link.remote_condition.name)
        logger.debug(event.link.remote_condition.description)
        logger.debug("closing connection to: %s" % event.connection.hostname)
        event.connection.close()

    def on_transport_error(self, event):
        logger.debug("on_transport_error")
        logger.debug(event)
        condition = event.transport.condition
        if condition:
            logger.debug(
                "transport error: %s: %s" % (condition.name, condition.description)
            )
            if condition.name in self.fatal_conditions:
                logger.debug("fatal error, close connection")
                event.connection.close()
        else:
            logger.debug("unspecified transport error")
