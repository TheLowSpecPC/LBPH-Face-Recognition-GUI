import face_recognition as fr
import cv2, os
print(fr)

def str():
    cwd = os.getcwd()

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read(r'C:\Users\Moiz\IdeaProjects\Face recognition GUI\traningData.yml')

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

    while True:
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
            if(confidence>=40):
                fr.put_text(test_img,'Unknown',x,y)
                continue
            fr.put_text(test_img,predicted_name,x,y)

        resized_img=cv2.resize(test_img,(1000,700))

        cv2.imshow("Face Detection",resized_img)

        if cv2.waitKey(10)==ord('q'):
            break
    return "Gud"