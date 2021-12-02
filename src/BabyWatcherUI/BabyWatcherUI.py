import cv2
from flask import Flask, render_template, url_for, redirect, flash, request
from werkzeug.utils import secure_filename

from Yolo import Run_Yolo

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route("/")
def home():
    return render_template('home.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/yolo')
def upload_form():
    return render_template('upload.html')

@app.route('/yolo', methods=['POST'])
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
        finalImage, bbExists = Run_Yolo.analyzeImage(path)
        print(bbExists)
        cv2.imwrite(path, finalImage)

        return render_template('upload.html', filename=filename, bbExists=bbExists, ai = 'yolo')
    else:
        return redirect(request.url)


@app.route('/app2')
def upload_form2():
    return render_template('upload.html')

@app.route('/app2', methods=['POST'])
def upload_image2():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        #TODO: CONNECT TO THE OTHER APPROACH
        # # Save image and perform analysis on it
        # path = "./static/" + filename
        # file.save(path)
        # finalImage, bbExists = Run_Yolo.analyzeImage(path)
        # print(bbExists)
        # cv2.imwrite(path, finalImage)
        bbExists = False

        return render_template('upload.html', filename=filename, bbExists=bbExists, ai = 'app2')
    else:
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
