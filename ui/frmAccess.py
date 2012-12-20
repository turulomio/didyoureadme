from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys, psycopg2,  psycopg2.extras
from Ui_frmAccess import *

class frmAccess(QDialog, Ui_frmAccess):
    def __init__(self, mem,  parent = None, name = None, modal = False):
        QDialog.__init__(self,  parent)
        self.mem=mem
        if name:
            self.setObjectName(name)
        self.setModal(True)
        self.setupUi(self)

        self.txtDB.setText(self.mem.cfgfile.database)
        self.txtPort.setText(self.mem.cfgfile.port)
        self.txtUser.setText(self.mem.cfgfile.user)
        self.txtServer.setText(self.mem.cfgfile.server)        

    def check_connection(self):
        strmq="dbname='{0}' port='{1}' user='{2}' host='{3}' password='{4}'".format(self.txtDB.text(),  self.txtPort.text(), self.txtUser.text(), self.txtServer.text(),  self.txtPass.text())
        try:
            con=psycopg2.extras.DictConnection(strmq)
            con.close()
            return True
        except psycopg2.Error:
            return False

    
    @pyqtSignature("")
    def on_cmdYN_accepted(self):
        
        self.mem.cfgfile.database=(self.txtDB.text())
        self.mem.cfgfile.port=(self.txtPort.text())
        self.mem.cfgfile.user=(self.txtUser.text()) 
        self.mem.cfgfile.pwd=(self.txtPass.text()) 
        self.mem.cfgfile.server=(self.txtServer.text()) 
        if self.check_connection()==False:
            m=QMessageBox()
            m.setText(self.trUtf8("Connection error. Try it again"))
            m.exec_()        
            sys.exit(255)
        self.mem.cfgfile.save()
        self.done(0)

    @pyqtSignature("")
    def on_cmdYN_rejected(self):
        sys.exit(255)
