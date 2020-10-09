from tools.SMI.UI.design.window import WindowUI
from tools.SMI.UI.logic.tree_item import TreeItem
from saber.definitions.template import Template
from tools.recursive_template_import import recursiveTemplateImport
from saber.file import *

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QTreeWidget, QMessageBox


import os


class Window(WindowUI):
    def __init__(self):
        WindowUI.__init__(self)
        self.paks = {}
        self.tree_items = []

        self.scope_layout.addRow("Scope", self.scope_combo)
        self.layout.addLayout(self.scope_layout)
        self.layout.addWidget(self.open_paks)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.scope = ""

        self.file_open.triggered.connect(self.open)
        self.file_save_as.triggered.connect(self.saveAs)

        self.edit_extract.triggered.connect(self.extract)
        self.edit_extract_recursive.triggered.connect(self.extractRecursive)
        self.edit_inject.triggered.connect(self.inject)
        self.edit_inject_recursive.triggered.connect(self.injectRecursive)
        self.edit_delete.triggered.connect(self.delete)
        self.edit_build.triggered.connect(self.buildImeta)

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
            self.scope_combo.addItem(path.split("/")[-1].split(".")[0])

    def extract(self):
        for item in self.open_paks.selectedItems():
            path = QFileDialog.getExistingDirectory(self, "Save directory")
            s3d, imeta = self.paks[item.parent().text(0)]
            s3d.exportChild(path + "/" + item.text(0), item.text(0))

    def extractRecursive(self):
        for item in self.open_paks.selectedItems():
            path = QFileDialog.getExistingDirectory(self, "Save directory")
            s3d, ime = self.paks[item.parent().text(0)]

            # if it's not a template, just extract
            if s3d.children[item.text(0)].type != 12:
                s3d.exportChild(path + "/" + item.text(0), item.text(0))
                return

            os.mkdir(path + "/" + item.text(0))
            template = Template(s3d.children[item.text(0)].data)
            template.extractRecursive(ime, path + "/" + item.text(0))

    def inject(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open template", "", "template (*.tpl)")
        s3dpak, imeta = self.getScope()
        s3dpak.addEntry(path, "Template")
        test = self.open_paks.findItems(self.scope_combo.currentText(), Qt.MatchContains)
        test[0].addChildText(path.split("/")[-1].split(".")[0])

    def injectRecursive(self):
        path = QFileDialog.getExistingDirectory(self, "Template directory")
        s3dpak, imeta = self.getScope()

        self.paks[self.scope_combo.currentText()] = recursiveTemplateImport(s3dpak, imeta, path)

        test = self.open_paks.findItems(self.scope_combo.currentText(), Qt.MatchContains)
        test[0].addChildText(path.split("/")[-1].split(".")[0])

    def buildImeta(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Imeta", "", "imeta (*.imeta)");
        _, imeta, = self.getScope()
        imeta.save(path)

    def delete(self):
        pass



    def save(self):
        pass

    def saveAs(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "s3dpak (*.s3dpak)");
        s3dpak, imeta = self.getScope()
        s3dpak.save(path)



    def getScope(self):
        return self.paks[self.scope_combo.currentText()]