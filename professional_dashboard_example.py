import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

#DATA COLLECTION
data={
    'size':[500,700,1000,1200,1500,1800,2000],
    'price':[300,400,500,550,600,700,750]
}
##DATA CLEANING
df=pd.DataFrame(data)

#FEATURE SELECTION
# feature x and target y
x=df[['size']]
y=df['price']

#DATA SPLITING
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

# MODEL CREATION
model=LinearRegression()
#MODEL TRAINING
model.fit(x_train,y_train)

#MAKE PREDICTIONS
y_test_pred=model.predict(x_test)
y_train_pred=model.predict(x_train)
print("slope(m): ",model.coef_[0])
print("Intercept(c): ",model.intercept_)
print(y_test_pred)

#MODEL EVALUATION
mse=mean_squared_error(y_test,y_test_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(type(x))

#DATA VISUALIZATION
fig, axs=plt.subplots(2,2)
sharex=True
sharey=True
axs[0,0].plot(x_test,y_test,color='b')
axs[0,0].set_title("Ig")
axs[0,1].plot(x_train,y_train_pred,color='r')
axs[0,1].set_title("Miho")
axs[1,0].scatter(x_train,y_train_pred,color='r')
axs[1,0].set_title("Miho")
fig.supxlabel('X')
fig.supylabel('Y')
plt.tight_layout()
plt.legend()
plt.minorticks_on()
plt.show()
