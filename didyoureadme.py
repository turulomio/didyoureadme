#!/usr/bin/python3
import sys
import os
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

def qt_message_handler(mode, context, message):
    s="{} {}\n".format(datetime.datetime.now(),  message)
    print(s[:-1])
    with open(dirDocs+"log.txt", "a") as f:
        f.write(s)
        f.close()

if __name__=='__main__':#Needed due to multiprocessing in windows load all process again and launch frmAccess twice
    try:
        os.makedirs(dirTmp)
    except:
        pass
    try:
        os.makedirs(dirDocs)
    except:
        pass

    QtCore.qInstallMessageHandler(qt_message_handler)


    app = QApplication(sys.argv)
    app.setOrganizationName("Mariano Muñoz ©")
    app.setOrganizationDomain("turulomio.users.sourceforge.net")
    app.setApplicationName("DidYouReadMe")

    qDebug(QApplication.translate("DidYouReadMe", "Iniciando Didyoureadme-{}".format(version)))
    mem=Mem()

    app.setQuitOnLastWindowClosed(True)
    mem.setQTranslator(QTranslator(app))
    mem.languages.cambiar(mem.cfgfile.language)

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

    if mem.cfgfile.error==True:
        m=QMessageBox()
        m.setWindowIcon(QIcon(":/didyoureadme.png"))
        m.setIcon(QMessageBox.Information)
        m.setText(QApplication.translate("DidYouReadMe","An error loading settings happened. You must check your settings are ok"))
        m.exec_()      
        
    frmMain = frmMain(mem) 
    
    sys.exit(app.exec_())

