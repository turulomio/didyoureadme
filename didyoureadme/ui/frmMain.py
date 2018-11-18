import datetime
import urllib.request
import shutil
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from didyoureadme.libdidyoureadme import *
from didyoureadme.version import __version__, __versiondate__

from didyoureadme.ui.Ui_frmMain import *
from didyoureadme.ui.frmAbout import *
from didyoureadme.ui.frmSettings import *
from didyoureadme.ui.frmHelp import *
from didyoureadme.ui.frmDocumentsIBM import *
from didyoureadme.ui.frmGroupsIBM import *
from didyoureadme.ui.frmUsersIBM import *


class frmMain(QMainWindow, Ui_frmMain):#    
    def __init__(self, mem, parent = 0,  flags = False):
        QMainWindow.__init__(self)
        self.setupUi(self)      
        self.mem=mem          

        self.mem.data.load()
        
        self.users=None#Pointer
        self.documents=None#Pointer
        
        self.tblDocuments.settings(self.mem, "frmMain", "tblDocuments")
        self.tblDocuments.setVerticalHeaderHeight(None)
        self.tblUsers.settings(self.mem, "frmMain", "tblUsers")      
        self.tblUsers.setVerticalHeaderHeight(None)
        self.tblGroups.settings(self.mem, "frmMain", "tblGroups")
        self.tblGroups.setVerticalHeaderHeight(None)

        
        self.confirmclose=True
        
        self.setWindowTitle(self.tr("DidYouReadMe 2012-{} \xa9").format(__versiondate__.year))
        
        self.lblStatus=QLabel()
        self.lblStatusMail=QLabel()
        self.statusBar.addWidget(self.lblStatus)
        self.statusBar.addWidget(self.lblStatusMail)        
        
        self.grp.hide()
        self.wy.initiate(2011, datetime.date.today().year, datetime.date.today().year)
        self.wy.changed.connect(self.on_wy_changed)
        self.wym.initiate(2011,  datetime.date.today().year, datetime.date.today().year, datetime.date.today().month)
        self.wym.changed.connect(self.on_wym_changed)
                        
        self.showMaximized()
        
        self.tserver=None
        try:
            self.tserver=TWebServer(self.mem)
            self.tserver.start()
        except:
            self.mem.log(self.tr("Web server failed to start"))
            self.tserver=None
            pass
            
        self.tsend=TSend(self.mem)#Lanza TSend desde arranque
        self.tsend.start()

        ##Admin mode. Data base user must have didyoureadme_admin role
        if self.mem.isAdminMode()==True:
            self.setWindowTitle(self.tr("DidYouReadMe 2012-{0} \xa9 (Admin mode)").format(__versiondate__.year))
            self.setWindowIcon(self.mem.qicon_admin())
            self.update()

        self.mem.data.groups.qtablewidget(self.tblGroups)
        self.on_chkDocumentsExpired_stateChanged(self.chkDocumentsExpired.checkState())
        self.on_chkUsersInactive_stateChanged(self.chkUsersInactive.checkState())

        if datetime.date.today()-datetime.date.fromordinal(int(self.mem.settings.value("frmMain/lastupdate","1")))>=datetime.timedelta(days=30):
            print ("Looking for updates")
            self.checkUpdates(False)

    def __del__(self):
        self.tsend.shutdown()
        if self.tserver:
            self.tserver.server.shutdown()
            self.tserver.wait()
        self.tsend.wait()
        self.mem.__del__() 
        
        
    def updateStatusBar(self):
        status=""
        if self.tserver!=None:
            if self.tserver.isRunning()==True:
                status=self.tr("Running Web server at {}:{} (Errors: {}/{}).".format(self.mem.settings.value("webserver/interface", "127.0.0.1"), self.mem.settings.value("webserver/port", "8000"), self.tserver.server.errors, self.tserver.server.served+self.tserver.server.errors))
            else:
                status=self.tr("Web server is down. Check configuration.")
        if self.tsend.isRunning()==True:
            statusmail=self.tr("Running mail sender (Errors: {}/{}).".format(self.tsend.errors, self.tsend.errors+ self.tsend.sent))
        else:
            statusmail=self.tr("Mail sender is not working.")
        self.lblStatus.setText(status)
        self.lblStatusMail.setText(statusmail)
        
    @pyqtSlot()      
    def on_actionTablesUpdate_triggered(self):
        inicio=datetime.datetime.now()           
       
        #Actualiza users
        for u in self.mem.data.users_active.arr:
            u.updateSent()
            u.updateRead()
        #Consulta
        for i, d in enumerate(self.mem.data.documents_active.arr):
            if d.isExpired()==False:
                d.updateNums()

        self.users.qtablewidget(self.tblUsers)
        self.mem.data.groups.qtablewidget(self.tblGroups)
        self.documents.qtablewidget(self.tblDocuments)
        
        for table in [self.tblDocuments,  self.tblGroups, self.tblUsers]:
            table.resizeRowsToContents()
            table.resizeColumnsToContents()
            
        self.updateStatusBar()
        self.mem.log(self.tr("Update tables took {}".format(datetime.datetime.now()-inicio)))

    @pyqtSlot()      
    def on_wym_changed(self):
        self.on_chkDocumentsExpired_stateChanged(self.chkDocumentsExpired.checkState())
        
    @pyqtSlot()      
    def on_wy_changed(self):
        self.on_chkDocumentsExpired_stateChanged(self.chkDocumentsExpired.checkState())

    @pyqtSlot()      
    def on_actionAbout_triggered(self):
        fr=frmAbout(self,"frmabout")
        fr.open()
                
    @pyqtSlot()      
    def on_actionHelp_triggered(self):
        fr=frmHelp(self,"frmHelp")
        fr.open()
        
    @pyqtSlot()      
    def on_actionSendAgain_triggered(self):
        self.documents.selected.send_again()
        
        
        
    @pyqtSlot()      
    def on_actionSettings_triggered(self):
        f=frmSettings(self.mem,   self)
        f.exec_()
        self.retranslateUi(self)
        

        if f.result()==QDialog.Accepted:
            m=QMessageBox()
            m.setWindowIcon(QIcon(":/didyoureadme.png"))
            m.setIcon(QMessageBox.Information)
            m.setText(self.tr("DidYouReadMe is going to be closed to save settings."))
            m.exec_()    
            self.confirmclose=False    
            self.close()
        
    @pyqtSlot()      
    def on_actionUpdates_triggered(self):
        self.checkUpdates(True)
        
    def checkUpdates(self, showdialogwhennoupdates=False):
        try:
            web=urllib.request.urlopen('https://sourceforge.net/projects/didyoureadme/files/didyoureadme/').read()
        except:
            web=None
        if web==None:
            m=QMessageBox()
            m.setWindowIcon(QIcon(":/didyoureadme.png"))
            m.setIcon(QMessageBox.Information)
            m.setText(self.tr("I couldn't look for updates. Try it later.."))
            m.exec_() 
            return

        #Saca la version de internet
        remoteversion=None
        for line in web.split(b"\n"):
            if line.find(b'Click to enter didyoureadme-')!=-1:
                remoteversion=line.decode("utf-8").split('"')[1].split('-')[1]
                break
        #Si no hay version sale
        print ("Remote version",  remoteversion)
        if remoteversion==None:
            return
                
        if remoteversion==__version__.replace("+", ""):#Quita el más de desarrollo 
            if showdialogwhennoupdates==True:
                m=QMessageBox()
                m.setWindowIcon(QIcon(":/didyoureadme.png"))
                m.setIcon(QMessageBox.Information)
                m.setText(self.tr("DidYouReadMe is in the last version"))
                m.exec_() 
        else:
            m=QMessageBox()
            m.setWindowIcon(QIcon(":/didyoureadme.png"))
            m.setIcon(QMessageBox.Information)
            m.setTextFormat(Qt.RichText)#this is what makes the links clickable
            m.setText(self.tr("There is a new DidYouReadMe version. You can download it from <a href='http://didyoureadme.sourceforge.net'>http://didyoureadme.sourceforge.net</a> or directly from <a href='https://sourceforge.net/projects/didyoureadme/files/didyoureadme/didyoureadme-")+remoteversion+"/'>Sourceforge</a>")
            m.exec_()                 

        self.mem.settings.setValue("frmMain/lastupdate",datetime.date.today().toordinal())

                
    @pyqtSlot(QEvent)   
    def closeEvent(self,event):        
        if self.confirmclose==True:#Si es un cerrado interactivo
            reply = QMessageBox.question(self, self.tr("Quit DidYouReadMe?"), self.tr("If you close the app, the web server will be closed too and users won't be able to get files. Do you want to exit?"), QMessageBox.Yes, QMessageBox.No)
        else:
            reply=QMessageBox.Yes
        if reply == QMessageBox.Yes:
            self.mem.log("DidYouReadMe is closing now...")
            self.__del__()
            event.accept()
        else:
            event.ignore()
        
        
    @pyqtSlot()   
    def on_actionDocumentNew_triggered(self):
        f=frmDocumentsIBM(self.mem)
        f.exec_()
        self.on_actionTablesUpdate_triggered()
    
    @pyqtSlot()   
    def on_actionDocumentOpen_triggered(self):        
        if os.path.exists(dirDocs+self.documents.selected.hash)==False:
            m=QMessageBox()
            m.setIcon(QMessageBox.Information)
            m.setText(self.tr("File not found"))
            m.exec_() 
            return
        QApplication.setOverrideCursor(Qt.WaitCursor);
            
        file=dirTmp+os.path.basename(self.documents.selected.filename)
        shutil.copyfile(dirDocs+self.documents.selected.hash, file)
        self.mem.log(self.tr("Opening document {} from {}".format(self.documents.selected.id, file)))
        
        self.openWithDefaultApp(file)
            
        QApplication.restoreOverrideCursor()
    
    def openWithDefaultApp(self, file):
        if platform.system()=="Windows":
            QDesktopServices.openUrl(QUrl("file:///"+file))#Needs 3
        
        if os.path.exists("/usr/bin/kfmclient"):
            QProcess.startDetached("kfmclient", ["openURL", file] )
        elif os.path.exists("/usr/bin/gnome-open"):
            QProcess.startDetached( "gnome-open '" + file + "'" );
        else:         
            QDesktopServices.openUrl(QUrl("file://"+file));

        
    
    @pyqtSlot()   
    def on_actionDocumentReport_triggered(self):
        QApplication.setOverrideCursor(Qt.WaitCursor);
        
        doc=QTextDocument()
        comment=self.documents.selected.comment.replace("\n\n\n", "<p>")
        comment=comment.replace("\n\n", "<p>")
        comment=comment.replace("\n", "<p>")
        
        s=("<center><h1>"+self.tr("DidYouReadMe Report")+"</h1>"+
           self.tr("Generation time")+": {0}".format(str(now(self.mem.localzone))[:19]) +"</center>"+
           "<h2>"+self.tr("Document data")+"</h2>"+
           self.tr("Created")+": {0}".format(str(self.documents.selected.datetime)[:19])+ "<p>"+
           self.tr("name")+": {0}".format(self.documents.selected.name) + "<p>"+
           self.tr("Internal id")+": {0}".format(self.documents.selected.id) + "<p>"+
           self.tr("Filename")+": <a href='http://{0}:{1}/get/adminl{2}/{3}'>{4}</a><p>".format(self.mem.settings.value("webserver/ip", "127.0.0.1"),  self.mem.settings.value("webserver/port", "8000"),  self.documents.selected.hash, urllib.parse.quote(os.path.basename(self.documents.selected.filename.lower())), os.path.basename(self.documents.selected.filename )) +
            self.tr("Comment")+": {0}".format(comment) +"<p>"+
           "<h2>"+self.tr("User reads")+"</h2>"+
           "<p><table border='1'><thead><tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}</th></tr></thead>".format(self.tr("User"), self.tr("Sent"), self.tr("First read"), self.tr("Number of reads"))
           )
                    
        cur=self.mem.con.cursor()     
        cur.execute("select * from users, userdocuments where id_documents=%s and userdocuments.id_users=users.id order by name", (self.documents.selected.id, ))    
        for row in cur:
            s=s+"<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(row['name'], str(row['sent'])[:19], str(row['read'])[:19], row['numreads'])
        s=s+"</table><p>" 
        cur.close()
        
        doc.setHtml(s)
        printer=QPrinter()
        file=dirTmp+"{0} DidYouReadMe document.pdf".format(str(self.documents.selected.datetime)[:16]).replace(":", "").replace("-", "")
        self.mem.log(self.tr("Document {} report was generated in {}".format(self.documents.selected.id, file)))
        printer.setOutputFileName(file)
        printer.setOutputFormat(QPrinter.PdfFormat);
        doc.print(printer)
        printer.newPage()
        
        self.openWithDefaultApp(file)
        QApplication.restoreOverrideCursor();

    @pyqtSlot()   
    def on_actionDocumentExpire_triggered(self):
        if self.documents.selected.isExpired():#Already expired
            f=frmDocumentsIBM(self.mem, self.documents.selected)
            f.exec_()
        else:#Not expired yet
            if self.documents.selected.hasPendingMails():
                m=QMessageBox()
                m.setWindowIcon(QIcon(":/didyoureadme.png"))
                m.setIcon(QMessageBox.Information)
                m.setText(self.tr("You can't expire the document due to it has pending mails"))
                m.exec_()   
                return
            else:
                self.documents.selected.expiration=now(self.mem.localzone)
                self.documents.selected.save()#Update changes expiration
                self.mem.con.commit()
                self.mem.data.documents_active.remove(self.documents.selected)    
        self.on_actionTablesUpdate_triggered()
                
    @pyqtSlot()   
    def on_actionDocumentDelete_triggered(self):
        """Sólo se puede borrar en 4-5 minutos según base de datos o gui"""
        if self.chkDocumentsExpired.checkState()==Qt.Unchecked:
            self.documents.selected.delete()
            self.mem.con.commit()
            self.documents.remove(self.documents.selected)
            self.on_chkDocumentsExpired_stateChanged(self.chkDocumentsExpired.checkState())
        else:
            m=QMessageBox()
            m.setIcon(QMessageBox.Information)
            m.setText(self.tr("You can't delete an expired document"))
            m.exec_()                   
            
    @pyqtSlot()   
    def on_actionDocumentDeleteAdmin_triggered(self):
        """Deletes everything"""
        self.documents.selected.delete()#Delete ya lo quita del array self.mem.documents
        self.mem.con.commit()
        self.documents.remove(self.documents.selected)
        self.documents.qtablewidget(self.tblDocuments)
        
    @pyqtSlot()   
    def on_actionGroupEdit_triggered(self):
        f=frmGroupsIBM(self.mem, self.mem.data.groups.selected)
        f.exec_()
        self.mem.data.groups.qtablewidget(self.tblGroups)
  
  
    @pyqtSlot()   
    def on_actionGroupNew_triggered(self):
        f=frmGroupsIBM(self.mem, None)
        f.exec_()
        self.mem.data.groups.qtablewidget(self.tblGroups)


    @pyqtSlot()   
    def on_actionGroupDelete_triggered(self):
        self.mem.data.groups.selected.delete()
        self.mem.con.commit()
        self.mem.data.groups.remove(self.mem.data.groups.selected)
        self.mem.data.groups.qtablewidget(self.tblGroups)

    @pyqtSlot()   
    def on_actionUserEdit_triggered(self):
        f=frmUsersIBM(self.mem, self.users.selected)
        f.exec_()
        self.users.qtablewidget(self.tblUsers)
        self.mem.data.groups.qtablewidget(self.tblGroups)
  
  
    @pyqtSlot()   
    def on_actionUserNew_triggered(self):
        f=frmUsersIBM(self.mem, None)
        f.exec_()
        self.users.qtablewidget(self.tblUsers)
        self.mem.data.groups.qtablewidget(self.tblGroups)

    @pyqtSlot()   
    def on_actionUserDelete_triggered(self):            
        if self.users.selected.isDeletable()==True:
            self.users.selected.delete()
            self.mem.data.groups.quit_user_from_all_groups(self.users.selected)
            self.mem.con.commit()
            self.users.remove(self.users.selected)
            self.users.qtablewidget(self.tblUsers)
            self.mem.data.groups.qtablewidget(self.tblGroups)
        else:
            m=QMessageBox()
            m.setWindowIcon(QIcon(":/didyoureadme.png"))
            m.setIcon(QMessageBox.Information)
            m.setText(self.tr("You can't delete it, because user is in a group or DidYouReadMe sent him some documents.\nYou can deactivate him."))
            m.exec_()          
            return

    def on_tblDocuments_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionDocumentNew)    
        menu.addAction(self.actionDocumentDelete)
        if self.mem.isAdminMode()==True:
            menu.addAction(self.actionDocumentDeleteAdmin)
        menu.addSeparator()
        menu.addAction(self.actionDocumentExpire)
        menu.addSeparator()
        menu.addAction(self.actionSendAgain)
        menu.addSeparator()
        menu.addAction(self.actionDocumentOpen)
        menu.addAction(self.actionDocumentReport)
                    
                    
        if self.chkDocumentsExpired.checkState()==Qt.Checked:#Si está en expirados no puedo añadir documento
            self.actionDocumentNew.setEnabled(False)
        else:
            self.actionDocumentNew.setEnabled(True)
                    
        if self.documents.selected==None:
            self.actionDocumentDelete.setEnabled(False)
            self.actionDocumentDeleteAdmin.setEnabled(False)
            self.actionDocumentExpire.setEnabled(False)
            self.actionDocumentReport.setEnabled(False)
            self.actionDocumentOpen.setEnabled(False)
            self.actionSendAgain.setEnabled(False)
        else:
            if (now(self.mem.localzone)-self.documents.selected.datetime)>datetime.timedelta(seconds=45):
                self.actionDocumentDelete.setEnabled(False)
            else:
                self.actionDocumentDelete.setEnabled(True)
            self.actionDocumentDeleteAdmin.setEnabled(True)

            if self.documents.selected.isExpired():
                self.actionDocumentExpire.setText(self.tr("Change expiration"))
            else:
                self.actionDocumentExpire.setText(self.tr("Expire document"))
                
            self.actionDocumentReport.setEnabled(True)
            self.actionDocumentOpen.setEnabled(True)
            self.actionDocumentExpire.setEnabled(True)    
            self.actionSendAgain.setEnabled(True)
            
        menu.exec_(self.tblDocuments.mapToGlobal(pos))

    def on_tblDocuments_itemSelectionChanged(self):
        self.documents.selected=None
        for i in self.tblDocuments.selectedItems():
            if i.column()==0:#only once per row
                self.documents.selected=self.documents.arr[i.row()]
            
    def on_tblGroups_cellDoubleClicked(self, row, column):
        if self.mem.data.groups.selected==None:
            return
        qmessagebox(self.tr("Group has {} members".format(self.mem.data.groups.selected.members.length())))

    def on_tblGroups_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionGroupNew)    
        menu.addAction(self.actionGroupEdit)    
        menu.addAction(self.actionGroupDelete)
        if self.mem.data.groups.selected==None:
            self.actionGroupDelete.setEnabled(False)
            self.actionGroupEdit.setEnabled(False)
        else:
            if self.mem.data.groups.selected.id==1:# Todos los activos
                self.actionGroupDelete.setEnabled(False)   
                self.actionGroupEdit.setEnabled(False)           
            else:
                self.actionGroupDelete.setEnabled(True)   
                self.actionGroupEdit.setEnabled(True)            
        menu.exec_(self.tblGroups.mapToGlobal(pos))
        
        
    def on_tblGroups_itemSelectionChanged(self):
        self.mem.data.groups.selected=None
        for i in self.tblGroups.selectedItems():
            if i.column()==0:#only once per row
                self.mem.data.groups.selected=self.mem.data.groups.arr[i.row()]

    def on_tblUsers_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionUserNew)    
        menu.addAction(self.actionUserEdit)
        menu.addAction(self.actionUserDelete)
        if self.users.selected==None:
            self.actionUserDelete.setEnabled(False)
            self.actionUserEdit.setEnabled(False)
        else:
            self.actionUserDelete.setEnabled(True)
            self.actionUserEdit.setEnabled(True)
            
        menu.exec_(self.tblUsers.mapToGlobal(pos))
            
    def on_tblUsers_cellDoubleClicked(self, row, column):
        if self.users.selected==None:
            return
        
        resultado=[]
        for g in self.mem.data.groups.arr:
            if self.users.selected in g.members.arr:
                resultado.append(g)
        
        if len (resultado)==0:
            s=self.tr("User doesn't belong to any group.")
        else:
            s=self.tr("User belongs to the following groups:")+"\n"
            for g in resultado:
                s=s+"  - "+g.name+"\n"

        m=QMessageBox()
        m.setWindowIcon(QIcon(":/didyoureadme.png"))
        m.setIcon(QMessageBox.Information)
        m.setText(s[:-1])
        m.exec_()           
        
    def on_tblUsers_itemSelectionChanged(self):
        self.users.selected=None
        for i in self.tblUsers.selectedItems():
            if i.column()==0:#only once per row
                self.users.selected=self.users.arr[i.row()]
