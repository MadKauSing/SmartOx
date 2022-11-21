import librosa
def manipulate(data, speed_factor):
    return librosa.effects.time_stretch(data, speed_factor)