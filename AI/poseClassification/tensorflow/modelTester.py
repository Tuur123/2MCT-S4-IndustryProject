import cv2
import numpy as np
import mediapipe as mp

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

img_height = 320
img_width = 600

treshhold = 0.7
windowSize = 5
probablities = []
average = 0

classNames = ["Not Golfswing", "Golfswing"]
predictedLabel = ""

model = tf.keras.models.load_model('AI\\poseClassification\\tensorflow\\model.h5')
model.summary()

mpDraw = mp.solutions.drawing_utils
mPose = mp.solutions.pose
pose = mPose.Pose()

cap = cv2.VideoCapture(0)


while True:
    succes, frame = cap.read()
    
    if succes:

        normalizedFrame = cv2.resize(frame, (img_width, img_height))
        results = pose.process(normalizedFrame)

        mpDraw.draw_landmarks(normalizedFrame, results.pose_landmarks, mPose.POSE_CONNECTIONS)

        if results.pose_landmarks and len(results.pose_landmarks.landmark) == 33:
            
            landmarks = []
            for lm in results.pose_landmarks.landmark:
                landmarks.append(lm.x)
                landmarks.append(lm.y)

            # tf model implementatie
            prediction = model.predict(tf.expand_dims(landmarks, 0))
            score = tf.nn.softmax(prediction[0])

            probablities.append(score)

            if len(probablities) == windowSize:

                average = np.array(probablities).mean(axis=0)
                probablities = []
                
            cv2.putText(normalizedFrame, f"{classNames[np.argmax(average)]} {100 * np.max(average):.2f}% confidence.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.imshow('Capture', normalizedFrame)

        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

cap.release()