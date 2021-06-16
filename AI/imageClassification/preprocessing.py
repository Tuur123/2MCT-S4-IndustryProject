import cv2
import scipy.io
import numpy as np

data_path = 'E:\\GolfData\\golfDB.mat'
videos_path = "E:\\GolfData\\Videos\\"

frame_paths = {'positives': "E:\\GolfData\\Frames\\Positives\\", 'negatives': "E:\\GolfData\\Frames\\Negatives\\"}

width = 640
height = 360

mat = scipy.io.loadmat(data_path)
numvideos = len(mat["golfDB"][0])



def GetFrames():

    positivesDone = 0
    negativesDone = 0

    for video in mat["golfDB"][0]:
        slow = video[6][0][0]
        if not slow:
            continue
        videoname = videos_path + video[1][0] + ".mp4"
        framenumbers = video[7][0]
        view = video[5][0]
        
        # Open the video file  
        cap = cv2.VideoCapture(videoname)
        if cap.isOpened():
            numframes = cap.get(cv2.CAP_PROP_FRAME_COUNT)   # Number of frames
            framerate = cap.get(cv2.CAP_PROP_FPS)           # Frame rate

            for framenum in range(framenumbers[0], framenumbers[-1]):

                    if cap.set(cv2.CAP_PROP_POS_FRAMES, framenum):
                        ret, frame = cap.read()
                        if ret:
                            outputfilename = frame_paths['positives'] + video[1][0] + "_" + str(framenum) + ".png"
                            cv2.imwrite(outputfilename, frame)
                            positivesDone += 1

                            outputfilename = frame_paths['negatives'] + video[1][0] + "_" + str(framenum) + ".png"

                            negativeNoise = np.zeros((height, width), np.uint8)
                            cv2.randn(negativeNoise, (0), (99)) 
                            cv2.imwrite(outputfilename, negativeNoise)
                            negativesDone += 1


                            print(f"Done {positivesDone} positive frames and {negativesDone} negative frames.                  \r", end='')

                        else:
                            print("Could not read frame " + str(framenum) + " from " + videoname)
                    else:
                        print("Could not go to frame " + str(framenum) + " in " + videoname)
            else:
                print("Could not open " + videoname)


    print()


GetFrames()