# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
import face_recognition
import cv2
import os
import numpy as np
import time


class Ui_Dialog(object):
    
    def setupUi(self, Dialog):
        
        Dialog.setObjectName("IP")
        Dialog.resize(712, 560)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 511, 541))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setText("")
        self.label.setObjectName("label")
       
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(550, 90, 130, 112))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.browseImage = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.browseImage.setObjectName("browseImage")
        
        self.gridLayout.addWidget(self.browseImage, 4, 0, 1, 1)
        
        self.trainData = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.trainData.setObjectName("trainData")
        
        self.gridLayout.addWidget(self.trainData, 2, 0, 1, 1)
        
        self.recogniseStudents = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.recogniseStudents.setDefault(False)
        self.recogniseStudents.setFlat(False)
        self.recogniseStudents.setObjectName("recogniseStudents")
        
        self.gridLayout.addWidget(self.recogniseStudents, 0, 0, 1, 1)
        
        self.locateFaces = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.locateFaces.setObjectName("locateFaces")
        
        self.gridLayout.addWidget(self.locateFaces, 1, 0, 1, 1)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        self.browseImage.clicked.connect(self.setImage)
        self.locateFaces.clicked.connect(self.locfaces)
        self.trainData.clicked.connect(self.populateDB)
        self.recogniseStudents.clicked.connect(self.recStudents)
    
    def retranslateUi(self, Dialog):
        
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "IP"))
        self.browseImage.setText(_translate("Dialog", "Browse Image"))
        self.trainData.setText(_translate("Dialog", "Train Data"))
        self.recogniseStudents.setText(_translate("Dialog", "Recognise Students"))
        self.locateFaces.setText(_translate("Dialog", "Locate Faces"))

    def setImage(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "", "Image Files (*.png *.jpg *jpeg *.bmp);;All Files (*)") # Ask for file
        
        global filename
        filename = fileName
        
        if fileName: # If the user gives a file
            pixmap = QtGui.QPixmap(fileName) # Setup pixmap with the provided image
            pixmap = pixmap.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio) # Scale pixmap
            self.label.setPixmap(pixmap) # Set the pixmap onto the label
            self.label.setAlignment(QtCore.Qt.AlignCenter) # Align the label to center
        
    def locfaces(self):
        
        image = face_recognition.load_image_file(filename)
        face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=1, model="cnn")
        i = 0
        for face in face_locations:
           top, right, bottom, left = face
           face_image = image[top:bottom, left:right]
           pil_image = Image.fromarray(face_image)
           
        #        pil_image.show()
        #        image = face_recognition.load_image_file(pil_image)
           timestr = time.strftime("%Y%m%d-%H%M%S")
            
           pil_image.save(folder + 'image' + timestr + str(i) +'.jpg')
           i=i+1


        for (top, right, bottom, left) in face_locations:
                cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)
        
        im = Image.fromarray(image)
        
        pathsr = '/home/nishant/image.jpg'
        im.save(pathsr)
        
        pixmap = QtGui.QPixmap(pathsr) # Setup pixmap with the provided image
        os.remove(pathsr)
        pixmap = pixmap.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio) # Scale pixmap
        self.label.setPixmap(pixmap) # Set the pixmap onto the label
        self.label.setAlignment(QtCore.Qt.AlignCenter) # Align the label to center
        
        
    def populateDB(self):
        
        pid = []
        for filename in os.listdir(folder):
            encoding = {}
            path = folder +filename
            img = face_recognition.load_image_file(path)
            print(filename)
            if img is not None:
                en = face_recognition.face_encodings(img)
                if not en:
                    os.remove(path)
                    continue
                encoding = {'filename' : filename[0:len(filename) - 4], 'encoding': en[0].tolist() }
                pid.append(faces.insert_one(encoding).inserted_id)      
        return pid
        
    def recStudents(self ):
        
        global filename
        fname = filename
        print(fname)
        global result
        
        photo_encodings = self.encodeClassFaces(fname)
        known_faces = self.getEncodedList()
            
        for u_face in photo_encodings:
            res = False
            for known_face in known_faces:
                k_face = known_face['encoding']
                #print( known_face['filename'])
                res = face_recognition.compare_faces(u_face,np.asarray(k_face))
               # print(res[0])
                
                if res[0] == True:
                    result.append({'encoding' : u_face, 'filename': known_face['filename'] })
                    break
                else :
                    continue
            
            if res[0] == False:
                result.append({'encoding': u_face, 'filename': 'not found'})
                
        print(result)
        
        
    
    def getEncodedList(self):
        
        cursor = faces.find()
        x =[]
        for im in cursor:
             x.append(im) 
        
        return x

    def encodeClassFaces(self,filename):
        
        photo_encodings = []
        image = face_recognition.load_image_file(filename)
        face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=1, model="cnn")
        
        for face in face_locations:
            top, right, bottom, left = face
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
    
    #        pil_image.show()
    #        image = face_recognition.load_image_file(pil_image)
            en = face_recognition.face_encodings(np.array(pil_image))
            
            if not en:
                continue
            photo_encodings.append(en)
        
        return photo_encodings
    

        
if __name__ == "__main__":
    
    filename = ''
    global face_locations
    result = []
    
    import sys
    from pymongo import MongoClient
    db_client = MongoClient()
    folder = '/home/nishant/IP_Project/Images/'
    db = db_client.new_db
    faces = db.faces
    
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
