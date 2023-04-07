import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf

model =  tf.keras.models.load_model("crop_pred_model.h5")

cp = pd.read_csv('Crop_recommendation.csv')

X = cp.drop('label', axis = 1)
Y = cp['label']

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42,stratify=Y)

ct = make_column_transformer(
    (MinMaxScaler(), ['N','P','K','temperature','humidity','ph','rainfall']))

ct.fit(X_train)

def predict(N,P,K,temperature,humidity,ph,rainfall,Model=model,CT=ct):
    diagnose = {
        'N':[N],
        'P':[P],
        'K':[K],
        'temperature':[temperature],
        'humidity':[humidity],
        'ph':[ph],
        'rainfall':[rainfall]
    }

    df = pd.DataFrame(diagnose)
    df_ct = CT.transform(df)

    Y_preds = Model.predict(df_ct)
    y_pred = Y_preds.argmax(axis=1)

    return y_pred