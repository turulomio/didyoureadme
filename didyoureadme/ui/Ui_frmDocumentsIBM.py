# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'didyoureadme/ui/frmDocumentsIBM.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmDocumentsIBM(object):
    def setupUi(self, frmDocumentsIBM):
        frmDocumentsIBM.setObjectName("frmDocumentsIBM")
        frmDocumentsIBM.resize(571, 688)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/document.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmDocumentsIBM.setWindowIcon(icon)
        self.horizontalLayout = QtWidgets.QHBoxLayout(frmDocumentsIBM)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(frmDocumentsIBM)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txtTitle = QtWidgets.QLineEdit(frmDocumentsIBM)
        self.txtTitle.setObjectName("txtTitle")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtTitle)
        self.label_6 = QtWidgets.QLabel(frmDocumentsIBM)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lstGroups = QtWidgets.QListView(frmDocumentsIBM)
        self.lstGroups.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lstGroups.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lstGroups.setObjectName("lstGroups")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lstGroups)
        self.label_7 = QtWidgets.QLabel(frmDocumentsIBM)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.lstUsers = QtWidgets.QListView(frmDocumentsIBM)
        self.lstUsers.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lstUsers.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lstUsers.setObjectName("lstUsers")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lstUsers)
        self.label_2 = QtWidgets.QLabel(frmDocumentsIBM)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.laySend = QtWidgets.QHBoxLayout()
        self.laySend.setObjectName("laySend")
        self.txtFilename = QtWidgets.QLineEdit(frmDocumentsIBM)
        self.txtFilename.setReadOnly(True)
        self.txtFilename.setObjectName("txtFilename")
        self.laySend.addWidget(self.txtFilename)
        self.cmdFile = QtWidgets.QToolButton(frmDocumentsIBM)
        self.cmdFile.setObjectName("cmdFile")
        self.laySend.addWidget(self.cmdFile)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.laySend)
        self.label_5 = QtWidgets.QLabel(frmDocumentsIBM)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.txtComment = QtWidgets.QPlainTextEdit(frmDocumentsIBM)
        self.txtComment.setObjectName("txtComment")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.txtComment)
        self.label_3 = QtWidgets.QLabel(frmDocumentsIBM)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.teExpiration = QtWidgets.QDateEdit(frmDocumentsIBM)
        self.teExpiration.setCalendarPopup(True)
        self.teExpiration.setObjectName("teExpiration")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.teExpiration)
        self.verticalLayout.addLayout(self.formLayout)
        self.cmd = QtWidgets.QPushButton(frmDocumentsIBM)
        self.cmd.setIcon(icon)
        self.cmd.setObjectName("cmd")
        self.verticalLayout.addWidget(self.cmd)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(frmDocumentsIBM)
        QtCore.QMetaObject.connectSlotsByName(frmDocumentsIBM)

    def retranslateUi(self, frmDocumentsIBM):
        _translate = QtCore.QCoreApplication.translate
        frmDocumentsIBM.setWindowTitle(_translate("frmDocumentsIBM", "Add document"))
        self.label.setText(_translate("frmDocumentsIBM", "Document title"))
        self.label_6.setText(_translate("frmDocumentsIBM", "Groups to send"))
        self.label_7.setText(_translate("frmDocumentsIBM", "Users to send"))
        self.label_2.setText(_translate("frmDocumentsIBM", "Document to send"))
        self.cmdFile.setText(_translate("frmDocumentsIBM", "..."))
        self.label_5.setText(_translate("frmDocumentsIBM", "Add a comment"))
        self.label_3.setText(_translate("frmDocumentsIBM", "Document expiration"))
        self.teExpiration.setDisplayFormat(_translate("frmDocumentsIBM", "dd/MM/yyyy"))
        self.cmd.setText(_translate("frmDocumentsIBM", "Add document"))

import didyoureadme.images.didyoureadme_rc