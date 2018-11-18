# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'didyoureadme/ui/frmGroupsIBM.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmGroupsIBM(object):
    def setupUi(self, frmGroupsIBM):
        frmGroupsIBM.setObjectName("frmGroupsIBM")
        frmGroupsIBM.resize(558, 279)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/group.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmGroupsIBM.setWindowIcon(icon)
        frmGroupsIBM.setSizeGripEnabled(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(frmGroupsIBM)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl = QtWidgets.QLabel(frmGroupsIBM)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl.setFont(font)
        self.lbl.setStyleSheet("color: rgb(0, 192, 0);")
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout.addWidget(self.lbl)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(frmGroupsIBM)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txtName = QtWidgets.QLineEdit(frmGroupsIBM)
        self.txtName.setObjectName("txtName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtName)
        self.label_2 = QtWidgets.QLabel(frmGroupsIBM)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lstMembers = QtWidgets.QListView(frmGroupsIBM)
        self.lstMembers.setObjectName("lstMembers")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lstMembers)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(frmGroupsIBM)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(frmGroupsIBM)
        QtCore.QMetaObject.connectSlotsByName(frmGroupsIBM)

    def retranslateUi(self, frmGroupsIBM):
        _translate = QtCore.QCoreApplication.translate
        self.lbl.setText(_translate("frmGroupsIBM", "New Group"))
        self.label.setText(_translate("frmGroupsIBM", "Group name"))
        self.txtName.setText(_translate("frmGroupsIBM", "Group name"))
        self.label_2.setText(_translate("frmGroupsIBM", "Group members"))

import didyoureadme.images.didyoureadme_rc
