import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_frmDocumentsIBM import *
from libdidyoureadme import *

class frmDocumentsIBM(QDialog, Ui_frmDocumentsIBM):
    def __init__(self, mem, document=None, parent = None, name = None, modal = False):
        # tipo 1 - Insertar selDate=None
        # tipo2 - Modificar selDate!=None
        QDialog.__init__(self,  parent)
        self.setupUi(self)   
        self.mem=mem
        self.document=document
        if self.document==None:#New
            self.mem.users.qlistview(self.lstUsers, False, [])
            self.mem.groups.qlistview(self.lstGroups, [])
            self.selectedUsers=set()
            self.teExpiration.setDate(datetime.date.today()+datetime.timedelta(days=90))
        else:
            self.lstUsers.setEnabled(False)
            self.txtTitle.setEnabled(False)
            self.lstGroups.setEnabled(False)
            self.laySend.setEnabled(False)
            self.txtComment.setEnabled(False)
            self.txtFilename.setEnabled(False)
            self.cmdFile.setEnabled(False)
            self.txtTitle.setText(self.document.title)
            self.txtComment.setDocument(QTextDocument(self.document.comment))
            self.teExpiration.setDate(self.document.expiration)
            self.setWindowTitle(self.tr("Change expiration to document"))
            self.cmd.setText(self.tr("Change expiration"))

    def getSelectedUsers(self):        
        self.selectedUsers=set()
        for i in range(self.lstGroups.model().rowCount()):
            if self.lstGroups.model().index(i, 0).data(Qt.CheckStateRole)==Qt.Checked:
                grupo=self.lstGroups.model().index(i, 0).data(Qt.UserRole)
                for u in self.mem.groups.group(grupo).members:
                    self.selectedUsers.add(u)
        for i in range(self.lstUsers.model().rowCount()):
            if self.lstUsers.model().index(i, 0).data(Qt.CheckStateRole)==Qt.Checked:
                usuario=self.lstUsers.model().index(i, 0).data(Qt.UserRole)
                self.selectedUsers.add(self.mem.users.user(usuario))               
        
        self.cmd.setText(self.trUtf8("Send document to {0} users".format(len(list(self.selectedUsers)))))

    def on_lstUsers_clicked(self, modelindex):
        self.getSelectedUsers()

    def on_lstGroups_clicked(self, modelindex):
        self.getSelectedUsers()

    def on_cmd_pressed(self):
    

        if self.document==None:
            #Genera los self.selectedUsers a los que se enviar´a el documento
            if self.txtTitle.text()=="":
                m=QMessageBox()
                m.setIcon(QMessageBox.Information)
                m.setText(self.trUtf8("You must add a title of the document"))
                m.exec_()          
                return
            
            if not os.path.exists(self.txtFilename.text()):
                m=QMessageBox()
                m.setIcon(QMessageBox.Information)
                m.setText(self.trUtf8("I can't find the document"))
                m.exec_()          
                return
                
            if not os.path.isfile(self.txtFilename.text()):
                m=QMessageBox()
                m.setIcon(QMessageBox.Information)
                m.setText(self.trUtf8("You have not select a file. Please, select one."))
                m.exec_()          
                return
    
            if len(list(self.selectedUsers))==0:
                m=QMessageBox()
                m.setIcon(QMessageBox.Information)
                m.setText(self.trUtf8("You have to select at least one recipient"))
                m.exec_()          
                return            
            #Genera el documento
            self.document=Document(self.mem, now(self.mem.cfgfile.localzone), self.txtTitle.text(), self.txtFilename.text(), self.txtComment.toPlainText(),  dt(self.teExpiration.date().toPyDate(), datetime.time(23,59), self.mem.cfgfile.localzone))
            self.document.save(self.mem)
            
            #Genera el userdocument
            for u in list(self.selectedUsers):
                if u.active==True:
                    ud=UserDocument(u, self.document, self.mem)
                    ud.save()
            self.mem.documents.arr.append(self.document)
            self.mem.documents.sort()
            cur=self.mem.con.cursor()
            self.document.updateNums(cur)
            cur.close()
        else:
            self.document.expiration=dt(self.teExpiration.date().toPyDate(), datetime.time(23,59), self.mem.cfgfile.localzone)
            self.document.save(self.mem)
            if self.document.expiration>now(self.mem.cfgfile.localzone):
                self.mem.documents.arr.append(self.document)        
                self.mem.documents.sort()
            
            
        self.done(0)

    def on_cmdFile_released(self):
        cwd=os.getcwd()
        os.chdir(os.path.expanduser("~/"))
        self.txtFilename.setText(QFileDialog.getOpenFileName(self, "", "", self.trUtf8("All documents (*)")))
        os.chdir(cwd)
