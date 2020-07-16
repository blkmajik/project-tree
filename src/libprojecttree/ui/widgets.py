# Core
import time
import os
import os.path
import logging

# 3rd party
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtSvg

# 1st party
from .. import gui
from .. import paths

ICON_SIZE = 32


class IconLayout(QtWidgets.QVBoxLayout):
    """Create a layout with it's sole content being an icon
    """
    def __init__(self, image, width=ICON_SIZE, height=ICON_SIZE, parent=None):
        super().__init__(parent=parent)

        self.icon = Icon(image, width=width, height=height, parent=parent)
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(self.icon.pixmap(self.icon.size))
        self.addWidget(self.label)


class IconLabel(QtWidgets.QLabel):
    """Create new label widget with it's sole content as an icon

    """
    def __init__(self, image, width=ICON_SIZE, height=ICON_SIZE, parent=None):
        super().__init__(parent=parent)
        self.icon = Icon(image, width=width, height=height, parent=parent)
        self.setPixmap(self.icon.pixmap(self.icon.size))


class Icon(QtGui.QIcon):
    """Create an icon based off of an image name that we look up in a specific
    path.

    """
    def __init__(self, image, width=ICON_SIZE, height=ICON_SIZE, parent=None):
        super().__init__(parent=parent)
        self.size = QtCore.QSize(width, height)
        normal = os.path.join(paths.imgDir, image)
        root, ext = os.path.splitext(image)
        disabled = os.path.join(paths.imgDir, "%s-disabled%s" % (root, ext))

        self.addFile(normal, self.size, mode=self.Normal)
        if os.path.exists(disabled):
            self.addFile(disabled, self.size, mode=self.Disabled)


class DesignerWindow(QtWidgets.QMainWindow):
    def __init__(self, ui, parent=None):
        super().__init__(parent=parent)
        self.ui = ui()

        self.setupUi()
        self.createActions()
        self.connectSignals()

    def setupUi(self):
        self.ui.setupUi(self)

    def createActions(self):
        pass

    def connectSignals(self):
        pass

    def warn(self, message):
        self.setEnabled(True)
        self.status.showMessage(message, 10000)

    def _fail(self, msgType, message):
        self.setEnabled(True)
        self.status.showMessage(message, 10000)
        self.notice.showMessage(message, msgType)

    def failAuth(self, message):
        self._fail("auth-failed", message)

    def failApiAdd(self, message):
        self._fail("api-add-failed", message)

    def failApi(self, message):
        self._fail("api-generic-failed", message)

    def failSearch(self, message):
        self._fail("search-failed", message)
