from flask import Flask, request, render_template ,flash,  redirect, url_for
from flask import jsonify
import cv2
import math
import numpy as np 
import crack
import marbleColor
import homogeneous
import classification
import quality
import pattern
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import pickle
import tensorflow as tf
from keras_preprocessing.image import load_img, img_to_array
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

UPLOAD_FOLDER = os.getcwd()+"\\static\\uploads\\images\\"

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):     
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    islem="Anasayfa"
    return render_template('home.html',islem=islem)

@app.route('/crack', methods=['GET', 'POST'])
def marbleCrack():
    islem="Kırık Testi"
    if request.method == 'POST':
        img = request.files['file']
        
        if 'file' not in request.files:
            flash('Herhangi bir dosya bulunamadı')
            return redirect(request.url)

        file = request.files['file']
        
        if file.filename == '':
            flash('Herhangi bir dosya seçilmemiştir')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            now = datetime.now()
            current_time = now.strftime("%H-%M-%S")
            resim_adi=f"cikti_{current_time}.png"
            ret = crack.crack(path,resim_adi)
            if ret:
                return render_template('crack.html',resim_adi=resim_adi)
            else:
                return render_template('crack.html',hata="İşlevsel bir problem oluştu")

    return render_template('basee.html',islem=islem)

@app.route('/pattern', methods=['GET', 'POST'])
def marblePattern():
    islem="Desen Testi"
    if request.method == 'POST':
        img = request.files['file']
        
        if 'file' not in request.files:
            flash('Herhangi bir dosya bulunamadı')
            return redirect(request.url)

        file = request.files['file']
        
        if file.filename == '':
            flash('Herhangi bir dosya seçilmemiştir')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            now = datetime.now()
            current_time = now.strftime("%H-%M-%S")
            resim_adi=f"cikti_{current_time}.png"
            ret = pattern.pattern(path,resim_adi)
            if ret:
                return render_template('pattern.html',resim_adi=resim_adi,path=path)
            else:
                return render_template('pattern.html',hata="İşlevsel bir problem oluştu")

    return render_template('basee.html',islem=islem)

@app.route('/color', methods=['GET', 'POST'])
def colorMarble():
    islem="Renk Testi"
    colorName=marbleColor.color
    
    if request.method == 'POST':
        img = request.files['file']
        
        if 'file' not in request.files:
            flash('Herhangi bir dosya bulunamadı')
            return redirect(request.url)

        file = request.files['file']
        
        if file.filename == '':
            flash('Herhangi bir dosya seçilmemiştir')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(path)

            now = datetime.now()
            current_time = now.strftime("%H-%M-%S")

            resim_adi=f"cikti_{current_time}.png"
            
            ret = marbleColor.color(path,colorName)
            print(filename)
            if ret:
                
                return render_template('color.html',file=str(file.filename),colorName=str(ret[1]),colorCode=str(ret[0]))
            else:
                return render_template('color.html',hata="İşlevsel bir problem oluştu")
            
    return render_template('basee.html',islem=islem)

@app.route('/homogen', methods=['GET', 'POST'])
def marbleHomogen():
    islem="Homojenlik Testi"
    if request.method == 'POST':
        img = request.files['file']
        
        if 'file' not in request.files:
            flash('Herhangi bir dosya bulunamadı')
            return redirect(request.url)

        file = request.files['file']
        
        if file.filename == '':
            flash('Herhangi bir dosya seçilmemiştir')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            now = datetime.now()
            current_time = now.strftime("%H-%M-%S")
            resim_adi=f"cikti_{current_time}.png"
            ret = homogeneous.homogen(path,resim_adi)
            if ret:
                return render_template('homogen.html',resim_adi=resim_adi)
            else:
                return render_template('homogen.html',hata="İşlevsel bir problem oluştu")

    return render_template('basee.html',islem=islem)

@app.route('/classification', methods=['GET', 'POST'])
def MarbleClassification():
    islem="Mermer Sınıflandırma"
    if request.method == 'POST':
        img = request.files['file']
        
        if 'file' not in request.files:
            flash('Herhangi bir dosya bulunamadı')
            return redirect(request.url)

        file = request.files['file']
        
        if file.filename == '':
            flash('Herhangi bir dosya seçilmemiştir')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            now = datetime.now()
            current_time = now.strftime("%H-%M-%S")
            resim_adi=f"cikti_{current_time}.png"
            ret = classification.predict(path)
            if ret:
                return render_template('classification.html',path=path,sinif=str(ret[0]))
            else:
                return render_template('classification.html',hata="İşlevsel bir problem oluştu")

    return render_template('basee.html',islem=islem)


@app.route('/quality', methods=['GET', 'POST'])
def MarbleQualityCheck():
    islem="Kalite Testi"
    if request.method == 'POST':
        img = request.files['file']
        
        if 'file' not in request.files:
            flash('Herhangi bir dosya bulunamadı')
            return redirect(request.url)

        file = request.files['file']
        
        if file.filename == '':
            flash('Herhangi bir dosya seçilmemiştir')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(path)
            file.save(path)
            now = datetime.now()
            current_time = now.strftime("%H-%M-%S")
            resim_adi=f"cikti_{current_time}.png"
           
            ret = quality.MarbleQualityCheck(path)
            if ret:
                return render_template('quality.html',file=str(file.filename),className=ret[0],classQuality=ret[1])

            else:
                return render_template('quality.html',hata="İşlevsel bir problem oluştu")

    return render_template('basee.html',islem=islem)
   
    
if __name__ == '__main__':
    app.run(debug=True)
