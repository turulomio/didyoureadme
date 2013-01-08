import   datetime,  urllib.request,  multiprocessing,  sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from libdidyoureadme import *

from Ui_frmMain import *
from frmAbout import *
from frmSettings import *
from frmHelp import *
from frmAccess import *
from frmDocumentsIBM import *
from frmGroupsIBM import *
from frmUsersIBM import *

            
class frmMain(QMainWindow, Ui_frmMain):#    
    def __init__(self, cfgfile, parent = 0,  flags = False):
        QMainWindow.__init__(self)
        self.confirmclose=True
        self.cfgfile=cfgfile
        self.accesspass=False
        
        self.documents=[]
        self.users=[]
        
        self.errorsending=0
        
        self.setupUi(self)

        sb = QStatusBar()
        sb.setFixedHeight(18)
        self.setStatusBar(sb)
        
        self.showMaximized()

        self.mem=Mem(cfgfile)
        access=frmAccess(self.mem)
        access.setWindowTitle(self.trUtf8("Login to DidYouReadMe"))
        salida=access.exec_()
        if salida==QDialog.Rejected:
            sys.exit(255)
            return
            
        self.accesspass=True#Se usa en el destructor
            
        
        self.mem.con=self.mem.connect()

        self.mem.cargar_datos()

        self.server = multiprocessing.Process(target=self.httpserver, args=())
        self.server.start()


        
        self.tblGroups.verticalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.tblGroups.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.tblUsers.verticalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.tblUsers.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.tblDocuments.verticalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.tblDocuments.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)

        self.tblGroups_reload()
        self.tblUsers_reload(c2b(self.chkUsersInactive.checkState()))
        self.tblDocuments_reload(c2b(self.chkDocumentsClosed.checkState()))

        if datetime.date.today()-datetime.date.fromordinal(self.mem.cfgfile.lastupdate)>=datetime.timedelta(days=30):
            print ("Looking for updates")
            self.checkUpdates(False)

        self.tupdatedata=TUpdateData(self.mem)
        self.tupdatedata.start()
        
        self.timerUpdateData=QTimer()
        QObject.connect(self.timerUpdateData, SIGNAL("timeout()"), self.updateData) 
        self.timerUpdateData.start(10000)
        
        
        self.tsend=TSend(self.mem)#Lanza TSend desde arranque
        self.tsend.start()
        
        self.timerSendMessages=QTimer()
        QObject.connect(self.timerSendMessages, SIGNAL("timeout()"), self.send) 
        self.timerSendMessages.start(10000)
        
        
    def __del__(self):
        if self.accesspass==True:
            self.timerSendMessages.stop()
            self.timerUpdateData.stop()
            self.server.terminate()
            self.tsend.join()
            self.tupdatedata.join()
            self.mem.__del__() 
        
    def httpserver(self):
        from bottle import route, run,  error, static_file
        @route('/get/<filename>/<name>')
        def get(filename,  name):
            f=open(dirReaded+filename, "w")
            f.close()
            return static_file(filename.split("l")[1], root=dirDocs,  download=name)
        
        @error(404)
        def error404(error):
            return 'Nothing here, sorry'
            
        run (host=self.mem.cfgfile.webserver, port=int(self.mem.cfgfile.webserverport), debug=False)

    def updateStatusBar(self):
        #Actualiza statusbar
        if self.server.is_alive()==True:
            status=self.trUtf8("Running web server at {0}:{1}. ".format(self.mem.cfgfile.webserver, self.mem.cfgfile.webserverport))
        else:
            status=self.trUtf8("Web server is down. Check configuration. ")
        self.statusBar().showMessage(status + self.trUtf8("{0} sending errors".format(self.errorsending)))    

    def send(self):
#        print (self.tsend.isAlive(), "send isalive")
        if self.tsend.isAlive()==False:
            self.errorsending=self.errorsending+self.tsend.errorsending
            del self.tsend#Lo borro porque sino no me volvia a enviar
            QCoreApplication.processEvents()
            self.tsend=TSend(self.mem)
            self.tsend.start()      
            
        self.updateStatusBar()

    @pyqtSlot()      
    def on_actionTablesUpdate_triggered(self):
        self.tblUsers_reload(c2b(self.chkUsersInactive.checkState()))
        self.tblGroups_reload()
        self.tblDocuments_reload(c2b(self.chkDocumentsClosed.checkState()))
        self.updateStatusBar()
        
    def tblGroups_reload(self):
        self.tblGroups.setRowCount(len(self.mem.groups.arr))
        self.mem.groups.arr=sorted(self.mem.groups.arr, key=lambda g: g.name)
        for i, p in enumerate(self.mem.groups.arr):
            self.tblGroups.setItem(i, 0, QTableWidgetItem(p.name))
            p.members=sorted(p.members, key=lambda u: u.name)
            users=""
            for u in p.members:
                users=users+u.name+"\n"
            self.tblGroups.setItem(i, 1, QTableWidgetItem(users[:-1]))
        self.tblGroups.clearSelection()    

    def tblUsers_reload(self, inactive=False):
        self.users=[]
        for i, u in enumerate(self.mem.users.arr):
            if (inactive==True and u.active==True) or (inactive==False and u.active==False):
                continue
            self.users.append(u)
        
        self.tblUsers.setRowCount(len(self.users))
        self.users=sorted(self.users, key=lambda u: u.name)
        for i, u in enumerate(self.users):
            self.tblUsers.setItem(i, 0, qdatetime(u.datetime, self.mem.cfgfile.localzone))
            if u.post==None:
                post=""
            else:
                post=u.post
            self.tblUsers.setItem(i, 1, QTableWidgetItem(post))
            self.tblUsers.setItem(i, 2, QTableWidgetItem(u.name))
            self.tblUsers.setItem(i, 3, QTableWidgetItem(u.mail))
            self.tblUsers.setItem(i, 4, QTableWidgetItem(str(u.read)))
            self.tblUsers.setItem(i, 5, QTableWidgetItem(str(u.sent)))
        self.tblUsers.clearSelection()   
        
    def tblDocuments_reload(self, closed=False):
        self.documents=[]
        for i, d in enumerate(self.mem.documents.arr):
            if (closed==False and d.closed==True) or (closed==True and d.closed==False):
                continue
            self.documents.append(d)
        
        self.tblDocuments.setRowCount(len(self.documents))
        self.documents=sorted(self.documents, key=lambda d: d.datetime)
        for i, d in enumerate(self.documents):
            self.tblDocuments.setItem(i, 0, qdatetime(d.datetime, self.mem.cfgfile.localzone))
            self.tblDocuments.setItem(i, 1, QTableWidgetItem(d.title))
            self.tblDocuments.setItem(i, 2, QTableWidgetItem(os.path.basename(d.filename)))
            self.tblDocuments.setItem(i, 3, QTableWidgetItem(str(d.numplanned)))
            self.tblDocuments.setItem(i, 4, QTableWidgetItem(str(d.numsents)))
            self.tblDocuments.setItem(i, 5, QTableWidgetItem(str(d.numreads)))
            if d.numreads==d.numplanned and d.numplanned>0:
                for column in range( 3, 6):
                    self.tblDocuments.item(i, column).setBackgroundColor(QColor(198, 205, 255))

        self.tblDocuments.setCurrentCell(len(self.documents)-1, 0)                    
        self.tblDocuments.clearSelection()    

    def updateData(self):
        """Parsea el directorio readed y actualizada dotos"""
#        print (self.tupdatedata.isAlive(), "updatedata isalive")
        if self.tupdatedata.isAlive()==False:
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
        f=frmSettings(self.cfgfile,   self)
        f.exec_()
        self.retranslateUi(self)
        

        if f.result()==QDialog.Accepted:
            m=QMessageBox()
            m.setIcon(QMessageBox.Information)
            m.setText(self.trUtf8("DidYouReadMe is going to be closed to save settings."))
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
            m.setText(self.trUtf8("I couldn't look for updates. Try it later.."))
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
                m.setText(self.trUtf8("DidYouReadMe is in the last version"))
                m.exec_() 
        else:
            m=QMessageBox()
            m.setIcon(QMessageBox.Information)
            m.setTextFormat(Qt.RichText)#this is what makes the links clickable
            m.setText(self.trUtf8("There is a new DidYouReadMe version. You can download it from <a href='http://didyoureadme.sourceforge.net'>http://didyoureadme.sourceforge.net</a> or directly from <a href='https://sourceforge.net/projects/didyoureadme/files/didyoureadme/didyoureadme-")+remoteversion+"/'>Sourceforge</a>")
            m.exec_()                 

        self.cfgfile.lastupdate=datetime.date.today().toordinal()
        self.cfgfile.save()

                
    @pyqtSlot(QEvent)   
    def closeEvent(self,event):        
        if self.confirmclose==True:#Si es un cerrado interactivo
            reply = QMessageBox.question(self, self.trUtf8("Quit DidYouReadMe?"), self.trUtf8("If you close the app, the web server will be closed too. Users won't be able to get files.Do you with to exit?"), QMessageBox.Yes, QMessageBox.No)
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
        self.tblDocuments_reload(c2b(self.chkDocumentsClosed.checkState()))
    
    @pyqtSlot()   
    def on_actionDocumentOpen_triggered(self):        
        selected=None
        for i in self.tblDocuments.selectedItems():#itera por cada item no row.
            selected=self.documents[i.row()]
            
    
        try:
            os.makedirs(dirTmp)
        except:
            pass            
            
        file=dirTmp+os.path.basename(selected.filename)
        shutil.copyfile(dirDocs+selected.hash, file)
            
        m=QMessageBox()
        m.setIcon(QMessageBox.Information)                    
        m.setTextFormat(Qt.RichText)
        m.setText(self.trUtf8("To see the document click the followling link:")+"<p><a href='file://{0}'>{1}</a>".format(file, os.path.basename(selected.filename)))
        m.exec_() 
        os.unlink(file)
        
    
    @pyqtSlot()   
    def on_actionDocumentReport_triggered(self):
        selected=None
        for i in self.tblDocuments.selectedItems():#itera por cada item no row.
            selected=self.documents[i.row()]
        doc=QTextDocument()
        s=("<center><h1>"+self.trUtf8("DidYouReadMe Report")+"</h1>"+
           self.trUtf8("Generation time")+": {0}".format(str(now(self.mem.cfgfile.localzone))[:19]) +"</center>"+
           "<h2>"+self.trUtf8("Document data")+"</h2>"+
           self.trUtf8("Created")+": {0}".format(str(selected.datetime)[:19])+ "<p>"+
           self.trUtf8("Title")+": {0}".format(selected.title) + "<p>"+
           self.trUtf8("Filename")+": {0}".format(selected.filename) +"<p>"+
           self.trUtf8("Comment")+": {0}".format(selected.comment) +"<p>"+
           "<h2>"+self.trUtf8("User reads")+"</h2>"+
           "<p><table border='1'><thead><tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}</th></tr></thead>".format(self.trUtf8("User"), self.trUtf8("Sent"), self.trUtf8("First read"), self.trUtf8("Number of reads"))
           )
           
                    
        cur=self.mem.con.cursor()     
        cur.execute("select * from users, userdocuments where id_documents=%s and userdocuments.id_users=users.id order by name", (selected.id, ))    
        for row in cur:
            s=s+"<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(row['name'], str(row['sent'])[:19], str(row['read'])[:19], row['numreads'])
        s=s+"</table><p>" 
        cur.close()
        
        doc.setHtml(s)
        printer=QPrinter()
        file=os.path.expanduser("~/{0} DidYouReadMe document.pdf".format(str(selected.datetime)[:19]))
        printer.setOutputFileName(file)
        printer.setOutputFormat(QPrinter.PdfFormat);
        doc.print(printer)
        printer.newPage()
        
        
        m=QMessageBox()
        m.setIcon(QMessageBox.Information)                    
        m.setTextFormat(Qt.RichText)
        m.setText(self.trUtf8("Document generated in:")+"<p><a href='file://{0}'>{0}</a>".format(file))
        m.exec_() 
                
    @pyqtSlot()   
    def on_actionDocumentClose_triggered(self):
        selected=None
        for i in self.tblDocuments.selectedItems():#itera por cada item no row.
            selected=self.documents[i.row()]
        selected.closed=not selected.closed
        selected.save(self.mem)
        
            
        
        self.tblDocuments_reload(c2b(self.chkDocumentsClosed.checkState())        )
                
    @pyqtSlot()   
    def on_actionDocumentDelete_triggered(self):
        """Sólo se puede borrar en 4-5 minutos seg´un base de datos o gui"""
        #Borra el registro de base de datosv
        selected=None
        for i in self.tblDocuments.selectedItems():#itera por cada item no row.
            selected=self.documents[i.row()]
        
        selected.delete(self.mem)
        self.tblDocuments_reload(c2b(self.chkDocumentsClosed.checkState()))
        
    @pyqtSlot()   
    def on_actionGroupEdit_triggered(self):
        for i in self.tblGroups.selectedItems():#itera por cada item no row.
            selected=self.mem.groups.arr[i.row()]
        f=frmGroupsIBM(self.mem, selected)
        f.exec_()
        self.tblGroups_reload()  
  
  
    @pyqtSlot()   
    def on_actionGroupNew_triggered(self):
        f=frmGroupsIBM(self.mem, None)
        f.exec_()
        self.tblGroups_reload()
#        salida=QInputDialog.getText(self,self.trUtf8("Add new group"),self.trUtf8("Group name:"))
#        if salida[1]==True:
#            g=Group(salida[0], [])
#            g.save(self.mem, cur)
#        print (salida)

    @pyqtSlot()   
    def on_actionGroupDelete_triggered(self):
        #Borra el registro de la base de datos
        for i in self.tblGroups.selectedItems():#itera por cada item no row.
            selected=self.mem.groups.arr[i.row()]
            
        selected.delete(self.mem)
        
        
        self.tblGroups_reload()

    @pyqtSlot()   
    def on_actionUserEdit_triggered(self):
        for i in self.tblUsers.selectedItems():#itera por cada item no row.
            selected=self.users[i.row()]
        f=frmUsersIBM(self.mem, selected)
        f.exec_()
        self.tblUsers_reload(c2b(self.chkUsersInactive.checkState()))  
        self.tblGroups_reload()#Se actualiza grupo 1
  
  
    @pyqtSlot()   
    def on_actionUserNew_triggered(self):
        f=frmUsersIBM(self.mem, None)
        f.exec_()
        self.tblUsers_reload(c2b(self.chkUsersInactive.checkState()))
        self.tblGroups_reload()#Se actualiza grupo 1

    @pyqtSlot()   
    def on_actionUserDelete_triggered(self):
        for i in self.tblUsers.selectedItems():#itera por cada item no row.
            selected=self.users[i.row()]
            
        if selected.isDeletable(self.mem)==True:
            selected.delete(self.mem)
            #Recarga grupo de todos
            self.mem.groups.reload_from_mem()
        else:
            m=QMessageBox()
            m.setIcon(QMessageBox.Information)
            m.setText(self.trUtf8("You can't delete it, because user is in a group or DidYouReadMe sent him some documents.\nYou can deactivate him."))
            m.exec_()          
            return
        self.tblUsers_reload(c2b(self.chkUsersInactive.checkState()))
        self.tblGroups_reload()#Se actualiza grupo 1

    def on_tblDocuments_customContextMenuRequested(self,  pos):
        selected=None
        for i in self.tblDocuments.selectedItems():#itera por cada item no row.
            selected=self.documents[i.row()]

        menu=QMenu()
        menu.addAction(self.actionDocumentNew)    
        menu.addAction(self.actionDocumentDelete)
        menu.addSeparator()
        menu.addAction(self.actionDocumentClose)
        menu.addSeparator()
        menu.addAction(self.actionDocumentOpen)
        menu.addAction(self.actionDocumentReport)
                    
        
        
        if selected ==None:
            self.actionDocumentDelete.setEnabled(False)
            self.actionDocumentClose.setEnabled(False)
            self.actionDocumentReport.setEnabled(False)
            self.actionDocumentOpen.setEnabled(False)
        else:
            print (selected)
            if (now(self.mem.cfgfile.localzone)-selected.datetime)>datetime.timedelta(seconds=45):
                self.actionDocumentDelete.setEnabled(False)
            else:
                self.actionDocumentDelete.setEnabled(True)

            self.actionDocumentReport.setEnabled(True)
            self.actionDocumentOpen.setEnabled(True)
            self.actionDocumentClose.setEnabled(True)
            if selected.closed==True:
                self.actionDocumentClose.setChecked(Qt.Checked)
            else:
                self.actionDocumentClose.setChecked(Qt.Unchecked)       
            
        menu.exec_(self.tblDocuments.mapToGlobal(pos))
        
    def on_tblGroups_customContextMenuRequested(self,  pos):
        selected=None
        for i in self.tblGroups.selectedItems():#itera por cada item no row.
            selected=self.mem.groups.arr[i.row()]

        menu=QMenu()
        menu.addAction(self.actionGroupNew)    
        menu.addAction(self.actionGroupEdit)    
        menu.addAction(self.actionGroupDelete)
        if selected ==None:
            self.actionGroupDelete.setEnabled(False)
            self.actionGroupEdit.setEnabled(False)
        else:
            print (selected)
            if selected.id==1:# Todos los activos
                self.actionGroupDelete.setEnabled(False)   
                self.actionGroupEdit.setEnabled(False)           
            else:
                self.actionGroupDelete.setEnabled(True)   
                self.actionGroupEdit.setEnabled(True)            
        menu.exec_(self.tblGroups.mapToGlobal(pos))
        
        
    def on_tblUsers_customContextMenuRequested(self,  pos):
        selected=None
        for i in self.tblUsers.selectedItems():#itera por cada item no row.
            selected=self.users[i.row()]

        menu=QMenu()
        menu.addAction(self.actionUserNew)    
        menu.addAction(self.actionUserEdit)
        menu.addAction(self.actionUserDelete)
        if selected ==None:
            self.actionUserDelete.setEnabled(False)
            self.actionUserEdit.setEnabled(False)
        else:
            self.actionUserDelete.setEnabled(True)
            self.actionUserEdit.setEnabled(True)
            
        menu.exec_(self.tblUsers.mapToGlobal(pos))
            
    def on_tblUsers_cellDoubleClicked(self, row, column):
        selected=None
        for i in self.tblUsers.selectedItems():#itera por cada item no row.
            selected=self.users[i.row()]
            
        if selected==None:
            return
        
        resultado=[]
        for g in self.mem.groups.arr:
            if selected in g.members:
                resultado.append(g)
        
        if len (resultado)==0:
            s=self.trUtf8("User doesn't belong to any group.")
        else:
            s=self.trUtf8("User belongs to the following groups:")+"\n"
            for g in resultado:
                s=s+"  - "+g.name+"\n"

        m=QMessageBox()
        m.setIcon(QMessageBox.Information)
        m.setText(s[:-1])
        m.exec_()           
        
    def on_tblDocuments_cellDoubleClicked(self, row, column):
        selected=None
        for i in self.tblDocuments.selectedItems():#itera por cada item no row.
            selected=self.documents[i.row()]
            
        if selected==None:
            return
        
        
            
            
        cur=self.mem.con.cursor()     
        cur.execute("select id_users from userdocuments where id_documents=%s and sent is not null and read is null;", (selected.id, ))
    
        if cur.rowcount==0 and selected.closed==False:
            reply = QMessageBox.question(self, 'Mensaje', self.trUtf8('This message have been read for everybody.\nDo you want to close and hide it?'),     QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QMessageBox.Yes:
                selected.closed=True
                selected.save(self.mem)
                self.tblDocuments_reload(c2b(self.chkDocumentsClosed.checkState()))
                cur.close()
            return
                
        if cur.rowcount>0:
            s=self.trUtf8("Users haven't read the selected document:")+"\n"
            for row in cur:
                u=self.mem.users.user(row['id_users'])
                s=s+"  - "+u.name+"\n"
        else:
            s=self.trUtf8("Everybody read the document.")

        m=QMessageBox()
        m.setIcon(QMessageBox.Information)
        m.setText(s[:-1])
        m.exec_()           
        
        cur.close()
        
    def on_chkUsersInactive_stateChanged(self, state):
        if state==Qt.Unchecked:
            self.tblUsers_reload(False)
        else:
            self.tblUsers_reload(True)
        
    def on_chkDocumentsClosed_stateChanged(self, state):
        if state==Qt.Unchecked:
            self.tblDocuments_reload(False)
        else:
            self.tblDocuments_reload(True)
            
