import os
import torch
import torchaudio
import matplotlib.pyplot as plt
import urllib.request

from flask import Flask,render_template,url_for,request, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

ALLOWED_EXTENSIONS = {'wav'}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_name)
            waveform, sample_rate = torchaudio.load(path_name)
            plt.plot(sample_rate)
            print("Shape of waveform: {}".format(waveform.size()))
            print("Sample rate of waveform: {}".format(sample_rate))
            plt.figure()
            plt.plot(waveform.t().numpy())
            return redirect('/')

@app.route('/predict' ,methods=['POST'])
def predict():
	return render_template('result.html')

# @app.route('/<filename>')
# def uploaded_file(filename):
#     filename = 'http://127.0.0.1:5000/uploads/' + filename
#     return render_template('template.html', filename=filename)

# @app.route('/uploads/<filename>')
# def send_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
	app.run(debug=True)