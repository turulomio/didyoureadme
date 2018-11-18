import argparse
import sys
import platform

"""
    Curiosidades:
    - En algunas imagenes al cargarlas me sal´ia Libpng warning: iCCP: known incorrect sRGB profile.
      para evitarlo use imagemagic con el comando : convert document.png -strip document.png  y se solucion´o el problema
"""

from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from didyoureadme.ui.frmMain import frmMain
from didyoureadme.ui.frmAccess import frmAccess
from didyoureadme.libdidyoureadme import dirDocs, dirTmp, makedirs, Mem, qmessagebox,  now
from didyoureadme.version import __version__, __versiondate__
import didyoureadme.libdbupdates

def main():
    makedirs(dirTmp)
    makedirs(dirDocs)

    app = QApplication(sys.argv)
    app.setOrganizationName("Mariano Muñoz ©")
    app.setOrganizationDomain("turulomio.users.sourceforge.net")
    app.setApplicationName("DidYouReadMe")


    parser=argparse.ArgumentParser(
             prog='didyoureadme', 
             description=app.translate("Core",'System to control who and when a group reads a document send by mail. It uses postgresql to store information'),
             epilog=app.translate("Core","Developed by Mariano Muñoz 2015-{}".format(__versiondate__.year)),
             formatter_class=argparse.RawTextHelpFormatter
         )
    if platform.system()=="Windows":
             parser.add_argument('--shortcuts-create', help="Create shortcuts for Windows", action='store_true', default=False)
             parser.add_argument('--shortcuts-remove', help="Remove shortcuts for Windows", action='store_true', default=False)

    args=parser.parse_args()        

    if platform.system()=="Windows":
             if args.shortcuts_create:
                     from xulpymoney.shortcuts import create
                     create()
                     sys.exit(0)
             if args.shortcuts_remove:
                     from xulpymoney.shortcuts import remove
                     remove()
                     sys.exit(0)

    mem=Mem()
    mem.log(QApplication.translate("DidYouReadMe", "Iniciando Didyoureadme-{}".format(__version__)))

    app.setQuitOnLastWindowClosed(True)
    mem.setQTranslator(QTranslator(app))
    print(mem.language)

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
        
    if abs((mem.con.server_datetime()-now(mem.localzone)).total_seconds())>60:#
        mem.log("SERVER DATETIME AND SYSTEM DATETIME IS BIGGER THAN 60 SECONDS. MAILS CAN BE DELAYED")
        
    ##Update database
    update=didyoureadme.libdbupdates.Update(mem)
    if update.need_update()==True:
        if mem.isAdminMode():
            update.run()
        else:
            qmessagebox(QApplication.translate("DidYouReadMe","DidYouReadMe needs to update its database schema. Please login with an admin role."))
            sys.exit(3)
    update.syncing_files()
            
    frmmain = frmMain(mem) 
    frmmain.show()
    
    sys.exit(app.exec_())

