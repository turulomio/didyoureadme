from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from didyoureadme.ui.Ui_frmUsersIBM import *
from didyoureadme.libdidyoureadme import *

class frmUsersIBM(QDialog, Ui_frmUsersIBM):
    def __init__(self, mem, user=None,  parent = None, name = None, modal = False):
        QDialog.__init__(self,  parent)
        self.setupUi(self)   
        self.mem=mem
        
        if user==None:   
            self.lbl.setText(self.tr("Add a new user"))
            self.user=User(self.mem, None, None, None, None, True)
            self.setWindowTitle(self.tr("New user"))
            self.chkActive.setEnabled(False)
            self.type=1#New
        else:
            self.user=user
            self.was_active=self.user.active
            self.setWindowTitle(self.tr("Edit user"))
            self.txtName.setText(self.user.name)
            self.txtPost.setText(self.user.post)
            self.txtMail.setText(self.user.mail)
            self.chkActive.setCheckState(b2c(self.user.active))
            self.type=2#Edit

        
    def on_buttonBox_accepted(self):
        self.user.datetime=now(self.mem.localzone)
        self.user.post=self.txtPost.text()
        self.user.name=self.txtName.text()
        self.user.mail=self.txtMail.text()
        self.user.active=c2b(self.chkActive.checkState())
        self.user.save()
        if self.type==1:#new
            self.mem.data.users_active.append(self.user)
            self.mem.data.groups.find(1).members.append(self.user)#Añade el usuario al grupo uno. el de todos
        else:#edit
            if self.was_active==True:
                if self.user.active==False:#Cambia
                    self.mem.data.users_active.remove(self.user)
                    self.mem.data.users_inactive.append(self.user)  
                    self.mem.data.groups.quit_user_from_all_groups(self.user)
            else:#Cambia de inactivo a activo
                if self.user.active==True:#Cambia
                    self.mem.data.users_active.append(self.user)
                    self.mem.data.users_inactive.remove(self.user)
                    self.mem.data.groups.find(1).members.append(self.user)#Añade el usuario al grupo uno. el de todos     
        self.mem.con.commit()
        self.accept()
        
    def on_buttonBox_rejected(self):
        self.reject()

