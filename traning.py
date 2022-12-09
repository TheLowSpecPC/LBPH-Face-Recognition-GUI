import face_recognition as fr
import cv2, os

def tran():
    cwd = os.getcwd()
    print (fr)

    faces,faceID=fr.lables_for_training_data(cwd+'/images')
    face_recognizer=fr.train_classifier(faces,faceID)
    face_recognizer.save(cwd+'/traningData.yml')

    cv2.destroyAllWindows()
    return "Finished Training"