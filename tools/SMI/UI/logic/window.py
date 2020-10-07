from tools.SMI.UI.design.window import WindowUI
from tools.SMI.UI.logic.tree_item import TreeItem
from saber.definitions.template import Template
from tools.recursive_template_import import recursiveTemplateImport
from saber.file import *

from PyQt5.QtWidgets import QFileDialog, QTreeWidget, QMessageBox


import os


class Window(WindowUI):
    def __init__(self):
        WindowUI.__init__(self)
        self.paks = {}
        self.tree_items = []

        self.layout.addWidget(self.open_paks)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.file_open.triggered.connect(self.open)

        self.edit_extract.triggered.connect(self.extract)
        self.edit_extract_recursive.triggered.connect(self.extractRecursive)

    def open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open S3dpak", "", "s3dpak (*.s3dpak)")
        imeta_path = path.split(".")[0] + ".imeta"
        if path != "":
            # create the objects
            imeta = Imeta()
            s3dpak = SaberPak()

            # verify imeta path
            if not os.path.exists(imeta_path):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("The imeta wasn't in the same directory as the s3dpak\nPress OK to locate the imeta.")
                msg.setWindowTitle("Unable to locate imeta")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                returnValue = msg.exec()
                if returnValue == QMessageBox.Cancel:
                    return
                imeta_path, _ = QFileDialog.getOpenFileName(self, "Open Imeta", "", "imeta (*.imeta)")

            # load the data
            s3dpak.load(path, True)
            imeta.load(imeta_path)

            # parse data
            s3dpak.parseData()
            imeta.parseData()

            # save the opened packs as a dictionary mapping s3dpak name to s3dpak and imeta
            self.paks.update({path.split("/")[-1].split(".")[0]: (s3dpak, imeta)})

            # add the data to the treewidget
            entry = TreeItem(path.split("/")[-1].split(".")[0])
            self.open_paks.addTopLevelItem(entry)

            for name in s3dpak.names():
                entry.addChildText(name)

            self.tree_items.append(entry)

    def extract(self):
        for item in self.open_paks.selectedItems():
            test = (item.parent().text(0), item.text(0))
            s3d, imeta = self.paks[item.parent().text(0)]
            s3d.exportChild("test", item.text(0))

    def extractRecursive(self):
        for item in self.open_paks.selectedItems():
            s3d, ime = self.paks[item.parent().text(0)]
            template = Template(s3d.children[item.text(0)].data)
            template.extractRecursive(ime, "test")