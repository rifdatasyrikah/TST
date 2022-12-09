
import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
import pickle

data_admisi = pd.read_csv("adm_data.csv", sep=",")

data_admisi = data_admisi[["GRE Score","TOEFL Score","University Rating","SOP","LOR", "CGPA", "Research", "Chance of Admit"]]
data_admisi["CGPA"] = data_admisi["CGPA"].apply(lambda x: (x*4)/10) #mengonversi nilai GPA dari rentang 0-10 menjadi 0-4
predict_admisi = "Chance of Admit"
print(data_admisi)
x = np.array(data_admisi.drop(columns=predict_admisi))
y = np.array(data_admisi[predict_admisi])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y, test_size=0.1)

linear = linear_model.LinearRegression()
linear.fit(x_train, y_train)
acc = linear.score(x_test, y_test)
print(acc)

with open("admition.pickle", "wb") as f:
    pickle.dump(linear, f)