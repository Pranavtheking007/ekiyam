#importing libraries
import flask
from flask import Flask , render_template , send_file , request
from flask import Flask, render_template, request, session, redirect
import os
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import Crop_model as CM
import Waste_Cost as WC
import numpy as np
#app function initialised
app = Flask(__name__)

model_seg = load_model('Waste_Segregation.h5')
# model_bottle = load_model('wasteV2.h5')
model_check = load_model('wasteV3.h5')

def Waste_Pred(Waste):
  test_image = load_img(Waste, target_size = (256, 256)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) 
  
  result = model_seg.predict(test_image) 
  print('@@ Raw result = ', result)
  
  pred = np.argmax(result, axis=1)

  return pred

def Waste_Bottle(Bottle):
  test_image = load_img(Bottle, target_size = (256, 256)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) 
  
  result = model_seg.predict(test_image) 
  print('@@ Raw result = ', result)
  
  pred = np.argmax(result, axis=1)

  return pred

def Check_Pred(Check):
  test_image = load_img(Check, target_size = (256, 256)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) 
  
  result = model_check.predict(test_image) 
  print('@@ Raw result = ', result)
  
  pred = np.argmax(result, axis=1)

  return pred

# index page
@app.route("/")
def index():
    return render_template('index.html')

# Case Study page
@app.route("/singapore.html")
def casestudy():
    return render_template("/singapore.html")

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

        X = str(CM.predict(nitrogen,phosphorous,potassium,temperature,humidity,ph,rainfall))

        if (X=='[0]'):
            return render_template('agriwasteresult.html',data_pred='Rice')
        elif (X=='[1]'):
            return render_template('agriwasteresult.html',data_pred='Maize ')
        elif (X=='[2]'):
            return render_template('agriwasteresult.html',data_pred='Jute')
        elif (X=='[3]'):
            return render_template('agriwasteresult.html',data_pred='Cotton')
        elif (X=='[4]'):
            return render_template('agriwasteresult.html',data_pred='Coconut')
        elif (X=='[5]'):
            return render_template('agriwasteresult.html',data_pred='Papaya')
        elif (X=='[6]'):
            return render_template('agriwasteresult.html',data_pred='Orange')
        elif (X=='[7]'):
            return render_template('agriwasteresult.html',data_pred='Apple')
        elif (X=='[8]'):
            return render_template('agriwasteresult.html',data_pred='Muskmelon')
        elif (X=='[9]'):
            return render_template('agriwasteresult.html',data_pred='Watermelon')
        elif (X=='[10]'):
            return render_template('agriwasteresult.html',data_pred='Grapes')
        elif (X=='[11]'):
            return render_template('agriwasteresult.html',data_pred='Mango')
        elif (X=='[12]'):
            return render_template('agriwasteresult.html',data_pred='Banana')
        elif (X=='[13]'):
            return render_template('agriwasteresult.html',data_pred='Pomegranate')
        elif (X=='[14]'):
            return render_template('agriwasteresult.html',data_pred='Lentil')
        elif (X=='[15]'):
            return render_template('agriwasteresult.html',data_pred='Blackgram')
        elif (X=='[16]'):
            return render_template('agriwasteresult.html',data_pred='Mungbean')
        elif (X=='[17]'):
            return render_template('agriwasteresult.html',data_pred='Mothbeans')
        elif (X=='[18]'):
            return render_template('agriwasteresult.html',data_pred='Pigeonpeas')
        elif (X=='[19]'):
            return render_template('agriwasteresult.html',data_pred='Kidneybeans')
        elif (X=='[20]'):
            return render_template('agriwasteresult.html',data_pred='Chickpeas')
        elif (X=='[21]'):
            return render_template('agriwasteresult.html',data_pred='Coffee')
        

        
        
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
        texile = request.form['texile']
        other = request.form['other']
        sor = request.form['sor']

        X=str(WC.prediction(tc,region,area,alt,pden,wden,urb,fee,paper,glass,wood,metal,plastic,raee,texile,other,sor))
        return render_template('wastemanagementresult.html',res=X)


#Waste Check waste form
@app.route("/checkform.html",methods = ['GET','POST'])
def checkform():
    if request.method == 'GET':
        return render_template("/checkform.html")
    if request.method == 'POST':
        file = request.files['file'] # fet input
        filename = file.filename      
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('static/upload', filename)
        file.save(file_path)
        print(file_path)
        X = str(Check_Pred(Check=file_path))
        if (X=='[0]'):
            return render_template('checkresult.html',data_pred='Cardboard')
        if (X=='[1]'):
            return render_template('checkresult.html',data_pred='Glass')
        if (X=='[2]'):
            return render_template('checkresult.html',data_pred='Metal')
        if (X=='[3]'):
            return render_template('checkresult.html',data_pred='Paper')
        if (X=='[4]'):
            return render_template('checkresult.html',data_pred='Plastic')
        if (X=='[5]'):
            return render_template('checkresult.html',data_pred='Others')



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
        
        if(X=='[0]'):
            return render_template("organic_wastesegregationresult.html")
        if(X=='[1]'):
            return render_template("recycleable_wastesegregationresult.html")
     


##bottle segregation
@app.route("/bottlesegregationabout.html")
def bottle():
    return render_template("/bottlesegregationabout.html")

#bottle segregation form
@app.route("/bottlesegregation.html")
def  bottleform():
    if request.method =="GET":
        return render_template("/bottlesegregation.html")
# @app.route("/bottlesegregationabout.html")
# def  bottleformabout():
#     if request.method =="POST":
#             file = request.files['file'] # fet input
#             filename = file.filename      
#             print("@@ Input posted = ", filename)
            
#             file_path = os.path.join('static/upload', filename)
#             file.save(file_path)
#             print(file_path)
#             X = str(Waste_Pred(Waste=file_path))
            
            # if(X=='[0]'):
            #     return render_template("organic_wastesegregationresult.html.html")
            # if(X=='[1]'):
            #     return render_template("recycleable_wastesegregationresult.html")
        
# @app.route("/potatoes.html",methods = ["GET","POST"])
# def potatoes():
    
#     return render_template("potatoes.html")


if __name__ == "__main__":
    app.run(debug = True) 