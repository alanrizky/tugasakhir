import os
import pickle

import cv2
import face_recognition
from imutils import paths

imagePaths = list(paths.list_images("dataset"))  # folder dataset
knownEncodings = []
knownNames = []

for (i, imagePath) in enumerate(imagePaths):
    print("[INFO] memproses file citra {}/{}".format(i + 1,
                                                     len(imagePaths)))
    name = imagePath.split(os.path.sep)[-2]
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,
                                            model="cnn")
    encodings = face_recognition.face_encodings(rgb, boxes, model="large")
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)

for encode in knownEncodings:
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open("encodings_file.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()
