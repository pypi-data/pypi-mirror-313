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

from substrateinterface import ExtrinsicReceipt, Keypair
from substrateinterface.exceptions import SubstrateRequestException

from tikka.interfaces.adapters.network.connection import NetworkConnectionError
from tikka.interfaces.adapters.network.transfers import (
    NetworkTransfersException,
    NetworkTransfersInterface,
)


class NetworkTransfers(NetworkTransfersInterface):
    """
    NetworkTransfers class
    """

    def send(
        self, sender_keypair: Keypair, recipient_address: str, amount: int
    ) -> Optional[ExtrinsicReceipt]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkTransfersInterface.send.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkTransfersException(NetworkConnectionError())

        params = {"" "dest": recipient_address, "value": amount}
        try:
            call = self.connections.rpc.client.compose_call(
                call_module="Balances",
                call_function="transfer_keep_alive",
                call_params=params,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)

        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=sender_keypair
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)

        try:
            # fixme: code stuck infinitely if no blocks are created on blockchain
            #       should have a timeout option
            receipt = self.connections.rpc.client.submit_extrinsic(
                extrinsic, wait_for_inclusion=True, wait_for_finalization=False
            )
            logging.debug(
                "Extrinsic '%s' sent and included in block '%s'",
                receipt.extrinsic_hash,
                receipt.block_hash,
            )
        except SubstrateRequestException as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)

        if receipt.is_success is False:
            logging.error(receipt.error_message)
            raise NetworkTransfersException(receipt.error_message["name"])

        return receipt

    def send_with_comment(
        self, sender_keypair: Keypair, recipient_address: str, amount: int, comment: str
    ) -> Optional[ExtrinsicReceipt]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkTransfersInterface.send_with_comment.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkTransfersException(NetworkConnectionError())

        transfer_params = {"dest": recipient_address, "value": amount}
        try:
            transfer_call = self.connections.rpc.client.compose_call(
                call_module="Balances",
                call_function="transfer_keep_alive",
                call_params=transfer_params,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)

        remark_params = {"remark": comment}
        try:
            remark_call = self.connections.rpc.client.compose_call(
                call_module="System",
                call_function="remark_with_event",
                call_params=remark_params,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)

        try:
            call = self.connections.rpc.client.compose_call(
                call_module="Utility",
                call_function="batch",
                call_params={"calls": [transfer_call, remark_call]},
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)
        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=sender_keypair
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)

        try:
            # fixme: code stuck infinitely if no blocks are created on blockchain
            #       should have a timeout option
            receipt = self.connections.rpc.client.submit_extrinsic(
                extrinsic, wait_for_inclusion=True, wait_for_finalization=False
            )
            logging.debug(
                "Extrinsic '%s' sent and included in block '%s'",
                receipt.extrinsic_hash,
                receipt.block_hash,
            )
        except SubstrateRequestException as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)

        if receipt.is_success is False:
            logging.error(receipt.error_message)
            raise NetworkTransfersException(receipt.error_message["name"])

        return receipt

    def fees(
        self, sender_keypair: Keypair, recipient_address: str, amount: int
    ) -> Optional[int]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkTransfersInterface.fees.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkTransfersException(NetworkConnectionError())

        params = {"dest": recipient_address, "value": amount}
        try:
            call = self.connections.rpc.client.compose_call(
                call_module="Balances",
                call_function="transfer_keep_alive",
                call_params=params,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)

        try:
            # Get payment info
            payment_info = self.connections.rpc.client.get_payment_info(
                call=call, keypair=sender_keypair
            )
        except SubstrateRequestException as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)

        if payment_info is None:
            return None

        return payment_info["partialFee"]

    def transfer_all(
        self, sender_keypair: Keypair, recipient_address: str, keep_alive: bool = False
    ) -> Optional[ExtrinsicReceipt]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkTransfersInterface.transfer_all.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkTransfersException(NetworkConnectionError())

        params = {"dest": recipient_address, "keep_alive": keep_alive}
        try:
            call = self.connections.rpc.client.compose_call(
                call_module="Balances",
                call_function="transfer_all",
                call_params=params,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)

        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=sender_keypair
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)

        try:
            # fixme: code stuck infinitely if no blocks are created on blockchain
            #       should have a timeout option
            receipt = self.connections.rpc.client.submit_extrinsic(
                extrinsic, wait_for_inclusion=True
            )
            logging.debug(
                "Extrinsic '%s' sent and included in block '%s'",
                receipt.extrinsic_hash,
                receipt.block_hash,
            )
        except SubstrateRequestException as exception:
            logging.exception(exception)
            raise NetworkTransfersException(exception)

        if receipt.is_success is False:
            logging.error(receipt.error_message)
            raise NetworkTransfersException(receipt.error_message["name"])

        return receipt
