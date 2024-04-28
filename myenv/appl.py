import cv2
import numpy as np
from flask import Flask, render_template, Response, send_file

app = Flask(__name__)

class PhotoBooth:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.filter = None

    def take_photo(self):
        ret, frame = self.capture.read()
        if ret:
            if self.filter:
                frame = self.apply_filter(frame)
            cv2.imwrite("static/photo.jpg", frame)
            return True
        else:
            return False

    def apply_filter(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

    def generate_frames(self):
        while True:
            success, frame = self.capture.read()
            if not success:
                break
            else:
                if self.filter:
                    frame = self.apply_filter(frame)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(PhotoBooth().generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_photo')
def take_photo():
    booth = PhotoBooth()
    if booth.take_photo():
        return "Photo taken successfully"
    else:
        return "Failed to take photo"

@app.route('/get_photo')
def get_photo():
    return send_file("static/photo.jpg", mimetype='image/jpeg')


# Ruta para reiniciar el sistema
@app.route('/restart_system', methods=['POST'])
def restart_system():
    # Aquí colocarías tu lógica para reiniciar el sistema
    print('Restarting system')
    return '', 204


if __name__ == "__main__":
    app.run(debug=True)