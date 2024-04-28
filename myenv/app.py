# Importar los módulos necesarios
from flask import Flask, render_template, request
import cv2
import numpy as np
from PIL import Image
from escpos.printer import Usb

# Inicializar la aplicación Flask
app = Flask(__name__)

# Ruta principal - Página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Función para tomar una fotografía
@app.route('/take_photo', methods=['POST'])
def take_photo():
    # Capturar la foto utilizando OpenCV
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    # Guardar la imagen
    cv2.imwrite('static/photo.jpg', frame)
    return 'Foto capturada exitosamente!'

# Función para imprimir la última fotografía
@app.route('/print_photo', methods=['POST'])
def print_photo():
    # Inicializar la impresora
    printer = Usb(0x0416, 0x5011)

    # Abrir la última foto capturada
    image_path = 'static/photo.jpg'
    image = Image.open(image_path)

    # Imprimir la imagen
    printer.image(image)
    printer.cut()

    return 'Foto impresa correctamente!'

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)