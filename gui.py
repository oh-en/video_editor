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
import cv2

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


intro_video_path = None  # i think this defines the default state incase intro_video isn't selected
outro_video_path = None  # same thing, should get redefined if button pressed
path_to_image = None
audio_path = None


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

    # first check the resolution, find min h and w. scale to this minimum?
    # maybe i should just follow the radio buttons exactly instead and avoid checks, og 1080p and 4k

    # min_h = 1e6
    # min_w = 1e6

    # if intro_check.get():
    #
    #     vid = cv2.VideoCapture(intro_video_path)
    #     if vid.get(cv2.CAP_PROP_FRAME_HEIGHT) < min_h:
    #         min_h = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #     if vid.get(cv2.CAP_PROP_FRAME_WIDTH) < min_w:
    #         min_w = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    #
    # for file in os.listdir(video_path):
    #     vid = cv2.VideoCapture(file)
    #     if vid.get(cv2.CAP_PROP_FRAME_HEIGHT) < min_h:
    #         min_h = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #     if vid.get(cv2.CAP_PROP_FRAME_WIDTH) < min_w:
    #         min_w = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    #
    # if outro_check.get():
    #
    #     vid = cv2.VideoCapture(outro_video_path)
    #     if vid.get(cv2.CAP_PROP_FRAME_HEIGHT) < min_h:
    #         min_h = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #     if vid.get(cv2.CAP_PROP_FRAME_WIDTH) < min_w:
    #         min_w = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    global intro_video_path
    global outro_video_path
    global video_path

    if resolution.get() == 1:
        # converts them to 1080p
        if intro_check.get():
            command = "ffmpeg -i {} -vf scale=1920:1080 scaled_intro.mp4".format(intro_video_path)
            intro_video_path = 'scaled_intro.mp4' # updates the intro_video_path
            subprocess.call(command, shell=True)
        os.mkdir('temp_videos')
        for i, file in enumerate(sorted(os.listdir(video_path))):
            command = "ffmpeg -i {} -vf scale=1920:1080 temp_videos/vid_{}.mp4".format(os.path.abspath(os.path.join(video_path, file)), i) # converts every video to the resolution, adds it to temp file
            subprocess.call(command, shell=True)
        video_path = os.path.abspath('temp_videos/') # update the video path to the temp videos
        if outro_check.get():
            command = "ffmpeg -i {} -vf scale=1920:1080 scaled_outro.mp4".format(outro_video_path)
            outro_video_path = 'scaled_outro.mp4'  # updates the intro_video_path
            subprocess.call(command, shell=True)

    if resolution.get() == 2:
        # converts them to 4k
        command = "ffmpeg -i videos_concat.mp4 -vf scale=3840:2160 scaled.mp4"
        subprocess.call(command, shell=True)


    # creates the video file that is read by ffmpeg
    # if there is an intro video that has been selected, write that first, else just write the videos
    if intro_check.get(): # if this box is checked
        with open('video_file_paths.txt', 'w') as f:
            f.write('file ' + "'{}'".format(intro_video_path) + '\n')
            for file in sorted(os.listdir(video_path)):
                f.write('file ' + "'{}'".format(os.path.abspath(os.path.join(video_path, file))) + '\n')
        path_to_videotxt = os.path.abspath('video_file_paths.txt')
    else:
        with open('video_file_paths.txt', 'w') as f:
            for file in sorted(os.listdir(video_path)):  # sorted list here
                f.write('file ' + "'{}'".format(os.path.abspath(os.path.join(video_path, file))) + '\n')
        path_to_videotxt = os.path.abspath('video_file_paths.txt')
    # if an outro video has been selected, add it to the end of the .txt file
    if outro_check.get():
        with open('video_file_paths.txt', 'a') as f:
            f.write('file ' + "'{}'".format(outro_video_path) + '\n')

    # takes in a list of video files on combines them together
    print('Merging Videos')
    ffmpeg.input(path_to_videotxt, format='concat', safe=0).output('videos_concat.mp4', c='copy').run(
        overwrite_output=True)
    print('Videos Merged Successfully')

    # makes the long audio file if one has been selected
    if music_check.get():
        print('Adding Audio Track')

        # creates the audio file that is read by ffmpeg
        with open('audio_file_paths.txt', 'w') as f:
            for i in range(20):  # repeat the same song 20 times so that it's definitely longer than the video
                f.write('file ' + "'{}'".format(os.path.abspath(audio_path)) + '\n')
        path_to_audiotxt = os.path.abspath('audio_file_paths.txt')

        ffmpeg.input(path_to_audiotxt, format='concat', safe=0).output('audio_concat.mp3', c='copy').run(
            overwrite_output=True)

        # takes created concatenated video and adds in the long audio file
        command = "ffmpeg -i videos_concat.mp4 -i audio_concat.mp3 -map 0:v -map 1:a -c:v copy -shortest output.mp4"
        subprocess.call(command, shell=True)
        print('Audio Added')
    else:
        os.rename('videos_concat.mp4', 'output.mp4')

    # final step, add the image then delete all the temp files
    # command = "ffmpeg -i output.mp4 -i 1.png -filter_complex "[0:v][1:v] overlay=0:H-h:enable='between(t,0,20)'" -pix_fmt yuv420p -c:a copy final.mp4"
    if overlay_check.get():
        print('Adding Image Overlay...')
        command = """ffmpeg -i output.mp4 -i {} -filter_complex "overlay=0:H-h" -codec:a copy final.mp4""".format(
            path_to_image)
        subprocess.call(command, shell=True)
        os.remove(path_to_videotxt)
        if audio_path: # if audio was selected, remove the txt file that was created
            os.remove(path_to_audiotxt)
        if os.path.exists('audio_concat.mp3'): # remove the concat file too
            os.remove('audio_concat.mp3')
        if os.path.exists('videos_concat.mp4'):
            os.remove('videos_concat.mp4')  # don't remove the output file, temp solution here for testing
        os.remove('output.mp4')
        print('Image Overlay added successfully!')
    else:
        os.remove(path_to_videotxt)
        if audio_path: # if audio was selected, remove the txt file that was created
            os.remove(path_to_audiotxt)
        if os.path.exists('audio_concat.mp3'):
            os.remove('audio_concat.mp3')
        if os.path.exists('videos_concat.mp4'):
            os.remove('videos_concat.mp4')  # don't remove the output file, temp solution here for testing

    print('Finished Creating Final Video')


