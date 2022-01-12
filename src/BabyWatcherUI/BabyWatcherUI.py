import cv2
from flask import Flask, render_template, url_for, redirect, flash, request
import os
from werkzeug.utils import secure_filename
from PIL import Image

from Yolo import Run_Yolo

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route("/")
def home():
    return render_template('home.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/xx')
def upload_form():
    return render_template('upload.html')


@app.route('/xx', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)


        # Save image and perform analysis on it

        path = "./BabyWatcherUI/static/" + filename
        file.save(path)
        finalImage = Run_Yolo.analyzeImage(path)
        cv2.imwrite(path, finalImage)

        return render_template('upload.html', filename=filename)
    else:
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
