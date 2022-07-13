import cv2
import numpy as np

videoName = yourVideoPathAndName #'DJI_0209.MP4'

#create a videoCapture Object (this allow to read frames one by one)
video = cv2.VideoCapture(videoName)
#check it's ok
if video.isOpened():
    print('Video Succefully opened')
else:
    print('Something went wrong check if the video name and path is correct')


#define a scale lvl for visualization
scaleLevel = 3 #it means reduce the size to 2**(scaleLevel-1)


# windowName = 'Video Reproducer'
# cv2.namedWindow(windowName )
# #let's reproduce the video
# while True:
#     ret,frame = video.read() #read a single frame 
#     if not ret: #this mean it could not read the frame 
#          print("Could not read the frame")   
#          cv2.destroyWindow(windowName)
#          break

#     reescaled_frame  = frame
#     for i in range(scaleLevel-1):
#         reescaled_frame = cv2.pyrDown(reescaled_frame)

#     cv2.imshow(windowName, reescaled_frame )

#     waitKey = (cv2.waitKey(1) & 0xFF)
#     if  waitKey == ord('q'): #if Q pressed you could do something else with other keypress
#          print("closing video and exiting")
#          cv2.destroyWindow(windowName)
#          video.release()
#          break
while(video.isOpened()):
      
  # Capture frame-by-frame
  ret, frame = video.read()
  if ret == True:
   
    # Display the resulting frame
    cv2.imshow('Frame', frame)
   
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
   
  # Break the loop
  else: 
    break
   
# When everything done, release 
# the video capture object
video.release()
   
# Closes all the frames
cv2.destroyAllWindows()