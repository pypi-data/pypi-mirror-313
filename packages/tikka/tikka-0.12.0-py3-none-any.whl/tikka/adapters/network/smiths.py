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
from datetime import datetime, timedelta
from typing import List, Optional

from substrateinterface import Keypair
from substrateinterface.exceptions import SubstrateRequestException

from tikka.domains.entities.smith import Smith, SmithStatus
from tikka.interfaces.adapters.network.connection import NetworkConnectionError
from tikka.interfaces.adapters.network.smiths import (
    NetworkSmithsException,
    NetworkSmithsInterface,
)


class NetworkSmiths(NetworkSmithsInterface):
    """
    NetworkSmiths class
    """

    status_map = {
        "Invited": SmithStatus.INVITED,
        "Pending": SmithStatus.PENDING,
        "Smith": SmithStatus.SMITH,
        "Excluded": SmithStatus.EXCLUDED,
    }

    def get_smith(self, identity_index: int) -> Optional[Smith]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkSmithsInterface.get_smith.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkSmithsException(NetworkConnectionError())

        try:
            result = self.connections.rpc.client.query(
                "SmithMembers", "Smiths", [identity_index]
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkSmithsException(exception)

        smith = None
        if result.value is not None:
            if result.value["expires_on"] is not None:
                expire_on_datetime = self.get_datetime_from_epoch(
                    result.value["expires_on"]
                )
            else:
                expire_on_datetime = None
            smith = Smith(
                identity_index=identity_index,
                status=self.status_map[result.value["status"]],
                expire_on=expire_on_datetime,
                certifications_received=result.value["received_certs"],
                certifications_issued=result.value["issued_certs"],
            )

        return smith

    def get_smiths(self, identity_indice: List[int]) -> List[Optional[Smith]]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkSmithsInterface.get_smiths.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkSmithsException(NetworkConnectionError())

        storage_keys = []
        for identity_index in identity_indice:
            storage_keys.append(
                self.connections.rpc.client.create_storage_key(
                    "SmithMembers", "Smiths", [identity_index]
                )
            )

        try:
            multi_result = self.connections.rpc.client.query_multi(storage_keys)
        except Exception as exception:
            logging.exception(exception)
            raise NetworkSmithsException(exception)

        smiths: List[Optional[Smith]] = []
        for index, (storage_key, value_obj) in enumerate(multi_result):
            if value_obj.value is not None:
                if value_obj.value["expires_on"] is not None:
                    expire_on_datetime = self.get_datetime_from_epoch(
                        value_obj.value["expires_on"]
                    )
                else:
                    expire_on_datetime = None
                smiths.append(
                    Smith(
                        identity_index=storage_keys[index].params[0],
                        status=self.status_map[value_obj.value["status"]],
                        expire_on=expire_on_datetime,
                        certifications_received=value_obj.value["received_certs"],
                        certifications_issued=value_obj.value["issued_certs"],
                    )
                )
            else:
                smiths.append(None)

        return smiths

    def invite(self, keypair: Keypair, identity_index: int) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkSmithsInterface.invite.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkSmithsException(NetworkConnectionError())

        params = {
            "receiver": identity_index,
        }

        try:
            call = self.connections.rpc.client.compose_call(
                call_module="SmithMembers",
                call_function="invite_smith",
                call_params=params,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkSmithsException(exception)

        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=keypair
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkSmithsException(exception)

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
            raise NetworkSmithsException(exception)

        if result.is_success is False:
            logging.error(result.error_message)
            raise NetworkSmithsException(result.error_message["name"])

    def accept_invitation(self, keypair: Keypair) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkSmithsInterface.accept_invitation.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkSmithsException(NetworkConnectionError())

        try:
            call = self.connections.rpc.client.compose_call(
                call_module="SmithMembers",
                call_function="accept_invitation",
                call_params=None,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkSmithsException(exception)

        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=keypair
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkSmithsException(exception)

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
            raise NetworkSmithsException(exception)

        if result.is_success is False:
            raise NetworkSmithsException(result.error_message["name"])

    def certify(self, keypair: Keypair, identity_index: int) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkSmithsInterface.certify.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkSmithsException(NetworkConnectionError())

        params = {
            "receiver": identity_index,
        }

        try:
            call = self.connections.rpc.client.compose_call(
                call_module="SmithMembers",
                call_function="certify_smith",
                call_params=params,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkSmithsException(exception)

        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=keypair
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkSmithsException(exception)

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
        if result.is_success is False:
            logging.error(result.error_message)
            raise NetworkSmithsException(result.error_message["name"])

    def get_datetime_from_epoch(self, epoch_index: int) -> Optional[datetime]:
        """
        Return a datetime object from an epoch index

        :param epoch_index: Epoch number
        :return:
        """
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkSmithsException(NetworkConnectionError())

        try:
            result = self.connections.rpc.client.get_constant("Babe", "EpochDuration")
        except Exception as exception:
            logging.exception(exception)
            raise NetworkSmithsException(exception)

        epoch_duration_in_blocks = result.value

        try:
            result = self.connections.rpc.client.get_constant(
                "Babe", "ExpectedBlockTime"
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkSmithsException(exception)

        block_duration_in_ms = result.value
        epoch_duration_in_ms = epoch_duration_in_blocks * block_duration_in_ms

        try:
            current_epoch_result = self.connections.rpc.client.query(
                "Babe", "EpochIndex"
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkSmithsException(exception)
        current_epoch_index = current_epoch_result.value

        current_time = datetime.now()
        epoch_diff = epoch_index - current_epoch_index
        if epoch_diff < 0:
            block_time = current_time - timedelta(
                milliseconds=abs(epoch_diff) * epoch_duration_in_ms
            )
        else:
            block_time = current_time + timedelta(
                milliseconds=abs(epoch_diff) * epoch_duration_in_ms
            )

        return block_time
