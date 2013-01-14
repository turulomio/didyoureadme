import os,  shutil
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_frmDocumentsIBM import *
from libdidyoureadme import *

class frmDocumentsIBM(QDialog, Ui_frmDocumentsIBM):
    def __init__(self, mem, parent = None, name = None, modal = False):
        # tipo 1 - Insertar selDate=None
        # tipo2 - Modificar selDate!=None
        QDialog.__init__(self,  parent)
        self.setupUi(self)   
        self.mem=mem
        self.mem.users.qcombobox(self.cmbUsers, False, [])
        self.mem.groups.qcombobox(self.cmbGroups, [])

    def on_cmd_pressed(self):
        #Genera los usuarios a los que se enviar´a el documento
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
        
        usuarios=set()
        for i in range(self.cmbGroups.count()):
            if self.cmbGroups.itemData(i, Qt.CheckStateRole)==Qt.Checked:
                grupo=self.cmbGroups.itemData(i, Qt.UserRole)
                for u in self.mem.groups.group(grupo).members:
                    usuarios.add(u)
        for i in range(self.cmbUsers.count()):
            if self.cmbUsers.itemData(i, Qt.CheckStateRole)==Qt.Checked:
                usuario=self.cmbUsers.itemData(i, Qt.UserRole)
                usuarios.add(self.mem.users.user(usuario))               

        if len(list(usuarios))==0:
            m=QMessageBox()
            m.setIcon(QMessageBox.Information)
            m.setText(self.trUtf8("You have to select at least one recipient"))
            m.exec_()          
            return

        #Genera el documento
        d=Document(now(self.mem.cfgfile.localzone), self.txtTitle.text(), self.txtFilename.text(), self.txtComment.toPlainText())
        cur=self.mem.con.cursor()
        d.save(self.mem)
        
        #Genera el userdocument
        for u in list(usuarios):
            if u.active==True:
                ud=UserDocument(u, d, self.mem)
                ud.save()
        self.mem.documents.arr.append(d)
        cur.close()
        
        #Lo copia
        shutil.copyfile(self.txtFilename.text(), dirDocs+d.hash)
        self.done(0)

    def on_cmdFile_released(self):
        cwd=os.getcwd()
        os.chdir(os.path.expanduser("~/"))
        self.txtFilename.setText(QFileDialog.getOpenFileName(self, "", "", self.trUtf8("All documents (*)")))
        os.chdir(cwd)
