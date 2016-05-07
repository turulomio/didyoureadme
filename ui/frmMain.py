import   datetime,  urllib.request,  multiprocessing,  sys
import shutil
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from libdidyoureadme import *
import libdbupdates

from Ui_frmMain import *
from frmAbout import *
from frmSettings import *
from frmHelp import *
from frmDocumentsIBM import *
from frmGroupsIBM import *
from frmUsersIBM import *


class frmMain(QMainWindow, Ui_frmMain):#    
    def __init__(self, mem, parent = 0,  flags = False):
        QMainWindow.__init__(self)
        self.setupUi(self)      
        self.mem=mem          

        self.users=None#Pointer
        self.documents=None#Pointer
        
        self.confirmclose=True
        self.accesspass=False
        
        self.errorsending=0
        self.errorupdating=0
        
        sb = QStatusBar()
        sb.setFixedHeight(18)
        self.setStatusBar(sb)
        
        self.showMaximized()
            
        self.accesspass=True#Se usa en el destructor
    
        ##Update database
        libdbupdates.Update(self.mem)
                
        self.mem.data.load()
        self.wym.hide()
        self.wym.initiate(2011,  datetime.date.today().year, datetime.date.today().year, datetime.date.today().month)
        self.wym.changed.connect(self.on_wym_changed)

        ##Admin mode
        if self.mem.adminmodeinparameters:
            m=QMessageBox()
            m.setIcon(QMessageBox.Information)
            input=QInputDialog.getText(self,  "DidYouReadMe",  self.tr("Please introduce Admin Mode password"), QLineEdit.Password)
            res=self.mem.check_admin_mode(input[0])
            if input[1]==True:
                if res==None:
                    self.setWindowTitle(self.tr("DidYouReadMe 2013-{0} © (Admin mode)").format(version_date.year))
                    self.setWindowIcon(self.mem.qicon_admin())
                    self.update()
                    self.mem.set_admin_mode(input[0])
                    self.mem.con.commit()
                    m.setText(self.tr("You have set the admin mode password. Please login again"))
                    m.exec_()
                    sys.exit(2)
                elif res==True:
                    self.mem.adminmode=True
                    self.setWindowTitle(self.tr("DidYouReadMe 2013-{0} © (Admin mode)").format(version_date.year))
                    self.setWindowIcon(self.mem.qicon_admin())
                    self.update()
                    m.setText(self.tr("You are logged as an administrator"))
                    m.exec_()   
            if input[1]==False or res==False:     
                    m.setText(self.tr("Bad 'Admin mode' password. You are logged as a normal user"))
                    m.exec_()   

        self.server = multiprocessing.Process(target=self.httpserver, args=())
        self.server.start()
        print("why")
        self.mem.data.groups.qtablewidget(self.tblGroups)
        self.on_chkDocumentsExpired_stateChanged(self.chkDocumentsExpired.checkState())
        self.on_chkUsersInactive_stateChanged(self.chkUsersInactive.checkState())

        if datetime.date.today()-datetime.date.fromordinal(self.mem.cfgfile.lastupdate)>=datetime.timedelta(days=30):
            print ("Looking for updates")
            self.checkUpdates(False)

        self.tupdatedata=TUpdateData(self.mem)
        self.tupdatedata.start()
        
        self.timerUpdateData=QTimer()
        self.timerUpdateData.timeout.connect(self.updateData)
        self.timerUpdateData.start(60000)
        
        self.tsend=TSend(self.mem)#Lanza TSend desde arranque
        self.tsend.start()
        
        self.timerSendMessages=QTimer()
        self.timerSendMessages.timeout.connect(self.send)
        self.timerSendMessages.start(50000)
        
        if self.mem.cfgfile.autoupdate=="True":
            self.timerUpdateTables=QTimer()
            self.timerUpdateTables.timeout.connect(self.on_actionTablesUpdate_triggered)
            self.timerUpdateTables.start(200000)
            
        print ("Aqui")
        
    def __del__(self):
        if self.accesspass==True:
            self.timerSendMessages.stop()
            self.timerUpdateData.stop()
            self.server.terminate()
            self.tsend.join()
            self.tupdatedata.join()
            self.mem.__del__() 
        
    def httpserver(self):
        if '/usr/bin' in sys.path: #En gentoo hay un ejecutable bottle.py, que ademas era 2.7, se quita del path
            sys.path.remove('/usr/bin')
            print('/usr/bin removed from path, to use site-packaged  version, check if problems')
            
        from bottle import route, run,  error, static_file
        print(dir(bottle))
        @route('/get/<filename>/<name>')
        def get(filename,  name):
            if filename.split("l")[0]!="admin":#Para informes no se contabilizará, luego no crea file            
                f=open(dirReaded+filename, "w")
                f.close()
            return static_file(filename.split("l")[1], root=dirDocs,  download=name)
        
        @error(404)
        def error404(error):
            return 'Nothing here, sorry'
        @error(403)
        def error403(error):
            return 'Nothing here, sorry'
            
        run (host=self.mem.cfgfile.webinterface, port=int(self.mem.cfgfile.webserverport), debug=False)

    def updateStatusBar(self):
        #Actualiza statusbar
        if self.server.is_alive()==True:
            status=self.tr("Running web server at {0}:{1}. ".format(self.mem.cfgfile.webinterface, self.mem.cfgfile.webserverport))
        else:
            status=self.tr("Web server is down. Check configuration. ")
        self.statusBar().showMessage(status + self.tr("{0} sending errors. {1} updating errors.".format(self.errorsending,  self.errorupdating)))    

    def send(self):
        print("Poraquin")
