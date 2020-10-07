from PyQt5.QtWidgets import QTreeWidgetItem


class TreeItem(QTreeWidgetItem):
    def __init__(self, text):
        QTreeWidgetItem.__init__(self)
        self.setText(0, text)

    def addChildText(self, text):
        entry = QTreeWidgetItem()
        entry.setText(0, text)
        self.addChild(entry)