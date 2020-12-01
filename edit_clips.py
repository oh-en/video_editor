import ffmpeg
import os
import subprocess

# in_file1 = ffmpeg.input('clips/my_gopro/GOPR3879.MP4')
# in_file2 = ffmpeg.input('clips/my_gopro/GOPR3880.MP4')
# overlay_file = ffmpeg.input('1.png')
# (
#     ffmpeg
#     .concat(
#         in_file1,
#         in_file2,
#     )
#     .overlay(overlay_file)
#     .output('out.mp4')
#     .run()
# )

# video_path = 'clips\JEEP'
# audio_path = 'audio\11175751_corporate-feel-good-ambient-background_by_bluefoxmusic_preview.mp3'

def make_video_txt_file(video_path):
    # takes in a folder and creates a .txt file ready to be concat by ffmpeg
    with open('video_file_paths.txt', 'w') as f:
        for file in os.listdir(video_path):
            f.write('file ' + "'{}'".format(os.path.abspath(os.path.join(video_path, file)))+ '\n')

def make_audio_txt_file(audio_path):
    # takes in an audio file and creates a .txt of the same thing repeated to be concat by ffmpeg
    with open('audio_file_paths.txt', 'w') as f:
        for i in range(20): # repeat the same song 20 times so that it's definitely longer than the video
            f.write('file ' + "'{}'".format(os.path.abspath(audio_path)) + '\n')

#make_audio_txt_file('audio\11175751_corporate-feel-good-ambient-background_by_bluefoxmusic_preview.mp3')
#make_video_txt_file('clips\JEEP')

# video = ffmpeg.input('clips/my_gopro/GOPR3879.MP4')
# video = ffmpeg.filter(video,'scale', width=1920, height=1080)
# video = ffmpeg.filter(video,'fps',fps=24,round='up')
# video = ffmpeg.output(video, 'scaled_outro.mp4', c='copy')
# video = ffmpeg.run(video)

command = "ffmpeg -i clips/my_gopro/GOPR3879.MP4 -vf scale=1920:1080 scaled_intro.mp4"
subprocess.call(command, shell=True)

command = "ffmpeg -i scaled_intro.mp4 -filter:v fps=fps=24 good_framerate.mp4"
subprocess.call(command, shell=True)