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
import sys
from typing import Optional

from PyQt5.QtCore import QLocale, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.authorities import AuthorityStatus
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.events import AccountEvent, ConnectionsEvent, CurrencyEvent
from tikka.domains.entities.identity import IdentityStatus
from tikka.domains.entities.node import Node
from tikka.domains.entities.smith import Smith, SmithStatus
from tikka.interfaces.adapters.network.smiths import NetworkSmithsException
from tikka.slots.pyqt.entities.constants import (
    ICON_LOADER,
    SMITH_CERTIFY_SELECTED_IDENTITY_INDEX,
    SMITH_INVITE_SELECTED_ACCOUNT_ADDRESS,
    SMITH_SELECTED_ACCOUNT_ADDRESS,
)
from tikka.slots.pyqt.resources.gui.widgets.smith_rc import Ui_SmithWidget
from tikka.slots.pyqt.windows.account_unlock import AccountUnlockWindow


class SmithWidget(QWidget, Ui_SmithWidget):
    """
    SmithWidget class
    """

    DELAY_BEFORE_UPDATE_MEMBERSHIP_STATUS_AFTER_REQUEST = 6000

    AUTHORITY_STATUS_NO = 0
    AUTHORITY_STATUS_INCOMING = 1
    AUTHORITY_STATUS_ONLINE = 2
    AUTHORITY_STATUS_OUTGOING = 3

    def __init__(
        self, application: Application, parent: Optional[QWidget] = None
    ) -> None:
        """
        Init SmithWidget instance

        :param application: Application instance
        :param parent: MainWindow instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self._ = self.application.translator.gettext
        self.account: Optional[Account] = None
        self.smith: Optional[Smith] = None
        self.authority_status: AuthorityStatus = AuthorityStatus.OFFLINE
        self.invite_account: Optional[Account] = None
        self.certify_smith: Optional[Smith] = None
        self.current_node = self.application.nodes.get(
            self.application.nodes.get_current_url()
        )

        # animated loading icon
        self.loader_movie = QMovie(ICON_LOADER)
        self.loader_movie.start()
        self.loaderIconLabel.setMovie(self.loader_movie)
        loader_icon_size_policy = self.loaderIconLabel.sizePolicy()
        loader_icon_size_policy.setRetainSizeWhenHidden(True)
        self.loaderIconLabel.setSizePolicy(loader_icon_size_policy)
        self.loaderIconLabel.hide()

        ##############################
        # ASYNC METHODS
        ##############################
        self.fetch_all_from_network_timer = QTimer()
        self.fetch_all_from_network_timer.timeout.connect(
            self.fetch_all_from_network_timer_function
        )
        self.rotate_keys_timer = QTimer()
        self.rotate_keys_timer.timeout.connect(self.rotate_keys_timer_function)
        self.publish_keys_timer = QTimer()
        self.publish_keys_timer.timeout.connect(self.publish_keys_timer_function)
        self.invite_member_timer = QTimer()
        self.invite_member_timer.timeout.connect(self.invite_member_timer_function)
        self.accept_invitation_timer = QTimer()
        self.accept_invitation_timer.timeout.connect(
            self.accept_invitation_timer_function
        )
        self.certify_smith_timer = QTimer()
        self.certify_smith_timer.timeout.connect(self.certify_smith_timer_function)
        self.go_online_timer = QTimer()
        self.go_online_timer.timeout.connect(self.go_online_timer_function)
        self.go_offline_timer = QTimer()
        self.go_offline_timer.timeout.connect(self.go_offline_timer_function)

        # events
        self.accountComboBox.activated.connect(self.on_account_combobox_index_changed)
        self.refreshSmithButton.clicked.connect(self._on_refresh_smith_button_clicked)
        self.rotateKeysButton.clicked.connect(self.rotate_keys_timer.start)
        self.publishKeysButton.clicked.connect(self.publish_keys_timer.start)
        self.acceptInvitationButton.clicked.connect(self.accept_invitation_timer.start)
        self.inviteButton.clicked.connect(self.invite_member_timer.start)
        self.inviteAccountComboBox.activated.connect(
            self.on_invite_account_combobox_index_changed
        )
        self.certifyButton.clicked.connect(self.certify_smith_timer.start)
        self.certifySmithComboBox.activated.connect(
            self.on_certify_smith_combobox_index_changed
        )
        self.goOnlineButton.clicked.connect(self.go_online_timer.start)
        self.goOfflineButton.clicked.connect(self.go_offline_timer.start)

        # subscribe to application events
        self.application.event_dispatcher.add_event_listener(
            CurrencyEvent.EVENT_TYPE_CHANGED, self._on_currency_event
        )
        self.application.event_dispatcher.add_event_listener(
            ConnectionsEvent.EVENT_TYPE_CONNECTED, self.on_connections_event
        )
        self.application.event_dispatcher.add_event_listener(
            ConnectionsEvent.EVENT_TYPE_DISCONNECTED, self.on_connections_event
        )

        self.application.event_dispatcher.add_event_listener(
            AccountEvent.EVENT_TYPE_ADD, self.on_add_account_event
        )
        self.application.event_dispatcher.add_event_listener(
            AccountEvent.EVENT_TYPE_DELETE, self.on_delete_account_event
        )
        self.application.event_dispatcher.add_event_listener(
            AccountEvent.EVENT_TYPE_UPDATE, self.on_update_account_event
        )

        # populate form
        self.init_account_combo_box()
        self.init_invite_account_combo_box()
        self.init_certify_smith_combo_box()

        self._update_ui()

    def update_account(self, account: Optional[Account]) -> None:
        """
        Update account and smith and authority status and certification list

        :param account: New account
        :return:
        """
        self.account = account
        self.authority_status = AuthorityStatus.OFFLINE

        if self.account is None:
            self.smith = None
        else:
            self.smith = None
            identity_index = self.application.identities.get_index_by_address(
                self.account.address
            )
            if identity_index is not None:
                # get smith status
                self.smith = self.application.smiths.get(identity_index)

            if self.smith is not None:
                self.authority_status = self.application.authorities.get_status(
                    self.smith.identity_index
                )

        # exclude new operating account from dependant list
        self.init_invite_account_combo_box()
        self.init_certify_smith_combo_box()

    def init_account_combo_box(self) -> None:
        """
        Init combobox with validated identity accounts (with wallets)

        :return:
        """
        self.accountComboBox.clear()
        self.accountComboBox.addItem("-", userData=None)

        for account in self.application.accounts.get_list():
            identity = self.application.identities.get_by_address(account.address)
            if (
                identity is not None
                and identity.status == IdentityStatus.MEMBER
                and self.application.wallets.exists(account.address)
            ):
                self.accountComboBox.addItem(
                    account.name if account.name is not None else account.address,
                    userData=account.address,
                )

        self.account = None
        preference_account_address_selected = self.application.preferences.get(
            SMITH_SELECTED_ACCOUNT_ADDRESS
        )
        if preference_account_address_selected is not None:
            preference_account_selected = self.application.accounts.get_by_address(
                preference_account_address_selected
            )
            if preference_account_selected is not None:
                index = self.accountComboBox.findData(
                    preference_account_address_selected
                )
                if index > -1:
                    self.accountComboBox.setCurrentIndex(index)
                    self.update_account(preference_account_selected)
                else:
                    self.application.preferences.set(
                        SMITH_SELECTED_ACCOUNT_ADDRESS, None
                    )

    def on_account_combobox_index_changed(self):
        """
        Triggered when account selection is changed

        :return:
        """
        address = self.accountComboBox.currentData()
        if address is not None:
            self.update_account(self.application.accounts.get_by_address(address))
        else:
            self.update_account(None)

        self._update_ui()

        self.application.preferences_repository.set(
            SMITH_SELECTED_ACCOUNT_ADDRESS,
            address,
        )

    def init_invite_account_combo_box(self) -> None:
        """
        Init combobox with validated identity accounts (not smith) to invite to be smith

        :return:
        """
        self.inviteAccountComboBox.clear()
        self.inviteAccountComboBox.addItem("-", userData=None)

        for account in self.application.accounts.get_list():
            if self.account is not None and self.account.address != account.address:
                identity = self.application.identities.get_by_address(account.address)
                if (
                    identity is not None
                    and identity.status == IdentityStatus.MEMBER
                    and not self.application.smiths.exists(identity.index)
                ):
                    self.inviteAccountComboBox.addItem(
                        account.name if account.name is not None else account.address,
                        userData=account.address,
                    )

        self.invite_account = None
        preference_invite_account_address_selected = self.application.preferences.get(
            SMITH_INVITE_SELECTED_ACCOUNT_ADDRESS
        )
        if preference_invite_account_address_selected is not None:
            preference_invite_account_selected = (
                self.application.accounts.get_by_address(
                    preference_invite_account_address_selected
                )
            )
            if preference_invite_account_selected is not None:
                index = self.inviteAccountComboBox.findData(
                    preference_invite_account_address_selected
                )
                if index > -1:
                    self.inviteAccountComboBox.setCurrentIndex(index)
                    self.invite_account = preference_invite_account_selected
                else:
                    self.application.preferences.set(
                        SMITH_INVITE_SELECTED_ACCOUNT_ADDRESS, None
                    )

    def on_invite_account_combobox_index_changed(self):
        """
        Triggered when invite account selection is changed

        :return:
        """
        address = self.inviteAccountComboBox.currentData()
        if address is not None:
            self.invite_account = self.application.accounts.get_by_address(address)
        else:
            self.invite_account = None

        self.application.preferences_repository.set(
            SMITH_INVITE_SELECTED_ACCOUNT_ADDRESS,
            None if self.invite_account is None else self.invite_account.address,
        )
        self._update_ui()

    def init_certify_smith_combo_box(self) -> None:
        """
        Init combobox with smith and pending smith accounts to certify

        :return:
        """
        self.certifySmithComboBox.clear()
        self.certifySmithComboBox.addItem("-", userData=None)

        smiths = [
            smith
            for smith in self.application.smiths.list()
            if (
                smith.status == SmithStatus.SMITH or smith.status == SmithStatus.PENDING
            )
        ]

        for smith in smiths:
            identity = self.application.identities.get(smith.identity_index)
            if identity is not None:
                account = self.application.accounts.get_by_address(identity.address)
                if (
                    account is not None
                    and self.account is not None
                    and account.address != self.account.address
                ):
                    self.certifySmithComboBox.addItem(
                        account.name if account.name is not None else account.address,
                        userData=smith.identity_index,
                    )

        self.certify_smith = None
        preference_certify_smith_identity_index_selected = (
            self.application.preferences.get(SMITH_CERTIFY_SELECTED_IDENTITY_INDEX)
        )
        if preference_certify_smith_identity_index_selected is not None:
            preference_certify_smith_selected = self.application.smiths.get(
                preference_certify_smith_identity_index_selected
            )
            if preference_certify_smith_selected is not None:
                index = self.certifySmithComboBox.findData(
                    preference_certify_smith_identity_index_selected
                )
                if index > -1:
                    self.certifySmithComboBox.setCurrentIndex(index)
                    self.certify_smith = preference_certify_smith_selected
                else:
                    self.application.preferences.set(
                        SMITH_CERTIFY_SELECTED_IDENTITY_INDEX, None
                    )

    def on_certify_smith_combobox_index_changed(self):
        """
        Triggered when certify smith selection is changed

        :return:
        """
        identity_index = self.certifySmithComboBox.currentData()
        if identity_index is not None:
            self.certify_smith = self.application.smiths.get(identity_index)
        else:
            self.certify_smith = None

        self.application.preferences_repository.set(
            SMITH_CERTIFY_SELECTED_IDENTITY_INDEX,
            None if self.certify_smith is None else self.certify_smith.identity_index,
        )
        self._update_ui()

    def rotate_keys_timer_function(self):
        """
        Triggered when user click on rotate keys button

        :return:
        """
        self.errorLabel.setText("")
        self.rotateKeysButton.setDisabled(True)
        try:
            result = self.application.authorities.network_rotate_keys(self.current_node)
        except Exception as exception:
            self.errorLabel.setText(self._(str(exception)))
        else:
            self.sessionKeysTextBrowser.setText(result)
            self.errorLabel.setText("")

        self.rotateKeysButton.setEnabled(True)
        self.rotate_keys_timer.stop()

    def invite_member_timer_function(self):
        """
        Triggered when user click on invite button

        :return:
        """
        self.errorLabel.setText("")

        if self.invite_account is None:
            self.loaderIconLabel.hide()
            self.invite_member_timer.stop()
            return

        # if account is locked...
        if not self.application.wallets.is_unlocked(self.account.address):
            # ask password...
            dialog_code = AccountUnlockWindow(
                self.application, self.account, self
            ).exec_()
            if dialog_code == QDialog.Rejected:
                self.loaderIconLabel.hide()
                self.invite_member_timer.stop()
                return

        self.loader_movie.start()
        self.loaderIconLabel.show()
        self.inviteButton.setDisabled(True)

        identity_index = self.application.identities.get_index_by_address(
            self.invite_account.address
        )
        try:
            self.application.smiths.network_invite_member(
                self.application.wallets.get_keypair(self.account.address),
                identity_index,
            )
        except Exception as exception:
            self.errorLabel.setText(self._(str(exception)))
        else:
            try:
                self.application.smiths.network_get_smith(identity_index)
            except Exception as exception:
                self.errorLabel.setText(self._(str(exception)))
            else:
                self.init_invite_account_combo_box()
                self._update_ui()
                self.fetch_all_from_network_timer.start(
                    self.DELAY_BEFORE_UPDATE_MEMBERSHIP_STATUS_AFTER_REQUEST
                )

        self.loaderIconLabel.hide()
        self.invite_member_timer.stop()

    def accept_invitation_timer_function(self):
        """
        Triggered when user click on accept invitation button

        :return:
        """
        self.errorLabel.setText("")

        if self.account is None:
            self.loaderIconLabel.hide()
            self.accept_invitation_timer.stop()
            return

        # if account is locked...
        if not self.application.wallets.is_unlocked(self.account.address):
            # ask password...
            dialog_code = AccountUnlockWindow(
                self.application, self.account, self
            ).exec_()
            if dialog_code == QDialog.Rejected:
                self.loaderIconLabel.hide()
                self.accept_invitation_timer.stop()
                return

        self.acceptInvitationButton.setDisabled(True)
        try:
            self.application.smiths.network_accept_invitation(
                self.application.wallets.get_keypair(self.account.address)
            )
        except Exception as exception:
            self.acceptInvitationButton.setEnabled(True)
            self.errorLabel.setText(self._(str(exception)))
            self.accept_invitation_timer.stop()
        else:
            self.fetch_all_from_network_timer.start(
                self.DELAY_BEFORE_UPDATE_MEMBERSHIP_STATUS_AFTER_REQUEST
            )

        self.accept_invitation_timer.stop()

    def certify_smith_timer_function(self):
        """
        Triggered when user click on certify button

        :return:
        """
        self.errorLabel.setText("")

        self.loader_movie.start()
        self.loaderIconLabel.show()
        self.certifyButton.setDisabled(True)

        if self.certify_smith is None:
            self.loaderIconLabel.hide()
            self.certifyButton.setEnabled(True)
            self.certify_smith_timer.stop()
            return

        # if account is locked...
        if not self.application.wallets.is_unlocked(self.account.address):
            # ask password...
            dialog_code = AccountUnlockWindow(
                self.application, self.account, self
            ).exec_()
            if dialog_code == QDialog.Rejected:
                self.loaderIconLabel.hide()
                self.certifyButton.setEnabled(True)
                self.certify_smith_timer.stop()
                return

        try:
            self.application.smiths.network_certify(
                self.application.wallets.get_keypair(self.account.address),
                self.certify_smith.identity_index,
            )
        except NetworkSmithsException as exception:
            self.errorLabel.setText(self._(str(exception)))
        else:
            try:
                self.application.smiths.network_get_smith(
                    self.certify_smith.identity_index
                )
            except Exception as exception:
                self.errorLabel.setText(self._(str(exception)))
            else:
                try:
                    self.smith = self.application.smiths.network_get_smith(
                        self.smith.identity_index
                    )
                except Exception as exception:
                    self.errorLabel.setText(self._(str(exception)))
                else:
                    self._update_ui()

        self.loaderIconLabel.hide()
        self.certifyButton.setEnabled(True)
        self.certify_smith_timer.stop()

    def publish_keys_timer_function(self):
        """
        Triggered when user click on publish keys button

        :return:
        """
        self.errorLabel.setText("")

        if self.account is None:
            return
        # if account is locked...
        if not self.application.wallets.is_unlocked(self.account.address):
            # ask password...
            dialog_code = AccountUnlockWindow(
                self.application, self.account, self
            ).exec_()
            if dialog_code == QDialog.Rejected:
                return

        self.publishKeysButton.setDisabled(True)
        try:
            self.application.authorities.network_publish_session_keys(
                self.application.wallets.get_keypair(self.account.address),
                self.current_node.session_keys,
            )
        except Exception as exception:
            self.errorLabel.setText(self._(str(exception)))

        self.publishKeysButton.setEnabled(True)
        self.publish_keys_timer.stop()

    def go_online_timer_function(self):
        """
        Triggered when user click on go online button

        :return:
        """
        self.errorLabel.setText("")

        if self.account is None:
            return
        # if account is locked...
        if not self.application.wallets.is_unlocked(self.account.address):
            # ask password...
            dialog_code = AccountUnlockWindow(
                self.application, self.account, self
            ).exec_()
            if dialog_code == QDialog.Rejected:
                return

        self.goOnlineButton.setDisabled(True)
        try:
            self.application.authorities.network_go_online(
                self.application.wallets.get_keypair(self.account.address)
            )
        except Exception as exception:
            self.errorLabel.setText(self._(str(exception)))
        else:
            self.fetch_all_from_network_timer.start(
                self.DELAY_BEFORE_UPDATE_MEMBERSHIP_STATUS_AFTER_REQUEST
            )

        self.goOnlineButton.setEnabled(True)
        self.go_online_timer.stop()

    def go_offline_timer_function(self):
        """
        Triggered when user click on go offline button

        :return:
        """
        self.errorLabel.setText("")

        if self.account is None:
            return
        # if account is locked...
        if not self.application.wallets.is_unlocked(self.account.address):
            # ask password...
            dialog_code = AccountUnlockWindow(
                self.application, self.account, self
            ).exec_()
            if dialog_code == QDialog.Rejected:
                return

        self.goOfflineButton.setDisabled(True)
        try:
            self.application.authorities.network_go_offline(
                self.application.wallets.get_keypair(self.account.address)
            )
        except Exception as exception:
            self.errorLabel.setText(self._(str(exception)))
        else:
            self.fetch_all_from_network_timer.start(
                self.DELAY_BEFORE_UPDATE_MEMBERSHIP_STATUS_AFTER_REQUEST
            )

        self.goOfflineButton.setEnabled(True)
        self.go_offline_timer.stop()

    def _on_refresh_smith_button_clicked(self, _):
        """ """
        self.fetch_all_from_network_timer.start()

    def fetch_all_from_network_timer_function(self):
        """
        Update identities, smiths and authorities from current url connection

        :return:
        """
        self.errorLabel.setText("")

        self.loader_movie.start()
        self.loaderIconLabel.show()

        try:
            identity_indice = [
                identity_index
                for identity_index in self.application.identities.network_get_identity_indice(
                    [
                        account.address
                        for account in self.application.accounts.get_list()
                    ]
                )
                if identity_index is not None
            ]
        except Exception as exception:
            self.errorLabel.setText(self._(str(exception)))
        else:
            try:
                self.application.identities.network_get_identities(identity_indice)
            except Exception as exception:
                self.errorLabel.setText(self._(str(exception)))
            else:
                try:
                    self.application.smiths.network_get_smiths(identity_indice)
                except Exception as exception:
                    self.errorLabel.setText(self._(str(exception)))
                else:
                    try:
                        self.application.authorities.network_get_all()
                    except Exception as exception:
                        self.errorLabel.setText(self._(str(exception)))
                    else:
                        self.init_account_combo_box()
                        self.init_invite_account_combo_box()
                        self.init_certify_smith_combo_box()

        self.refreshSmithButton.setEnabled(True)
        self.loaderIconLabel.hide()

        self._update_ui()

        self.fetch_all_from_network_timer.stop()

    def _update_ui(self):
        """
        Update node infos in UI

        :return:
        """
        display_smith_status = {
            SmithStatus.INVITED.value: self._("Invited"),
            SmithStatus.PENDING.value: self._("Pending"),
            SmithStatus.SMITH.value: self._("Smith"),
            SmithStatus.EXCLUDED.value: self._("Excluded"),
        }

        # validator node
        if self.current_node.unsafe_api_exposed is True:
            self.validatorNodeGroupBox.show()
        else:
            self.validatorNodeGroupBox.hide()

        self.urlValueLabel.setText(self.current_node.url)

        if self.current_node.session_keys is not None:
            self.sessionKeysTextBrowser.setText(self.current_node.session_keys)
        else:
            self.sessionKeysTextBrowser.setText("")

        # rotate keys only available on localhost via an ssh tunnel or other method...
        self.rotateKeysButton.setEnabled(
            "localhost" in self.application.nodes.get_current_url()
        )

        # disable all buttons
        self.publishKeysButton.setDisabled(True)
        self.inviteButton.setDisabled(True)
        self.inviteAccountComboBox.setDisabled(True)
        self.acceptInvitationButton.setDisabled(True)
        self.certifySmithComboBox.setDisabled(True)
        self.goOnlineButton.setDisabled(True)
        self.goOfflineButton.setDisabled(True)

        if self.account is not None:
            self.refreshSmithButton.setEnabled(True)
            if self.current_node.session_keys is not None:
                self.publishKeysButton.setEnabled(True)
            if self.smith is None:
                pass
            elif self.smith.status == SmithStatus.INVITED:
                self.acceptInvitationButton.setEnabled(True)
            elif self.smith.status == SmithStatus.SMITH:
                self.inviteButton.setEnabled(True)
                if self.inviteAccountComboBox.count() > 1:
                    self.inviteAccountComboBox.setEnabled(True)
                if self.certifySmithComboBox.count() > -1:
                    self.certifySmithComboBox.setEnabled(True)
                self.goOnlineButton.setEnabled(
                    self.authority_status == AuthorityStatus.OFFLINE
                )
                self.goOfflineButton.setEnabled(
                    self.authority_status == AuthorityStatus.ONLINE
                )

        if self.smith is not None:
            status_string = display_smith_status[self.smith.status.value]
            if self.smith.expire_on is not None:
                expire_on_localized_datetime_string = self.locale().toString(
                    self.smith.expire_on,
                    QLocale.dateTimeFormat(self.locale(), QLocale.ShortFormat),
                )
                status_string = (
                    f"{status_string} ({expire_on_localized_datetime_string})"
                )
            self.membershipValueLabel.setText(status_string)

            self.certifiersListWidget.clear()
            for certifier_identity_index in self.smith.certifications_received:
                self.certifiersListWidget.addItem(str(certifier_identity_index))

            self.certifiedListWidget.clear()
            for certified_identity_index in self.smith.certifications_issued:
                self.certifiedListWidget.addItem(str(certified_identity_index))
        else:
            self.membershipValueLabel.setText(self._("No"))
            # clear certification list
            self.certifiersListWidget.clear()
            self.certifiedListWidget.clear()

        if self.authority_status == AuthorityStatus.OFFLINE:
            self.authorityValueLabel.setText(self._("No"))
        elif self.authority_status == AuthorityStatus.INCOMING:
            self.authorityValueLabel.setText(self._("Incoming..."))
        elif self.authority_status == AuthorityStatus.ONLINE:
            self.authorityValueLabel.setText(self._("Online"))
        elif self.authority_status == AuthorityStatus.OUTGOING:
            self.authorityValueLabel.setText(self._("Outgoing..."))

    def _on_currency_event(self, _):
        """
        When a currency event is triggered

        :param _: CurrencyEvent instance
        :return:
        """
        self.init_account_combo_box()
        self.init_invite_account_combo_box()
        self.init_certify_smith_combo_box()
        if self.account is not None:
            self.fetch_all_from_network_timer.start()

        self._update_ui()

    def on_connections_event(self, _):
        """
        Triggered when the network connection if connected/disconnected

        :param _: ConnectionsEvent instance
        :return:
        """

        self.current_node = self.application.nodes.get(
            self.application.nodes.get_current_url()
        )
        self.init_account_combo_box()
        self._update_ui()

    def on_add_account_event(self, _):
        """
        Add account is selectors when account is created

        :return:
        """
        self.init_account_combo_box()
        self.init_invite_account_combo_box()
        self.init_certify_smith_combo_box()

    def on_delete_account_event(self, _):
        """
        Remove account from selector when account is deleted

        :return:
        """
        self.init_account_combo_box()
        self.init_invite_account_combo_box()
        self.init_certify_smith_combo_box()

        self._update_ui()

    def on_update_account_event(self, _):
        """
        Update account on page and selector when account is updated

        :return:
        """
        self.init_account_combo_box()
        self.init_invite_account_combo_box()
        self.init_certify_smith_combo_box()

        self._update_ui()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    qapp = QApplication(sys.argv)

    application_ = Application(DATA_PATH)

    main_window = QMainWindow()
    main_window.show()
    validator_node = Node(url="ws://localhost:9944")
    if application_.nodes.get(validator_node.url) is None:
        application_.nodes.add(validator_node)
    application_.nodes.set_current_url(validator_node.url)
    main_window.setCentralWidget(SmithWidget(application_, main_window))

    sys.exit(qapp.exec_())
