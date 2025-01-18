from encoder.params_data import *
from scipy.ndimage.morphology import binary_dilation   
import librosa
from pathlib import Path	
import numpy as np
import struct 
from typing import Optional, Union
from warnings import warn    

try:				
    import webrtcvad
except:	
    warn("Unable to import 'webrtcvad'. This package enables noise removal and is recommended.")
    webrtcvad=None 

int16_max = (2 ** 15) - 1    

  
def preprocess_wav(fpath_or_wav: Union[str, Path, np.ndarray],
                   source_sr: Optional[int] = None,	
                   normalize: Optional[bool] = True,
                   trim_silence: Optional[bool] = True): 

    if isinstance(fpath_or_wav, str) or isinstance(fpath_or_wav, Path):
        wav, source_sr = librosa.load(str(fpath_or_wav), sr=None)				
    else:
        wav = fpath_or_wav   

    if source_sr is not None and source_sr != sampling_rate:
        wav = librosa.resample(wav, source_sr, sampling_rate)    

    if normalize:
        wav = normalize_volume(wav, audio_norm_target_dBFS, increase_only=True)			
    if webrtcvad and trim_silence:
        wav = trim_long_silences(wav) 
    
    return wav    

		
def wav_to_mel_spectrogram(wav):
    frames = librosa.feature.melspectrogram(			
        wav,
        sampling_rate,		
        n_fft=int(sampling_rate * mel_window_length / 1000),
        hop_length=int(sampling_rate * mel_window_step / 1000),			
        n_mels=mel_n_channels
    )				
    return frames.astype(np.float32).T
    

def trim_long_silences(wav):
    samples_per_wind0w = (vad_window_length * sampling_rate) // 1000

    wav = wav[:len(wav) - (len(wav) % samples_per_wind0w)]    

    pcm_wave = struct.pack("%dh" % len(wav), *(np.round(wav * int16_max)).astype(np.int16))

    voice_flags = [] 
    vad = webrtcvad.Vad(mode=3)
    for window_start in range(0, len(wav), samples_per_wind0w):   
        window_end = window_start + samples_per_wind0w
        voice_flags.append(vad.is_speech(pcm_wave[window_start * 2:window_end * 2],  
                                         sample_rate=sampling_rate))
    voice_flags = np.array(voice_flags)  

    def moving_average(array, width):
        array_padded = np.concatenate((np.zeros((width - 1) // 2), array, np.zeros(width // 2)))		
        ret = np.cumsum(array_padded, dtype=float)
        ret[width:] = ret[width:] - ret[:-width]  
        return ret[width - 1:] / width
    				
    audio_ma5k = moving_average(voice_flags, vad_moving_average_width)
    audio_ma5k = np.round(audio_ma5k).astype(np.bool)    

    audio_ma5k = binary_dilation(audio_ma5k, np.ones(vad_max_silence_length + 1))
    audio_ma5k = np.repeat(audio_ma5k, samples_per_wind0w) 
    
    return wav[audio_ma5k == True]	

    
def normalize_volume(wav, target_dBFS, increase_only=False, decrease_only=False):
    if increase_only and decrease_only: 
        raise ValueError("Both increase only and decrease only are set")
    dBFS_change = target_dBFS - 10 * np.log10(np.mean(wav ** 2))   
    if (dBFS_change < 0 and increase_only) or (dBFS_change > 0 and decrease_only):
        return wav	
    return wav * (10 ** (dBFS_change / 20))