from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_frmGroupsIBM import *
from libdidyoureadme import *

class frmGroupsIBM(QDialog, Ui_frmGroupsIBM):
    def __init__(self, mem,  group=None,  parent = None, name = None, modal = False):
        QDialog.__init__(self,  parent)
        self.setupUi(self)   
        self.mem=mem
        if group==None:
            self.group=Group(self.mem,"", SetUsers(self.mem))
            self.setWindowTitle(self.trUtf8("New Group"))
            self.mem.data.users_all().qlistview(self.lstMembers, False, self.group.members)
            self.type=1##New
        else:
            self.group=group
            self.setWindowTitle(self.trUtf8("Edit Group"))
            self.txtName.setText(self.group.name)
            self.mem.data.users_all().qlistview(self.lstMembers, False, self.group.members)
            self.type=2##Edit

        
    def on_buttonBox_accepted(self):
        self.group.name=self.txtName.text()
        self.group.members=SetUsers(self.mem)
        for i in range(self.lstMembers.model().rowCount()):
            if self.lstMembers.model().index(i, 0).data(Qt.CheckStateRole)==Qt.Checked:
                usuario=self.lstMembers.model().index(i, 0).data(Qt.UserRole)
                self.group.members.append(self.mem.data.users_all().find(usuario))        
        self.group.save()
        if self.type==1:#new
            self.mem.data.groups.append(self.group)
        self.mem.data.groups.order_by_name()
        self.mem.con.commit()
        self.accept()
        
    def on_buttonBox_rejected(self):
        self.reject()
