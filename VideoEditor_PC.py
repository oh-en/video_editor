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

path_to_ffmpeg = r"ffmpeg\\bin\\ffmpeg.exe" # for my own use
path_to_probe = r"ffmpeg\\bin\\ffprobe.exe"
#path_to_ffmpeg = r"ffmpeg\\ffmpeg.exe" # for pyinstaller
#path_to_probe = r"ffmpeg\\ffprobe.exe"

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

def get_width(path_to_video):
    # vcap = cv2.VideoCapture(path_to_video)
    #
    # if vcap.isOpened():
    #     width = int(vcap.get(3))
    # return width

    probe = ffmpeg.probe(path_to_video, cmd=path_to_ffmpeg)
    video_streams = [stream for stream in probe['streams'] if stream['codec_type']=='video']
    width = video_streams[0]['width']
    return width


def get_length(filename):
    probe = ffmpeg.probe(filename, cmd=path_to_ffmpeg)
    video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
    time = float(video_streams[0]['duration'])
    return time


def get_state():
    print(resolution.get())

def add_audio(intro_path, video_folder, outro_path, out_video):
    global path_to_ffmpeg
    #start with a clean slate
    if os.path.exists('temp_audio/'):
        shutil.rmtree('temp_audio/')
    if os.path.exists('outro_audio.mp3'):
        os.remove('outro_audio.mp3')
    if os.path.exists('intro_audio.mp3'):
        os.remove('intro_audio.mp3')
    if os.path.exists('video_audio_file_paths.txt'):
        os.remove('video_audio_file_paths.txt')

    # step 1: make the audio files
    if intro_path:
        command = """{} -i "{}" -vn intro_audio.mp3""".format(path_to_ffmpeg, intro_path) # convert to mp3
        subprocess.call(command, shell=True)
        intro_audio_path = 'intro_audio.mp3'
    os.mkdir('temp_audio/')
    for i, file in enumerate(sorted(os.listdir(video_folder))):
        command = """{} -i "{}" -vn temp_audio/audio_{}.mp3""".format(path_to_ffmpeg, os.path.join(video_folder,file),i)  # convert to mp3
        subprocess.call(command, shell=True)
    video_audio_path = 'temp_audio/'
    if outro_path:
        command = """{} -i "{}" -vn outro_audio.mp3""".format(path_to_ffmpeg, outro_path) # convert to mp3
        subprocess.call(command, shell=True)
        outro_audio_path = 'outro_audio.mp3'

    # step2: concat them
    if intro_path:  # if this box is checked
        with open('video_audio_file_paths.txt', 'w') as f:
            f.write('file ' + "'{}'".format(intro_audio_path) + '\n')
            for file in sorted(os.listdir(video_audio_path)):
                f.write('file ' + "'{}'".format(os.path.abspath(os.path.join(video_audio_path, file))) + '\n')
        path_to_videoaudiotxt = os.path.abspath('video_audio_file_paths.txt')
    else:
        with open('video_audio_file_paths.txt', 'w') as f:
            for file in sorted(os.listdir(video_audio_path)):
                f.write('file ' + "'{}'".format(os.path.abspath(os.path.join(video_audio_path, file))) + '\n')
        path_to_videoaudiotxt = os.path.abspath('video_audio_file_paths.txt')
    # if an outro video has been selected, add it to the end of the .txt file
    if outro_path:
        with open('video_audio_file_paths.txt', 'a') as f:
            f.write('file ' + "'{}'".format(outro_audio_path) + '\n')

    command = """{} -f concat -safe 0 -i video_audio_file_paths.txt -c copy output.mp3""".format(path_to_ffmpeg)
    subprocess.call(command, shell=True)
    if os.path.exists('temp_audio/'):
        shutil.rmtree('temp_audio/')
    if os.path.exists('outro_audio.mp3'):
        os.remove('outro_audio.mp3')
    if os.path.exists('intro_audio.mp3'):
        os.remove('intro_audio.mp3')

    # step3: add audio to the file
    command = """{} -i {} -i output.mp3 -c copy -map 0:v:0 -map 1:a:0 video_audio.mp4""".format(path_to_ffmpeg,out_video)
    subprocess.call(command, shell=True)
    os.remove('output.mp3')
    os.remove('video_audio_file_paths.txt')


