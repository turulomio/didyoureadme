from PyQt5.QtCore import *
from PyQt5.QtGui import *
from didyoureadme.ui.Ui_frmGroupsIBM import *
from didyoureadme.libdidyoureadme import *
from PyQt5.QtWidgets import *

class frmGroupsIBM(QDialog, Ui_frmGroupsIBM):
    def __init__(self, mem,  group=None,  parent = None, name = None, modal = False):
        QDialog.__init__(self,  parent)
        self.setupUi(self)   
        self.mem=mem
        if group==None:
            self.group=Group(self.mem,"", SetUsers(self.mem))
            self.setWindowTitle(self.tr("New Group"))
            self.mem.data.users_active.qlistview(self.lstMembers, self.group.members)
            self.type=1##New
        else:
            self.group=group
            self.setWindowTitle(self.tr("Edit Group"))
            self.txtName.setText(self.group.name)
            self.mem.data.users_active.qlistview(self.lstMembers, self.group.members)
            self.type=2##Edit

        
    def on_buttonBox_accepted(self):
        self.group.name=self.txtName.text()
        self.group.members=self.mem.data.users_active.qlistview_getselected(self.lstMembers, self.mem)
        self.group.save()
        if self.type==1:#new
            self.mem.data.groups.append(self.group)
        self.mem.data.groups.order_by_name()
        self.mem.con.commit()
        self.accept()
        
    def on_buttonBox_rejected(self):
        self.reject()
