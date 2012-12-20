from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_frmGroupsIBM import *
from libdidyoureadme import *

class frmGroupsIBM(QDialog, Ui_frmGroupsIBM):
    def __init__(self, mem,  group=None,  parent = None, name = None, modal = False):
        # tipo 1 - Insertar selDate=None
        # tipo2 - Modificar selDate!=None
        QDialog.__init__(self,  parent)
        self.setupUi(self)   
        self.mem=mem
        
        if group==None:
            self.group=Group("", [])
            self.setWindowTitle(self.trUtf8("New Group"))
            self.mem.users.qcombobox(self.cmbMembers, False, [])
        else:
            self.group=group
            self.setWindowTitle(self.trUtf8("Edit Group"))
            self.txtName.setText(self.group.name)
            self.mem.users.qcombobox(self.cmbMembers, False, self.group.members)

        
    def on_buttonBox_accepted(self):
        self.group.name=self.txtName.text()
        self.group.members=self.mem.users.qcombobox2list(self.cmbMembers)
        self.group.save(self.mem)
        self.accept()
        
    def on_buttonBox_rejected(self):
        self.reject()
