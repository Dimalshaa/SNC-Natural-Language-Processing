# GOTO: http://stackabuse.com/decision-trees-in-python-with-scikit-learn/
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt 
import time

#IPython workaround for '%matplotlib inline'
#from IPython import get_ipython
#get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.model_selection import train_test_split  
from sklearn.tree import DecisionTreeClassifier  
from sklearn.metrics import classification_report, confusion_matrix  
from sklearn.metrics import precision_recall_fscore_support 


# Importing the Dataset
dataset = pd.read_csv("./ml-database/learning_set.csv")  

# Data Analysis
#dataset.shape
#dataset.head()  

# Preparing the Data
# Here the X variable contains all the columns from the dataset, 
# except the "Authentic" and "Ime_dat" columns. 
X = dataset.drop(['Ime_dat','Authentic'], axis=1) 
y = dataset['Authentic'] # The y variable contains the values from the "Authentic" column. 

#print X

M = []
A = []

for i in range(0,10000):

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05) # Split up 20% of the data in to the test set and 80% for training


    # Training and Making Predictions
    classifier = DecisionTreeClassifier()  
    classifier.fit(X_train, y_train)  

    y_pred = classifier.predict(X_test) 


    # Evaluating the Algorithm
    m = precision_recall_fscore_support(y_test, y_pred, average=None)
    a = precision_recall_fscore_support(y_test, y_pred, average='macro')

    if i == 0:
        for index in range(0, len(m)):
            M.append(m[index])

        for index in range(0, len(a)):
            A.append(a[index])
    else:
        for index in range(0, len(m)):
            M[index] += m[index]

        for index in range(0, len(a)):
            if a[index] != None:
                A[index] += a[index]


for index in range(0, len(m)):
    M[index] /= 10000

for index in range(0, len(a)):
    if a[index] != None:
        A[index] /= 10000


#print M
#print A

print "             precision    recall  f1-score   support"
print "                                                    "
print "      False      ",  "%.2f" % M[0][0], "    ", "%.2f" % M[1][0], "    ", "%.2f" % M[2][0] , "       ", M[3][0]
print "       True      ",  "%.2f" % M[0][1], "    ", "%.2f" % M[1][1], "    ", "%.2f" % M[2][1] , "      ", M[3][1]
print "                                                    "
print "avg / total      ",  "%.2f" % A[0], "    ", "%.2f" % A[1], "    ", "%.2f" % A[2] , "      ", M[3][0] + M[3][1]