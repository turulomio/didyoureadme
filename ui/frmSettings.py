# -*- coding: utf-8 -*-
import  libdidyoureadme
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

from Ui_frmSettings import *

class frmSettings(QDialog, Ui_frmSettings):
    def __init__(self, cfgfile, parent = None, name = None, modal = False):
        QDialog.__init__(self, parent)
        self.cfgfile=cfgfile
        self.setupUi(self)
        if self.cfgfile.language=="en":
            self.cmbLanguage.setCurrentIndex(self.cmbLanguage.findText("English"))
        elif self.cfgfile.language=="es":
            self.cmbLanguage.setCurrentIndex(self.cmbLanguage.findText('Español'))
        self.txtWebServerIP.setText(self.cfgfile.webserver)
        self.txtWebServerPort.setText(self.cfgfile.webserverport)
        self.txtSupport.setPlainText(self.cfgfile.smtpsupport)
        self.txtSMTPUser.setText(self.cfgfile.smtpuser)
        self.txtSMTPPwd.setText(self.cfgfile.smtppwd)
        self.txtSMTPServer.setText(self.cfgfile.smtpserver)
        self.txtSMTPPort.setText(self.cfgfile.smtpport)
        self.txtSMTPFrom.setText(self.cfgfile.smtpfrom)
        if self.cfgfile.smtpTLS=="True":
            self.chkTLS.setCheckState(Qt.Checked)
            
        ifaces = QNetworkInterface.allInterfaces()
        for iface in ifaces:
            for addr in iface.addressEntries():
                self.cmbInterfaces.addItem("{0} - {1}".format(iface.humanReadableName(), addr.ip().toString() ), addr.ip().toString())
        self.cmbInterfaces.setCurrentIndex(self.cmbInterfaces.findData(self.cfgfile.webinterface))
        

    @pyqtSlot(str)      
    def on_cmbLanguage_currentIndexChanged(self, stri):
        if stri=="English":
            self.cfgfile.language="en"
        elif stri=='Español':
            self.cfgfile.language="es"
        
        libdidyoureadme.cargarQTranslator(self.cfgfile)
        self.retranslateUi(self)
        
    def on_buttonBox_accepted(self):
        self.cfgfile.webserver=self.txtWebServerIP.text()
        self.cfgfile.webserverport=self.txtWebServerPort.text()
        self.cfgfile.webinterface=self.cmbInterfaces.itemData(self.cmbInterfaces.currentIndex())
        self.cfgfile.smtpsupport=self.txtSupport.toPlainText()
        self.cfgfile.smtppwd=self.txtSMTPPwd.text()
        self.cfgfile.smtpserver=self.txtSMTPServer.text()
        self.cfgfile.smtpport=self.txtSMTPPort.text()
        self.cfgfile.smtpuser=self.txtSMTPUser.text()
        self.cfgfile.smtpfrom=self.txtSMTPFrom.text()
        if self.chkTLS.checkState()==Qt.Checked:
            self.cfgfile.smtpTLS="True"
        else:
            self.cfgfile.smtpTLS="False"
        self.cfgfile.save()
        
        self.on_cmbLanguage_currentIndexChanged(self.cmbLanguage.currentText())#Debe hacerse al final para que no afecte valores
