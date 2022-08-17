# -*- coding: utf-8 -*-
"""TW Credit Default Predictio_with Keras.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XObMlRgTVDiUFjO6PjAja20xN-sxmf6Q
"""

!pip install tensorflow

!pip install keras

tf.__version__

import tensorflow as tf

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import os
import numpy as np
import keras
from tensorflow import keras
import matplotlib.pyplot as plt
import itertools 
# %matplotlib inline

TW_data=pd.read_csv("/creditcarddefault.csv")

TW_data.head()

TW_data.describe()

TW_data.shape

TW_data.info()

#removing the customer id and name and saving the dependent varibale in x
x=TW_data.iloc[:,1:24].values
#saving the independent variable in y
y=TW_data.iloc[:,24].values
print(x)
print("**************************************************")
print(y)

x.shape

#splitting the data into train and test using train_test_split for cross validation
from sklearn.model_selection import train_test_split
#splittong the dT in 70:30 ratio
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=111)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

#scaling the data using preprossessing libraries
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
x_train=sc.fit_transform(x_train)
x_test=sc.transform(x_test)

x_train[:1]

#importing the required modules from keras
from keras.models import Sequential
from keras.layers import Dense

#Step 1 :: Initialinzing our model
class_model_keras =Sequential()

#Step 2:: Adding the layers to our NN
#In this step we add one input layer(which are the inputs directly ) multiple hidden layers and one output layer
#As there are 23 input values there will be 23 input nodes in the input layer
#Nodes in the hidden layer are free to our choice, however to have optinum error
#we can claculate the nodes in our first hidden layer to be (ip nodes+ 1)/2= (23+1)/2=12

#while initializing random weightd to our NN
#we pass the value to the hyperparameter init as "UNIFORM"
#UIFORM will ensure that the weights are given uniformly random and close to 0

#Also we would be specifying that activation function to be used. Let us use RELU in our model here

#1st Hidden layer
class_model_keras.add(Dense(24,input_dim=23,activation='relu'))
#2nd hidden layer
class_model_keras.add(Dense(12,activation='relu'))
#output layer
#sigmod activation is used to get the output between 0 and 1
class_model_keras.add(Dense(1,activation='sigmoid'))

class_model_keras.summary()

#Step 3:: compiling the neural network
#int this step we have liberty to choose the optimisation method we would use
#the loss function and the metrics that we require and the output
#binary_crossentropy loss function used when a binary output is expected
class_model_keras.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

#step 4:: Fitting the model
class_model_keras.fit(x_train,y_train,batch_size=10, epochs=100)

#Step 5:: Predicting the results for test data
predict_x=class_model_keras.predict(x_test) 
y_pred=np.argmax(predict_x,axis=1)
#y_pred=class_model_keras.predict_proba(x_test)
y_pred

pred=(y_pred>0.5)
pred

target_names=['no','yes']
def plot_confusion_matrix(cm,classes,normalize=False,title='Confusion matrix',cmap=plt.cm.Blues):
  plt.imshow(cm,interpolation='nearest',cmap=cmap)
  plt.title(title)
  plt.colorbar()
  tick_marks=np.arrange(len(classes))
  plt.xticks(tick_marks,classes,rotation=45)
  plt.yticks(tick_marks,classes)
  if normalize:
    cm=cm.astype('float')/cm.sum(axis=1)[:,np.new]
    print("Normalized Confusion Matrix")
  else:
    print("Confusion Matrix without normalization")
  print(cm)
  thresh=cm.max()/2
  for i,j in itertools.product(range(cm.shape[0]),range(cm.sjape[1])):
    plt.text(j,i,cm[i,j],horizontalalignment='center',color='white' if cm[i,j]>thresh else "black")
  
  plt.tight_layout()
  plt.ylabel("True")
  plt.xlabel("Predicted")

#Formulating the confusion matrix
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,pred)
plt.figure() 
plot_confusion_matrix(cm,classes=target_names,normalize=False)
plt.show()

#evaluating the model
scores=class_model_keras.evaluate(x_test,y_test)
scores