#        print (self.users.selected)
        
    def on_tblDocuments_cellDoubleClicked(self, row, column):
        if self.documents.selected==None:
            return
            
        cur=self.mem.con.cursor()     
        cur.execute("select id_users from userdocuments where id_documents=%s and sent is not null and read is null;", (self.documents.selected.id, ))
                   
        if cur.rowcount>0:
            s=self.tr("Users haven't read the selected document:")+"\n"
            for row in cur:
                u=self.mem.data.users_all().find(row['id_users'])
                s=s+"  - "+u.name+"\n"
        else:
            s=self.tr("Everybody read the document.")

        m=QMessageBox()
        m.setWindowIcon(QIcon(":/didyoureadme.png"))
        m.setIcon(QMessageBox.Information)
        m.setText(s[:-1])
        m.exec_()           
        
        cur.close()
        
    def on_chkUsersInactive_stateChanged(self, state):
        if state==Qt.Unchecked:
            self.users=self.mem.data.users_active
        else:
            self.users=self.mem.data.users_inactive
        self.users.qtablewidget(self.tblUsers)
        
    def on_chkDocumentsExpired_stateChanged(self, state):
        if state==Qt.Unchecked:        
            self.documents=self.mem.data.documents_active
            self.grp.hide()
        else:
            self.mem.data.documents_inactive=SetDocuments(self.mem)
            if self.radYear.isChecked()==True:
                self.mem.data.documents_inactive.load("select  id, datetime, title, comment, filename, hash, expiration  from documents where expiration<now() and date_part('year',datetime)={0} order by datetime;".format(self.wy.year))
            else:
                self.mem.data.documents_inactive.load("select  id, datetime, title, comment, filename, hash, expiration  from documents where expiration<now() and date_part('year',datetime)={0} and date_part('month',datetime)={1} order by datetime;".format(self.wym.year, self.wym.month))
            self.documents=self.mem.data.documents_inactive
            self.grp.show()
            
        self.documents.qtablewidget(self.tblDocuments)

    def on_radYear_toggled(self, toggle):
        if toggle==True:
            self.wym.setEnabled(False)
            self.wy.setEnabled(True)
        else:
            self.wym.setEnabled(True)
            self.wy.setEnabled(False)
        self.on_chkDocumentsExpired_stateChanged(self.chkDocumentsExpired.checkState())
