from PyQt5.QtWidgets import QApplication
from tools.SMI.UI.design.window import WindowUI

import sys


if __name__ == "__main__":
    app = QApplication([])
    window = WindowUI()

    sys.exit(app.exec_())