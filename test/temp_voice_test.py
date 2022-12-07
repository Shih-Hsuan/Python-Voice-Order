import pyaudio
import wave
from tempfile import NamedTemporaryFile

from pygame import mixer
from time import sleep

mixer.init()
def temp_voice():
    # sample chunk size
    chunk = 1024
    # sample format: paFloat32, paInt32, paInt24, paInt16, paInt8, paUInt8, paCustomFormat
    sample_format = pyaudio.paInt16
    # sound channel
    channels = 2
    # sample frequency rate: 44100 ( CD ), 48000 ( DVD ), 22050, 24000, 12000 and 11025
    fs = 44100
    # recording seconds
    seconds = 5

    p = pyaudio.PyAudio()
    # init pyaudio object

    print("starting recording...")

    # active voice stream
    stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)

    frames = []
    # voice list

    for i in range(0, int(fs / chunk * seconds)):
        # record voice into list
        data = stream.read(chunk)
        frames.append(data)

    # stop recording
    stream.stop_stream()
    # close stream
    stream.close()
    p.terminate()

    print('stop recording...')

    
    with NamedTemporaryFile(delete=True) as fp:
        # open voice file
        wf = wave.open("{}.wav".format(fp.name), 'wb')
        # set channel
        wf.setnchannels(channels)
        # set format
        wf.setsampwidth(p.get_sample_size(sample_format))
        # set sampling frequency rate
        wf.setframerate(fs)
        # save
        wf.writeframes(b''.join(frames))
        wf.close()
        mixer.music.load('{}.wav'.format(fp.name))
        mixer.music.play()

temp_voice()
sleep(5)