# Python program to create 
# a file explorer in Tkinter 

# import all components 
# from the tkinter library 
from tkinter import *
import sys
import threading
import os
import ffmpeg
import subprocess

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
    global video_path

    video_path = filedialog.askdirectory()
    video_folder_name = video_path.split('/')[-1]

    button_video.configure(text="Folder Opened: " + video_folder_name)


def browse_intro_video():
    global intro_video_path

    intro_video_path = filedialog.askopenfilename()
    intro_video_file_name = intro_video_path.split('/')[-1]

    button_introvideo.configure(text="File Opened: " + intro_video_file_name)


def browse_outro_video():
    global outro_video_path

    outro_video_path = filedialog.askopenfilename()
    outro_video_file_name = outro_video_path.split('/')[-1]

    button_outrovideo.configure(text="File Opened: " + outro_video_file_name)


def browseaudio():
    global audio_path

    audio_path = filedialog.askopenfilename()
    audio_folder_name = audio_path.split('/')[-1]

    # Change label contents
    button_audio.configure(text="File Opened: " + audio_folder_name)


def pick_image():
    global path_to_image

    image_path = filedialog.askopenfilename()
    image_folder_name = image_path.split('/')[-1]

    # Change label contents
    button_image.configure(text="File Opened: " + image_folder_name)

    path_to_image = os.path.abspath(image_path)

def get_state():
    print(resolution.get())


def compile_video():
    # creates the video file that is read by ffmpeg
    # if there is an intro video that has been selected, write that first, else just write the videos
    if intro_video_path:
        with open('video_file_paths.txt', 'w') as f:
            f.write('file ' + "'{}'".format(intro_video_path) + '\n')
            for file in os.listdir(video_path):
                f.write('file ' + "'{}'".format(os.path.abspath(os.path.join(video_path, file))) + '\n')
        path_to_videotxt = os.path.abspath('video_file_paths.txt')
    else:
        with open('video_file_paths.txt', 'w') as f:
            for file in os.listdir(video_path):
                f.write('file ' + "'{}'".format(os.path.abspath(os.path.join(video_path, file))) + '\n')
        path_to_videotxt = os.path.abspath('video_file_paths.txt')
    # if an outro video has been selected, add it to the end of the .txt file
    if outro_video_path:
        with open('video_file_paths.txt', 'a') as f:
            f.write('file ' + "'{}'".format(outro_video_path) + '\n')

    # creates the audio file that is read by ffmpeg
    with open('audio_file_paths.txt', 'w') as f:
        for i in range(20):  # repeat the same song 20 times so that it's definitely longer than the video
            f.write('file ' + "'{}'".format(os.path.abspath(audio_path)) + '\n')
    path_to_audiotxt = os.path.abspath('audio_file_paths.txt')

    # takes in a list of video files on combines them together
    ffmpeg.input(path_to_videotxt, format='concat', safe=0).output('videos_concat.mp4', c='copy').run(
        overwrite_output=True)

    # makes the long audio file
    ffmpeg.input(path_to_audiotxt, format='concat', safe=0).output('audio_concat.mp3', c='copy').run(
        overwrite_output=True)

    # converts them to 1080p, 10min for 1080p. 30min for 5k
    # command = "ffmpeg -i videos_concat.mp4 -vf scale=1920:1080 scaled.mp4"
    # subprocess.call(command, shell=True)

    # takes created concatenated video and adds in the long audio file
    command = "ffmpeg -i videos_concat.mp4 -i audio_concat.mp3 -map 0:v -map 1:a -c:v copy -shortest output.mp4"
    subprocess.call(command, shell=True)

    # command = "ffmpeg -i output.mp4 -i 1.png -filter_complex "[0:v][1:v] overlay=0:H-h:enable='between(t,0,20)'" -pix_fmt yuv420p -c:a copy final.mp4"
    command = """ffmpeg -i output.mp4 -i {} -filter_complex "overlay=0:H-h" -codec:a copy final.mp4""".format(
        path_to_image)
    subprocess.call(command, shell=True)

    os.remove(path_to_videotxt)
    os.remove(path_to_audiotxt)
    os.remove('audio_concat.mp3')
    os.remove('videos_concat.mp4')
    os.remove('output.mp4')


# Create the root window
window = Tk()

# Set window title 
window.title('File Explorer')

# Set window size 
window.geometry("800x400")

# Set window background color
window.config(background="white")

intro_check = IntVar()
music_check = IntVar()
overlay_check = IntVar()
outro_check = IntVar()
video_check = IntVar()
#resolution_check = IntVar()

intro_check_state = Checkbutton(window, text="intro", variable=intro_check)
music_check_state = Checkbutton(window, text="music", variable=music_check)
overlay_check_state = Checkbutton(window, text="overlay", variable=overlay_check)
outro_check_state = Checkbutton(window, text="outro", variable=outro_check)
video_check_state = Checkbutton(window, text="video", variable=video_check)

# Create a File Explorer label 
label_file_explorer = Label(window,
                            text="Video Maker",
                            width=50, height=5,
                            fg="blue")

button_video = Button(window,
                      text="select video folder",
                      width=45, height=4,
                      command=browsevideo)
button_introvideo = Button(window,
                      text="select intro video file",
                      width=45, height=4,
                      command=browse_intro_video)
button_outrovideo = Button(window,
                      text="select outro video file",
                      width=45, height=4,
                      command=browse_outro_video)
button_audio = Button(window,
                      text="select audio file",
                      width=45, height=4,
                      command=browseaudio)
button_image = Button(window,
                      text="select overlay image",
                      width=45, height=4,
                      command=pick_image)

button_makevideo = Button(window,
                          text='make video',
                          width=45, height=4,
                          # command=threading.Thread(target=compile_video)
                          command=compile_video
                          )

button_test = Button(window,
                      text="test",
                      width=45, height=4,
                      command=lambda: print(intro_check.get())
                      #command = get_state
                      )

button_exit = Button(window,
                     text="Exit",
                     width=45, height=4,
                     command=exit)

resolution = IntVar()
hd = Radiobutton(window,
              text="1080p",
              padx = 20,
              variable=resolution,
              value=1)
_4k = Radiobutton(window,
              text="4k",
              padx = 20,
              variable=resolution,
              value=2)

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

label_file_explorer.grid(column=0, row=0)
# label_file_explorer.pack(fill=X)
#label_file_explorer.place(relx=0, rely=0)

button_video.grid(column=0, row=1)
# button_video.pack(fill=X)
#button_video.place(relx=0, rely=.205)

button_audio.grid(column=0, row=2)
# button_audio.pack(fill=X)
#button_audio.place(relx=0, rely=.41)

button_image.grid(column=0, row=3)
button_introvideo.grid(column=0, row=4)
button_outrovideo.grid(column=0, row=5)


button_makevideo.grid(column=0, row=6)
# button_makevideo.pack(fill=X)
#button_makevideo.place(relx=0, rely=.615)

button_exit.grid(column=0, row=7)
# button_exit.pack(fill=X)
#button_exit.place(relx=0, rely=.820)

intro_check_state.grid(column=0,row=8)
music_check_state.grid(column=0,row=9)
overlay_check_state.grid(column=0,row=10)
outro_check_state.grid(column=0,row=11)
video_check_state.grid(column=0,row=12)
hd.grid(column=0,row=13)
_4k.grid(column=1,row=13)
button_test.grid(column=0, row=14)

# Let the window wait for any events 
window.mainloop()
