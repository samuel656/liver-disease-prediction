import joblib
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template,request, jsonify
from flask import Flask, redirect, url_for, render_template, request, flash

model = pickle.load(open('liver.pkl', 'rb'))
app = Flask(__name__,template_folder='templates')
@app.route('/')
def home():
    return render_template('liver.html')
    
def ValuePredictor(to_predict_list):
    # change the input data to a numpy array
    input_data_as_numpy_array= np.asarray(to_predict_list)

    # reshape the numpy array as we are predicting for only on instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    prediction = model.predict(input_data_reshaped)
    
    if (prediction[0]==2):
        return 1
    else:
        return 0
   

@app.route('/predict', methods=['GET', 'POST'])
def predict():   
   
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float,to_predict_list))
        if(len(to_predict_list)==9):
            result=ValuePredictor(to_predict_list)
            if(result==0):
                prediction = "No need to fear. You have no dangerous symptoms of the Liver disease!!"
            else:
                prediction = "Sorry you have chances of getting the Liver disease. Please consult the doctor immediately!"
                
    return render_template("result.html", prediction_text=prediction)   

if __name__ == "__main__":
    app.run(debug=True)
