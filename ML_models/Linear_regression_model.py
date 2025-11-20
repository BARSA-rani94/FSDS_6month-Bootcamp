# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 20:01:12 2025

@author: HP
"""

import pandas as  pd
import matplotlib.pyplot as plt
import numpy as np


dataset=pd.read_csv(r"C:\Users\HP\Downloads\Salary_Data.csv")

x=dataset.iloc[:,:-1].values
y=dataset.iloc[:,-1].values

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x, y, test_size=0.2, random_state=0)


from sklearn.linear_model import LinearRegression
regressor=LinearRegression()
regressor.fit(x_train,y_train)

y_pred=regressor.predict(x_test)

comparision=pd.DataFrame({'Actual':y_test,'Predicted':y_pred})
print(comparision)

plt.scatter(x_test,y_test,color='red')
plt.plot(x_train,regressor.predict(x_train),color='blue')
plt.title("Salary vs Experience (Test set)")
plt.xlabel("Years of experience")
plt.ylabel("Salary")
plt.show()




