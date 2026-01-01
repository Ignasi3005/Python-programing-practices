import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

#Data collection 
data={
    'AA':[1,2,3,4,5],
    'BB':[1,2,3,4,5],
}

#DATA CLEANING
df=pd.DataFrame(data)

#FEATURE SELECTION
x=df[['AA']]
y=df['BB']

#MODEL SELECTION
model=LinearRegression()

#DATA SPLITING
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=42)

#MODEL TRAINING
model.fit(x_train,y_train)

#PREDICTION
y_pred=model.predict(x_test)
print(y_pred)
print("slope:",model.coef_[0])
print("Intercept:",model.intercept_)
mse=mean_squared_error(x_test,y_test)
print("mse",mse)