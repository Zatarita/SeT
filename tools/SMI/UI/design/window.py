from PyQt5.QtWidgets import QMainWindow, QTreeWidget, QWidget, QVBoxLayout, QFormLayout, QComboBox


class WindowUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.open_paks = QTreeWidget()
        self.open_paks.setHeaderHidden(True)

        self.scope_layout = QFormLayout()
        self.layout = QVBoxLayout()
        self.widget = QWidget()

        self.scope_combo = QComboBox()

        self.file = self.menuBar().addMenu("File")
        self.file_open = self.file.addAction("Open")
        self.file_open.setShortcut("Ctrl+O")
        self.file_save = self.file.addAction("Save")
        self.file_save.setShortcut("Ctrl+S")
        self.file_save_as = self.file.addAction("Save As..")
        self.file_save_as.setShortcut("Ctrl+Shift+S")

        self.edit = self.menuBar().addMenu("Edit")
        self.edit_inject = self.edit.addAction("Inject")
        self.edit_inject_recursive = self.edit.addAction("Inject Recursive")
        self.edit_inject.setShortcut("Ctrl+I")
        self.edit_inject_recursive.setShortcut("Ctrl+Shift+I")

        self.edit_extract = self.edit.addAction("Extract")
        self.edit_extract_recursive = self.edit.addAction("Extract Recursive")
        self.edit_extract.setShortcut("Ctrl+E")
        self.edit_extract_recursive.setShortcut("Ctrl+Shift+E")

        self.edit.addSeparator()

        self.edit_delete = self.edit.addAction("Delete")
        self.edit_delete.setShortcut("Delete")

        self.edit.addSeparator()

        self.edit_build = self.edit.addAction("Build Imeta")
        self.edit_build.setShortcut("F2")

        self.initWindow()



    def initWindow(self):
        self.setWindowTitle("Saber Model Injector")
        self.setMinimumSize(300, 300)
        self.show()