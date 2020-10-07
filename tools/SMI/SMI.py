from PyQt5.QtWidgets import QApplication
from tools.SMI.UI.logic.window import Window

import sys


if __name__ == "__main__":
    app = QApplication([])
    window = Window()

    sys.exit(app.exec_())