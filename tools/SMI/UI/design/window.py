from PyQt5.QtWidgets import QMainWindow, QTreeWidget


class WindowUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.paks = QTreeWidget()
        self.initWindow()
        self.show()

    def initWindow(self):
        self.setWindowTitle("Saber Model Injector")
        self.setMinimumSize(300, 300)