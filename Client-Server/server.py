from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2

# Initialize the Flask application
app = Flask(__name__)

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Save the received image
    save_path = 'C:\\Users\\Rizki Awanta Jordhie\\Desktop\\image.jpg'
    cv2.imwrite(save_path, img)

    # build a response dict to send back to client
    response = {'message': 'rfid={}, image received and saved. size={}x{}, saved at: {}'.format(img.shape[1], img.shape[0], save_path)}
    
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="192.168.146.81", port=5000)
