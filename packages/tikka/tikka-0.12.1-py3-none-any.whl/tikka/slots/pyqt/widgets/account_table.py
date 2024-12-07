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

from PyQt5 import QtWidgets
from PyQt5.QtCore import QModelIndex, QMutex, QPoint, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyleOptionViewItem, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.events import AccountEvent, CurrencyEvent, UnitEvent
from tikka.interfaces.adapters.repository.accounts import AccountsRepositoryInterface
from tikka.slots.pyqt.entities.constants import (
    ACCOUNTS_TABLE_CATEGORY_FILTER_PREFERENCES_KEY,
    ACCOUNTS_TABLE_SORT_COLUMN_PREFERENCES_KEY,
    ACCOUNTS_TABLE_SORT_ORDER_PREFERENCES_KEY,
    ACCOUNTS_TABLE_WALLET_FILTER_PREFERENCES_KEY,
)
from tikka.slots.pyqt.entities.worker import AsyncQWorker
from tikka.slots.pyqt.models.account_table import AccountTableModel
from tikka.slots.pyqt.resources.gui.widgets.account_table_rc import (
    Ui_AccountTableWidget,
)
from tikka.slots.pyqt.widgets.account_menu import AccountPopupMenu


class IconDelegate(QtWidgets.QStyledItemDelegate):
    """
    IconDelegate class to center icons in table view
    """

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        """
        Init Style

        :param option: QStyleOptionViewItem instance
        :param index: QModelIndex instance
        :return:
        """
        super().initStyleOption(option, index)
        # resize width to actual width of icon
        option.decorationSize.setWidth(option.rect.width())


