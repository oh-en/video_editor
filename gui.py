from tkinter import *
import sys
import threading
import os
import ffmpeg
import subprocess
import shutil
import time
from tkinter import filedialog


class PrintLogger():  # this is for adding print statements to tkinter window
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
    global video_path_head
    global video_folder_name

    video_path_head = filedialog.askdirectory()
    video_folder_name = video_path_head.split('/')[-1]

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
    global intro_video_path
    global outro_video_path
    # global video_path
    # global video_folder_name
    global video_path_head

    # first delete all temp files if they exist so you start with a clean slate
    if os.path.exists('video_file_paths.txt'):
        os.remove('video_file_paths.txt')
    if os.path.exists('audio_file_paths.txt'):  # if audio was selected, remove the txt file that was created
        os.remove('audio_file_paths.txt')
    if os.path.exists('audio_concat.mp3'):  # remove the concat file too
        os.remove('audio_concat.mp3')
    if os.path.exists('videos_concat.mp4'):
        os.remove('videos_concat.mp4')  # don't remove the output file, temp solution here for testing
    if os.path.exists('scaled_intro.mp4'):
        os.remove('scaled_intro.mp4')
    if os.path.exists('scaled_outro.mp4'):
        os.remove('scaled_outro.mp4')
    if os.path.exists('temp_videos/'):
        shutil.rmtree('temp_videos/')
    if os.path.exists('good_framerate_intro.mp4'):
        os.remove('good_framerate_intro.mp4')
    if os.path.exists('good_framerate_outro.mp4'):
        os.remove('good_framerate_outro.mp4')
    if os.path.exists('output.mp4'):
        os.remove('output.mp4')
    if os.path.exists('final.mp4'):
        os.remove('final.mp4')

    for video_path in os.listdir(video_path_head):
        video_path = os.path.join(video_path_head, video_path)

        video_folder_name = video_path.split('/')[-1]
        output_path = os.path.abspath(os.path.join(video_path_head, video_folder_name + '.mp4'))

        if resolution.get() == 1:
            print(time.strftime("%H:%M:%S", time.localtime()), ': Converting to 1080p...')
            # converts them to 1080p
            if intro_check.get():
                command = "ffmpeg -i {} -vf scale=1920:1080 scaled_intro.mp4".format(intro_video_path)
                subprocess.call(command, shell=True)
                command = "ffmpeg -i scaled_intro.mp4 -filter:v fps=fps=24 good_framerate_intro.mp4"
                subprocess.call(command, shell=True)
                intro_video_path_scaled = os.path.abspath('good_framerate_intro.mp4')  # updates the intro_video_path

            os.mkdir('temp_videos')
            for i, file in enumerate(sorted(os.listdir(video_path))):
                command = "ffmpeg -i {} -vf scale=1920:1080 temp_videos/vid_{}.mp4".format(
                    os.path.abspath(os.path.join(video_path, file)),
                    i)  # converts every video to the resolution, adds it to temp file
                subprocess.call(command, shell=True)
                command = "ffmpeg -i temp_videos/vid_{}.mp4 -filter:v fps=fps=24 temp_videos/video_{}.mp4".format(i, i)
                subprocess.call(command, shell=True)
                os.remove('temp_videos/vid_{}.mp4'.format(i))
            video_path = os.path.abspath('temp_videos/')  # update the video path to the temp videos
            if outro_check.get():
                command = "ffmpeg -i {} -vf scale=1920:1080 scaled_outro.mp4".format(outro_video_path)
                subprocess.call(command, shell=True)
                command = "ffmpeg -i scaled_outro.mp4 -filter:v fps=fps=24 good_framerate_outro.mp4"
                subprocess.call(command, shell=True)
                outro_video_path_scaled = os.path.abspath('good_framerate_outro.mp4')  # updates the intro_video_path
            print(time.strftime("%H:%M:%S", time.localtime()), ': Videos successfully converted to 1080p')

        if resolution.get() == 2:
            print(time.strftime("%H:%M:%S", time.localtime()), ': Converting to 4k...')
            # converts them to 4k
            if intro_check.get():
                command = "ffmpeg -i {} -vf scale=3840:2160 scaled_intro.mp4".format(intro_video_path)
                subprocess.call(command, shell=True)
                command = "ffmpeg -i scaled_intro.mp4 -filter:v fps=fps=24 good_framerate_intro.mp4"
                subprocess.call(command, shell=True)
                intro_video_path_scaled = os.path.abspath('good_framerate_intro.mp4')  # updates the intro_video_path

            os.mkdir('temp_videos')
            for i, file in enumerate(sorted(os.listdir(video_path))):
                command = "ffmpeg -i {} -vf scale=3840:2160 temp_videos/vid_{}.mp4".format(
                    os.path.abspath(os.path.join(video_path, file)),
                    i)  # converts every video to the resolution, adds it to temp file
                subprocess.call(command, shell=True)
                command = "ffmpeg -i temp_videos/vid_{}.mp4 -filter:v fps=fps=24 temp_videos/video_{}.mp4".format(i, i)
                subprocess.call(command, shell=True)
                os.remove('temp_videos/vid_{}.mp4'.format(i))
            video_path = os.path.abspath('temp_videos/')  # update the video path to the temp videos
            if outro_check.get():
                command = "ffmpeg -i {} -vf scale=3840:2160 scaled_outro.mp4".format(outro_video_path)
                subprocess.call(command, shell=True)
                command = "ffmpeg -i scaled_outro.mp4 -filter:v fps=fps=24 good_framerate_outro.mp4"
                subprocess.call(command, shell=True)
                outro_video_path_scaled = os.path.abspath('good_framerate_outro.mp4')  # updates the intro_video_path
            print(time.strftime("%H:%M:%S", time.localtime()), ': Videos successfully converted to 4k')

        # creates the video file that is read by ffmpeg
        # if there is an intro video that has been selected, write that first, else just write the videos
        print(time.strftime("%H:%M:%S", time.localtime()), ': Collecting videos to merge...')
        if intro_check.get():  # if this box is checked
            with open('video_file_paths.txt', 'w') as f:
                f.write('file ' + "'{}'".format(intro_video_path_scaled) + '\n')
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
                f.write('file ' + "'{}'".format(outro_video_path_scaled) + '\n')

        # takes in a list of video files and combines them together
        print(time.strftime("%H:%M:%S", time.localtime()), ': Merging videos...')
        ffmpeg.input(path_to_videotxt, format='concat', safe=0).output('videos_concat.mp4', c='copy').run(
            overwrite_output=True)
        print(time.strftime("%H:%M:%S", time.localtime()), ': Videos merged successfully')

        # makes the long audio file if one has been selected
        if music_check.get():
            print(time.strftime("%H:%M:%S", time.localtime()), ': Adding audio to merged video...')

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
            print(time.strftime("%H:%M:%S", time.localtime()), ': Audio added successfully')
        else:
            os.rename('videos_concat.mp4', 'output.mp4')

        # final step, add the image then delete all the temp files
        if overlay_check.get():
            print(time.strftime("%H:%M:%S", time.localtime()), ': Adding image overlay...')
            command = """ffmpeg -i output.mp4 -i {} -filter_complex "overlay=0:H-h" -codec:a copy final.mp4""".format(
                path_to_image)
            subprocess.call(command, shell=True)
            os.remove(path_to_videotxt)
            if audio_path:  # if audio was selected, remove the txt file that was created
                os.remove(path_to_audiotxt)
            if os.path.exists('audio_concat.mp3'):  # remove the concat file too
                os.remove('audio_concat.mp3')
            if os.path.exists('videos_concat.mp4'):
                os.remove('videos_concat.mp4')  # don't remove the output file, temp solution here for testing
            if os.path.exists('scaled_intro.mp4'):
                os.remove('scaled_intro.mp4')
            if os.path.exists('scaled_outro.mp4'):
                os.remove('scaled_outro.mp4')
            if os.path.exists('temp_videos/'):
                shutil.rmtree('temp_videos/')
            if os.path.exists('good_framerate_intro.mp4'):
                os.remove('good_framerate_intro.mp4')
            if os.path.exists('good_framerate_outro.mp4'):
                os.remove('good_framerate_outro.mp4')
            os.remove('output.mp4')
            os.rename('final.mp4', output_path)
            print(time.strftime("%H:%M:%S", time.localtime()), ': Image overlay added successfully')
        else:
            os.remove(path_to_videotxt)
            if audio_path:  # if audio was selected, remove the txt file that was created
                os.remove(path_to_audiotxt)
            if os.path.exists('audio_concat.mp3'):
                os.remove('audio_concat.mp3')
            if os.path.exists('videos_concat.mp4'):
                os.remove('videos_concat.mp4')  # don't remove the output file, temp solution here for testing
            if os.path.exists('scaled_intro.mp4'):
                os.remove('scaled_intro.mp4')
            if os.path.exists('scaled_outro.mp4'):
                os.remove('scaled_outro.mp4')
            if os.path.exists('temp_videos/'):
                shutil.rmtree('temp_videos/')
            if os.path.exists('good_framerate_intro.mp4'):
                os.remove('good_framerate_intro.mp4')
            if os.path.exists('good_framerate_outro.mp4'):
                os.remove('good_framerate_outro.mp4')
            os.rename('output.mp4', output_path)

        print(time.strftime("%H:%M:%S", time.localtime()), ': Finished creating video!')
        print('Video located at: ', output_path)
        t.see('end')  # scrolls the text box to the end


