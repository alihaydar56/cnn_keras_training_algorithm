#import necessary libraries
import matplotlib.pyplot as plt
from keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import os
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Flatten, Activation
from tensorflow.keras.layers import Conv2D 
from tensorflow.keras.preprocessing.image import ImageDataGenerator


#download mnist data and split into train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()
#plot the first image in the dataset
plt.imshow(X_train[0])


#reshape data to fit model
X_train = X_train.reshape(60000,28,28,1)
X_test = X_test.reshape(10000,28,28,1)

#one-hot encode target column
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
y_train[0]

#create model
model = Sequential()

#add model layers
#2 dimensional matricies,creating filter 3x3 matricies,Rectified Linear Activation,shape of our model(size and type of our image)
model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(28,28,1)))
model.add(Conv2D(32, kernel_size=3, activation='relu'))
model.add(Flatten())#serves connection between Conv2D and Dense
model.add(Dense(10, activation='softmax'))# evaluate between 0-9 for 10 nodes and softmax function.

#compile model using accuracy as a measure of model performance
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
#train model
# training data,target data 
model.fit(X_train, y_train,validation_data=(X_test, y_test), epochs=1)

#show predictions for the first 4 images in the test set
model.predict(X_test[:4])

#show actual results for the first 4 images in the test set
y_test[:4]

#Defining batch size and performing on-the-fly data augmentation technique to enhance our training data.
batch_size = 32

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.4,
    height_shift_range=0.4,
    shear_range=0.2,
    zoom_range=0.3,
    horizontal_flip=True
)
# Note that the validation data should not be augmented!
val_datagen = ImageDataGenerator(
    rescale=1./255,
)
# Flow training images in batches of 32 using train_datagen generator
train_generator = train_datagen.flow(
    X_train,
    y_train,
    batch_size=batch_size
)
val_generator = val_datagen.flow(
    X_test,
    y_test,
    batch_size=batch_size
)

#Training the model over two epochs
epochs = 2
#using Adam Optimizer and Loss a Categorial loss
model_history = model.fit_generator(
    generator=train_generator, 
    steps_per_epoch=len(X_train)/batch_size,   
    epochs=epochs, 
    validation_steps=len(X_test)/batch_size, 
    validation_data=val_generator
)


#After training the custom model see the accuracy performance
acc = model_history.history['acc']  # taking acc from trained data
val_acc = model_history.history['val_acc'] #x_axis of graph
epochs = range(len(acc))
plt.plot(epochs, acc, 'r', label='Training accuracy') #label of trained accuracy with red color
plt.plot(epochs, val_acc, 'b', label='Validation accuracy') #label of validation accuracy with blue color
plt.title('Training and validation accuracy') #title of image
plt.legend(loc=0) #Graphic elements show the signs we specify on the graph.
plt.figure() #draw data
plt.show() #display

#After training the custom model see the loss performance
loss = model_history.history['loss'] # taking loss from trained data
val_loss = model_history.history['val_loss'] #y_axis graph
epochs = range(len(acc))
plt.plot(epochs, loss, 'r', label='Training loss') #label of trained loss with red color
plt.plot(epochs, val_loss, 'b', label='Validation loss') #label of validation loss with blue color
plt.title('Training and Validating Loss') # title of graph
plt.legend(loc=0) #Graphic elements show the signs we specify on the graph.
plt.figure() #draw data
plt.show() #display
