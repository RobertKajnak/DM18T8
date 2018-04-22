#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 23:22:16 2018

@author: edoardoguerriero
"""

# Import the necessary modules and libraries
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
import pandas as pd


# Create a random dataset
df = pd.read_csv('patient0.csv', delimiter=',')

df2 = df
df2 = df2.drop('mood', axis=1)
    
X = df2.values
Y = df['mood'].values
    
X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = 0.3, random_state = 100)
# Fit regression model
regr_1 = DecisionTreeRegressor(max_depth=5)

regr_1.fit(X, Y)


# Predict
X_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
y_1 = regr_1.predict(X_test)


# Plot the results
plt.figure()
plt.scatter(X, Y, s=20, edgecolor="black",
            c="darkorange", label="data")
plt.plot(X_test, y_1, color="cornflowerblue",
         label="max_depth=2", linewidth=2)
plt.xlabel("data")
plt.ylabel("target")
plt.title("Decision Tree Regression")
plt.legend()
plt.show()