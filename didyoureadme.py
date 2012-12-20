#!/usr/bin/python3
import sys, os, datetime
so="src.linux"
os.environ['didyoureadmeso']=so
#src.linux src.windows bin.linux bin.windows
if so=="src.windows" or so=="bin.windows":
    sys.path.append("../lib/didyoureadme")
elif so=="src.linux" or so=="bin.linux":
    sys.path.append("/usr/lib/didyoureadme")

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from frmMain import *
from libdidyoureadme import dirDocs, dirReaded, cargarQTranslator
    
try:
    os.makedirs(dirDocs)
    os.makedirs(dirReaded)
except:
    pass

cfgfile=ConfigFile(os.path.expanduser("~/.didyoureadme/")+ "didyoureadme.cfg")
cfgfile.save()

app = QApplication(sys.argv)
app.setApplicationName("didyoureadme {0}".format(str(datetime.datetime.now())))
app.setQuitOnLastWindowClosed(True)

cfgfile.qtranslator=QTranslator()
cargarQTranslator(cfgfile)

if cfgfile.error==True:
    m=QMessageBox()
    m.setIcon(QMessageBox.Information)
    m.setText(QApplication.translate("DidYouReadMe","An error loading settings happened. You must check your settings are ok"))
    m.exec_()      

frmMain = frmMain(cfgfile) 
frmMain.show()
sys.exit(app.exec_())

