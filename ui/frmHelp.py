from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_frmHelp import *

class frmHelp(QDialog, Ui_frmHelp):
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
        s=(self.trUtf8("<h2>User manual</h2>") +
        self.trUtf8("<h3>Configuration</h3>") +
        self.trUtf8("If you select 'auto update tables' tables will be updated each 10 seconds (Not recommended for slow computers).")+"<p>"+
        self.trUtf8("<h3>Documents</h3>") +
        self.trUtf8("To know people who haven't read the document, doubleclick in the documents table.")+" "+
        self.trUtf8("You can copy the text of the message.")+"<p>"+
        self.trUtf8("If the document has been read by all receipts, it will be colored in blue to highlight it, in order to be closed.")+
        self.trUtf8("<h4>Delete documents</h4>") +
        self.trUtf8("You have 1 minute to delete a document you have created, before the sending starts") +
        self.trUtf8("<h3>Mails</h3>") +
        self.trUtf8("Some mail clients detect the Didyoureadme mail as phising, if the url in the mail, has an IP instead of a DNS name. To avoid this you have to accept the mail in the client.")+
        self.trUtf8("<h3>Users</h3>") +
        self.trUtf8("To know the groups a user belongs, just double click in a user in the users table.")
        )
        
        self.browser.setHtml(s)

