from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
import base64
import psycopg2
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Facerecog/Trainer/trainer.yml')
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

font = cv2.FONT_HERSHEY_SIMPLEX

def recognizeFace(save_path, person_id):
    # initiate id counter
    id = 0
    confidence = 0

    cursor.execute("SELECT person_id, username, card_id FROM person ORDER BY person_id ASC")
    userList = cursor.fetchall()
    print(userList)

    if userList:
        res = []
        for item in userList:
            item_dict = {'person_id': item[0], 'username': item[1], 'card_id': item[2]}
            res.append(item_dict)
        print(res)

    # Read the input image
    img = cv2.imread(save_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        recognized_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # Check if confidence is less than 80 ==> "0" is a perfect match
        if confidence < 80:
            
            confidence = "  {0}%".format(round(100 - confidence))

            # Use a list comprehension to find the corresponding username and card_id
            matching_users = [(item[1], item[2]) for item in userList if item[0] == recognized_id]

            # Check if any matching user is found
            if matching_users:
                username, card_id = matching_users[0]
                print(f"Username for ID {recognized_id}: {username}")
                print(f"Card ID for ID {recognized_id}: {card_id}")
            else:
                print(f"No user found for ID {recognized_id}")

                        
            print("Person_id:", person_id)
            print("recognized_id:", recognized_id)
        else:
            recognized_id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, str(recognized_id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)


    if (recognized_id == person_id):
        print("Access Granted")
        return 1
    else:
        print("Access Denied")
        return 0

conn = psycopg2.connect(
    host="jordhie-sbd.postgres.database.azure.com",  
    database="nfacenet", #
    user="jordhieSBD", 
    password="730867Tn",
    port=5432
    #sslmode = True
)

app = Flask(__name__)

cursor = conn.cursor()



# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    # Get RFID ID from form data
    json_data = request.get_json()
    rfid_id = json_data.get('rfid_id')
    image_base64 = json_data.get('image')
    roomName = json_data.get('roomName')
    image_data = np.frombuffer(base64.b64decode(image_base64), np.uint8)
    img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    # Save the received image
    save_path = f'Facerecog\\ReceiveData\\{rfid_id}.jpg'
    cv2.imwrite(save_path, img)

    try:
        # memeriksa apakah id terdaftar, mengambil path
        cursor.execute("SELECT full_name,access_level,person_id FROM person WHERE card_id = %s",(rfid_id,))
        user = cursor.fetchone()
        if user:
            person_id = user[2]
            # membaca gambar
            recognized = recognizeFace(save_path, person_id)
            print(recognized)
            # mencocokkan gambar

            try:
                cursor.execute("SELECT access_level FROM room WHERE room_name = %s",(roomName,))
                roomAccess = cursor.fetchone()
                if recognized == 1:
                    if user[1] >= roomAccess[0]:
                        response = {'success':True,'message': f'Welcome {user[0]}, Access Granted'}
                        # print(f'image received and saved. size={img.shape[1]}x{img.shape[0]}, saved at: {save_path}') 
                        response_pickled = jsonpickle.encode(response)
                        return Response(response=response_pickled, status=200, mimetype="application/json")
                    else:
                        response={'success':False,'message':f'RFID ID={rfid_id} Access Mismatch'}
                        response_pickled = jsonpickle.encode(response)
                        return Response(response=response_pickled, status=404, mimetype="application/json")
                else:
                    response={'success':False,'message':f'RFID ID={rfid_id} Access Denied'}
                    response_pickled = jsonpickle.encode(response)
                    return Response(response=response_pickled, status=404, mimetype="application/json")
            except Exception as e:
                response={'success':False,'message':f'room not found'}
                response_pickled = jsonpickle.encode(response)
                return Response(response=response_pickled, status=500, mimetype="application/json")
                  
            # response.status_code=200
            # response = {'success':'true','message': f'RFID ID={rfid_id}, image received and saved. size={img.shape[1]}x{img.shape[0]}, saved at: {save_path}'}
            # response_pickled = jsonpickle.encode(response)
            # return Response(response=response_pickled, status=200, mimetype="application/json")
        else:
            response={'success':False,'message':f'RFID ID={rfid_id} not found. access denied'}
            response_pickled = jsonpickle.encode(response)
            return Response(response=response_pickled, status=404, mimetype="application/json")
    except Exception as e:
        print(str(e))
        #response = make_response(jsonify({'message': 'an error has ocuured', 'error': str(e),'success':False}))
        response={'success':False,'message':f'server error 1'}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=500, mimetype="application/json")
    

   
    

# start flask app
app.run(host="127.0.0.1", port=5000)   #192.168.146.81