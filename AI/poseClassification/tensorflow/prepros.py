import cv2
import scipy.io
import os

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 120
width = 640
height = 360
outputvideo = cv2.VideoWriter("GolfDB.mp4", fourcc, fps, (width,height))

mat = scipy.io.loadmat("E:\GolfData\golfDB.mat")
f = open('View.txt', 'w')
    
numvideos = len(mat["golfDB"][0])
count=0 
for video in mat["golfDB"][0]:
    slow = video[6][0][0]
    if not slow:
        continue
    videoname = "E:\GolfData\Videos\\" + video[1][0] + ".mp4"
    framenumbers = video[7][0]
    view = video[5][0]
    
    # Open the video file  
    cap = cv2.VideoCapture(videoname)
    if cap.isOpened():
        numframes = cap.get(cv2.CAP_PROP_FRAME_COUNT)   # Number of frames
        framerate = cap.get(cv2.CAP_PROP_FPS)           # Frame rate
        for i in range(10):
            f.write("%s\n" % view)
            framenum = framenumbers[i]
            if cap.set(cv2.CAP_PROP_POS_FRAMES, framenum):
                ret, frame = cap.read()
                if ret:
                    outputfilename = "./positive/positive_sample" + "_" + str(count) + ".jpg"
                    count += 1
                    cv2.imwrite(outputfilename, frame)
                    outputvideo.write(frame)
                else:
                    print("Could not read frame " + str(framenum) + " from " + videoname)
            else:
                print("Could not go to frame " + str(framenum) + " in " + videoname)
    else:
        print("Could not open " + videoname)
        
outputvideo.release()
f.close()