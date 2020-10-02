from tools.tex_mod.UI.design.window import WindowUI
from saber.file import Ipak

from PyQt5.QtWidgets import QFileDialog, QTreeWidgetItem, QTreeWidget


class Window(WindowUI):
    def __init__(self):
        WindowUI.__init__(self)

        self.ipak = Ipak()
        self.current_item = ""
        self.current_file = ""

        self.initMenu()
        self.initElements()

        self.show()

    def initMenu(self):
        self.file_open.triggered.connect(self.open)
        self.file_save.triggered.connect(self.save)
        self.file_save_as.triggered.connect(self.saveAs)

        self.edit_import_dds.triggered.connect(self.importDDS)
        self.edit_import_raw.triggered.connect(self.importRaw)
        self.edit_export.triggered.connect(self.export)
        self.edit_delete.triggered.connect(self.delete)

    def initElements(self):
        self.save_dds_button.clicked.connect(self.saveDDSClicked)
        self.import_dds_button.clicked.connect(self.loadDDSClicked)
        self.save_dds_button.setText("Save to DDS")
        self.import_dds_button.setText("Load from DDS")

        self.file_contents.itemDoubleClicked.connect(self.doubleClick)
        #self.name.textChanged.connect(self.nameChanged)
        self.texture_width.textChanged.connect(self.widthChanged)
        self.texture_height.textChanged.connect(self.heightChanged)
        self.mipmap_count.textChanged.connect(self.mipmapChanged)
        self.face_count.textChanged.connect(self.faceCountChanged)
        self.type.currentTextChanged.connect(self.typeChanged)

# -------------------------------------------------------------------UI Functions
    def saveDDSClicked(self):
        pass

    def loadDDSClicked(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open DDS", "", "dds texure (*.dds)")
        if file != "":
            self.ipak.children[self.current_item].loadFromDDS(file)
            self.populateCurrent()

    def doubleClick(self, item, column):
        self.current_item = item.text(0)
        self.populateCurrent()

    def populateCurrent(self):
        self.name.setText(self.current_item)
        self.type.setCurrentText(self.ipak.type_definitions.get(self.ipak.children[self.current_item].type))
        self.texture_height.setText(str(self.ipak.children[self.current_item].height))
        self.texture_width.setText(str(self.ipak.children[self.current_item].width))
        self.mipmap_count.setValue(self.ipak.children[self.current_item].mip_map_count)
        self.face_count.setValue(self.ipak.children[self.current_item].face_count)

    #adds some complications ill take care of later

    #def nameChanged(self):
        #if self.current_item == "": return
        #self.ipak.imeta.children[self.current_item].string = self.name.text()
        #self.file_contents.currentItem().setText(0,self.name.text())

    def widthChanged(self):
        if self.current_item == "": return
        self.ipak.children[self.current_item].width = int(self.texture_width.text())

    def heightChanged(self):
        if self.current_item == "": return
        self.ipak.children[self.current_item].height = int(self.texture_height.text())

    def mipmapChanged(self):
        if self.current_item == "": return
        self.ipak.children[self.current_item].mip_map_count = int(self.mipmap_count.text())

    def faceCountChanged(self):
        if self.current_item == "": return
        self.ipak.children[self.current_item].face_count = int(self.face_count.text())

    def typeChanged(self, string):
        if self.current_item == "": return
        for item, value in self.ipak.type_definitions.items():
            if value == string:
                self.ipak.children[self.current_item].type = item
        self.ipak.imeta.children[self.current_item].typeFromIpakChild(self.ipak.children[self.current_item])

# -------------------------------------------------------------------Menu Functions
    # -----------------------------------------------------File Menu
    def open(self):
        self.current_file, _ = QFileDialog.getOpenFileName(self, "Open Ipak", "", "Ipak (*.ipak)")
        if self.current_file != "":
            self.ipak.load(self.current_file, True)
            self.ipak.parseData()

            for name in self.ipak.names():
                self.file_contents.addTopLevelItem(QTreeWidgetItem(self.file_contents, [name]))

    def save(self):
        if self.current_file:
            self.ipak.save(self.current_file)
        else:
            self.saveAs()

    def saveAs(self):
        self.current_file, _ = QFileDialog.getSaveFileName(self, "Save File", "", "ipak (*.ipak)")
        self.ipak.save(self.current_file)

    # -----------------------------------------------------Edit Menu
    def importDDS(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Texture", "", "dds texture (*.dds)")
        if file != "":
            self.ipak.loadFromDDS(file)
            self.file_contents.addTopLevelItem(QTreeWidgetItem(self.file_contents, [file.split("/")[-1].split(".")[0]]))

    def importRaw(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Texture", "", "dds texture (*.dds)")
        if file != "":
            self.ipak.loadFromRaw(file)
            self.file_contents.addTopLevelItem(QTreeWidgetItem(self.file_contents, [file.split("/")[-1].split(".")[0]]))

    def export(self):
        if self.current_item == "": return
        self.ipak.exportChild("test", self.current_item)

    def delete(self):
        pass
