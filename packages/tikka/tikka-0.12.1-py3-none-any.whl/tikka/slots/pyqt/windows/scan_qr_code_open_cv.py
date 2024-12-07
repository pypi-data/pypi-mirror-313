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
from typing import List, Optional

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QDialog, QWidget
from substrateinterface.utils.ss58 import is_valid_ss58_address

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.events import AccountEvent
from tikka.slots.pyqt.entities.constants import ADDRESS_MONOSPACE_FONT_NAME
from tikka.slots.pyqt.resources.gui.windows.scan_qrcode_rc import Ui_ScanQRCodeDialog


class ScanQRCodeOpenCVWindow(QDialog, Ui_ScanQRCodeDialog):
    """
    ScanQRCodeOpenCVWindow class
    """

    def __init__(self, application: Application, parent: Optional[QWidget] = None):
        """
        Init scan qrcode OpenCV window

        :param application: Application instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self._ = self.application.translator.gettext
        self.address: Optional[str] = None

        # set monospace font to address field
        monospace_font = QFont(ADDRESS_MONOSPACE_FONT_NAME)
        monospace_font.setStyleHint(QFont.Monospace)
        self.addressValueLabel.setFont(monospace_font)

        # buttons
        self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)

        # events
        self.buttonBox.accepted.connect(self.on_accepted_button)
        self.buttonBox.rejected.connect(self.close)

        camera_index = self.get_available_camera_opencv_index()
        if camera_index is not None:
            self.address = self.opencv_webcam_qrcode_scanner(camera_index)
            if self.address is not None:
                self.addressValueLabel.setText(self.address)
                self.errorLabel.setText("")
                self.buttonBox.button(self.buttonBox.Ok).setEnabled(True)
            else:
                self.errorLabel.setText(self._("QRCode Scanner canceled"))
        else:
            self.errorLabel.setText(self._("No camera available"))

    @staticmethod
    def opencv_webcam_qrcode_scanner(camera_index: int) -> Optional[str]:
        """
        Open OpenCV webcam window to scan QR Code

        :param camera_index: Camera index to use as scanner
        :return:
        """
        # if OpenCV lib is imported at start of the module, this error occurs :
        #
        # QObject::moveToThread: Current thread (0x55a5fbae7cc0) is not the object's thread (0x55a5fc1c79f0).
        # Cannot move to target thread (0x55a5fbae7cc0)
        #
        # qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in
        # "/home/vit/Documents/dev/python/tikka/.venv/lib/python3.7/site-packages/cv2/qt/plugins"
        # even though it was found.
        # This application failed to start because no Qt platform plugin could be initialized. Reinstalling the
        # application may fix this problem.
        #
        # Available platform plugins are: xcb, eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl,
        # wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl.
        #
        # So we import OpenCV lib here, as a dirty trick to display OpenCV window in Qt GUI
        import cv2

        address: Optional[str] = None
        detector = cv2.QRCodeDetector()
        cap = cv2.VideoCapture(camera_index)
        while True:
            _, img = cap.read()
            # detect and decode
            data, bbox, _ = detector.detectAndDecode(img)
            # check if there is a QRCode in the image
            if data:
                if is_valid_ss58_address(data):
                    address = data
                    break
            cv2.imshow("QRCODE Scanner", img)
            key = cv2.waitKey(1)
            # close window to stop loop
            if cv2.getWindowProperty("QRCODE Scanner", cv2.WND_PROP_VISIBLE) < 1:
                break
            # Esc key to stop loop
            if key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

        return address

    @staticmethod
    def get_available_camera_opencv_index() -> Optional[int]:
        """
        Return first available working camera index or None

        :return:
        """
        import cv2

        non_working_ports: List[int] = []
        dev_port = 0
        working_ports: List[int] = []
        available_ports: List[int] = []
        while (
            len(non_working_ports) < 5
        ):  # if there are more than 5 non working ports stop the testing.
            camera = cv2.VideoCapture(dev_port)
            if not camera.isOpened():
                non_working_ports.append(dev_port)
                logging.debug("Port %s is not working." % dev_port)
            else:
                is_reading, img = camera.read()
                width = camera.get(3)
                height = camera.get(4)
                if is_reading:
                    logging.debug(
                        "Camera %s is working and reads images (%s x %s)"
                        % (dev_port, width, height)
                    )
                    working_ports.append(dev_port)
                else:
                    logging.debug(
                        "Port %s for camera ( %s x %s) is present but does not reads."
                        % (dev_port, width, height)
                    )
                    available_ports.append(dev_port)
            dev_port += 1
        if len(working_ports) > 0:
            return working_ports[0]
        return None

    def on_accepted_button(self) -> None:
        """
        Triggered when user click on ok button

        :return:
        """
        if self.address is not None:
            account = self.application.accounts.get_by_address(self.address)
            if account is None:
                # create account instance
                account = Account(self.address, name=self._("Added from a QRCode"))

                # add instance in application
                self.application.accounts.add(account)
            else:
                # dispatch event
                event = AccountEvent(
                    AccountEvent.EVENT_TYPE_ADD,
                    account,
                )
                self.application.event_dispatcher.dispatch_event(event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    window = ScanQRCodeOpenCVWindow(application_)
    if window.address is not None:
        # display window
        window.exec_()