# Create the root window
window = Tk()

# Set window title 
window.title('File Explorer')

# Set window size 
window.geometry("750x600")

# Set window background color
window.config(background="white")

intro_check = IntVar()
music_check = IntVar()
overlay_check = IntVar()
outro_check = IntVar()
video_check = IntVar() # I'm not sure if I'm going to use this button
# resolution_check = IntVar()

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
video_label = Label(window,
                            text="Select Video",
                            width=50, height=5,
                            #fg="blue"
                    )
audio_label = Label(window,
                            text="Select Audio",
                            width=50, height=5,
                            #fg="blue"
                    )
image_label = Label(window,
                            text="Select Image",
                            width=50, height=5,
                            #fg="blue"
                    )
intro_label = Label(window,
                            text="Select Intro",
                            width=50, height=5,
                            #fg="blue"
                    )
outro_label = Label(window,
                            text="Select Outro",
                            width=50, height=5,
                            #fg="blue"
                    )

button_video = Button(window,
                      text="Browse",
                      width=15, height=1,
                      command=browsevideo)
button_introvideo = Button(window,
                           text="select intro video file",
                           width=15, height=1,
                           command=browse_intro_video)
button_outrovideo = Button(window,
                           text="select outro video file",
                           width=15, height=1,
                           command=browse_outro_video)
button_audio = Button(window,
                      text="select audio file",
                      width=15, height=1,
                      command=browseaudio)
button_image = Button(window,
                      text="select overlay image",
                      width=15, height=1,
                      command=pick_image)

button_makevideo = Button(window,
                          text='make video',
                          width=50, height=10,
                          # command=threading.Thread(target=compile_video)
                          command=compile_video
                          )

button_test = Button(window,
                     text="test",
                     width=15, height=1,
                     command=lambda: print(intro_check.get())
                     # command = get_state
                     )

button_exit = Button(window,
                     text="Exit",
                     width=50, height=15,
                     command=exit)

resolution = IntVar()
OG = Radiobutton(window,
                 text="Original Resolution (Note: All videos must have the same resolution)",
                 padx=20,
                 variable=resolution,
                 value=0)
hd = Radiobutton(window,
                 text="1080p",
                 padx=20,
                 variable=resolution,
                 value=1)
_4k = Radiobutton(window,
                  text="4k",
                  padx=20,
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

#label_file_explorer.grid(column=0, row=0)
# label_file_explorer.pack(fill=X)
label_file_explorer.place(relx=0, rely=0)
video_label.place(x=0,y=90)
audio_label.place(x=0, y=180)
image_label.place(x=0, y=270)
intro_label.place(x=0, y=360)
outro_label.place(x=0, y=450)

#button_video.grid(column=0, row=1)
# button_video.pack(fill=X)
button_video.place(x=350, y=165, anchor=SE)
button_audio.place(x=350, y=165+90, anchor=SE)
button_image.place(x=350, y=165+90*2, anchor=SE)
button_introvideo.place(x=350, y=165+90*3, anchor=SE)
button_outrovideo.place(x=350, y=165+90*4, anchor=SE)
# button_audio.pack(fill=X)
# button_audio.place(relx=0, rely=.41)



button_makevideo.place(x=360, y=0)
button_exit.place(x=360, y=180)
# button_makevideo.pack(fill=X)
# button_makevideo.place(relx=0, rely=.615)


# button_exit.pack(fill=X)
# button_exit.place(relx=0, rely=.820)

intro_check_state.place(x=350, y=165+90*3-25, anchor=SE)
intro_label.lower()
music_check_state.place(x=350, y=165+90-25, anchor=SE)
audio_label.lower()

overlay_check_state.place(x=350, y=165+90*2-25, anchor=SE)
image_label.lower()

outro_check_state.place(x=350, y=165+90*4-25, anchor=SE)
outro_label.lower()

#video_check_state.place(x=800,y=0)


hd.place(x=90, y=165+90*5-75)
_4k.place(x=190, y=165+90*5-75)
OG.place(x=0, y=165+90*5-45)
#button_test.grid(column=0, row=14)

# Let the window wait for any events 
window.mainloop()
