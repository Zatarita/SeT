from PyQt5.QtWidgets import QMainWindow, QTreeWidget, QVBoxLayout, QHBoxLayout, QWidget,\
                            QLineEdit, QPushButton, QSpinBox, QComboBox, QFormLayout, QLabel
from PyQt5.QtGui import QImage


class WindowUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.widget = QWidget()
        self.primary_layout = QHBoxLayout()
        self.file_contents = QTreeWidget()
        self.secondary_layout = QFormLayout()

        self.name = QLineEdit()
        self.texture_height = QLineEdit()
        self.texture_width = QLineEdit()
        self.texture_size = QLineEdit()
        self.mipmap_count = QSpinBox()
        self.face_count = QSpinBox()

        self.type = QComboBox()

        self.image = QLabel()
        self.preview = QImage()

        self.save_dds_button = QPushButton()
        self.import_dds_button = QPushButton()

        self.file_menu = self.menuBar().addMenu("File")
        self.file_open = self.file_menu.addAction("Open")
        self.file_save = self.file_menu.addAction("Save")
        self.file_save_as = self.file_menu.addAction("Save As...")

        self.edit_menu = self.menuBar().addMenu("Edit")
        self.edit_import_dds = self.edit_menu.addAction("Import DDS")
        self.edit_import_raw = self.edit_menu.addAction("Import Raw")
        self.edit_export = self.edit_menu.addAction("Export")
        self.edit_delete = self.edit_menu.addAction("Delete")
        self.edit_menu.addSeparator()

        self.initWindow()

    def initWindow(self):
        self.setWindowTitle("Saber Tex Mod")
        self.setMinimumSize(600, 250)

        self.type.addItems(["ARGB8888", "AI88", "OXT1", "AXT1", "XT3", "XT5", "XRGB8888", "DXN", "XT5A"])

        self.primary_layout.addWidget(self.file_contents)
        self.secondary_layout.addRow("Preview", self.image)
        self.secondary_layout.addRow("Name", self.name)
        self.secondary_layout.addRow("Type", self.type)
        self.secondary_layout.addRow("Height", self.texture_height)
        self.secondary_layout.addRow("Width", self.texture_width)
        self.secondary_layout.addRow("Mipmap Count", self.mipmap_count)
        self.secondary_layout.addRow("Face Count", self.face_count)
        self.secondary_layout.addRow("", self.save_dds_button)
        self.secondary_layout.addRow("", self.import_dds_button)

        self.texture_size.setEnabled(False)

        self.primary_layout.addLayout(self.secondary_layout)
        self.widget.setLayout(self.primary_layout)

        self.setCentralWidget(self.widget)

