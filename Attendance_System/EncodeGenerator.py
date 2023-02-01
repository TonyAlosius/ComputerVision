import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://golden-eagles-93625-default-rtdb.firebaseio.com/",
    'storageBucket': "golden-eagles-93625.appspot.com"
})


# Fetch the students images and split it into image list
# and studentsId for encoding
folderImgPath = 'Images'
imgPathList = os.listdir(folderImgPath)
imgList = []
studentsId = []
for path in imgPathList:
    imgList.append(cv2.imread(os.path.join(folderImgPath, path)))
    studentsId.append(os.path.splitext(path)[0])

    # Adding new Images to Storage
    fileName = f'{folderImgPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    # print(path)
    # print(os.path.splitext(path)[0])
print(studentsId)


# Encode the images into pixels using face_encoding()
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        # Converting from color BGR2RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


# Driver Code
print("Encoding Started")
encodeListKnown = findEncodings(imgList)
encodingListKnownWithIds = [encodeListKnown, studentsId]
# print(encodeListKnown)
print("Encoding Completed")

# Saving the encoded part on to the file
file = open("EncodeFile.p", "wb")
pickle.dump(encodingListKnownWithIds, file)
file.close()
print("File Saved")


