import numpy as np
import cv2
import os

cwd = os.getcwd()
def faceDetection(test_img):
    gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    face_haar = cv2.CascadeClassifier(cwd+"/haarcascade_frontalface_default.xml")
    faces = face_haar.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=3)
    return faces, gray_img


def lables_for_training_data(directory):
    faces = []
    faceID = []

    for path, subdirnames, filenames in os.walk(directory):
        for filename in filenames:
            try:
                if filename.startswith("."):
                    print("Skipping system file")
                    continue
                id = os.path.basename(path)
                img_path = os.path.join(path, filename)
                print("Image Path: ", img_path)
                print("ID: ", id)
                test_img = cv2.imread(img_path)
                if test_img is None:
                    print("Not Loaded Properly")
                    continue

                faces_rect, gray_img = faceDetection(test_img)
                (x, y, w, h) = faces_rect[0]
                roi_gray = gray_img[y:y + w, x:x + h]
                faces.append(roi_gray)
                faceID.append(int(id))
            except:
                print("bad image")
    return faces, faceID


def train_classifier(faces, faceID):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(faceID))
    return face_recognizer


def draw_rect(test_img, face):
    (x, y, w, h) = face
    cv2.rectangle(test_img, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)


def put_text(test_img, label_name, x, y):
    cv2.putText(test_img, label_name, (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 3)
