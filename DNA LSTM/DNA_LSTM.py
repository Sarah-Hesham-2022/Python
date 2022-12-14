#this is used to write console output to a text file
import sys

#this is used to produce a random element from the arrays
import numpy as np

#for our model building
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing import sequence

from sklearn.model_selection import train_test_split #for splitting our data

# fix random seed for reproducibility
tf.random.set_seed(10)

# Writing to an excel 
# sheet using Python
#If you don't have it ,open console in python and type : 

#pip install XlsxWriter

import xlsxwriter
from xlsxwriter import Workbook
  
# Workbook is created
workbook = xlsxwriter.Workbook('Sheet Numerical Data.xlsx')
  
# add_sheet is used to create sheet.
sheet1 = workbook.add_worksheet()

#sheet1.write(row, col, data)
  
myFile=open("C:/Users/Sarah Hesham/OneDrive/Documents/Python/DNA LSTM/Data.data")

line=myFile.readline()

sheet1.write(0,0,"Prediction")

colCount=1

rowCount=1

#Here I am reperesenting each index as a column with its index in the sequence DNA
while(colCount < 61):

    sheet1.write(0,colCount,colCount-1)
    colCount= colCount +1

colCount=0

#It is mentioned in the data description that there are no empty sets, but there as some inaccurate sets
#and they mentioned that letter D was either an A,G,T in the original data set but they are not so sure
#and same with N,S and R
#I solved this problem by using randomization
#which is substituting this set with any of the suspicious letters randomly

d=[0,2,3]
n=[0,1,2,3]
s=[1,2]
r=[0,2]

#here I am preparing my data for the model to be only numeric
#EI =0
#IE =1
#A  =0
#C  =1
#G  =2
#C  =3

while(line):

    if(line[0:2]=="EI"):
        sheet1.write(rowCount,0,0)
    elif(line[0:2]=="IE"):
        sheet1.write(rowCount,0,1)

    seq=line[39:100]

    for i in range(len(seq)-1):
        if(seq[i]=="A"):
            sheet1.write(rowCount,i+1,0)
        elif(seq[i]=="C"):
            sheet1.write(rowCount,i+1,1)
        elif(seq[i]=="G"):
            sheet1.write(rowCount,i+1,2)
        elif(seq[i]=="T"):
            sheet1.write(rowCount,i+1,3)
        elif(seq[i]=="D"):
            sheet1.write(rowCount,i+1,np.random.choice(d, size=1))
        elif(seq[i]=="N"):
            sheet1.write(rowCount,i+1,np.random.choice(n, size=1))
        elif(seq[i]=="S"):
            sheet1.write(rowCount,i+1,np.random.choice(s, size=1))
        elif(seq[i]=="R"):
            sheet1.write(rowCount,i+1,np.random.choice(r, size=1))

    rowCount=rowCount+1
    line=myFile.readline()

#Essential to save the work
workbook.close()

#Importing the dataset
import pandas as pd
data = pd.read_excel("Sheet Numerical Data.xlsx")
data.to_csv("Sheet Numerical Data.csv")

import pandas as pd
data = pd.read_csv("Sheet Numerical Data.csv")

features=[]

for i in range(60):
    features.append(str(i))

#I am doing this with the X as I have named my columns as indices of the sequences
X = data.loc[:, features]

y = data.loc[:, ["Prediction"]]

# load the dataset 
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,shuffle=True)

#To write to the text file
sys.stdout = open("Result Output.txt", "w")

# create the model
embedding_vecor_length = 32
model = Sequential()
model.add(Embedding(5000, embedding_vecor_length, input_length=60))
model.add(Bidirectional(LSTM(200, dropout=0.2, recurrent_dropout=0.2)))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train, epochs=4, batch_size=64)

# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

#Close the writing text file
sys.stdout.close()