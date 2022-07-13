import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import os 
import keyboard
import threading
from sys import stdin
from queue import Queue

class App:
    def __init__(self, window, window_title, video_source=0, loop_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.loop_source = loop_source

        # open loop source
        self.loop = MyVideoCapture(self.loop_source, loop=True)

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        self.currently_playing = self.loop

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = 1920, height = 1080)
        self.canvas.pack()

        #make the window fullscreen
        self.window.attributes('-fullscreen', True)

        #creates a thread to enable listeners
        input_thread = threading.Thread(target=self.add_input)
        input_thread.daemon = True
        input_thread.start()

        

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.currently_playing.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)

    def add_input(self):
        while True:
            key = keyboard.read_key()
            print (key)


class MyVideoCapture:
    def __init__(self, video_source=0, loop=False):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        self.loop = loop

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.total_frame_count = self.vid.get(cv2.CAP_PROP_FRAME_COUNT)
        self.current_frame = 0

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()

            #looper part of the function
            # taken from here: https://stackoverflow.com/a/27890487
            self.current_frame += 1

            if self.loop == True and self.current_frame == self.vid.get(cv2.CAP_PROP_FRAME_COUNT):
                self.current_frame = 0 
                self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)

            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                # self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
video_source = os.getcwd() + "\\text.mp4"
loop_source = os.getcwd() + "\\arrow.gif"

App(tkinter.Tk(), video_source, video_source=video_source, loop_source=loop_source)