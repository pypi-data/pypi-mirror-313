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
from typing import Dict, List

from substrateinterface import Keypair
from substrateinterface.exceptions import SubstrateRequestException

from tikka.domains.entities.authorities import AuthorityStatus
from tikka.interfaces.adapters.network.authorities import (
    NetworkAuthoritiesException,
    NetworkAuthoritiesInterface,
)
from tikka.interfaces.adapters.network.connection import NetworkConnectionError


class NetworkAuthorities(NetworkAuthoritiesInterface):
    """
    NetworkAuthorities class
    """

    def rotate_keys(self) -> str:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.rotate_keys.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkAuthoritiesException(NetworkConnectionError())

        try:
            result = self.connections.rpc.client.rpc_request("author_rotateKeys", [])
        except Exception as exception:
            logging.exception(exception)
            if len(exception.args) > 0 and isinstance(exception.args[0], dict):
                exception = exception.args[0]["message"]
            raise NetworkAuthoritiesException(exception)

        if result is None:
            raise NetworkAuthoritiesException("No result from author_rotateKeys")

        return result.get("result")

    def has_session_keys(self, session_keys: str) -> bool:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.has_session_keys.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkAuthoritiesException(NetworkConnectionError())

        try:
            result = self.connections.rpc.client.rpc_request(
                "author_hasSessionKeys", [session_keys]
            ).get("result")
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAuthoritiesException(exception)

        return result

    def publish_session_keys(self, keypair: Keypair, session_keys: str) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.publish_session_keys.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkAuthoritiesException(NetworkConnectionError())

        session_keys_bytearray = bytearray.fromhex(session_keys)
        params = {
            "keys": {
                "grandpa": f"0x{session_keys_bytearray[0:32].hex()}",
                "babe": f"0x{session_keys_bytearray[32:64].hex()}",
                "im_online": f"0x{session_keys_bytearray[64:96].hex()}",
                "authority_discovery": f"0x{session_keys_bytearray[96:128].hex()}",
            }
        }

        try:
            call = self.connections.rpc.client.compose_call(
                call_module="AuthorityMembers",
                call_function="set_session_keys",
                call_params=params,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAuthoritiesException(exception)

        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=keypair
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAuthoritiesException(exception)

        try:
            # fixme: code stuck infinitely if no blocks are created on blockchain
            #       should have a timeout option
            result = self.connections.rpc.client.submit_extrinsic(
                extrinsic, wait_for_inclusion=True
            )
        except SubstrateRequestException as exception:
            logging.exception(exception)
            raise NetworkAuthoritiesException(exception)

        logging.debug(
            "Extrinsic '%s' sent and included in block '%s'",
            result.extrinsic_hash,
            result.block_hash,
        )

        if result.is_success is False:
            logging.error(result.error_message)
            raise NetworkAuthoritiesException(result.error_message["name"])

    def go_online(self, keypair: Keypair) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.go_online.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkAuthoritiesException(NetworkConnectionError())

        try:
            call = self.connections.rpc.client.compose_call(
                call_module="AuthorityMembers",
                call_function="go_online",
                call_params=None,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAuthoritiesException(exception)

        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=keypair
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAuthoritiesException(exception)

        try:
            # fixme: code stuck infinitely if no blocks are created on blockchain
            #       should have a timeout option
            result = self.connections.rpc.client.submit_extrinsic(
                extrinsic, wait_for_inclusion=True
            )
            logging.debug(
                "Extrinsic '%s' sent and included in block '%s'",
                result.extrinsic_hash,
                result.block_hash,
            )
        except SubstrateRequestException as exception:
            logging.exception(exception)
            raise NetworkAuthoritiesException(exception)

        if result.is_success is False:
            logging.error(result.error_message)
            raise NetworkAuthoritiesException(result.error_message["name"])

    def go_offline(self, keypair: Keypair) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.go_offline.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkAuthoritiesException(NetworkConnectionError())

        try:
            call = self.connections.rpc.client.compose_call(
                call_module="AuthorityMembers",
                call_function="go_offline",
                call_params=None,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAuthoritiesException(exception)

        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=keypair
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAuthoritiesException(exception)

        try:
            # fixme: code stuck infinitely if no blocks are created on blockchain
            #       should have a timeout option
            result = self.connections.rpc.client.submit_extrinsic(
                extrinsic, wait_for_inclusion=True
            )
            logging.debug(
                "Extrinsic '%s' sent and included in block '%s'",
                result.extrinsic_hash,
                result.block_hash,
            )
        except SubstrateRequestException as exception:
            logging.exception(exception)
            raise NetworkAuthoritiesException(exception)

        if result.is_success is False:
            logging.error(result.error_message)
            raise NetworkAuthoritiesException(result.error_message["name"])

    def get_status(self, identity_index: int) -> AuthorityStatus:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.get_status.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkAuthoritiesException(NetworkConnectionError())

        status = AuthorityStatus.OFFLINE
        storage_keys = [
            self.connections.rpc.client.create_storage_key(
                "AuthorityMembers", "OnlineAuthorities"
            ),
            self.connections.rpc.client.create_storage_key(
                "AuthorityMembers", "IncomingAuthorities"
            ),
            self.connections.rpc.client.create_storage_key(
                "AuthorityMembers", "OutgoingAuthorities"
            ),
        ]
        try:
            multi_result = self.connections.rpc.client.query_multi(storage_keys)
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAuthoritiesException(exception)

        online_authorities = multi_result[0][1].value
        incoming_authorities = multi_result[1][1].value
        outgoing_authorities = multi_result[3][1].value

        if identity_index in online_authorities:
            status = AuthorityStatus.ONLINE
        elif identity_index in incoming_authorities:
            status = AuthorityStatus.INCOMING
        elif identity_index in outgoing_authorities:
            status = AuthorityStatus.OUTGOING

        return status

    def get_all(self) -> Dict[int, List[int]]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.get_all.__doc__
        )
        all_by_status = {}

        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkAuthoritiesException(NetworkConnectionError())

        storage_keys = [
            self.connections.rpc.client.create_storage_key(
                "AuthorityMembers", "OnlineAuthorities"
            ),
            self.connections.rpc.client.create_storage_key(
                "AuthorityMembers", "IncomingAuthorities"
            ),
            self.connections.rpc.client.create_storage_key(
                "AuthorityMembers", "OutgoingAuthorities"
            ),
        ]
        try:
            multi_result = self.connections.rpc.client.query_multi(storage_keys)
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAuthoritiesException(exception)

        all_by_status[AuthorityStatus.ONLINE.value] = multi_result[0][1].value
        all_by_status[AuthorityStatus.INCOMING.value] = multi_result[1][1].value
        all_by_status[AuthorityStatus.OUTGOING.value] = multi_result[2][1].value

        return all_by_status