def makethevideo():
    quick = threading.Thread(target=compile_video)
    quick.start()


# Create the root window
window = Tk()

# Set window title 
window.title('File Explorer')

# Set window size 
window.geometry("900x800")

# Set window background color
window.config(background="white")

intro_check = IntVar()
music_check = IntVar()
overlay_check = IntVar()
outro_check = IntVar()
video_check = IntVar()  # I'm not sure if I'm going to use this button
# resolution_check = IntVar()

intro_check_state = Checkbutton(window, text="intro", variable=intro_check)
music_check_state = Checkbutton(window, text="audio", variable=music_check)
overlay_check_state = Checkbutton(window, text="overlay", variable=overlay_check)
outro_check_state = Checkbutton(window, text="outro", variable=outro_check)
video_check_state = Checkbutton(window, text="video", variable=video_check)

# Create a File Explorer label 
label_file_explorer = Label(window,
                            text="Automated Video Editor",
                            width=50, height=5,
                            fg="white",
                            bg='dark slate gray',
                            font=(None,10))
video_label = Label(window,
                    text="Select Video",
                    width=50, height=5,
                    bg='slate gray',
                    )
audio_label = Label(window,
                    text="Select Audio",
                    width=50, height=5,
                    bg='slate gray'
                    )
image_label = Label(window,
                    text="Select Image",
                    width=50, height=5,
                    bg='slate gray'
                    )
