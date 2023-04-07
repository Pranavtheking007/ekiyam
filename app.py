#importing libraries
import flask
from flask import Flask , render_template , send_file , request
from flask import Flask, render_template, request, session, redirect
import os
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

import numpy as np
#app function initialised
app = Flask(__name__)

model_seg = load_model('Waste_Segregation.h5')

def Waste_Pred(Waste):
  test_image = load_img(Waste, target_size = (256, 256)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) 
  
  result = model_seg.predict(test_image) 
  print('@@ Raw result = ', result)
  
  pred = np.argmax(result, axis=1)

  return pred

# index page
@app.route("/")
def index():
    return render_template('index.html')

# agri page
@app.route("/agriwasteabout.html")
def agriabout():
    return render_template("/agriwasteabout.html")

#agri waste form
@app.route("/agriwasteform.html",methods = ['GET','POST'])
def agriwasteform():
    if request.method == 'GET':
        return render_template("/agriwasteform.html")
    if request.method =='POST':
        nitrogen = request.form['N']
        phosphorous = request.form['P']
        potassium = request.form['K']
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        ph = request.form['ph']
        rainfall = request.form['rainfall']

        print(nitrogen,phosphorous,potassium,temperature,humidity,ph,rainfall)
        
        
#waste management about
@app.route("/wastemanagementabout.html")
def wasteabout():
    return render_template("/wastemanagementabout.html")

#waste management form
@app.route("/wastemanagementform.html",methods = ['GET','POST'])
def wastemanageform():
    if request.method == 'GET':
        return render_template("/wastemanagementform.html")
    if request.method == 'POST':
        tc = request.form['tc']
        region = request.form['region']
        area = request.form['area']
        alt = request.form['alt']
        pden = request.form['pden']
        wden = request.form['wden']
        urb = request.form['urb']
        fee = request.form['fee']
        paper = request.form['paper']
        glass = request.form['glass']
        wood = request.form['wood']
        metal = request.form['metal']
        plastic = request.form['plastic']
        raee = request.form['raee']
        textile = request.form['texile']
        other = request.form['other']
        sor = request.form['sor']

        print(tc,region,area,alt,pden,wden,urb,fee,paper,glass,wood,metal,plastic,raee,textile,other,sor)



#waste segregation about
@app.route("/wastesegregationabout.html")
def wasteseg():
    if request.method == "GET":
        return render_template("wastesegregationabout.html")

# @app.route("/wastesegregation.html")
# def waste():
#     return render_template("/wastesegregation.html")
   
# #waste segregation form
@app.route("/wastesegregation.html",methods = ['GET','POST'])
def wastesegform():
    if request.method =="GET":
         return render_template("/wastesegregation.html") 
    if request.method =="POST":
        file = request.files['file'] # fet input
        filename = file.filename      
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('static/upload', filename)
        file.save(file_path)
        print(file_path)
        X = str(Waste_Pred(Waste=file_path))

        return X
     


##bottle segregation
@app.route("/bottlesegregationabout.html")
def bottle():
    return render_template("/bottlesegregationabout.html")

#bottle segregation form
@app.route("/bottlesegregation.html")
def  bottleform():
    return render_template("/bottlesegregation.html")







if __name__ == "__main__":
    app.run(debug = True) 