# DATA ANALYSIS WITH PANDAS
# DATAFRAME,SERIES CREATION & MANIPULATION
import pandas as pd 
#SERIES CREATION
#from list
S1=pd.Series([1,2,3,4,5,6,7])
#from list with custom index
S2=pd.Series([10,20,30],index=["a","b","c"])
#f 
data={"Names":["Ignasi","Mark","Louis","Luke"],
      "Age":[24,23,25,26],
      "score":[90,85,70,60]}
df=pd.DataFrame(data)
df["mean"]=df[["Age","score"]].mean(axis=1) #This add avarage of Age and scores

print(df)
print(df["Names"]) #This prints names column
print(df.loc[1])
print(df.sort_values(by="mean",ascending=True))
