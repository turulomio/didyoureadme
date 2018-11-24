## @brief Widget to purge documents
import datetime
from didyoureadme.ui.Ui_wdgDocumentsPurge import Ui_wdgDocumentsPurge
from PyQt5.QtWidgets import QWidget, QMessageBox
from didyoureadme.libdidyoureadme import qmessagebox, SetDocuments

class wdgDocumentsPurge(QWidget, Ui_wdgDocumentsPurge):
    def __init__(self, mem, parent):
        QWidget.__init__(self,  parent)
        self.setupUi(self)
        self.mem=mem
        
        #Minimum of 2 year or date_from for date_to
        datetime_first=SetDocuments(self.mem).datetime_first_document()
        if datetime_first==None:
            qmessagebox(self.tr("There are not documents. You can't purge anything."))
            self.date_from=datetime.date.today()
            self.date_to=datetime.date.today()
        else:
            self.date_from=datetime_first.date()
            self.date_to=datetime.date.today()-datetime.timedelta(days=365*2)
            if self.date_to<self.date_from:
                self.date_to=self.date_from
                
        self.calFrom.setSelectedDate(self.date_from)
        self.calTo.setSelectedDate(self.date_to)
        self.tblDocuments_update()  
        
    def on_calFrom_selectionChanged(self):
        self.date_from=self.calFrom.selectedDate().toPyDate()
        self.error_dates()
        self.tblDocuments_update()

    def on_calTo_selectionChanged(self):
        self.date_to=self.calTo.selectedDate().toPyDate()
        self.error_dates()
        self.tblDocuments_update()
        
    def error_dates(self):
        if self.date_to<self.date_from:
            qmessagebox(self.tr("To date can't be before From date"))
            self.calTo.setSelectedDate(self.date_from)
        
    def tblDocuments_update(self):
        self.documents=SetDocuments(self.mem)  
        self.documents.load("select id,datetime,title,filename,comment,expiration,hash from documents where datetime::date between '{}' and '{}'".format(self.date_from, self.date_to))
        self.tblDocuments.settings(self.mem,"wdgDocumentsPurge", "tblDocuments")
        self.documents.qtablewidget(self.tblDocuments)
        
    def on_cmdPurge_released(self):
        reply = QMessageBox.question(self, self.tr("Purge documents?"), self.tr("You are going to purge documents in the table. If you continue you will delete permanently this data. Do you want to purge them?"), QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.mem.log("Purging")
            for d in self.documents.arr:
                d.delete()
                self.mem.log("Purging document {}".format(d.id))
            self.mem.con.commit()
        else:
            self.mem.log("Not purging")
        self.tblDocuments_update()
        self.cmdPurge.setEnabled(False)
        
