from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *

from didyoureadme.ui.Ui_frmSettings import *

class frmSettings(QDialog, Ui_frmSettings):
    def __init__(self, mem, parent = None, name = None, modal = False):
        QDialog.__init__(self, parent)
        self.mem=mem
        self.parent=parent
        self.setupUi(self)
        self.mem.languages.qcombobox(self.cmbLanguage, self.mem.language)
        self.txtWebServerIP.setText(self.mem.settings.value("webserver/ip", "127.0.0.1"))
        self.txtWebServerPort.setText(self.mem.settings.value("webserver/port", "8000"))
        self.txtSupport.setPlainText(self.mem.settings.value("smtp/support", "Please, contact system administrator"))
        self.txtSMTPUser.setText(self.mem.settings.value("smtp/smtpuser", "smtpuser"))
        self.txtSMTPPwd.setText(self.mem.settings.value("smtp/smtppwd", "*"))
        self.txtSMTPServer.setText(self.mem.settings.value("smtp/smtpserver", "smtpserver"))
        self.txtSMTPPort.setText(self.mem.settings.value("smtp/smtpport", "25"))
        self.txtSMTPFrom.setText(self.mem.settings.value("smtp/from", "didyoureadme@donotanswer.com"))
        if self.mem.settings.value("smtp/tls", "False")=="True":
            self.chkTLS.setCheckState(Qt.Checked)
            
        ifaces = QNetworkInterface.allInterfaces()
        for iface in ifaces:
            for addr in iface.addressEntries():
                self.cmbInterfaces.addItem("{0} - {1}".format(iface.humanReadableName(), addr.ip().toString() ), addr.ip().toString())
        self.cmbInterfaces.setCurrentIndex(self.cmbInterfaces.findData(self.mem.settings.value("webserver/interface", "127.0.0.1")))
        

    @pyqtSlot(str)      
    def on_cmbLanguage_currentIndexChanged(self, stri):
        self.mem.language=self.mem.languages.find_by_id(self.cmbLanguage.itemData(self.cmbLanguage.currentIndex()))
        self.mem.settings.setValue("mem/language", self.mem.language.id)
        self.mem.languages.cambiar(self.mem.language.id)
        self.retranslateUi(self)
        self.parent.retranslateUi(self.parent)
        
    def on_buttonBox_accepted(self):
        self.mem.settings.setValue("webserver/ip", self.txtWebServerIP.text())
        self.mem.settings.setValue("webserver/port", self.txtWebServerPort.text())
        self.mem.settings.setValue("webserver/interface", self.cmbInterfaces.itemData(self.cmbInterfaces.currentIndex()))
        self.mem.settings.setValue("smtp/support",self.txtSupport.toPlainText())
        self.mem.settings.setValue("smtp/smtppwd", self.txtSMTPPwd.text())
        self.mem.settings.setValue("smtp/smtpserver",self.txtSMTPServer.text())
        self.mem.settings.setValue("smtp/smtpport",self.txtSMTPPort.text())
        self.mem.settings.setValue("smtp/smtpuser",self.txtSMTPUser.text())
        self.mem.settings.setValue("smtp/from",self.txtSMTPFrom.text())
        if self.chkTLS.checkState()==Qt.Checked:
            self.mem.settings.setValue("smtp/tls","True")
        else:
            self.mem.settings.setValue("smtp/tls","False")
        
        self.on_cmbLanguage_currentIndexChanged(self.cmbLanguage.currentText())#Debe hacerse al final para que no afecte valores
