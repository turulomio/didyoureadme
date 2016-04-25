#!/usr/bin/python3
import sys, os, datetime
import platform


if platform.system()=="Windows":
    sys.path.append("ui/")
    sys.path.append("images/")
else:
    sys.path.append("/usr/lib/didyoureadme")
    
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from frmMain import *
from libdidyoureadme import dirDocs, dirReaded

        
try:
    os.makedirs("/tmp/didyoureadme")
except:
    pass
try:
    os.makedirs(dirDocs)
    os.makedirs(dirReaded)
except:
    pass

#def on_trayIcon_triggered( reason):
#    print ("hola")


mem=Mem()

app = QApplication(sys.argv)
app.setApplicationName("didyoureadme {0}".format(datetime.datetime.now()))
app.setQuitOnLastWindowClosed(True)

mem.setQTranslator(QTranslator(app))
mem.languages.cambiar(mem.cfgfile.language)

if mem.cfgfile.error==True:
    m=QMessageBox()
    m.setIcon(QMessageBox.Information)
    m.setText(QApplication.translate("DidYouReadMe","An error loading settings happened. You must check your settings are ok"))
    m.exec_()      

if "admin" in sys.argv:
    mem.adminmodeinparameters=True
    
frmMain = frmMain(mem) 

w=QWidget()
#trayIcon = QSystemTrayIcon(QIcon(":/didyoureadme.png"), w)
#        self.trayIcon.menu.addAction(self.actionExit)
#        self.trayIcon.menu.addSeparator()
#        self.trayIcon.menu.addAction(self.actionAbout)
#QObject.connect(trayIcon, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),   on_trayIcon_triggered) 
#trayIcon.show()
#trayIcon.setToolTip("Octopy Multi-Clipboard Manager") 
frmMain.show()
#trayIcon.showMessage("hola", "hola")
sys.exit(app.exec_())

