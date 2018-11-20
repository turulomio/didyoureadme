import sys

from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtGui import QIcon
"""
    Curiosidades:
    - En algunas imagenes al cargarlas me sal´ia Libpng warning: iCCP: known incorrect sRGB profile.
      para evitarlo use imagemagic con el comando : convert document.png -strip document.png  y se solucion´o el problema
"""

from didyoureadme.ui.frmMain import frmMain
from didyoureadme.ui.frmAccess import frmAccess
from didyoureadme.libdidyoureadme import Mem, qmessagebox,  now
import didyoureadme.libdbupdates

def main(parameters=None):

    mem=Mem()

    access=frmAccess(mem)
    access.setLabel(mem.tr("Please login to the DidYouReadMe database"))
    access.config_load()
    access.exec_()

    if access.result()==QDialog.Rejected: 
        m=QMessageBox()
        m.setWindowIcon(QIcon(":/didyoureadme.png"))
        m.setIcon(QMessageBox.Information)
        m.setText(mem.tr("Error conecting to {} database in {} server").format(access.con.db, access.con.server))
        m.exec_()   
        sys.exit(1)
    access.config_save()
    mem.con=access.con
    access.hide()

    if mem.hasDidyoureadmeRole()==False:
        qmessagebox(mem.tr( "Database user hasn't a valid DidYouReadMe role"))
        sys.exit(2)
        
    if abs((mem.con.server_datetime()-now(mem.localzone)).total_seconds())>60:#
        mem.log("SERVER DATETIME AND SYSTEM DATETIME IS BIGGER THAN 60 SECONDS. MAILS CAN BE DELAYED")
        
    ##Update database
    update=didyoureadme.libdbupdates.Update(mem)
    if update.need_update()==True:
        if mem.isAdminMode():
            update.run()
        else:
            qmessagebox(mem.tr("DidYouReadMe needs to update its database schema. Please login with an admin role."))
            sys.exit(3)
    update.syncing_files()
            
    frmmain = frmMain(mem) 
    frmmain.show()
    
    sys.exit(mem.app.exec_())