def compile_video():
    global intro_video_path
    global outro_video_path
    # global video_path
    # global video_folder_name
    global video_path_head
    global path_to_image

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
    if os.path.exists('overlay_vids/'):
        shutil.rmtree('overlay_vids/')
    if os.path.exists('good_framerate_intro.mp4'):
        os.remove('good_framerate_intro.mp4')
    if os.path.exists('good_framerate_outro.mp4'):
        os.remove('good_framerate_outro.mp4')
    if os.path.exists('output.mp4'):
        os.remove('output.mp4')
    if os.path.exists('final.mp4'):
        os.remove('final.mp4')
    if os.path.exists('scaled.png'):
        os.remove('scaled.png')

    for video_path in os.listdir(video_path_head):
        video_path = os.path.join(video_path_head, video_path)
        video_folder_name = video_path.split('\\')[-1]
        og_video_path = video_path

        if os.path.isdir(video_path) and video_folder_name[0] != '.':

            output_path = os.path.abspath(os.path.join(video_path_head, video_folder_name + '.mp4'))

            if resolution.get() == 1:
                print(time.strftime("%H:%M:%S", time.localtime()), ': Converting to 1080p...')
                # converts them to 1080p
                if intro_check.get():
                    command = """{} -i "{}" -vf scale=1920:1080 -r 24 -c:v libx264 good_framerate_intro.mp4""".format(
                        path_to_ffmpeg, intro_video_path)
                    subprocess.call(command, shell=True)
                    intro_video_path_scaled = os.path.abspath('good_framerate_intro.mp4')  # updates the intro_video_path

                os.mkdir('temp_videos')
                for i, file in enumerate(sorted(os.listdir(video_path))):
                    if os.path.isdir(video_path) and video_folder_name[0] != '.' and file[0]!= '.':
                        if overlay_check.get():
                            width = 1920
                            command = """{} -i "{}" -y -v quiet -vf scale={}:-1 scaled.png""".format(path_to_ffmpeg,
                                                                                                     path_to_image,
                                                                                                     width)

                            subprocess.call(command, shell=True)
                            command = """{} -i "{}" -filter_complex "movie="scaled.png"[image],[0:v]scale=1920:1080[scaled],[scaled][image]overlay=0:H-h[out]" -r 24 -vcodec libx264 -map [out] temp_videos/video_{}.mp4""".format(
                                path_to_ffmpeg, os.path.abspath(os.path.join(video_path, file)), i)
                            subprocess.call(command, shell=True)
                        else:
                            command = """{} -i "{}" -vf scale=1920:1080 -r 24 -c:v libx264 temp_videos/video_{}.mp4""".format(
                                path_to_ffmpeg, os.path.abspath(os.path.join(video_path, file)), i)
                            subprocess.call(command, shell=True)
                        if os.path.exists('scaled.png'):
                            os.remove('scaled.png')
                video_path = os.path.abspath('temp_videos/')  # update the video path to the temp videos
                if outro_check.get():
                    command = """{} -i "{}" -vf scale=1920:1080 -r 24 -c:v libx264 good_framerate_outro.mp4""".format(
                        path_to_ffmpeg, outro_video_path)
                    subprocess.call(command, shell=True)
                    outro_video_path_scaled = os.path.abspath('good_framerate_outro.mp4')  # updates the intro_video_path
                print(time.strftime("%H:%M:%S", time.localtime()), ': Videos successfully converted to 1080p')

            if resolution.get() == 2:
                print(time.strftime("%H:%M:%S", time.localtime()), ': Converting to 4k...')
                # converts them to 4k
                if intro_check.get():
                    command = """{} -i "{}" -vf scale=3840:2160 -r 24 -c:v libx264 good_framerate_intro.mp4""".format(
                        path_to_ffmpeg, intro_video_path)
                    subprocess.call(command, shell=True)
                    intro_video_path_scaled = os.path.abspath('good_framerate_intro.mp4')  # updates the intro_video_path

                os.mkdir('temp_videos')
                for i, file in enumerate(sorted(os.listdir(video_path))):
                    if os.path.isdir(video_path) and video_folder_name[0] != '.' and file[0]!= '.':
                        if overlay_check.get():
                            width = 3840
                            command = """{} -i "{}" -y -v quiet -vf scale={}:-1 scaled.png""".format(path_to_ffmpeg,
                                                                                                     path_to_image,
                                                                                                     width)

                            subprocess.call(command, shell=True)
                            command = """{} -i "{}" -filter_complex "movie="scaled.png"[image],[0:v]scale=3840:2160[scaled],[scaled][image]overlay=0:H-h[out]" -r 24 -vcodec libx264 -map [out] temp_videos/video_{}.mp4""".format(
                                path_to_ffmpeg, os.path.abspath(os.path.join(video_path, file)), i)
                            subprocess.call(command, shell=True)
                        else:
                            command = """{} -i "{}" -vf scale=3840:2160 -r 24 -c:v libx264 temp_videos/video_{}.mp4""".format(
                                path_to_ffmpeg, os.path.abspath(os.path.join(video_path, file)), i)
                            subprocess.call(command, shell=True)
                video_path = os.path.abspath('temp_videos/')  # update the video path to the temp videos
                if outro_check.get():
                    command = """{} -i "{}" -vf scale=3840:2160 -r 24 -c:v libx264 good_framerate_outro.mp4""".format(
                        path_to_ffmpeg, outro_video_path)
                    subprocess.call(command, shell=True)
                    outro_video_path_scaled = os.path.abspath('good_framerate_outro.mp4')  # updates the intro_video_path
                print(time.strftime("%H:%M:%S", time.localtime()), ': Videos successfully converted to 4k')

            if resolution.get() == 0:
                if intro_check.get():
                    intro_video_path_scaled = intro_video_path
                if outro_check.get():
                    outro_video_path_scaled = outro_video_path

            # creates the video file that is read by ffmpeg
            # if there is an intro video that has been selected, write that first, else just write the videos
            print(time.strftime("%H:%M:%S", time.localtime()), ': Collecting videos to merge...')
            if intro_check.get():  # if this box is checked
                with open('video_file_paths.txt', 'w') as f:
                    f.write('file ' + "'{}'".format(intro_video_path_scaled) + '\n')
                    for file in sorted(os.listdir(video_path)):
                        if os.path.isdir(video_path) and video_folder_name[0] != '.' and file[0]!= '.':
                            f.write('file ' + "'{}'".format(os.path.abspath(os.path.join(video_path, file))) + '\n')
                path_to_videotxt = os.path.abspath('video_file_paths.txt')
            else:
                with open('video_file_paths.txt', 'w') as f:
                    for file in sorted(os.listdir(video_path)):  # sorted list here
                        if os.path.isdir(video_path) and video_folder_name[0] != '.' and file[0]!= '.':
                            f.write('file ' + "'{}'".format(os.path.abspath(os.path.join(video_path, file))) + '\n')
                path_to_videotxt = os.path.abspath('video_file_paths.txt')
            # if an outro video has been selected, add it to the end of the .txt file
            if outro_check.get():
                with open('video_file_paths.txt', 'a') as f:
                    f.write('file ' + "'{}'".format(outro_video_path_scaled) + '\n')

            # takes in a list of video files and combines them together
            print(time.strftime("%H:%M:%S", time.localtime()), ': Merging videos...')
            # ffmpeg.input(path_to_videotxt, format='concat', safe=0).output('videos_concat.mp4', c='copy').run(cmd=path_to_ffmpeg,
            #     overwrite_output=True)
            command = """{} -f concat -safe 0 -i "{}" -c copy videos_concat.mp4""".format(path_to_ffmpeg, path_to_videotxt)
            subprocess.call(command, shell=True)

            add_audio(intro_video_path, og_video_path, outro_video_path, 'videos_concat.mp4')
            os.remove('videos_concat.mp4')

            print(time.strftime("%H:%M:%S", time.localtime()), ': Videos merged successfully')

            # makes the long audio file if one has been selected
            if music_check.get():
                print(time.strftime("%H:%M:%S", time.localtime()), ': Adding audio to merged video...')

                # creates the audio file that is read by ffmpeg
                with open('audio_file_paths.txt', 'w') as f:
                    for i in range(20):  # repeat the same song 20 times so that it's definitely longer than the video
                        f.write('file ' + "'{}'".format(os.path.abspath(audio_path)) + '\n')
                path_to_audiotxt = os.path.abspath('audio_file_paths.txt')

                ffmpeg.input(path_to_audiotxt, format='concat', safe=0).output('audio_concat.mp3', c='copy').run(cmd=path_to_ffmpeg,
                    overwrite_output=True)

                # takes created concatenated video and adds in the long audio file command = "ffmpeg -i
                # videos_concat.mp4 -i audio_concat.mp3 -map 0:v -map 1:a -c:v copy -shortest output.mp4"
                command = """{} -i video_audio.mp4 -i audio_concat.mp3 -filter_complex "[1:a]volume=0.25,apad[A];[0:a][A]amerge[out]" -c:v copy -map 0:v -map [out] -y -shortest output.mp4""".format(path_to_ffmpeg)
                subprocess.call(command, shell=True)
                print(time.strftime("%H:%M:%S", time.localtime()), ': Audio added successfully')
                if os.path.exists('video_audio.mp4'):
                    os.remove('video_audio.mp4') # this file is not needed anymore
            else:
                os.rename('video_audio.mp4', 'output.mp4')


            # final step, add the image then delete all the temp files
            # if overlay_check.get():
            #     width = get_width('output.mp4')
            #     if intro_check.get():
            #         intro_time = get_length(intro_video_path)
            #     else:
            #         intro_time = 0
            #     if outro_check.get():
            #         outro_time = get_length(outro_video_path)
            #     else:
            #         outro_time = 0
            #     video_time = get_length('output.mp4')
            #     print(time.strftime("%H:%M:%S", time.localtime()), ': Adding image overlay...')
            #     command = """{} -i "{}" -y -v quiet -vf scale={}:-1 scaled.png""".format(path_to_ffmpeg,
            #         path_to_image, width)
            #     subprocess.call(command, shell=True)
            #     command = """{} -i output.mp4 -i scaled.png -filter_complex "overlay=0:H-h:enable='between(t,{},{})'" -codec:a copy final.mp4""".format(path_to_ffmpeg, intro_time,video_time-outro_time)
            #     subprocess.call(command, shell=True)
            #     os.remove(path_to_videotxt)
            #     os.remove('scaled.png')
            #     if audio_path:  # if audio was selected, remove the txt file that was created
            #         os.remove(path_to_audiotxt)
            #     if os.path.exists('audio_concat.mp3'):  # remove the concat file too
            #         os.remove('audio_concat.mp3')
            #     if os.path.exists('videos_concat.mp4'):
            #         os.remove('videos_concat.mp4')  # don't remove the output file, temp solution here for testing
            #     if os.path.exists('scaled_intro.mp4'):
            #         os.remove('scaled_intro.mp4')
            #     if os.path.exists('scaled_outro.mp4'):
            #         os.remove('scaled_outro.mp4')
            #     if os.path.exists('temp_videos/'):
            #         shutil.rmtree('temp_videos/')
            #     if os.path.exists('good_framerate_intro.mp4'):
            #         os.remove('good_framerate_intro.mp4')
            #     if os.path.exists('good_framerate_outro.mp4'):
            #         os.remove('good_framerate_outro.mp4')
            #     os.remove('output.mp4')
            #     os.rename('final.mp4', output_path)
            #     print(time.strftime("%H:%M:%S", time.localtime()), ': Image overlay added successfully')
            # else:
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
            if os.path.exists('overlay_vids/'):
                shutil.rmtree('overlay_vids/')
            if os.path.exists('good_framerate_intro.mp4'):
                os.remove('good_framerate_intro.mp4')
            if os.path.exists('good_framerate_outro.mp4'):
                os.remove('good_framerate_outro.mp4')
            if os.path.exists('converted_outro.mp4'):
                os.remove('converted_outro.mp4')
            if os.path.exists('converted_intro.mp4'):
                os.remove('converted_intro.mp4')
            os.rename('output.mp4', output_path)

            print(time.strftime("%H:%M:%S", time.localtime()), ': Finished creating video!')
            print('Video located at: ', output_path)
            t.see('end')  # scrolls the text box to the end
        else:
            pass


def makethevideo():
    quick = threading.Thread(target=compile_video)
    quick.start()


# Create the root window
window = Tk()

# Set window title 
window.title('File Explorer')

# Set window size 
window.geometry("900x770")

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
                     command=lambda: sys.exit())

resolution = IntVar()
# OG = Radiobutton(window,
#                  text="Original Resolution (Note: All videos must have the same resolution and frame rate)",
#                  padx=20,
#                  variable=resolution,
#                  value=0,
#                  wraplength = 300,
#                  bg='lavender')
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
button_makevideo.place(x=0, y=125 + 90 * 5)
button_exit.place(x=0, y=125 + 90 * 6)

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
# OG.place(x=0, y=165 + 90 * 5 - 45)

# Let the window wait for any events 
window.mainloop()
