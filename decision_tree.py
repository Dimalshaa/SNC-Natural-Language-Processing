# GOTO: http://stackabuse.com/decision-trees-in-python-with-scikit-learn/
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt 

#IPython workaround for '%matplotlib inline'
#from IPython import get_ipython
#get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.model_selection import train_test_split  
from sklearn.tree import DecisionTreeClassifier  
from sklearn.metrics import classification_report, confusion_matrix, average_precision_score, f1_score   


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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.85) # Split up 20% of the data in to the test set and 80% for training


# Training and Making Predictions
classifier = DecisionTreeClassifier()  
classifier.fit(X_train, y_train)  

y_pred = classifier.predict(X_test) 




# Evaluating the Algorithm
print(confusion_matrix(y_test, y_pred))  
print(classification_report(y_test, y_pred))




