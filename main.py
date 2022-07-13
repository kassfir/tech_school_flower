import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import os 
from keyboard import read_key
import threading

class App:
    def __init__(self, window, window_title, video_source=0, loop_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.loop_source = loop_source

        # open loop source and video source
        self.loop = MyVideoCapture(self.loop_source, loop=True)
        self.vid = MyVideoCapture(self.video_source)

        #the video currently playing will reference either vid or loop
        self.currently_playing = self.loop

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        #make the window fullscreen
        self.window.attributes('-fullscreen', True)

        #creates a thread to enable listeners - currently it's keyboard listeners but could be sensor listeners.
        input_thread = threading.Thread(target=self.add_input)
        input_thread.daemon = True #<-- makes the thread destroyable
        input_thread.start()

        #stores the last pressed key, but can store last event, e.g. sensor input
        self.last_input = ''

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 13
        self.update()

        self.window.mainloop()

    def update(self):

        #if the thread determines the user pressed esc, kill the app
        if self.last_input == 'esc':
            exit()

        #if the thread determines the user pressed space, launch the video.
        if self.last_input == 'space':
            self.currently_playing = self.vid
            self.last_input = ''

        # else, get a frame from the video source and business as usual
        ret, frame = self.currently_playing.get_frame()

        #if the current frame happens to be the last one, restart the video and move to loop
        #fyi, if the current frame happens to be the last one, it restarts the video and sets it to the loop
        if self.currently_playing.current_frame == self.currently_playing.total_frame_count:
            self.currently_playing.restart_video()
            self.currently_playing = self.loop

        #if the video frame is obtained successfully, render it on screen
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)

    def add_input(self):
        #creates a listener that (for now) registers all keyboard events
        while True:
            self.last_input = read_key()
            print(self.last_input)


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

            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    #set video source to 0th frame
    def restart_video(self):
        self.current_frame = 0 
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
        

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
video_source = os.getcwd() + "\\text_short.mp4"
loop_source = os.getcwd() + "\\arrow.gif"

App(tkinter.Tk(), video_source, video_source=video_source, loop_source=loop_source)