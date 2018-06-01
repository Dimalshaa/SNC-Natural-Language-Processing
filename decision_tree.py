# GOTO: http://stackabuse.com/decision-trees-in-python-with-scikit-learn/
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt 
import time

# Turn off warnings:
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split  
from sklearn.metrics import classification_report, confusion_matrix  
from sklearn.metrics import precision_recall_fscore_support 
from sklearn import tree

# Fine-tunning:
from sklearn.preprocessing import LabelBinarizer
from sklearn.ensemble import RandomForestClassifier

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


# Importing the Dataset
dataset = pd.read_csv("./ml-database/learning_set.csv") 

# Binarization of the data
lb = LabelBinarizer()
index = 0
for i in dataset:
    if index != 0 and index != len(dataset)-1:
        dataset[i] = lb.fit_transform(dataset[i].values) 

# Data Analysis
#dataset.shape
#dataset.head()  

# Preparing the Data
# Here the X variable contains all the columns from the dataset, 
# except the "Authentic" and "Ime_dat" columns. 
X = dataset.drop(['Ime_dat','Authentic', 'Num_signs', 'Num_words', 'Num_chars'], axis=1) 
y = dataset['Authentic'] # The y variable contains the values from the "Authentic" column. 

#print X

M = []
A = []


classifiers = [
    #KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    #SVC(gamma=2, C=1),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=5),
    #RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    #MLPClassifier(alpha=1),
    AdaBoostClassifier(),
    #GaussianNB(),
    #QuadraticDiscriminantAnalysis()
    ]


N = 10000
for c in classifiers:
    for i in range(0,N):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05) # Split up 20% of the data in to the test set and 80% for training


        # Training and Making Predictions
        classifier = c #RandomForestClassifier(max_depth=5)  
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
        M[index] /= N

    for index in range(0, len(a)):
        if a[index] != None:
            A[index] /= N

    print str(c)
    print "             precision    recall  f1-score   support"
    print "                                                    "
    print "      False      ",  "%.2f" % M[0][0], "    ", "%.2f" % M[1][0], "    ", "%.2f" % M[2][0] , "       ", M[3][0]
    print "       True      ",  "%.2f" % M[0][1], "    ", "%.2f" % M[1][1], "    ", "%.2f" % M[2][1] , "      ", M[3][1]
    print "                                                    "
    print "avg / total      ",  "%.2f" % A[0], "    ", "%.2f" % A[1], "    ", "%.2f" % A[2] , "      ", M[3][0] + M[3][1]




"""
# export Decision Tree to PDF(.dot)
classifier = DecisionTreeClassifier()  
classifier.fit(X_train, y_train)  

with open("classifier.dot", "w") as f:
    f = tree.export_graphviz(classifier, out_file=f)

"""
