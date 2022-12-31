import numpy as np
import cv2
import os
import argparse

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
    cv2.putText(test_img, label_name, (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 255, 0), 3)


def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn=frame.copy()
    frameHeight=frameOpencvDnn.shape[0]
    frameWidth=frameOpencvDnn.shape[1]
    blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections=net.forward()
    faceBoxes=[]
    for i in range(detections.shape[2]):
        confidence=detections[0,0,i,2]
        if confidence>conf_threshold:
            x1=int(detections[0,0,i,3]*frameWidth)
            y1=int(detections[0,0,i,4]*frameHeight)
            x2=int(detections[0,0,i,5]*frameWidth)
            y2=int(detections[0,0,i,6]*frameHeight)
            faceBoxes.append([x1,y1,x2,y2])
            cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn,faceBoxes


parser=argparse.ArgumentParser()
parser.add_argument('--image')

args=parser.parse_args()

faceProto=cwd+"/gender/opencv_face_detector.pbtxt"
faceModel=cwd+"/gender/opencv_face_detector_uint8.pb"
ageProto=cwd+"/gender/age_deploy.prototxt"
ageModel=cwd+"/gender/age_net.caffemodel"
genderProto=cwd+"/gender/gender_deploy.prototxt"
genderModel=cwd+"/gender/gender_net.caffemodel"

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList=['Male','Female']

faceNet=cv2.dnn.readNet(faceModel,faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)

video=cv2.VideoCapture(args.image if args.image else 0)
padding=20