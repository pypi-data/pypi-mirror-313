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

from tikka.domains.entities.node import Node
from tikka.interfaces.adapters.network.connection import NetworkConnectionError
from tikka.interfaces.adapters.network.nodes import (
    NetworkNodesException,
    NetworkNodesInterface,
)


class NetworkNodes(NetworkNodesInterface):
    """
    NetworkNodes class
    """

    def get(self) -> Node:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkNodesInterface.get.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkNodesException(NetworkConnectionError())

        try:
            peer_id = self.connections.rpc.client.rpc_request(
                "system_localPeerId", []
            ).get("result")
        except Exception as exception:
            logging.exception(exception)
            raise NetworkNodesException(exception)

        try:
            current_block = self.connections.rpc.client.rpc_request(
                "system_syncState", []
            ).get("result")["currentBlock"]
        except Exception as exception:
            logging.exception(exception)
            raise NetworkNodesException(exception)

        try:
            current_epoch_result = self.connections.rpc.client.query(
                "Babe", "EpochIndex"
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkNodesException(exception)

        unsafe_api_exposed = True
        # try:
        #     result = self.connections.rpc.client.rpc_request(
        #         "author_hasSessionKeys", [""]
        #     ).get("result")
        # except Exception as exception:
        #     logging.exception(exception)
        #     unsafe_api_exposed = False

        try:
            self.connections.rpc.client.rpc_request("babe_epochAuthorship", []).get(
                "result"
            )
        except Exception as exception:
            logging.exception(exception)
            unsafe_api_exposed = False

        return Node(
            self.connections.rpc.client.url,
            peer_id=peer_id,
            block=current_block,
            software=self.connections.rpc.client.name,
            software_version=self.connections.rpc.client.version,
            epoch_index=current_epoch_result.value,
            unsafe_api_exposed=unsafe_api_exposed,
        )
