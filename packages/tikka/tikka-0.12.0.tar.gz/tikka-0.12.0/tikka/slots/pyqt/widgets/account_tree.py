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

from PyQt5.QtCore import QModelIndex, QMutex, QPoint, QRect
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QWidget,
)

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.category import Category
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.events import (
    AccountEvent,
    CategoryEvent,
    CurrencyEvent,
    UnitEvent,
)
from tikka.slots.pyqt.entities.worker import AsyncQWorker
from tikka.slots.pyqt.models.account_tree import AccountTreeModel, MemberStatusRole
from tikka.slots.pyqt.resources.gui.widgets.account_tree_rc import Ui_AccountTreeWidget
from tikka.slots.pyqt.widgets.account_menu import AccountPopupMenu
from tikka.slots.pyqt.widgets.category_menu import CategoryPopupMenu


class AccountIconsItemDelegate(QStyledItemDelegate):
    """
    Class used to display member status icon for accounts
    """

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        """
        Draw member status icon and wallet lock status icon side by side

        :param painter: QPainter instance
        :param option: QStyleOptionViewItem instance
        :param index: QModelIndex instance
        :return:
        """
        super().paint(painter, option, index)
        member_pixmap: QPixmap = index.data(MemberStatusRole)
        if isinstance(member_pixmap, QPixmap):
            member_rect = QRect(
                option.rect.x() - member_pixmap.rect().width() - 2,
                option.rect.y(),
                member_pixmap.rect().width(),
                member_pixmap.rect().height(),
            )
            painter.drawPixmap(member_rect, member_pixmap)


class AccountTreeWidget(QWidget, Ui_AccountTreeWidget):
    """
    AccountTreeWidget class
    """

    def __init__(
        self,
        application: Application,
        mutex: QMutex,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Init AccountTreeWidget instance

        :param application: Application instance
        :param mutex: QMutex instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self._ = self.application.translator.gettext
        self.mutex = mutex
        self.account_tree_model = AccountTreeModel(self.application, self.locale())
        self.treeView.setModel(self.account_tree_model)
        self.treeView.setHeaderHidden(True)
        self.treeView.expandAll()
        self.treeView.resizeColumnToContents(0)
        # set style sheet
        self.treeView.setStyleSheet("QTreeView::item {" "padding: 5px;" "}")
        self.treeView.setItemDelegateForColumn(0, AccountIconsItemDelegate())
        # init expand/collapse state of categories
        self.recursive_expand_or_collapse_categories(QModelIndex())
        self.treeView.resizeColumnToContents(1)

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
        self.addCategoryButton.clicked.connect(self.on_add_category_button_clicked)
        self.refreshButton.clicked.connect(self.fetch_from_network_async_qworker.start)
        self.treeView.customContextMenuRequested.connect(self.on_context_menu)
        self.treeView.expanded.connect(self.on_expanded)
        self.treeView.collapsed.connect(self.on_collapsed)
        self.treeView.model().dataChanged.connect(self.on_data_changed)

        # application events
        self.application.event_dispatcher.add_event_listener(
            CategoryEvent.EVENT_TYPE_ADD, self.on_category_add_event
        )
        self.application.event_dispatcher.add_event_listener(
            CategoryEvent.EVENT_TYPE_DELETE, self.on_category_delete_event
        )
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

    def rename_category(self):
        """
        Set the current selected category in edit mode in tree view

        :return:
        """
        index = self.treeView.currentIndex()
        item = index.internalPointer()
        if isinstance(item.element, Category):
            self.treeView.edit(self.treeView.currentIndex())

    def add_category(self, parent: QModelIndex):
        """
        Add a new category in index in edit mode

        :param parent: Parent QModelIndex instance
        :return:
        """
        self.treeView.model().insertRow(0, parent)
        self.recursive_expand_or_collapse_categories(QModelIndex())
        self.treeView.edit(self.treeView.model().index(0, 0, parent))

    def add_sub_category(self):
        """
        Add new sub category in current selected category

        :return:
        """
        index = self.treeView.currentIndex()
        item = index.internalPointer()
        if isinstance(item.element, Category):
            self.add_category(index)

    def on_data_changed(self, _):
        """
        Triggered when data changed in tree view model

        :return:
        """
        self._update_model()

    def recursive_expand_or_collapse_categories(self, index: QModelIndex) -> None:
        """
        Expand or collapse categories in tree view depending on expanded attribute

        :param index: Index to expand/collapse
        :return:
        """
        item = index.internalPointer()
        if item is not None:
            element = index.internalPointer().element
            if isinstance(element, Category):
                if element.expanded is True:
                    self.treeView.expand(index)
                else:
                    self.treeView.collapse(index)
            else:
                self.treeView.expand(index)
        for row in range(0, self.account_tree_model.rowCount(index)):
            self.recursive_expand_or_collapse_categories(
                self.account_tree_model.index(row, 0, index)
            )
        self.treeView.resizeColumnToContents(0)

    def on_expanded(self, index: QModelIndex) -> None:
        """
        Triggered when user expand a row

        :param index: QModelIndex instance of expanded row
        :return:
        """
        # get selected element
        element = index.internalPointer().element
        if isinstance(element, Category) and element.expanded is False:
            self.application.categories.expand(element)

    def on_collapsed(self, index: QModelIndex) -> None:
        """
        Triggered when user collapse a row

        :param index: QModelIndex instance of collapsed row
        :return:
        """
        # get selected element
        element = index.internalPointer().element
        if isinstance(element, Category) and element.expanded is True:
            self.application.categories.collapse(element)

    def _update_model(self):
        """
        Triggered when adding a category

        :return:
        """
        self.treeView.model().init_data()
        self.treeView.resizeColumnToContents(0)
        self.recursive_expand_or_collapse_categories(QModelIndex())

    def on_add_category_button_clicked(self):
        """
        Triggered when user click on addCategoryButton

        :return:
        """
        self.add_category(self.treeView.rootIndex())

    def on_category_add_event(self, _):
        """
        When add category event is triggered

        :return:
        """
        self._update_model()

    def on_category_delete_event(self, _):
        """
        When delete category event is triggered

        :return:
        """
        self._update_model()

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
        current_element = self.treeView.currentIndex().internalPointer().element
        if isinstance(current_element, Account):
            # display account popup menu at click position
            AccountPopupMenu(self.application, current_element, self.mutex, self).exec_(
                self.treeView.mapToGlobal(position)
            )
        else:
            # display category popup menu at click position
            CategoryPopupMenu(
                self.application, current_element, self.mutex, self
            ).exec_(self.treeView.mapToGlobal(position))

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
    main_window.showMaximized()

    main_window.setCentralWidget(AccountTreeWidget(application_, QMutex(), main_window))

    sys.exit(qapp.exec_())
