# Run this program on your local python
# interpreter, provided you have installed
# the required libraries.

# Importing the required packages
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

class DecisionTree:
	def __init__(self, data):
			self.balance_data = data
			self.importdata()

	# Function importing Dataset
	def importdata(self):
		# Printing the dataswet shape
		print ("Dataset Length: ", len(self.balance_data))
		print ("Dataset Shape: ", self.balance_data.shape)
		
		# Printing the dataset obseravtions
		print ("Dataset: ",self.balance_data.head())
		return self.balance_data

	# Function to split the dataset
	def splitdataset(self):

		# Separating the target variable
		X = self.balance_data.values[:, 1:5]
		Y = self.balance_data.values[:, 0]

		# Splitting the dataset into train and test
		X_train, X_test, y_train, y_test = train_test_split(
		X, Y, test_size = 0.3, random_state = 100)
		
		return X, Y, X_train, X_test, y_train, y_test
		
	# Function to perform training with giniIndex.
	def train_using_gini(self,X_train, X_test, y_train):

		# Creating the classifier object
		clf_gini = DecisionTreeClassifier(criterion = "gini",
				random_state = 100,max_depth=3, min_samples_leaf=5)

		# Performing training
		clf_gini.fit(X_train, y_train)
		return clf_gini
		
	# Function to perform training with entropy.
	def tarin_using_entropy(self,X_train, X_test, y_train):

		# Decision tree with entropy
		clf_entropy = DecisionTreeClassifier(
				criterion = "entropy", random_state = 100,
				max_depth = 3, min_samples_leaf = 5)

		# Performing training
		clf_entropy.fit(X_train, y_train)
		return clf_entropy


	# Function to make predictions
	def prediction(self,X_test, clf_object):

		# Predicton on test with giniIndex
		y_pred = clf_object.predict(X_test)
		print("Predicted values:")
		print(y_pred)
		return y_pred
		
	# Function to calculate accuracy
	def cal_accuracy(self,y_test, y_pred):
		
		print("Confusion Matrix: ",
			confusion_matrix(y_test, y_pred))
		
		print ("Accuracy : ",
		accuracy_score(y_test,y_pred)*100)
		
		print("Report : ",
		classification_report(y_test, y_pred))

	# Driver code
	def start(self):
		
		# Building Phase
		data = self.balance_data
		X, Y, X_train, X_test, y_train, y_test = self.splitdataset()
		clf_gini = self.train_using_gini(X_train, X_test, y_train)
		clf_entropy = self.tarin_using_entropy(X_train, X_test, y_train)
		
		# Operational Phase
		print("Results Using Gini Index:")
		
		# Prediction using gini
		y_pred_gini = self.prediction(X_test, clf_gini)
		self.cal_accuracy(y_test, y_pred_gini)
		
		print("Results Using Entropy:")
		# Prediction using entropy
		y_pred_entropy = self.prediction(X_test, clf_entropy)
		self.cal_accuracy(y_test, y_pred_entropy)

