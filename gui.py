# Python program to create 
# a file explorer in Tkinter 

# import all components 
# from the tkinter library 
from tkinter import *
import sys
import threading

# import filedialog module 
from tkinter import filedialog


class PrintLogger():  # create file like object
    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.insert(END, text)  # write text to textbox
        # could also scroll to end of textbox here to make sure always visible

    def flush(self):  # needed for file like object
        pass


def browsevideo():
    global video
    video = filedialog.askdirectory()
    video_folder_name = video.split('/')[-1]

    # Change label contents
    button_video.configure(text="Folder Opened: " + video_folder_name)
    print(video)


def browseaudio():
    global audio
    audio = filedialog.askopenfilename()
    audio_folder_name = audio.split('/')[-1]

    # Change label contents
    button_audio.configure(text="File Opened: " + audio_folder_name)
    print(audio)


def make_video():
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    from moviepy.video.compositing.concatenate import concatenate_videoclips
    from moviepy.video.VideoClip import ImageClip
    from moviepy.audio.fx.audio_loop import audio_loop
    from moviepy.video.fx.resize import resize
    import os

    audio_clip = AudioFileClip(audio)

    all_videos = []
    for file in os.listdir(video):
        all_videos.append(VideoFileClip(os.path.join(video, file)).fx(resize, width=1920))

    final = concatenate_videoclips(all_videos,
                                   # method='compose',
                                   )  # method allows me to avoid glitches with resolution

    logo = (ImageClip("1.png")
            .set_duration(final.duration)
            .fx(resize, 0.5)  # if you need to resize...
            # .margin(right=8, top=8, opacity=0)  # (optional) logo-border padding
            .set_pos(("left", "bottom")))

    final = CompositeVideoClip([final, logo])  # for putting text on the clip

    final = final.set_audio(audio_clip.fx(audio_loop, duration=final.duration))
    final.write_videofile("test_my_videos.mp4",
                          fps=24,
                          # bitrate='1000k',
                          codec='libx264'
                          # preset='ultrafast',
                          # threads=6
                          )


# Create the root window
window = Tk()

# Set window title 
window.title('File Explorer')

# Set window size 
window.geometry("800x400")

# Set window background color
window.config(background="white")

# Create a File Explorer label 
label_file_explorer = Label(window,
                            text="Video Maker",
                            width=50, height=5,
                            fg="blue")

button_video = Button(window,
                      text="select video folder",
                      width=45, height=4,
                      command=browsevideo)
button_audio = Button(window,
                      text="select audio file",
                      width=45, height=4,
                      command=browseaudio)

button_makevideo = Button(window,
                          text='make video',
                          width=45, height=4,
                          # command=threading.Thread(target=make_video).start())
                          command=make_video)

button_exit = Button(window,
                     text="Exit",
                     width=45, height=4,
                     command=exit)

# t = Text()
# t.pack()
# # create instance of file like object
# pl = PrintLogger(t)
# # replace sys.stdout with our object
# sys.stdout = pl
# sys.stderr = pl

# sys.stdout = open('out.log', 'w')
# sys.stderr = sys.stdout

# Grid method is chosen for placing 
# the widgets at respective positions 
# in a table like structure by 
# specifying rows and columns

# label_file_explorer.grid(column=0, row=0)
# label_file_explorer.pack(fill=X)
label_file_explorer.place(relx=0, rely=0)

# button_video.grid(column=0, row=1)
# button_video.pack(fill=X)
button_video.place(relx=0, rely=.205)

# button_audio.grid(column=0, row=2)
# button_audio.pack(fill=X)
button_audio.place(relx=0, rely=.41)

# button_makevideo.grid(column=1, row=1)
# button_makevideo.pack(fill=X)
button_makevideo.place(relx=0, rely=.615)

# button_exit.grid(column=1, row=2)
# button_exit.pack(fill=X)
button_exit.place(relx=0, rely=.820)

# Let the window wait for any events 
window.mainloop()
