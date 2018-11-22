from didyoureadme.ui.Ui_wdgDocumentsSearch import Ui_wdgDocumentsSearch
from PyQt5.QtWidgets import QWidget, QMenu
from didyoureadme.libdidyoureadme import SetDocuments

class wdgDocumentsSearch(QWidget, Ui_wdgDocumentsSearch):
    def __init__(self, mem,  parent):
        QWidget.__init__(self,  parent)
        self.setupUi(self)
        self.mem=mem
        self.documents=SetDocuments(self.mem)


    def on_cmdSearch_released(self):
        self.documents=SetDocuments(self.mem)
        sql=self.mem.con.mogrify("""
            select 
                id, datetime, title, filename, comment, expiration, hash 
            from 
                documents 
            where 
                upper(title) like %s ESCAPE ''
            order by datetime""", ("%%{}%%".format(self.txtSearch.text()).upper(), ))
        self.documents.load(sql)
        self.tblDocuments.settings(self.mem,"wdgDocumentsSearch", "tblDocuments")
        self.documents.qtablewidget(self.tblDocuments)
        
        
    def on_tblDocuments_customContextMenuRequested(self,  pos):
        return
        menu=QMenu()
        menu.addAction(self.actionDocumentOpen)
        menu.addAction(self.actionDocumentReport)
                    
        if self.documents.selected==None:
            self.actionDocumentReport.setEnabled(False)
            self.actionDocumentOpen.setEnabled(False)
        else:
            self.actionDocumentReport.setEnabled(True)
            self.actionDocumentOpen.setEnabled(True)            
        menu.exec_(self.tblDocuments.mapToGlobal(pos))

    def on_tblDocuments_itemSelectionChanged(self):
        self.documents.selected=None
        for i in self.tblDocuments.selectedItems():
            if i.column()==0:#only once per row
                self.documents.selected=self.documents.arr[i.row()]

