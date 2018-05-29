import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split  
from sklearn import svm


# Importing the Dataset
dataset = pd.read_csv("./ml-database/learning_set.csv")  

# Data Analysis
#dataset.shape
#dataset.head()  

# Preparing the Data
X = dataset.drop('Authentic', axis=1) # Here the X variable contains all the columns from the dataset, except the "Class" column, which is the label. 
X = dataset.drop('Ime_dat', axis=1) # Delete filenames
y = dataset['Authentic'] # The y variable contains the values from the "Class" column. 


#for i in range(0,1000):
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.00) # Split up 20% of the data in to the test set and 80% for training

