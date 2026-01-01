import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.preprocessing import PolynomialFeatures
import joblib
#DATA CLEANING
df=pd.read_excel('master.xlsx')
print(df)
#FEATURE ENGINEERING
x=df[['b']]
y=df['J']
#DATA SPLITING
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
#POLYNOMILA 
poly=PolynomialFeatures(degree=4,include_bias=False)
x_train_poly=poly.fit_transform(x_train)
x_test_poly=poly.fit_transform(x_test)
#MODEL CREATION
model=LinearRegression()
#MODEL TRAINING
model.fit(x_train_poly,y_train)

#Model and preprocessing
joblib.dump(model,"Rig.model.pkl")
joblib.dump(poly,"feature.pkl")
print("SAVED")
