from didyoureadme.version import __versiondate__
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from didyoureadme.ui.Ui_frmAbout import *


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
        self.lblVersion.setText(self.tr("version {0}").format(__versiondate__))
        self.textBrowser.setHtml(
            self.tr("Web page is at <a href=\"http://didyoureadme.sourceforge.net\">http://didyoureadme.sourceforge.net</a><p> <p>")+
            self.tr("This app has been developed by Mariano Muñoz.<p>")+
            self.tr("It has been translated by:")+
            "<ul><li>Mariano Muñoz</li></ul><p>\n"+
            self.tr("to the following languages<p>")+
            "<ul><li>English</li><li>Espa\xf1ol</li></ul><p>")
