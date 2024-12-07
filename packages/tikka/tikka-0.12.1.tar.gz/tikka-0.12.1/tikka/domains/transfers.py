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
from typing import Optional

from substrateinterface import ExtrinsicReceipt, Keypair

from tikka.domains.entities.events import TransferEvent
from tikka.domains.events import EventDispatcher
from tikka.domains.wallets import Wallets
from tikka.interfaces.adapters.network.transfers import NetworkTransfersInterface


class Transfers:
    """
    Transfers domain class
    """

    def __init__(
        self,
        wallets: Wallets,
        network: NetworkTransfersInterface,
        event_dispatcher: EventDispatcher,
    ):
        """
        Init Transfers domain

        :param wallets: Wallets domain
        :param network: NetworkTransfersInterface adapter instance
        :param event_dispatcher: EventDispatcher instance
        """
        self.wallets = wallets
        self.network = network
        self.event_dispatcher = event_dispatcher

    def network_fees(
        self, sender_keypair: Keypair, recipient_address: str, amount: int
    ) -> Optional[int]:
        """
        Fetch transfer fees from network and return it if request is successful

        :param sender_keypair: Sender Keypair instance
        :param recipient_address: Recipient address
        :param amount: Amount in blockchain unit
        :return:
        """
        return self.network.fees(sender_keypair, recipient_address, amount)

    def network_send(
        self, sender_keypair: Keypair, recipient_address: str, amount: int
    ) -> Optional[ExtrinsicReceipt]:
        """
        Send transfer to network and return ExtrinsicReceipt if request is successful

        :param sender_keypair: Sender Keypair instance
        :param recipient_address: Recipient address
        :param amount: Amount in blockchain unit
        :return:
        """
        receipt = self.network.send(sender_keypair, recipient_address, amount)

        if receipt is not None and receipt.is_success is True:
            # dispatch event
            event = TransferEvent(
                TransferEvent.EVENT_TYPE_SENT,
            )
            self.event_dispatcher.dispatch_event(event)

        return receipt

    def network_send_with_comment(
        self, sender_keypair: Keypair, recipient_address: str, amount: int, comment: str
    ) -> Optional[ExtrinsicReceipt]:
        """
        Send transfer to network and return ExtrinsicReceipt if request is successful

        :param sender_keypair: Sender Keypair instance
        :param recipient_address: Recipient address
        :param amount: Amount in blockchain unit
        :param comment: Comment from user
        :return:
        """
        receipt = self.network.send_with_comment(
            sender_keypair, recipient_address, amount, comment
        )

        if receipt is not None and receipt.is_success is True:
            # dispatch event
            event = TransferEvent(
                TransferEvent.EVENT_TYPE_SENT,
            )
            self.event_dispatcher.dispatch_event(event)

        return receipt

    def network_send_all(
        self, sender_keypair: Keypair, recipient_address: str, keep_alive: bool = False
    ) -> Optional[ExtrinsicReceipt]:
        """
        Send transfer to network and return ExtrinsicReceipt if request is successful

        :param sender_keypair: Sender Keypair instance
        :param recipient_address: Recipient address
        :param keep_alive: Optional, default False
        :return:
        """
        receipt = self.network.transfer_all(
            sender_keypair, recipient_address, keep_alive
        )

        if receipt is not None and receipt.is_success is True:
            # dispatch event
            event = TransferEvent(
                TransferEvent.EVENT_TYPE_SENT,
            )
            self.event_dispatcher.dispatch_event(event)

        return receipt