#        print (self.tsend.isAlive(), "send isalive")
        if self.tsend.isAlive()==False:
            self.errorsending=self.errorsending+self.tsend.errorsending
            del self.tsend#Lo borro porque sino no me volvia a enviar
            QCoreApplication.processEvents()
            self.tsend=TSend(self.mem)
            self.tsend.start()      
            
        self.updateStatusBar()

    
    def on_trayIcon_triggered(self, reason):
        print ("hola")

#    @pyqtSlot()      
#    def on_actionBackup_triggered(self):
#        QProcess.startDetached("didyoureadme-backup", [self.mem.cfgfile.server, self.mem.cfgfile.port, self.mem.cfgfile.user, self.mem.cfgfile.database] )
#        m=QMessageBox()
#        m.setText(QApplication.translate("DidYouReadMe","Backup will be created in the home directory"))
#        m.exec_()
#        
    @pyqtSlot()      
    def on_actionTablesUpdate_triggered(self):
        inicio=datetime.datetime.now()
        self.users.qtablewidget(self.tblUsers)
        self.mem.data.groups.qtablewidget(self.tblGroups)
        self.documents.qtablewidget(self.tblDocuments)
        self.updateStatusBar()
        print ("Update tables took {}".format(datetime.datetime.now()-inicio))

    @pyqtSlot()      
    def on_wym_changed(self):
        self.on_chkDocumentsExpired_stateChanged(self.chkDocumentsExpired.checkState())

    def updateData(self):
        """Parsea el directorio readed y actualizada dotos"""
        if self.tupdatedata.isAlive()==False:
            self.errorupdating=self.errorupdating+self.tupdatedata.errorupdating
            del self.tupdatedata#Lo borro porque sino no me volvia a enviar
            QCoreApplication.processEvents()
            self.tupdatedata=TUpdateData(self.mem)
            self.tupdatedata.start()      

    @pyqtSlot()      
    def on_actionAbout_triggered(self):
        fr=frmAbout(self,"frmabout")
        fr.open()
                
    @pyqtSlot()      
    def on_actionHelp_triggered(self):
        fr=frmHelp(self,"frmHelp")
        fr.open()
        
    @pyqtSlot()      
    def on_actionSettings_triggered(self):
        f=frmSettings(self.mem,   self)
        f.exec_()
        self.retranslateUi(self)
        

        if f.result()==QDialog.Accepted:
            m=QMessageBox()
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
            m.setIcon(QMessageBox.Information)
            m.setText(self.tr("I couldn't look for updates. Try it later.."))
            m.exec_() 
            return

        #Saca la version de internet
        remoteversion=None
        for line in web.split(b"\n"):
            if line.find(b'folder warn')!=-1:
                remoteversion=line.decode("utf-8").split('didyoureadme-')[1].split('"') [0]
                break
        #Si no hay version sale
        print ("Remote version",  remoteversion)
        if remoteversion==None:
            return
                
        if remoteversion==version.replace("+", ""):#Quita el más de desarrollo 
            if showdialogwhennoupdates==True:
                m=QMessageBox()
                m.setIcon(QMessageBox.Information)
                m.setText(self.tr("DidYouReadMe is in the last version"))
                m.exec_() 
        else:
            m=QMessageBox()
            m.setIcon(QMessageBox.Information)
            m.setTextFormat(Qt.RichText)#this is what makes the links clickable
            m.setText(self.tr("There is a new DidYouReadMe version. You can download it from <a href='http://didyoureadme.sourceforge.net'>http://didyoureadme.sourceforge.net</a> or directly from <a href='https://sourceforge.net/projects/didyoureadme/files/didyoureadme/didyoureadme-")+remoteversion+"/'>Sourceforge</a>")
            m.exec_()                 

        self.mem.cfgfile.lastupdate=datetime.date.today().toordinal()
        self.mem.cfgfile.save()

                
    @pyqtSlot(QEvent)   
    def closeEvent(self,event):        
        if self.confirmclose==True:#Si es un cerrado interactivo
            reply = QMessageBox.question(self, self.tr("Quit DidYouReadMe?"), self.tr("If you close the app, the web server will be closed too. Users won't be able to get files.Do you with to exit?"), QMessageBox.Yes, QMessageBox.No)
        else:
            reply=QMessageBox.Yes
        if reply == QMessageBox.Yes:
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
        
        self.openWithDefaultApp(file)
            
        QApplication.restoreOverrideCursor();
    
    def openWithDefaultApp(self, file):
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
           self.tr("Generation time")+": {0}".format(str(now(self.mem.cfgfile.localzone))[:19]) +"</center>"+
           "<h2>"+self.tr("Document data")+"</h2>"+
           self.tr("Created")+": {0}".format(str(self.documents.selected.datetime)[:19])+ "<p>"+
           self.tr("name")+": {0}".format(self.documents.selected.name) + "<p>"+
           self.tr("Internal id")+": {0}".format(self.documents.selected.id) + "<p>"+
           self.tr("Filename")+": <a href='http://{0}:{1}/get/adminl{2}/{3}'>{4}</a><p>".format(self.mem.cfgfile.webserver,  self.mem.cfgfile.webserverport, self.documents.selected.hash, urllib.parse.quote(os.path.basename(self.documents.selected.filename.lower())), os.path.basename(self.documents.selected.filename )) +
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
        file=dirTmp+"{0} DidYouReadMe document.pdf".format(str(self.documents.selected.datetime)[:19])
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
                m.setIcon(QMessageBox.Information)
                m.setText(self.tr("You can't expire the document due to it has pending mails"))
                m.exec_()   
                return
            else:
                self.documents.selected.expiration=now(self.mem.cfgfile.localzone)
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
            m.setIcon(QMessageBox.Information)
            m.setText(self.tr("You can't delete it, because user is in a group or DidYouReadMe sent him some documents.\nYou can deactivate him."))
            m.exec_()          
            return

    def on_tblDocuments_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionDocumentNew)    
        menu.addAction(self.actionDocumentDelete)
        if self.mem.adminmode==True:
            menu.addAction(self.actionDocumentDeleteAdmin)
        menu.addSeparator()
        menu.addAction(self.actionDocumentExpire)
        menu.addSeparator()
        menu.addAction(self.actionDocumentOpen)
        menu.addAction(self.actionDocumentReport)
                    
        if self.documents.selected==None:
            self.actionDocumentDelete.setEnabled(False)
            self.actionDocumentDeleteAdmin.setEnabled(False)
            self.actionDocumentExpire.setEnabled(False)
            self.actionDocumentReport.setEnabled(False)
            self.actionDocumentOpen.setEnabled(False)
        else:
            if (now(self.mem.cfgfile.localzone)-self.documents.selected.datetime)>datetime.timedelta(seconds=45):
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
            
        menu.exec_(self.tblDocuments.mapToGlobal(pos))

    def on_tblDocuments_itemSelectionChanged(self):
        self.documents.selected=None
        for i in self.tblDocuments.selectedItems():
            if i.column()==0:#only once per row
                self.documents.selected=self.documents.arr[i.row()]
#        print (self.documents.selected)
        
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
#        print (self.mem.data.groups.selected)

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
        for g in self.mem.groups.arr:
            if self.users.selected in g.members:
                resultado.append(g)
        
        if len (resultado)==0:
            s=self.tr("User doesn't belong to any group.")
        else:
            s=self.tr("User belongs to the following groups:")+"\n"
            for g in resultado:
                s=s+"  - "+g.name+"\n"

        m=QMessageBox()
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
            self.documents.qtablewidget(self.tblDocuments)
            self.wym.hide()
        else:
            self.mem.data.documents_inactive=SetDocuments(self.mem)
            self.mem.data.documents_inactive.load("select  id, datetime, title, comment, filename, hash, expiration  from documents where expiration<now() and date_part('year',datetime)={0} and date_part('month',datetime)={1} order by datetime;".format(self.wym.year, self.wym.month))
            self.documents=self.mem.data.documents_inactive
            self.documents.qtablewidget(self.tblDocuments)
            self.wym.show()
            
