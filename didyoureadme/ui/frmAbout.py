from didyoureadme.version import __version__
from PyQt5.QtWidgets import QDialog
from didyoureadme.ui.Ui_frmAbout import Ui_frmAbout
from didyoureadme.libdidyoureadme import Statistics

class frmAbout(QDialog, Ui_frmAbout):
    def __init__(self, mem, parent = None):
        """
        Constructor
        
        @param parent The parent widget of this dialog. (QWidget)
        @param name The name of this dialog. (QString)
        @param modal Flag indicating a modal dialog. (boolean)
        """
        QDialog.__init__(self, parent)
        self.mem=mem
        self.setupUi(self)
        self.lblVersion.setText(self.tr("Version {}").format(__version__))
        self.textBrowser.setHtml(
            self.tr("""Web page is at <a href="https://github.com/Turulomio/didyoureadme">GitHub</a><p> <p>""")+
            self.tr("This app has been developed by Mariano Mu\\xf1oz.<p>")+
            self.tr("It has been translated by:")+
            "<ul><li>Mariano Mu\\xf1oz</li></ul><p>\n"+
            self.tr("to the following languages<p>")+
            "<ul><li>English</li><li>Espa\xf1ol</li></ul><p>")
        #Table
        self.tblStatistics.settings(self.mem, "frmAbout", "tblStatistics")
        s=Statistics(self.mem)
        s.qtablewidget(self.tblStatistics)
