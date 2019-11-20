import os
import torch
import torchaudio
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import urllib.request

from flask import Flask,render_template,url_for,request, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename

# Return true if uploaded file is of correct type (.wav)
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

ALLOWED_EXTENSIONS = {'wav'}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Directory where we want to save uploads
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def home():
	return render_template('home.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return render_template('home.html')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template('home.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_name)
            waveform, sample_rate = torchaudio.load(path_name)
            plt.plot(sample_rate)
            figure = plt.figure()
            plt.plot(waveform.t().numpy())
            figure_location = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.png')
            figure.savefig(figure_location)
            print(figure_location)
            name = './static/uploads/'+filename+'.png'
            return render_template('home.html', name=name)
        else:
            return redirect(request.url) 

if __name__ == '__main__':
	app.run(debug=True)