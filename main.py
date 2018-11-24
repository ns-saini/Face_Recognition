# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(712, 560)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 50, 691, 481))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.horizontalLayoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.recogniseStudents = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.recogniseStudents.setDefault(False)
        self.recogniseStudents.setFlat(False)
        self.recogniseStudents.setObjectName("recogniseStudents")
        self.verticalLayout.addWidget(self.recogniseStudents)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.trainData = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.trainData.setObjectName("trainData")
        self.verticalLayout.addWidget(self.trainData)
        self.browseImage = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.browseImage.setObjectName("browseImage")
        self.verticalLayout.addWidget(self.browseImage)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayoutWidget.raise_()
        self.graphicsView.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.recogniseStudents.setText(_translate("Dialog", "Recognise Students"))
        self.pushButton_2.setText(_translate("Dialog", "Locate Faces"))
        self.trainData.setText(_translate("Dialog", "Train Data"))
        self.browseImage.setText(_translate("Dialog", "Browse Image"))

