from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *

from Ui_frmSettings import *

class frmSettings(QDialog, Ui_frmSettings):
    def __init__(self, mem, parent = None, name = None, modal = False):
        QDialog.__init__(self, parent)
        self.mem=mem
        self.setupUi(self)
        self.mem.languages.qcombobox(self.cmbLanguage, self.mem.languages.find(self.mem.cfgfile.language))
        self.txtWebServerIP.setText(self.mem.cfgfile.webserver)
        self.txtWebServerPort.setText(self.mem.cfgfile.webserverport)
        self.txtSupport.setPlainText(self.mem.cfgfile.smtpsupport)
        self.txtSMTPUser.setText(self.mem.cfgfile.smtpuser)
        self.txtSMTPPwd.setText(self.mem.cfgfile.smtppwd)
        self.txtSMTPServer.setText(self.mem.cfgfile.smtpserver)
        self.txtSMTPPort.setText(self.mem.cfgfile.smtpport)
        self.txtSMTPFrom.setText(self.mem.cfgfile.smtpfrom)
        if self.mem.cfgfile.smtpTLS=="True":
            self.chkTLS.setCheckState(Qt.Checked)
        if self.mem.cfgfile.autoupdate=="False":
            self.chkAutoUpdate.setCheckState(Qt.Unchecked)
            
        ifaces = QNetworkInterface.allInterfaces()
        for iface in ifaces:
            for addr in iface.addressEntries():
                self.cmbInterfaces.addItem("{0} - {1}".format(iface.humanReadableName(), addr.ip().toString() ), addr.ip().toString())
        self.cmbInterfaces.setCurrentIndex(self.cmbInterfaces.findData(self.mem.cfgfile.webinterface))
        

    @pyqtSlot(str)      
    def on_cmbLanguage_currentIndexChanged(self, stri):
        self.mem.languages.cambiar(self.cmbLanguage.itemData(self.cmbLanguage.currentIndex()))
        self.retranslateUi(self)
        
    def on_buttonBox_accepted(self):
        self.mem.cfgfile.webserver=self.txtWebServerIP.text()
        self.mem.cfgfile.webserverport=self.txtWebServerPort.text()
        self.mem.cfgfile.webinterface=self.cmbInterfaces.itemData(self.cmbInterfaces.currentIndex())
        self.mem.cfgfile.smtpsupport=self.txtSupport.toPlainText()
        self.mem.cfgfile.smtppwd=self.txtSMTPPwd.text()
        self.mem.cfgfile.smtpserver=self.txtSMTPServer.text()
        self.mem.cfgfile.smtpport=self.txtSMTPPort.text()
        self.mem.cfgfile.smtpuser=self.txtSMTPUser.text()
        self.mem.cfgfile.smtpfrom=self.txtSMTPFrom.text()
        if self.chkTLS.checkState()==Qt.Checked:
            self.mem.cfgfile.smtpTLS="True"
        else:
            self.mem.cfgfile.smtpTLS="False"
        if self.chkAutoUpdate.checkState()==Qt.Checked:
            self.mem.cfgfile.autoupdate="True"
        else:
            self.mem.cfgfile.autoupdate="False"
        self.mem.cfgfile.save()
        
        self.on_cmbLanguage_currentIndexChanged(self.cmbLanguage.currentText())#Debe hacerse al final para que no afecte valores
