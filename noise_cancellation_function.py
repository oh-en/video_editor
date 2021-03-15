import noisereduce as nr
from scipy.io import wavfile
import subprocess
import numpy as np
import os

def cancel_audio(file):
    """
    This takes a path to a video file, grabs the audio from it, cancels the background noise,
    and adds the audio back to the video file
    
    getting the audio file and adding it back to the video are done using ffmpeg
    
    noise cancellation done using noisereduce: https://github.com/timsainb/noisereduce
    """

    command = """ffmpeg -i "{}" -vn audio.wav""".format(file) # get the audio
    subprocess.call(command, shell=True)

    rate, data = wavfile.read("audio.wav") # read this audio file into python
    
    data = data[:,0].astype(float) # make it single channel audio, idk how to do dual channel audio
    noise = data[int(rate/4):int(rate/2)] # takes a sample of the noise
    # noise is sampled from .25 - .5 seconds.

    reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noise, verbose=False) # reduce the noise of this file

    m = np.max(np.abs(reduced_noise)) # convert cancelled noise back to a usable data format for wavfile.write
    sigf32 = (reduced_noise/m).astype(np.float32)
    wavfile.write('noise_reduce_audio.wav',rate,sigf32) # write this back to an audio file
    
    command = """ffmpeg -i {} -i noise_reduce_audio.wav -map 0:v -map 1:a -c:v copy -shortest output.mp4""".format(file) # get the audio
    subprocess.call(command, shell=True)
    
    os.remove('noise_reduce_audio.wav') # remove created files
    os.remove('audio.wav')