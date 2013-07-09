from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_frmUsersIBM import *
from libdidyoureadme import *

class frmUsersIBM(QDialog, Ui_frmUsersIBM):
    def __init__(self, mem, user=None,  parent = None, name = None, modal = False):
        QDialog.__init__(self,  parent)
        self.setupUi(self)   
        self.mem=mem
        
        if user==None:   
            self.lbl.setText(self.trUtf8("Add a new user"))
            self.user=User(None, None, None, None, True)
            self.setWindowTitle(self.trUtf8("New user"))
            self.chkActive.setEnabled(False)
        else:
            self.user=user
            self.setWindowTitle(self.trUtf8("Edit user"))
            self.txtName.setText(self.user.name)
            self.txtPost.setText(self.user.post)
            self.txtMail.setText(self.user.mail)
            self.chkActive.setCheckState(b2c(self.user.active))

        
    def on_buttonBox_accepted(self):
        self.user.datetime=now(self.mem.cfgfile.localzone)
        self.user.post=self.txtPost.text()
        self.user.name=self.txtName.text()
        self.user.mail=self.txtMail.text()
        self.user.active=c2b(self.chkActive.checkState())
        self.user.save(self.mem)
        if self.user.active==False:
            self.mem.groups.quit_user_from_all_groups(self.user)
        self.accept()
        
    def on_buttonBox_rejected(self):
        self.reject()