intro_label = Label(window,
                    text="Select Intro",
                    width=50, height=5,
                    bg='slate gray'
                    )
outro_label = Label(window,
                    text="Select Outro",
                    width=50, height=5,
                    bg='slate gray'
                    )

button_video = Button(window,
                      text="Browse",
                      width=25, height=1,
                      command=browsevideo)
button_introvideo = Button(window,
                           text="Browse",
                           width=25, height=1,
                           command=browse_intro_video)
button_outrovideo = Button(window,
                           text="Browse",
                           width=25, height=1,
                           command=browse_outro_video)
button_audio = Button(window,
                      text="Browse",
                      width=25, height=1,
                      command=browseaudio)
button_image = Button(window,
                      text="Browse",
                      width=25, height=1,
                      command=pick_image)
button_makevideo = Button(window,
                          text='Make Video',
                          width=50, height=5,
                          # command=threading.Thread(target=lambda: compile_video)
                          bg='lawn green',
                          command=makethevideo
                          )
button_test = Button(window,
                     text="test",
                     width=15, height=1,
                     command=lambda: print(intro_check.get())
                     # command = get_state
                     )
button_exit = Button(window,
                     text="Exit",
                     width=50, height=5,
                     bg='firebrick3',
                     command=exit)

resolution = IntVar()
OG = Radiobutton(window,
                 text="Original Resolution (Note: All videos must have the same resolution and frame rate)",
                 padx=20,
                 variable=resolution,
                 value=0,
                 wraplength = 300,
                 bg='lavender')
hd = Radiobutton(window,
                 text="1080p",
                 padx=20,
                 variable=resolution,
                 value=1,
                 bg='lavender')
_4k = Radiobutton(window,
                  text="4k",
                  padx=20,
                  variable=resolution,
                  value=2,
                  bg='lavender')

t = Text(height=45,width=60)
t.place(x=380, y=0)
# create instance of file like object
pl = PrintLogger(t)
# replace sys.stdout with our object
sys.stdout = pl
# sys.stderr = pl

# sys.stdout = open('out.log', 'w')
sys.stderr = sys.stdout

# labels
label_file_explorer.place(relx=0, rely=0)
video_label.place(x=0, y=90)
audio_label.place(x=0, y=180)
image_label.place(x=0, y=270)
intro_label.place(x=0, y=360)
outro_label.place(x=0, y=450)

# buttons
button_video.place(x=350, y=165, anchor=SE)
button_audio.place(x=350, y=165 + 90, anchor=SE)
button_image.place(x=350, y=165 + 90 * 2, anchor=SE)
button_introvideo.place(x=350, y=165 + 90 * 3, anchor=SE)
button_outrovideo.place(x=350, y=165 + 90 * 4, anchor=SE)
button_makevideo.place(x=0, y=165 + 90 * 5)
button_exit.place(x=0, y=165 + 90 * 6)

# checkboxes
intro_check_state.place(x=349, y=165 + 90 * 3 - 28, anchor=SE)
intro_label.lower()
music_check_state.place(x=349, y=165 + 90 - 28, anchor=SE)
audio_label.lower()
overlay_check_state.place(x=349, y=165 + 90 * 2 - 28, anchor=SE)
image_label.lower()
outro_check_state.place(x=349, y=165 + 90 * 4 - 28, anchor=SE)
outro_label.lower()

# radio buttons
hd.place(x=90, y=165 + 90 * 5 - 75)
_4k.place(x=190, y=165 + 90 * 5 - 75)
OG.place(x=0, y=165 + 90 * 5 - 45)

# Let the window wait for any events 
window.mainloop()
