import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import pathlib
import pydot

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import regularizers
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import Sequential


data_dir = pathlib.Path("E:\GolfData\Frames")
checkpoint_filepath = "AI\\imageClassification\\models\\testing\\model.h5"

# loader parameters
batch_size = 16
img_width = 600
img_height = 320


train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_ds.class_names

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

model = Sequential([

    # preprocessing and feature augmentation
  layers.Conv2D(64, (3,3), activation='relu', input_shape=(img_height, img_width, 3)),
  layers.MaxPooling2D(2, 2),

  tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),

  tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),

  tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),

  tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),

  tf.keras.layers.Flatten(),

  layers.Dense(64, activation='relu'),
  layers.Dropout(0.2),
  tf.keras.layers.Dense(2, activation='sigmoid')
])


# This callback will stop the training when there is no improvement in
# the loss for five consecutive epochs.
earlyStop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
saveModel = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_filepath, save_weights_only=False, monitor='val_loss', mode='min', save_best_only=True)
tensorboard = tf.keras.callbacks.TensorBoard(log_dir="AI\\imageClassification\\models\\testing\\logs", histogram_freq=1)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Check its architecture
model.summary()

epochs = 100

try:
  history = model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=[saveModel, tensorboard, earlyStop])
except KeyboardInterrupt:
  print("\nStopping training...")