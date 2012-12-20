import libdidyoureadme
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_frmAbout import *


class frmAbout(QDialog, Ui_frmAbout):
    def __init__(self, parent = None, name = None, modal = False):
        """
        Constructor
        
        @param parent The parent widget of this dialog. (QWidget)
        @param name The name of this dialog. (QString)
        @param modal Flag indicating a modal dialog. (boolean)
        """
        QDialog.__init__(self, parent)
        if name:
            self.setObjectName(name)
        self.setupUi(self)
        self.lblVersion.setText(self.trUtf8("Version {0}").format(libdidyoureadme.version))
        self.textBrowser.setHtml(
            self.trUtf8("Web page is at <a href=\"http://didyoureadme.sourceforge.net\">http://didyoureadme.sourceforge.net</a><p> <p>")+
            self.trUtf8("This app has been developed by Mariano Muñoz.<p>")+
            self.trUtf8("It has been translated by:")+
            "<ul><li>Mariano Muñoz</li></ul><p>\n"+
            self.trUtf8("to the following languages<p>")+
            "<ul><li>English</li><li>Espa\xf1ol</li></ul><p>"+
            self.trUtf8("Bottle (<a href=\"http://bottlepy.org/docs/dev/\">http://bottlepy.org/docs/dev/</a>) has been used as the associated web server."))
