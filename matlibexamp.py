import joblib
import numpy as np

#Load model
model=joblib.load("Rig.model.pkl")
poly=joblib.load("feature.pkl")
x_new=np.array([[5],[40]])
x_new_poly=poly.transform(x_new)
y_pred=model.predict(x_new_poly)
print(y_pred)