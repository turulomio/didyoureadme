from didyoureadme.ui.Ui_wdgDocumentsSearch import Ui_wdgDocumentsSearch
from PyQt5.QtWidgets import QDialog

class wdgDocumentsSearch(QDialog, Ui_wdgDocumentsSearch):
    def __init__(self, mem,  group=None,  parent = None, name = None, modal = False):
        QDialog.__init__(self,  parent)
        self.setupUi(self)
        self.mem=mem
