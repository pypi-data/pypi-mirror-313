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
import sys
from typing import Optional

import qrcode
from PyQt5.QtCore import QMutex, QPoint
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.address import DisplayAddress
from tikka.domains.entities.constants import AMOUNT_UNIT_KEY, DATA_PATH
from tikka.domains.entities.events import AccountEvent, TransferEvent, UnitEvent
from tikka.domains.entities.identity import IdentityStatus
from tikka.domains.entities.smith import SmithStatus
from tikka.slots.pyqt.entities.constants import (
    ADDRESS_MONOSPACE_FONT_NAME,
    ICON_ACCOUNT_NO_WALLET,
    ICON_ACCOUNT_WALLET_LOCKED,
    ICON_ACCOUNT_WALLET_UNLOCKED,
    SELECTED_UNIT_PREFERENCES_KEY,
)
from tikka.slots.pyqt.entities.qrcode_image import QRCodeImage
from tikka.slots.pyqt.entities.worker import AsyncQWorker
from tikka.slots.pyqt.resources.gui.widgets.account_rc import Ui_AccountWidget
from tikka.slots.pyqt.widgets.account_menu import AccountPopupMenu
from tikka.slots.pyqt.windows.transfer import TransferWindow


class AccountWidget(QWidget, Ui_AccountWidget):
    """
    AccountWidget class
    """

    def __init__(
        self,
        application: Application,
        account: Account,
        mutex: QMutex,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Init AccountWidget instance

        :param application: Application instance
        :param account: Account instance
        :param mutex: QMutex instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self._ = self.application.translator.gettext

        self.account = account
        self.mutex = mutex

        self.monospace_font = QFont(ADDRESS_MONOSPACE_FONT_NAME)
        self.monospace_font.setStyleHint(QFont.Monospace)
        self.addressValueLabel.setFont(self.monospace_font)
        self.addressValueLabel.setText(self.account.address)

        # creating a pix map of qr code
        qr_code_pixmap = qrcode.make(
            self.account.address, image_factory=QRCodeImage
        ).pixmap()

        # set qrcode to the label
        self.QRCodeAddressLabel.setPixmap(qr_code_pixmap)

        self._update_ui()

        ##############################
        # ASYNC METHODS
        ##############################
        # Create a QWorker object
        self.fetch_from_network_async_qworker = AsyncQWorker(
            self.fetch_from_network, self.mutex
        )
        self.fetch_from_network_async_qworker.finished.connect(
            self._on_finished_fetch_from_network
        )

        # events
        self.refreshButton.clicked.connect(self.fetch_from_network_async_qworker.start)
        self.transferToButton.clicked.connect(self.transfer)
        self.customContextMenuRequested.connect(self.on_context_menu)

        # application events
        self.application.event_dispatcher.add_event_listener(
            AccountEvent.EVENT_TYPE_UPDATE, lambda e: self._update_ui()
        )
        self.application.event_dispatcher.add_event_listener(
            UnitEvent.EVENT_TYPE_CHANGED, lambda e: self._update_ui()
        )
        self.application.event_dispatcher.add_event_listener(
            TransferEvent.EVENT_TYPE_SENT, lambda e: self._on_transfer_sent()
        )

        if self.application.connections.is_connected():
            self.fetch_from_network_async_qworker.start()

    def transfer(self):
        """
        When user click on transfer to button

        :return:
        """
        TransferWindow(
            self.application, self.mutex, None, self.account, parent=self.parent()
        ).exec_()

    def _on_transfer_sent(self):
        """
        Triggered after a successful transfer event

        :return:
        """
        # update account balance from network
        self.fetch_from_network_async_qworker.start()

    def fetch_from_network(self):
        """
        Get last account data from the network

        :return:
        """
        if not self.application.connections.is_connected():
            return

        self.refreshButton.setEnabled(False)

        try:
            self.account = self.application.accounts.network_get_balance(self.account)
        except Exception as exception:
            self.errorLabel.setText(self._(str(exception)))
        else:
            try:
                identity_index = self.application.identities.network_get_index(
                    self.account.address
                )
            except Exception as exception:
                self.errorLabel.setText(self._(str(exception)))
            else:
                if identity_index is not None:
                    try:
                        self.application.identities.network_get_identity(identity_index)
                    except Exception as exception:
                        self.errorLabel.setText(self._(str(exception)))
                    else:
                        try:
                            self.application.smiths.network_get_smith(identity_index)
                        except Exception as exception:
                            self.errorLabel.setText(self._(str(exception)))

    def _on_finished_fetch_from_network(self):
        """
        Triggered when async request fetch_from_network is finished

        :return:
        """
        self.application.accounts.update(self.account)
        self.refreshButton.setEnabled(True)

    def _update_ui(self):
        """
        Update UI from self.account

        :return:
        """
        display_identity_status = {
            IdentityStatus.UNCONFIRMED.value: self._("Unconfirmed"),
            IdentityStatus.UNVALIDATED.value: self._("Unvalidated"),
            IdentityStatus.MEMBER.value: self._("Member"),
            IdentityStatus.NOT_MEMBER.value: self._("Not member"),
            IdentityStatus.REVOKED.value: self._("Revoked"),
        }

        display_smith_status = {
            SmithStatus.INVITED.value: self._("Invited"),
            SmithStatus.PENDING.value: self._("Pending"),
            SmithStatus.SMITH.value: self._("Smith"),
            SmithStatus.EXCLUDED.value: self._("Excluded"),
        }

        unit_preference = self.application.preferences_repository.get(
            SELECTED_UNIT_PREFERENCES_KEY
        )
        if unit_preference is not None:
            amount = self.application.amounts.get_amount(unit_preference)
        else:
            amount = self.application.amounts.get_amount(AMOUNT_UNIT_KEY)

        if self.account.name is None:
            self.nameLabel.setText("")
        else:
            self.nameLabel.setText(self.account.name)

        if self.account.balance is None:
            self.balanceLabel.setText("?")
        else:
            self.balanceLabel.setText(
                self.locale().toCurrencyString(
                    amount.value(self.account.balance), amount.symbol()
                )
            )

        if self.application.wallets.exists(self.account.address):
            if self.application.wallets.is_unlocked(self.account.address):
                self.lockStatusIcon.setPixmap(QPixmap(ICON_ACCOUNT_WALLET_UNLOCKED))
            else:
                self.lockStatusIcon.setPixmap(QPixmap(ICON_ACCOUNT_WALLET_LOCKED))
        else:
            self.lockStatusIcon.setPixmap(QPixmap(ICON_ACCOUNT_NO_WALLET))

        identity = self.application.identities.get_by_address(self.account.address)
        if identity is not None:
            self.identityValueLabel.setText(
                display_identity_status[identity.status.value]
            )
            smith = self.application.smiths.get(identity.index)
            if smith is not None:
                self.smithValuelabel.setText(display_smith_status[smith.status.value])
            else:
                self.smithValuelabel.setText(self._("No"))
        else:
            self.identityValueLabel.setText(self._("No"))
            self.smithValuelabel.setText(self._("No"))

        if self.account.root is None and self.account.path is None:
            self.derivationValueLabel.setText(self._("Root"))
        else:
            root_account = self.application.accounts.get_by_address(self.account.root)
            if root_account is not None and root_account.name is not None:
                self.derivationValueLabel.setFont(QFont())
                self.derivationValueLabel.setText(root_account.name + self.account.path)
            else:
                self.derivationValueLabel.setFont(self.monospace_font)
                self.derivationValueLabel.setText(
                    DisplayAddress(self.account.root).shorten + self.account.path
                )

    def on_context_menu(self, position: QPoint):
        """
        When right button on account tab

        :return:
        """
        # display popup menu at click position
        menu = AccountPopupMenu(self.application, self.account, self.mutex, self)
        menu.exec_(self.mapToGlobal(position))


if __name__ == "__main__":
    qapp = QApplication(sys.argv)

    application_ = Application(DATA_PATH)
    account_ = Account("5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY")

    main_window = QMainWindow()
    main_window.show()

    main_window.setCentralWidget(
        AccountWidget(application_, account_, QMutex(), main_window)
    )

    sys.exit(qapp.exec_())
