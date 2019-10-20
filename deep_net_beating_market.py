import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import adam
import pandas as pd
import os

dirpath = os.getcwd()
in_path = dirpath+ '\\returns_with_benchmark\\'

def get_data(input_directory):
    dataset_df = pd.read_csv(input_directory+'\\performance.csv',
                              sep=',', 
                              index_col='Date',
                              parse_dates = True)
    
    target_ser = pd.read_csv(input_directory+'\\VSbench.csv',
                              sep=',',
                              index_col=0,
                              header= None,
                              names = ['VSbench'])
    return dataset_df, target_ser

dataset_1, target_1 = get_data(in_path + '2011-01-31_2012-01-31')
dataset_2, target_2 = get_data(in_path + '2014-06-30_2015-06-30')
dataset_3, target_3 = get_data(in_path + '2015-06-30_2016-06-29')

dataset = np.concatenate((dataset_1.values[1:, :].T, dataset_2.values[1:, :].T),
                         axis = 0)
target_ser = np.concatenate((target_1, target_2))

vali_dataset = dataset_3.values[1:, :].T

vali_target = np.array([int(i[0]) for i in target_3.values])
target = np.array([int(i[0]) for i in target_ser])

# split into input (dataset) and output (y) variables


# define the keras model
model = Sequential()
model.add(Dense(100, input_dim=252, activation='relu'))
model.add(Dense(80, activation='relu'))
model.add(Dense(40, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile the keras model
adam_opt = adam(lr = 0.01)
model.compile(loss='binary_crossentropy', optimizer= adam_opt, metrics=['accuracy'])

# fit the keras model on the dataset
hist = model.fit(dataset, target, epochs=300, batch_size=10, verbose = 2, )

# evaluate the keras model
_, accuracy = model.evaluate(vali_dataset, vali_target)
print('Accuracy: %.2f' % (accuracy*100))

# make class predictions with the model
# gives around 70.33% accuracy when trained with performance 
# gives around 60 % accuracy when trained with return
predictions = model.predict_classes(vali_dataset)
# summarize the first few cases
for i in range(10):
	print('%s => %d (expected %d)' % (dataset[i][:5], predictions[i], target[i]))