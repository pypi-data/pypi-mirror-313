# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import logging
from typing import Optional

from tikka.adapters.network.thread_safe_substrate_interface import (
    ThreadSafeSubstrateInterface,
)
from tikka.domains.entities.node import Node
from tikka.interfaces.adapters.network.connection import ConnectionInterface

# websocket timeout
RPC_CONNECTION_TIMEOUT = 30


class RPCConnection(ConnectionInterface):
    """
    RPCConnection class
    """

    def __init__(self) -> None:
        """
        Init RPCConnection instance

        RPC client is available in self.client after connect()
        """
        self.client: Optional[ThreadSafeSubstrateInterface] = None

    def connect(self, node: Node) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            ConnectionInterface.connect.__doc__
        )
        try:
            # fixme:    use type_registry_preset='default' to fix error on Type MultiAddress
            #           https://github.com/polkascan/py-substrate-interface/issues/110
            self.client = ThreadSafeSubstrateInterface(
                url=node.url, ws_options={"timeout": RPC_CONNECTION_TIMEOUT}
            )
        except Exception as exception:
            self.client = None
            logging.exception(exception)

        if self.client is not None:
            # fixme: workaround for a decode error with fees see #7
            self.client.config["rpc_methods"] = self.client.rpc_request(
                "rpc_methods", []
            )["result"]["methods"]
            self.client.config["rpc_methods"].remove("state_call")

    def disconnect(self) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            ConnectionInterface.disconnect.__doc__
        )
        if self.client is not None:
            self.client.close()
            self.client = None

    def is_connected(self) -> bool:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            ConnectionInterface.is_connected.__doc__
        )
        return self.client is not None
