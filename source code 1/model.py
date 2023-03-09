import joblib

import pandas as pd
from sklearn.naive_bayes import GaussianNB

df1 = pd.read_csv("july_wqc_edit.csv")

X1 = df1[["Do", "Ph", "ORP", "EC", "TDS", "Water_Temp", "CDO", "CpH", "CORP", "CEC", "CTDS", "CWT"]]
y1 = df1["wqc"]

clf1 = GaussianNB() 
clf1.fit(X1, y1)

joblib.dump(clf1, "clfwq.pkl")