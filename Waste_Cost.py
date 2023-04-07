#Regular EDA(Exploratory Data Analysis) & Plotting Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.compose import ColumnTransformer

Waste_Cost = pd.read_csv('https://raw.githubusercontent.com/kuchbhi-kunal/ekyam/main/public_data_waste_fee.csv')

Waste_Cost.drop('isle',axis=1,inplace=True)
Waste_Cost.drop('msw_so',axis=1,inplace=True)
Waste_Cost.drop('msw_un',axis=1,inplace=True)
Waste_Cost.drop('roads',axis=1,inplace=True)
Waste_Cost.drop('sea',axis=1,inplace=True)
Waste_Cost.drop('cres',axis=1,inplace=True)
Waste_Cost.drop('csor',axis=1,inplace=True)
Waste_Cost.drop('proads',axis=1,inplace=True)
Waste_Cost.drop('gdp',axis=1,inplace=True)
Waste_Cost.drop('wage',axis=1,inplace=True)

for i in range(len(Waste_Cost['finance'])):
  Waste_Cost.iloc[i,26] = np.exp(Waste_Cost.iloc[i,26])

Waste_Cost['pop'].fillna(Waste_Cost['pop'].mean(),inplace=True)
Waste_Cost['finance'].fillna(Waste_Cost['finance'].mean(),inplace=True)

Waste_Cost['finance_per_capita'] = Waste_Cost['finance']/Waste_Cost['pop']
Waste_Cost.drop('finance',axis=1,inplace=True)

Waste_Cost.drop('name',axis=1,inplace=True)
Waste_Cost.drop('province',axis=1,inplace=True)
Waste_Cost.drop('pop',axis=1,inplace=True)

y=0
for i in Waste_Cost['region']:
  if i =="Valle_d'Aosta":
    print(y)
  y+=1

Waste_Cost.drop([3623],axis=0,inplace=True)
Waste_Cost.drop('s_wteregio',axis=1,inplace=True)

for label, content in Waste_Cost.items():
    if pd.api.types.is_numeric_dtype(content):
        if pd.isnull(content).sum():
            #Fill missing numeric valuees with median
            Waste_Cost[label] = content.fillna(content.median())

for label, content in Waste_Cost.items():
    if pd.api.types.is_object_dtype(content):
        if pd.isnull(content).sum():
            #Fill missing numeric valuees with median
            Waste_Cost[label] = content.fillna(content.mode())

Waste_Cost.drop('istat',axis=1,inplace=True)
Waste_Cost.drop('d_fee',axis=1,inplace=True)
Waste_Cost.drop('sample',axis=1,inplace=True)
Waste_Cost.drop('organic',axis=1,inplace=True)
Waste_Cost.drop('s_landfill',axis=1,inplace=True)
Waste_Cost.drop('geo',axis=1,inplace=True)
Waste_Cost.drop('msw',axis=1,inplace=True)

Y = Waste_Cost['finance_per_capita']
Waste_Cost.drop('finance_per_capita',axis=1,inplace=True)

X_train, X_test, Y_train, Y_test = train_test_split(Waste_Cost,Y,test_size=0.2,random_state=42,stratify=Waste_Cost['urb'])

columns = list(X_train.columns)
columns.remove('region')
columns.remove('fee')

ct = ct = make_column_transformer(
    (MinMaxScaler(), columns),
    (OneHotEncoder(handle_unknown='ignore'),['region','fee']))

ct.fit(X_train)

model = tf.keras.models.load_model("Waste_Fee.h5")

def prediction(region,tc,area,alt,pden,wden,urb,fee,paper,glass,wood,metal,plastic,raee,textile,other,sor):
   preds = {
      'region':region,
      'tc':tc,
      'area':area,
      'alt':alt,
      'pden':pden,
      'wden':wden,
      'urb':urb,
      'fee':fee,
      'paper':paper,
      'glass':glass,
      'wood':wood,
      'metal':metal,
      'plastic':plastic,
      'raee':raee,
      'textile':textile,
      'other':other,
      'sor':sor
   }
   df = pd.DataFrame(preds)
   df_ct = ct.transform(df)

   res = model.predict(df_ct)

   return res
