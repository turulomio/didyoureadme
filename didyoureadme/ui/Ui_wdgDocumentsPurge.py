# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'didyoureadme/ui/wdgDocumentsPurge.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_wdgDocumentsPurge(object):
    def setupUi(self, wdgDocumentsPurge):
        wdgDocumentsPurge.setObjectName("wdgDocumentsPurge")
        wdgDocumentsPurge.resize(837, 676)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(wdgDocumentsPurge)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lblApp = QtWidgets.QLabel(wdgDocumentsPurge)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lblApp.setFont(font)
        self.lblApp.setAlignment(QtCore.Qt.AlignCenter)
        self.lblApp.setObjectName("lblApp")
        self.verticalLayout_3.addWidget(self.lblApp)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.label_4 = QtWidgets.QLabel(wdgDocumentsPurge)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMaximumSize(QtCore.QSize(76, 76))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/admin.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.label_3 = QtWidgets.QLabel(wdgDocumentsPurge)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.groupBox = QtWidgets.QGroupBox(wdgDocumentsPurge)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.calFrom = QtWidgets.QCalendarWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calFrom.sizePolicy().hasHeightForWidth())
        self.calFrom.setSizePolicy(sizePolicy)
        self.calFrom.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calFrom.setDateEditEnabled(False)
        self.calFrom.setObjectName("calFrom")
        self.verticalLayout.addWidget(self.calFrom)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.calTo = QtWidgets.QCalendarWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calTo.sizePolicy().hasHeightForWidth())
        self.calTo.setSizePolicy(sizePolicy)
        self.calTo.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calTo.setDateEditEnabled(False)
        self.calTo.setObjectName("calTo")
        self.verticalLayout_2.addWidget(self.calTo)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addWidget(self.groupBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.tblDocuments = myQTableWidget(wdgDocumentsPurge)
        self.tblDocuments.setObjectName("tblDocuments")
        self.tblDocuments.setColumnCount(0)
        self.tblDocuments.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tblDocuments)
        self.cmdPurge = QtWidgets.QPushButton(wdgDocumentsPurge)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.cmdPurge.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/admin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdPurge.setIcon(icon)
        self.cmdPurge.setObjectName("cmdPurge")
        self.verticalLayout_3.addWidget(self.cmdPurge)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)

        self.retranslateUi(wdgDocumentsPurge)
        QtCore.QMetaObject.connectSlotsByName(wdgDocumentsPurge)

    def retranslateUi(self, wdgDocumentsPurge):
        _translate = QtCore.QCoreApplication.translate
        self.lblApp.setText(_translate("wdgDocumentsPurge", "Purge documents"))
        self.label_3.setText(_translate("wdgDocumentsPurge", "In this dialog you can massively delete documents. Be careful, it\'s an action that can\'t be undone"))
        self.label.setText(_translate("wdgDocumentsPurge", "Select a date to purge FROM"))
        self.label_2.setText(_translate("wdgDocumentsPurge", "Select a date to purge TO"))
        self.cmdPurge.setText(_translate("wdgDocumentsPurge", "Purge documents"))

from didyoureadme.ui.myqtablewidget import myQTableWidget
import didyoureadme.images.didyoureadme_rc
