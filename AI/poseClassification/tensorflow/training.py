import pathlib
import numpy as np
import pandas as pd

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import regularizers
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split


data_dir = pathlib.Path("AI\poseClassification\\tensorflow\\data.csv")
checkpoint_filepath = "AI\\poseClassification\\tensorflow\\model.h5"

col_names = ["filename", "class", 
            "nose_x", "nose_y", "left_eye_inner_x", "left_eye_inner_y", "left_eye_x", "left_eye_y" 
            , "left_eye_outer_x" , "left_eye_outer_y" , "right_eye_inner_x" , "right_eye_inner_y"
            , "right_eye_x", "right_eye_y" , "right_eye_outer_x" , "right_eye_outer_y"
            , "left_ear_x" , "left_ear_y" , "right_ear_x" , "right_ear_y" , "mouth_left_x", "mouth_left_y"
            , "mouth_right_x" , "mouth_right_y", "left_shoulder_x", "left_shoulder_y", "right_shoulder_x", 
            "right_shoulder_y", "left_elbow_x", "left_elbow_y", "right_elbow_x", "right_elbow_y",
            "left_wrist_x", "left_wrist_y" , "right_wrist_x" , "right_wrist_y", "left_pinky_x", "left_pink_y", 
            "right_pinky_x", "right_pinky_y", "left_index_x", "left_index_y", "right_index_x", "right_index_y",
            "left_thumb_x", "left_thumb_y", "right_thumb_x", "right_thumb_y", "left_hip_x", "left_hip_y",
            "right_hip_x", "right_hip_y", "left_knee_x", "left_knee_y", "right_knee_x", "right_knee_y",
            "left_ankle_x", "left_ankle_y", "right_ankle_x", "right_ankle_y", "left_heel_x", "left_heel_y", 
            "right_heel_x", "right_heel_y", "left_foot_index_x", "left_foot_index_y", "right_foot_index_x", "right_foot_index_y",]

poseData = pd.read_csv(data_dir, names=col_names)
poseData = poseData.drop("filename", axis = 1)

target = poseData["class"]
features = poseData.drop("class", axis = 1)
features = np.array(features)

model = tf.keras.Sequential([
  layers.Input(shape=(66,)),
    layers.Dense(265),
    layers.Dense(2)
])

model.compile(loss = tf.losses.BinaryCrossentropy(), optimizer = tf.optimizers.Adam(), metrics=['accuracy'])



# This callback will stop the training when there is no improvement in
# the loss for five consecutive epochs.
# earlyStop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
saveModel = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_filepath, save_weights_only=False, monitor='accuracy', mode='max', save_best_only=True)
tensorboard = tf.keras.callbacks.TensorBoard(log_dir="AI\\poseClassification\\tensorflow\\logs", histogram_freq=1)

model.summary()

epochs = 5

try:
  history = model.fit(features, target, epochs=epochs, callbacks=[saveModel, tensorboard])
except KeyboardInterrupt:
  print("\nStopping training...")
  
