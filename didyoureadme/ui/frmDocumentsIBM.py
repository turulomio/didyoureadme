import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from didyoureadme.ui.Ui_frmDocumentsIBM import *
from didyoureadme.libdidyoureadme import *

class frmDocumentsIBM(QDialog, Ui_frmDocumentsIBM):
    def __init__(self, mem, document=None, parent = None, name = None, modal = False):
        # tipo 1 - Insertar selDate=None
        # tipo2 - Modificar selDate!=None
        QDialog.__init__(self,  parent)
        self.setupUi(self)   
        self.mem=mem
        self.document=document
        if self.document==None:#New
            self.mem.data.users_active.qlistview(self.lstUsers, SetUsers(self.mem))
            self.mem.data.groups.qlistview(self.lstGroups, SetGroups(self.mem))
            self.selectedUsers=SetUsers(self.mem)
            self.teExpiration.setDate(datetime.date.today()+datetime.timedelta(days=90))
        else:
            self.lstUsers.setEnabled(False)
            self.txtTitle.setEnabled(False)
            self.lstGroups.setEnabled(False)
            self.laySend.setEnabled(False)
            self.txtComment.setEnabled(False)
            self.txtFilename.setEnabled(False)
            self.cmdFile.setEnabled(False)
            self.txtTitle.setText(self.document.name)
            self.txtComment.setDocument(QTextDocument(self.document.comment))
            self.teExpiration.setDate(self.document.expiration+datetime.timedelta(days=1))
            self.setWindowTitle(self.tr("Change expiration to document"))
            self.cmd.setText(self.tr("Change expiration"))

    def getSelectedUsers(self):        
        del self.selectedUsers
        self.selectedUsers=SetUsers(self.mem)
        for g in self.mem.data.groups.qlistview_getselected(self.lstGroups, self.mem).arr:
            self.selectedUsers=self.selectedUsers.union(g.members, self.mem)        
        self.selectedUsers=self.selectedUsers.union(self.mem.data.users_active.qlistview_getselected(self.lstUsers, self.mem), self.mem)
        self.cmd.setText(self.tr("Send document to {0} users".format(self.selectedUsers.length())))

    def on_lstUsers_clicked(self, modelindex):
        self.getSelectedUsers()

    def on_lstGroups_clicked(self, modelindex):
        self.getSelectedUsers()

    def on_cmd_pressed(self):
        if self.document==None: #Nuevo
            #Genera los self.selectedUsers a los que se enviará el documento
            if self.txtTitle.text()=="":
                m=QMessageBox()
                m.setWindowIcon(QIcon(":/didyoureadme.png"))
                m.setIcon(QMessageBox.Information)
                m.setText(self.tr("You must add a title of the document"))
                m.exec_()          
                return
            
            if not os.path.exists(self.txtFilename.text()):
                m=QMessageBox()
                m.setWindowIcon(QIcon(":/didyoureadme.png"))
                m.setIcon(QMessageBox.Information)
                m.setText(self.tr("I can't find the document"))
                m.exec_()          
                return
                
            if not os.path.isfile(self.txtFilename.text()):
                m=QMessageBox()
                m.setWindowIcon(QIcon(":/didyoureadme.png"))
                m.setIcon(QMessageBox.Information)
                m.setText(self.tr("You have not select a file. Please, select one."))
                m.exec_()          
                return
    
            if self.selectedUsers.length()==0:
                m=QMessageBox()
                m.setWindowIcon(QIcon(":/didyoureadme.png"))
                m.setIcon(QMessageBox.Information)
                m.setText(self.tr("You have to select at least one recipient"))
                m.exec_()          
                return            
            #Genera el documento
            self.document=Document(self.mem).init__create( now(self.mem.localzone), self.txtTitle.text(), self.txtFilename.text(), self.txtComment.toPlainText(),  dt(self.teExpiration.date().toPyDate(), datetime.time(23,59), self.mem.localzone))
            self.document.save()
            
            #Genera el userdocument
            for u in self.selectedUsers.arr:
                if u.active==True:
                    ud=UserDocument(u, self.document, self.mem)
                    ud.save()
            self.mem.data.documents_active.append(self.document)
            self.mem.data.documents_active.order_by_datetime()
            self.document.updateNums()
        else:
            self.document.expiration=dt(self.teExpiration.date().toPyDate(), datetime.time(23,59), self.mem.localzone)
            self.document.save()
            if self.document.isExpired()==False:
                self.mem.data.documents_inactive.remove(self.document)
                self.mem.data.documents_active.append(self.document)        
                self.mem.data.documents_active.order_by_datetime()
        self.mem.con.commit()
        self.mem.log(self.tr("Document {} added to the system".format(self.document.id)))
        self.done(0)

    def on_cmdFile_released(self):
        cwd=os.getcwd()
        os.chdir(os.path.expanduser("~/"))
        self.txtFilename.setText(QFileDialog.getOpenFileName(self, "", "", self.tr("All documents (*)")) [0])
        os.chdir(cwd)
