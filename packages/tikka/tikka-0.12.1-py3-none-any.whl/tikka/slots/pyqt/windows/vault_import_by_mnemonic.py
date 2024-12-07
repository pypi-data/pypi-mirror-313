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
from collections import OrderedDict
from typing import Optional

from mnemonic import Mnemonic
from mnemonic.mnemonic import ConfigurationError
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QWidget
from substrateinterface import Keypair, KeypairType

from tikka.domains.application import Application
from tikka.domains.entities.constants import DATA_PATH, WALLETS_PASSWORD_LENGTH
from tikka.libs.secret import generate_alphabetic, sanitize_mnemonic_string
from tikka.slots.pyqt.entities.constants import (
    ADDRESS_MONOSPACE_FONT_NAME,
    DEBOUNCE_TIME,
)
from tikka.slots.pyqt.resources.gui.windows.vault_import_by_mnemonic_rc import (
    Ui_VaultImportByMnemonicDialog,
)


class VaultImportByMnemonicWindow(QDialog, Ui_VaultImportByMnemonicDialog):
    """
    VaultImportByMnemonicWindow class
    """

    language_code_map = {
        "english": "en",
        "french": "fr",
        "chinese_simplified": "zh-hans",
        "chinese_traditional": "zh-hant",
        "italian": "it",
        "japanese": "ja",
        "korean": "ko",
        "spanish": "es",
    }

    def __init__(self, application: Application, parent: Optional[QWidget] = None):
        """
        Init import vault by mnemonic window

        :param application: Application instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self._ = self.application.translator.gettext
        self.language_code = "en"

        # Mnemonic language selector translated
        self.mnemonic_language_displayed = OrderedDict(
            [
                ("en", self._("English")),
                ("fr", self._("French")),
                ("zh-hans", self._("Chinese simplified")),
                ("zh-hant", self._("Chinese traditional")),
                ("it", self._("Italian")),
                ("ja", self._("Japanese")),
                ("ko", self._("Korean")),
                ("es", self._("Spanish")),
            ]
        )

        monospace_font = QFont(ADDRESS_MONOSPACE_FONT_NAME)
        monospace_font.setStyleHint(QFont.Monospace)
        self.addressValueLabel.setFont(monospace_font)

        # buttons
        self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)

        # events
        self.mnemonicLineEdit.textChanged.connect(self._on_mnemonic_changed)
        self.showButton.clicked.connect(self.on_show_button_clicked)
        self.passwordChangeButton.clicked.connect(self._generate_wallet_password)
        self.buttonBox.accepted.connect(self.on_accepted_button)
        self.buttonBox.rejected.connect(self.close)

        # debounce timers
        self.mnemonic_debounce_timer = QTimer()
        self.mnemonic_debounce_timer.timeout.connect(self._mnemonic_debounce_call)

        # fill form
        self.storedPasswordFrame.hide()
        self._generate_wallet_password()

    def _on_mnemonic_changed(self):
        """
        Triggered when mnemonic is changed

        :return:
        """
        if self.mnemonic_debounce_timer.isActive():
            self.mnemonic_debounce_timer.stop()
        self.mnemonic_debounce_timer.start(DEBOUNCE_TIME)

    def _mnemonic_debounce_call(self):
        """
        Debounce function triggered only after idle time when typing mnemonic

        :return:
        """
        # stop mnemonic_debounce_timer to avoid infinite loop
        if self.mnemonic_debounce_timer.isActive():
            self.mnemonic_debounce_timer.stop()

        self.errorLabel.setText("")

        if self.verify_user_entry() is not True:
            return

        try:
            self._generate_address()
        except Exception:
            self.errorLabel.setText(self._("Mnemonic or language not valid!"))
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return

        self._update_wallet_password_fields()

        self.buttonBox.button(self.buttonBox.Ok).setEnabled(True)

    def on_show_button_clicked(self):
        """
        Triggered when user click on show button

        :return:
        """
        if self.mnemonicLineEdit.echoMode() == QLineEdit.Password:
            self.mnemonicLineEdit.setEchoMode(QLineEdit.Normal)
            self.storedpasswordLineEdit.setEchoMode(QLineEdit.Normal)
            self.showButton.setText(self._("Hide"))
        else:
            self.mnemonicLineEdit.setEchoMode(QLineEdit.Password)
            self.storedpasswordLineEdit.setEchoMode(QLineEdit.Password)
            self.showButton.setText(self._("Show"))

    def _update_wallet_password_fields(self):
        """
        Show stored password or new password depending on root account exists or not

        :return:
        """
        # if root account exists, hide the password field
        mnemonic = sanitize_mnemonic_string(self.mnemonicLineEdit.text())
        root_keypair = Keypair.create_from_mnemonic(
            mnemonic=mnemonic,
            language_code=self.language_code,
            crypto_type=KeypairType.SR25519,
            ss58_format=self.application.currencies.get_current().ss58_format,
        )
        if self.application.passwords.exists(root_keypair.ss58_address):
            stored_password = self.application.passwords.get_clear_password(
                root_keypair
            )
            self.storedpasswordLineEdit.setText(stored_password)
            self.storedPasswordFrame.show()
            self.passwordFrame.hide()
        else:
            self.storedPasswordFrame.hide()
            self.passwordFrame.show()

    def _generate_address(self) -> str:
        """
        Generate, display and return address

        :return:
        """
        # sanitize mnemonic string
        mnemonic = sanitize_mnemonic_string(self.mnemonicLineEdit.text())

        address = Keypair.create_from_uri(
            suri=mnemonic,
            ss58_format=self.application.currencies.get_current().ss58_format,
            crypto_type=KeypairType.SR25519,
            language_code=self.language_code,
        ).ss58_address

        self.addressValueLabel.setText(address)
        return address

    def verify_user_entry(self) -> bool:
        """
        Verify user entry, return True if OK, False otherwise

        :return:
        """
        # verify mnemonic
        mnemonic = sanitize_mnemonic_string(self.mnemonicLineEdit.text())
        try:
            self.language_code = self.language_code_map[
                Mnemonic.detect_language(mnemonic)
            ]
        except ConfigurationError as exception:
            logging.exception(exception)
            self.addressValueLabel.setText("")
            self.errorLabel.setText(self._("Language not detected"))
            self.mnemonicLanguageValueLabel.setText("")
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return False

        if not Keypair.validate_mnemonic(mnemonic, self.language_code):
            self.addressValueLabel.setText("")
            self.errorLabel.setText(self._("Mnemonic not valid!"))
            self.mnemonicLanguageValueLabel.setText("")
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return False

        self.mnemonicLanguageValueLabel.setText(
            self.mnemonic_language_displayed[self.language_code]
        )

        return True

    def _generate_wallet_password(self):
        """
        Generate new password for wallet encryption in UI

        :return:
        """
        self.passwordLineEdit.setText(generate_alphabetic(WALLETS_PASSWORD_LENGTH))

    def on_accepted_button(self):
        """
        Triggered when user click on ok button

        :return:
        """
        # user inputs
        mnemonic = sanitize_mnemonic_string(self.mnemonicLineEdit.text())
        name = self.nameLineEdit.text().strip()

        # generated inputs
        password = self.passwordLineEdit.text()

        self.application.vaults.import_from_network(
            mnemonic, self.language_code, name, password
        )


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    VaultImportByMnemonicWindow(application_).exec_()
