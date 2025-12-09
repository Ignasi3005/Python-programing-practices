#CREATING PI CHARTS USING PYTHON
import matplotlib.pyplot as plt
lab=["Ignasi","Kalisio","Miho"]
Age=[24,52,86]
scores=[90,60,50]
plt.pie(Age,labels=lab)
plt.title("MIHO CLASS")
plt.pie(scores,labels=lab)
plt.title("MIHO EX")
plt.legend()
plt.show()