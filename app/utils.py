import os
from scipy import signal
import numpy as np
import soundfile as sf
from scipy import signal


def db(x,MIN_AMP,AMP_FAC):
    return 20. * np.log10(np.maximum(x, np.max(x) / MIN_AMP) * AMP_FAC)
    
def reduce_standarize(x):
    return (x - 7.6765018) / 17.440527


def individual_feature_extractor_pred(audio_len, nperseg = 512, noverlap = 256):
    def extract_features(data):
        real_length = len(data)
        residual = real_length % 16384

        pad = np.zeros((16384-residual))

        data = np.concatenate([data,pad])

        data = data.reshape(-1,audio_len)
        X = []
        complex_list = []

        for ch in data:
            _, _, complex_ = signal.stft(ch, fs=16000, nperseg=nperseg, noverlap=noverlap)
            mag_mix = np.abs(complex_)
            x = reduce_standarize(db(mag_mix,10000.,10000.))
            X.append(np.transpose(x,[1,0])[...,np.newaxis])
            complex_list.append(np.transpose(complex_,[1,0])[...,np.newaxis])

        return X, complex_list, real_length

    return extract_features


def individual_create_predictions_pred(results,complex_,real_length,file_name,folder, nperseg = 512, noverlap = 256):
        recovered_a = []
        recovered_b = []
        for predicted_, complex_mix in zip(results,complex_):
            _, source_recovered_a = signal.istft(np.transpose(predicted_[...,0] * complex_mix[...,0],[1,0]), fs=16000 ,nperseg= nperseg, noverlap = noverlap)
            _, source_recovered_b = signal.istft(np.transpose(( 1 - predicted_[...,0]) * complex_mix[...,0],[1,0]), fs=16000 ,nperseg= nperseg, noverlap = noverlap)
            recovered_a.append(source_recovered_a)
            recovered_b.append(source_recovered_b)
            
        sf.write("{}/{}.wav".format(folder,file_name.split(".")[0]),np.array(recovered_a).reshape(-1)[0:real_length],16000)
        sf.write("{}/{}_b.wav".format(folder,file_name.split(".")[0]),np.array(recovered_b).reshape(-1)[0:real_length],16000)


def _find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename