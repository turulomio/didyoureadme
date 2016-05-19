#!/usr/bin/python3
import sys
import platform
import datetime

if platform.system()=="Windows":
    sys.path.append("ui/")
    sys.path.append("images/")
else:
    sys.path.append("/usr/lib/didyoureadme")
    
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from frmMain import *
from frmAccess import *
from libdidyoureadme import dirDocs, version,  dirTmp
import libdbupdates

def qt_message_handler(mode, context, message):
    s="{} {}\n".format(str(datetime.datetime.now()),  message)
    print(s[:-1])
    with open(dirDocs+"log.txt", "a") as f:
        f.write(s)
        f.close()

if __name__=='__main__':#Needed due to multiprocessing in windows load all process again and launch frmAccess twice
    makedirs(dirTmp)
    makedirs(dirDocs)

    QtCore.qInstallMessageHandler(qt_message_handler)


    app = QApplication(sys.argv)
    app.setOrganizationName("Mariano Muñoz ©")
    app.setOrganizationDomain("turulomio.users.sourceforge.net")
    app.setApplicationName("DidYouReadMe")

    qDebug(QApplication.translate("DidYouReadMe", "Iniciando Didyoureadme-{}".format(version)))
    mem=Mem()

    app.setQuitOnLastWindowClosed(True)
    mem.setQTranslator(QTranslator(app))
    
    access=frmAccess(mem)
    access.setLabel(QApplication.translate("DidYouReadMe","Please login to the DidYouReadMe database"))
    access.config_load()
    access.exec_()

    if access.result()==QDialog.Rejected: 
        m=QMessageBox()
        m.setWindowIcon(QIcon(":/didyoureadme.png"))
        m.setIcon(QMessageBox.Information)
        m.setText(QApplication.translate("DidYouReadMe","Error conecting to {} database in {} server").format(access.con.db, access.con.server))
        m.exec_()   
        sys.exit(1)
    access.config_save()
    mem.con=access.con
    access.hide()

    if mem.hasDidyoureadmeRole()==False:
        qmessagebox(QApplication.translate("DidYouReadMe", "Database user hasn't a valid DidYouReadMe role"))
        sys.exit(2)
        
    ##Update database
    update=libdbupdates.Update(mem)
    if update.need_update()==True:
        if mem.isAdminMode():
            update.run()
        else:
            qmessagebox(QApplication.translate("Core","DidYouReadMe needs to update its database schema. Please login with an admin role."))
            sys.exit(3)
    update.syncing_files()
            
    frmMain = frmMain(mem) 
    
    sys.exit(app.exec_())

