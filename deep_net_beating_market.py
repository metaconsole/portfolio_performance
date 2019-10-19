import numpy as np
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import os

dirpath = os.getcwd()

dataset_df = pd.read_csv(dirpath+ '\\returns_with_benchmark\\returns.csv',
                              sep=',', 
                              index_col='Date',
                              parse_dates = True)
dataset = dataset_df.values[1:, :].T

target_ser = pd.read_csv(dirpath+ '\\returns_with_benchmark\\VSbench.csv',
                              sep=',',
                              index_col=0,
                              header= None,
                              names = ['VSbench'])
target = np.array([int(i[0]) for i in target_ser.values])
predicted_stocks = target_ser.index
# split into input (dataset) and output (y) variables


# define the keras model
model = Sequential()
model.add(Dense(100, input_dim=252, activation='relu'))
model.add(Dense(60, activation='relu'))
model.add(Dense(40, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['binary_accuracy'])

# fit the keras model on the dataset
model.fit(dataset, target, epochs=150, batch_size=10)

# evaluate the keras model
_, accuracy = model.evaluate(dataset, target)
print('Accuracy: %.2f' % (accuracy*100))

# make class predictions with the model
predictions = model.predict_classes(dataset)
# summarize the first 5 cases
for i in range(20):
	print('%s => %d (expected %d)' % (dataset[i][:5], predictions[i], target[i]))