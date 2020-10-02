from tools.tex_mod.UI.logic.window import Window

from PyQt5.QtWidgets import QApplication

import sys
from os import system


if __name__ == "__main__":
    app = QApplication([])
    window = Window()

    sys.exit(app.exec_())