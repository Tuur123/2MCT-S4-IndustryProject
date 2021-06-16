from flask import Flask, request, logging, jsonify
from werkzeug.utils import secure_filename
import cv2
import socket
import pickle
import struct
import base64

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((socket.gethostname(), 9999))

ALLOWED_EXTENSIONS = {'mp4'}
app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def uploadToExternalServer():
    if request.method == 'POST':
        base64EncodedFile = base64.b64encode(request.get_data())
        with open("golfswing.mp4", "wb") as fh:
            fh.write(base64.decodebytes(base64EncodedFile))
        send_video("golfswing.mp4")
        return jsonify({'res': 'success'}), 201

def send_video(video):
    img_height = 320
    img_width = 640

    cap = cv2.VideoCapture(video)

    while True:
        succes, frame = cap.read()

        if succes:
            frameResized = cv2.resize(frame, (img_width, img_height))
            frameSer = pickle.dumps(frameResized)

            msg = struct.pack("Q", len(frameSer)) + frameSer
            serverSocket.sendall(msg)

            cv2.imshow("Capture", frameResized)

            if cv2.waitKey(10) == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break
        else:
            cap.release()
            cv2.destroyAllWindows()
            break

# Start app
try:
    if __name__ == '__main__':
        app.run(host="0.0.0.0", debug=True)

except KeyboardInterrupt:
    serverSocket.close()
    print("Closing client.")
