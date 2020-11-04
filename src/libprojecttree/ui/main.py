# Core
import time
import os
import os.path
import logging
import shlex
import hashlib
import base64

# 3rd party
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtSvg

# 1st party
from . import widgets
from .. import gui

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Window(widgets.DesignerWindow):
    def __init__(self, ui, path, parent=None):
        self.base = path
        super().__init__(ui, parent=parent)
        self.name = os.path.basename(self.base)
        self.setWindowTitle("%s - %s - Project Tree" % (self.name, self.base))
        icon = widgets.Icon("project.svg", parent=self)
        self.setWindowIcon(icon)


    def setupUi(self):
        super().setupUi()
        self.model =  QtWidgets.QFileSystemModel()
        self.model.setRootPath(self.base)
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setRootIndex(self.model.index(self.base))

        self.fixColumns()

    def connectSignals(self):
        super().connectSignals()
        self.ui.treeView.doubleClicked.connect(self.onDoubleClick)


    def fixColumns(self):
        width = self.model.columnCount()

        for i in range(1, width):
            #mode = QtWidgets.QHeaderView.ResizeToContents
            #if i == 0:
            #    mode = QtWidgets.QHeaderView.Stretch
            self.ui.treeView.setColumnHidden(i, True)
            #().setSectionResizeMode(i, mode)

    def onDoubleClick(self, index):
        log = logging.getLogger("%s.Window.onDoubleClick" % __name__)
        data = index.data()
        fullPath = self.model.filePath(index)
        fullPathEnc = fullPath.encode("utf-8")
        server = base64.b64encode(hashlib.md5(fullPathEnc).digest())
        cmd = [
                "gvim",
                "--servername", server.decode("utf-8"),
                "-geometry", "80x57",
                "--remote-silent",
                fullPath,
                ]
        log.info("Executing: %s" % " ".join([shlex.quote(x) for x in cmd]))
        if not os.path.isfile(fullPath):
            return
        
        pid = os.fork()
        if pid == 0:
            # Child
            os.execvp(cmd[0], cmd)
            os._exit()
            
