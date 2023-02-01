import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://golden-eagles-93625-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')
data = {
    "21I506":
        {
            "name": "Tony Alosius",
            "major": "Ai&Ds",
            "starting_year": 2021,
            "total_attendance": 1,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2023-10-14 00:13:54"
        },
    "20I153":
        {
            "name": "Sriram",
            "major": "Ai&Ds",
            "starting_year": 2020,
            "total_attendance": 1,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2023-12-13 00:13:50"
        },
    "Unauthorized":
        {
            "last_detected_time": "2023-12-13 00:13:50"
        }
}


for key, value in data.items():
    ref.child(key).set(value)
