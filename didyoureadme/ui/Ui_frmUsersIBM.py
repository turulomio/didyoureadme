# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'didyoureadme/ui/frmUsersIBM.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmUsersIBM(object):
    def setupUi(self, frmUsersIBM):
        frmUsersIBM.setObjectName("frmUsersIBM")
        frmUsersIBM.resize(645, 171)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmUsersIBM.setWindowIcon(icon)
        frmUsersIBM.setSizeGripEnabled(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(frmUsersIBM)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl = QtWidgets.QLabel(frmUsersIBM)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl.setFont(font)
        self.lbl.setStyleSheet("color: rgb(0, 192, 0);")
        self.lbl.setText("")
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout.addWidget(self.lbl)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(frmUsersIBM)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txtName = QtWidgets.QLineEdit(frmUsersIBM)
        self.txtName.setObjectName("txtName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtName)
        self.label_2 = QtWidgets.QLabel(frmUsersIBM)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.txtPost = QtWidgets.QLineEdit(frmUsersIBM)
        self.txtPost.setObjectName("txtPost")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtPost)
        self.label_3 = QtWidgets.QLabel(frmUsersIBM)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.txtMail = QtWidgets.QLineEdit(frmUsersIBM)
        self.txtMail.setObjectName("txtMail")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txtMail)
        self.verticalLayout.addLayout(self.formLayout)
        self.chkActive = QtWidgets.QCheckBox(frmUsersIBM)
        self.chkActive.setChecked(True)
        self.chkActive.setTristate(False)
        self.chkActive.setObjectName("chkActive")
        self.verticalLayout.addWidget(self.chkActive)
        self.buttonBox = QtWidgets.QDialogButtonBox(frmUsersIBM)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(frmUsersIBM)
        QtCore.QMetaObject.connectSlotsByName(frmUsersIBM)

    def retranslateUi(self, frmUsersIBM):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("frmUsersIBM", "User name"))
        self.label_2.setText(_translate("frmUsersIBM", "User post"))
        self.label_3.setText(_translate("frmUsersIBM", "User mail"))
        self.chkActive.setText(_translate("frmUsersIBM", "User is active"))

import didyoureadme.images.didyoureadme_rc
