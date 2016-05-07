#!/usr/bin/python3
import sys, os
import platform

if platform.system()=="Windows":
    sys.path.append("ui/")
    sys.path.append("images/")
else:
    sys.path.append("/usr/lib/didyoureadme")
    
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from frmMain import *
from frmAccess import *
from libdidyoureadme import dirDocs, dirReaded

if __name__=='__main__':#Needed due to multiprocessing in windows load all process again and launch frmAccess twice
    try:
        os.makedirs("/tmp/didyoureadme")
    except:
        pass
    try:
        os.makedirs(dirDocs)
        os.makedirs(dirReaded)
    except:
        pass

    app = QApplication(sys.argv)
    app.setOrganizationName("Mariano Muñoz ©")
    app.setOrganizationDomain("turulomio.users.sourceforge.net")
    app.setApplicationName("DidYouReadMe")

    mem=Mem()


    app.setQuitOnLastWindowClosed(True)

    mem.setQTranslator(QTranslator(app))
    mem.languages.cambiar(mem.cfgfile.language)

    access=frmAccess(mem)
    access.setLabel(QApplication.translate("Core","Please login to the xulpymoney database"))
    access.config_load()
    access.exec_()

    if access.result()==QDialog.Rejected: 
        m=QMessageBox()
        m.setIcon(QMessageBox.Information)
        m.setText(QApplication.translate("Core","Error conecting to {} database in {} server").format(access.con.db, access.con.server))
        m.exec_()   
        sys.exit(1)
    access.config_save()
    mem.con=access.con
    access.hide()

    if mem.cfgfile.error==True:
        m=QMessageBox()
        m.setIcon(QMessageBox.Information)
        m.setText(QApplication.translate("DidYouReadMe","An error loading settings happened. You must check your settings are ok"))
        m.exec_()      

    if "admin" in sys.argv:
        mem.adminmodeinparameters=True
        
    frmMain = frmMain(mem) 
    sys.exit(app.exec_())

