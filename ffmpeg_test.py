import ffmpeg
import subprocess
import os


def make_video_txt_file(video_path):

    global path_to_videotxt
    # takes in a folder and creates a .txt file ready to be concat by ffmpeg
    with open('video_file_paths.txt', 'w') as f:
        for file in os.listdir(video_path):
            f.write('file ' + "'{}'".format(os.path.abspath(os.path.join(video_path, file)))+ '\n')

    path_to_videotxt = os.path.abspath('video_file_paths.txt')

def make_audio_txt_file(audio_path):

    global path_to_audiotxt
    # takes in an audio file and creates a .txt of the same thing repeated to be concat by ffmpeg
    with open('audio_file_paths.txt', 'w') as f:
        for i in range(20): # repeat the same song 20 times so that it's definitely longer than the video
            f.write('file ' + "'{}'".format(os.path.abspath(audio_path)) + '\n')

    path_to_audiotxt = os.path.abspath('audio_file_paths.txt')

def compile_video():

    #takes in a list of video files on combines them together
    ffmpeg.input(path_to_videotxt, format='concat', safe=0).output('videos_concat.mp4', c='copy').run(overwrite_output=True)

    # makes the long audio file
    ffmpeg.input(path_to_audiotxt, format='concat', safe=0).output('audio_concat.mp3', c='copy').run(overwrite_output=True)

    # converts them to 1080p, 10min for 1080p. 30min for 5k
    command = "ffmpeg -i videos_concat.mp4 -vf scale=1920:1080 scaled.mp4"
    subprocess.call(command, shell=True)

    # takes created concatenated video and adds in the long audio file
    command = "ffmpeg -i scaled.mp4 -i audio_concat.mp3 -map 0:v -map 1:a -c:v copy -shortest output.mp4"
    subprocess.call(command, shell=True)

    #command = "ffmpeg -i output.mp4 -i 1.png -filter_complex "[0:v][1:v] overlay=0:H-h:enable='between(t,0,20)'" -pix_fmt yuv420p -c:a copy final.mp4"
    command = """ffmpeg -i output.mp4 -i 1.png -filter_complex "overlay=0:H-h" -codec:a copy final.mp4"""
    subprocess.call(command, shell=True)


video_path = 'clips\JEEP'
audio_path = 'audio/11175751_corporate-feel-good-ambient-background_by_bluefoxmusic_preview.mp3'

make_video_txt_file(video_path)
make_audio_txt_file(audio_path)

compile_video()


# now delete the audio file

# input_video = ffmpeg.input('videos_concat.mp4')
# input_audio = ffmpeg.input('audio_concat.mp3')
#
# ffmpeg.concat(input_video, input_audio, v=1, a=1).output('finished_video.mp4').run()
# print('this has been completed')

# looks at txt file to create long audio file
#"ffmpeg -f concat -safe 0 -i audio.txt -c copy audio_concat.mp3"






#video = ffmpeg.input("ffmpeg_test.mp4")
#audio = ffmpeg.input("audio/11175751_corporate-feel-good-ambient-background_by_bluefoxmusic_preview.mp3")

#ffmpeg.concat(video, audio, v=1, a=1).output(r"C:\Users\owenb\PycharmProjects\movie_editing\output.mp4").run(overwrite_output=True)

#out = ffmpeg.output(video, audio, 'audi_test.mp4', vcodec='copy', acodec='aac', strict='experimental')
#out.run()