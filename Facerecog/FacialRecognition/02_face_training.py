import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
path = 'Facerecog\OpenCV-Face-Recognition\Dataset'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id)

            # Print the image path being processed
            print("Processing Image:", imagePath)

    return faceSamples, ids

print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces, ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write('Facerecog/Trainer/trainer.yml')


# Print the number of unique user IDs
unique_user_ids = set(ids)
print("\n [INFO] {0} unique user IDs:".format(len(unique_user_ids)))
print(unique_user_ids)

# Print the number of faces trained and end the program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
