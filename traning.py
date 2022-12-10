import face_recognition as fr
import cv2, os


cwd = os.getcwd()
print (fr)

faces,faceID=fr.lables_for_training_data(cwd+'/images')
face_recognizer=fr.train_classifier(faces,faceID)
face_recognizer.save(cwd+'/traningData.yml')
print("Done!")

cv2.destroyAllWindows()