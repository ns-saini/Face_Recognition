#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 20:07:58 2018

@author: nishant
"""

from PIL import Image
import face_recognition
import cv2
import os
import pymongo
import pprint
import numpy as np
import time

from pymongo import MongoClient
db_client = MongoClient()
folder = '/home/nishant/IP_Project/Images/'
db = db_client.new_db
faces = db.faces

path = '/home/nishant/a3.jpg'
u_path = '/home/nishant/a4.jpg'
image = face_recognition.load_image_file(u_path)


face_locations = findFaces(path,folder);

photo_encodings = encodeClassFaces(image);

known_faces = getEncodedList()

studentList = recogniseStudents(photo_encodings, known_faces)



def populateDB():
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


def getEncodedList():
    cursor = faces.find()
    x =[]
    for im in cursor:
         x.append(im) 
    
    return x



def findFaces(path,folder):
    image = face_recognition.load_image_file(path)
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
    
    
    return face_locations

def encodeClassFaces(image):
    
    photo_encodings = []
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

def recogniseStudents(photo_encodings,known_faces ):
    
    result = []
    
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
    
    return result