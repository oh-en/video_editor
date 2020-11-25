import ffmpeg
import os

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
make_video_txt_file('clips\JEEP')