import face_recognition as fr
import cv2, os
print(fr)

cwd = os.getcwd()

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(cwd+"/traningData.yml")

cap=cv2.VideoCapture(0)
size=(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

key=[]
value=[]

for i in os.listdir(cwd+"/Info"):
    key.append(int(i[:len(i)-4]))

for j in os.listdir(cwd+"/Info"):
    with open(cwd+"/Info/"+j, "r")as b:
        value.append(b.readline())
        b.close()

name = dict(zip(key,value))

while cv2.waitKey(1)<0 :

    ret,test_img=cap.read()
    face_detected,gray_img=fr.faceDetection(test_img)
    print("Face detected: ",face_detected)
    for(x,y,w,h) in face_detected:
        cv2.rectangle(test_img,(x,y),(x+w,y+h),(0,255,0),thickness=2)

    for face in face_detected:
        (x,y,w,h)=face
        roi_gray=gray_img[y:y+w,x:x+h]
        lable,confidence=face_recognizer.predict(roi_gray)
        print("Confidence: ",confidence)
        print("Lable: ",lable)
        fr.draw_rect(test_img,face)
        predicted_name=name[lable]
        if(confidence>=50):
            fr.put_text(test_img,'Unknown',x,y)
            continue
        fr.put_text(test_img,predicted_name,x,y)

    if cv2.waitKey(10)==ord('q'):
        break

    #genter and age

    resized_img1=cv2.resize(test_img,(1000,700))
    hasFrame,frame=cap.read()
    if not hasFrame:
        cv2.waitKey()
        break

    resultImg,faceBoxes=fr.highlightFace(fr.faceNet,frame)
    if not faceBoxes:
        print("No face detected")
        cv2.imshow("Face Recognition", resized_img1)

    for faceBox in faceBoxes:
        try:
            face=frame[max(0,faceBox[1]-fr.padding):
                       min(faceBox[3]+fr.padding,frame.shape[0]-1),max(0,faceBox[0]-fr.padding)
                                                                :min(faceBox[2]+fr.padding, frame.shape[1]-1)]

            blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), fr.MODEL_MEAN_VALUES, swapRB=False)
            fr.genderNet.setInput(blob)
            genderPreds=fr.genderNet.forward()
            gender=fr.genderList[genderPreds[0].argmax()]
            print(f'Gender: {gender}')

            fr.ageNet.setInput(blob)
            agePreds=fr.ageNet.forward()
            age=fr.ageList[agePreds[0].argmax()]
            print(f'Age: {age[1:-1]} years')
        except:
            continue

        cv2.putText(test_img, f'{gender}, {age}', (x+150, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)
        resized_img=cv2.resize(test_img,(1000,700))
        cv2.imshow("Face Recognition", resized_img)