class AccountTableWidget(QWidget, Ui_AccountTableWidget):
    """
    AccountTableWidget class
    """

    def __init__(
        self,
        application: Application,
        mutex: QMutex,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Init AccountTableWidget instance

        :param application: Application instance
        :param mutex: QMutex instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self.mutex = mutex
        self.account_table_model = AccountTableModel(self.application, self.locale())
        self._ = self.application.translator.gettext

        # use icon delegate to center icons
        delegate = IconDelegate(self.tableView)
        self.tableView.setItemDelegate(delegate)

        # setup table view
        self.tableView.setModel(self.account_table_model)
        # set header sort column and sort order icon
        sort_column_preference = self.application.preferences_repository.get(
            ACCOUNTS_TABLE_SORT_COLUMN_PREFERENCES_KEY
        )
        if sort_column_preference is not None:
            sort_column_index = int(sort_column_preference)
        else:
            sort_column_index = -1
        repository_sort_order = self.application.preferences_repository.get(
            ACCOUNTS_TABLE_SORT_ORDER_PREFERENCES_KEY
        )
        self.tableView.horizontalHeader().setSortIndicator(
            sort_column_index,
            Qt.AscendingOrder
            if repository_sort_order == AccountsRepositoryInterface.SORT_ORDER_ASCENDING
            else Qt.DescendingOrder,
        )
        self.tableView.setSortingEnabled(True)
        self.init_category_filter()
        self.init_wallet_filter()
        self.tableView.resizeColumnsToContents()

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

        # table events
        self.tableView.customContextMenuRequested.connect(self.on_context_menu)
        self.tableView.model().dataChanged.connect(self.on_data_changed)
        self.categoryComboBox.currentIndexChanged.connect(
            self.on_category_filter_changed
        )
        self.walletComboBox.currentIndexChanged.connect(self.on_wallet_filter_changed)
        # application events
        self.application.event_dispatcher.add_event_listener(
            UnitEvent.EVENT_TYPE_CHANGED, self.on_unit_event
        )
        self.application.event_dispatcher.add_event_listener(
            CurrencyEvent.EVENT_TYPE_CHANGED, self.on_currency_event
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

    def init_category_filter(self):
        """
        Fill category filter combo box with all categories and a blank choice

        :return:
        """
        # init combo box
        self.categoryComboBox.addItem(self._("No filter"), userData=None)
        for category in self.application.categories.list_all():
            self.categoryComboBox.addItem(category.name, userData=category.id.hex)

        # set current category filter from preferences
        category_id = self.application.preferences_repository.get(
            ACCOUNTS_TABLE_CATEGORY_FILTER_PREFERENCES_KEY
        )
        self.categoryComboBox.setCurrentIndex(
            self.categoryComboBox.findData(category_id)
        )

    def on_category_filter_changed(self, _):
        """
        Update preferences with category filter for table view

        :return:
        """
        category_id = self.categoryComboBox.currentData()
        self.application.preferences_repository.set(
            ACCOUNTS_TABLE_CATEGORY_FILTER_PREFERENCES_KEY,
            None if category_id is None else str(category_id),
        )
        self._update_model()

    def init_wallet_filter(self):
        """
        Fill wallet filter combo box with None (with and without), True (with) or False (without)

        :return:
        """
        # init combo box
        self.walletComboBox.addItem(self._("No filter"), userData=None)
        self.walletComboBox.addItem(self._("Yes"), userData=True)
        self.walletComboBox.addItem(self._("No"), userData=False)

        # set current category filter from preferences
        wallet_filter_preference = self.application.preferences_repository.get(
            ACCOUNTS_TABLE_WALLET_FILTER_PREFERENCES_KEY
        )
        wallet_filter = None
        if wallet_filter_preference is not None:
            # preference store boolean as integer in a string column ("0" or "1")
            # convert it to boolean
            wallet_filter = int(wallet_filter_preference) == 1
        self.walletComboBox.setCurrentIndex(self.walletComboBox.findData(wallet_filter))

    def on_wallet_filter_changed(self, _):
        """
        Update preferences with wallet filter for table view

        :return:
        """
        wallet_filter = self.walletComboBox.currentData()
        self.application.preferences_repository.set(
            ACCOUNTS_TABLE_WALLET_FILTER_PREFERENCES_KEY, wallet_filter
        )
        self._update_model()

    def on_data_changed(self, _):
        """
        Triggered when data changed in table model

        :return:
        """
        self._update_model()

    def _update_model(self):
        """
        Update all data in model

        :return:
        """
        self.tableView.model().init_data()
        self.tableView.resizeColumnsToContents()

    def on_unit_event(self, _):
        """
        When a unit event is triggered

        :return:
        """
        self._update_model()

    def on_currency_event(self, _):
        """
        When a currency event is triggered

        :return:
        """
        self._update_model()

    def on_add_account_event(self, _):
        """
        Add account row when account is created

        :return:
        """
        self._update_model()

    def on_delete_account_event(self, _):
        """
        Remove account row when account is deleted

        :return:
        """
        self._update_model()

    def on_update_account_event(self, _):
        """
        Update account row when account is updated

        :return:
        """
        self._update_model()

    def on_context_menu(self, position: QPoint):
        """
        When right button on table widget

        :param position: QPoint instance
        :return:
        """
        # get selected account
        table_view_row = self.tableView.currentIndex().internalPointer()
        account = self.application.accounts.get_by_address(table_view_row.address)
        if account is not None:
            # display popup menu at click position
            AccountPopupMenu(self.application, account, self.mutex, self).exec_(
                self.tableView.mapToGlobal(position)
            )

    def fetch_from_network(self):
        """
        Fetch table model accounts data from the network

        :return:
        """
        self.refreshButton.setEnabled(False)
        self.errorLabel.setText("")

        try:
            self.application.accounts.network_update_balances(
                self.application.accounts.get_list()
            )
        except Exception as exception:
            self.errorLabel.setText(self._(str(exception)))

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

    def _on_finished_fetch_from_network(self):
        """
        Triggered when async request fetch_from_network is finished

        :return:
        """
        self.refreshButton.setEnabled(True)
        self._update_model()


if __name__ == "__main__":
    qapp = QApplication(sys.argv)

    application_ = Application(DATA_PATH)

    main_window = QMainWindow()
    main_window.show()

    main_window.setCentralWidget(
        AccountTableWidget(application_, QMutex(), main_window)
    )

    sys.exit(qapp.exec_())
