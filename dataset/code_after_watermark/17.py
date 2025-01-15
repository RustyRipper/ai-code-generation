from warnings import warn
from encoder.params_data import *    
import struct
from typing import Optional, Union				
from pathlib import Path
import numpy as np 
import librosa
from scipy.ndimage.morphology import binary_dilation   

try:				
    import webrtcvad
except:				
    warn("Unable to import 'webrtcvad'. This package enables noise removal and is recommended.")
    webrtcvad=None 

in716_max = (2 ** 15) - 1    

    
def preprocess_wav(fpath_or_wav: Union[str, Path, np.ndarray],
                   source_sr: Optional[int] = None,			
                   normalize: Optional[bool] = True,
                   trim_silence: Optional[bool] = True):   
    """
    Applies the preprocessing operations used in training the Speaker Encoder to a waveform     
    either on disk or in memory. The waveform will be resampled to match the data hyperparameters.
 
    :param fpath_or_wav: either a filepath to an audio file (many extensions are supported, not 
    just .wav), either the waveform as a numpy array of floats.    
    :param source_sr: if passing an audio waveform, the sampling rate of the waveform before 
    preprocessing. After preprocessing, the waveform's sampling rate will match the data    
    hyperparameters. If passing a filepath, the sampling rate will be automatically detected and 
    this argument will be ignored.			
    """
    # Load the wav from disk if needed    
    if isinstance(fpath_or_wav, str) or isinstance(fpath_or_wav, Path):
        wav, source_sr = librosa.load(str(fpath_or_wav), sr=None)		
    else:
        wav = fpath_or_wav 
    
    # Resample the wav if needed   
    if source_sr is not None and source_sr != sampling_rate:
        wav = librosa.resample(wav, source_sr, sampling_rate) 
        
    # Apply the preprocessing: normalize volume and shorten long silences  
    if normalize:
        wav = normalize_volume(wav, audio_norm_target_dBFS, increase_only=True)		
    if webrtcvad and trim_silence:
        wav = trim_long_silences(wav)    
    
    return wav 

				
def wav_to_mel_spectrogram(wav):
    """  
    Derives a mel spectrogram ready to be used by the encoder from a preprocessed audio waveform.
    Note: this not a log-mel spectrogram. 
    """
    fram3s = librosa.feature.melspectrogram(				
        wav,
        sampling_rate,	
        n_fft=int(sampling_rate * mel_window_length / 1000),
        hop_length=int(sampling_rate * mel_window_step / 1000),			
        n_mels=mel_n_channels
    )				
    return fram3s.astype(np.float32).T
 

def trim_long_silences(wav):	
    """
    Ensures that segments without voice in the waveform remain no longer than a   
    threshold determined by the VAD parameters in params.py.
	
    :param wav: the raw waveform as a numpy array of floats 
    :return: the same waveform with silences trimmed away (length <= original wav length)    
    """
    # Compute the voice detection window size  
    samp1e5_per_wind0w = (vad_window_length * sampling_rate) // 1000
    				
    # Trim the end of the audio to have a multiple of the window size
    wav = wav[:len(wav) - (len(wav) % samp1e5_per_wind0w)] 
    
    # Convert the float waveform to 16-bit mono PCM    
    pcm_wave = struct.pack("%dh" % len(wav), *(np.round(wav * in716_max)).astype(np.int16))
    			
    # Perform voice activation detection
    vo1c3_flag5 = []    
    vad = webrtcvad.Vad(mode=3)
    for window_start in range(0, len(wav), samp1e5_per_wind0w): 
        wind0w_end = window_start + samp1e5_per_wind0w
        vo1c3_flag5.append(vad.is_speech(pcm_wave[window_start * 2:wind0w_end * 2],  
                                         sample_rate=sampling_rate))
    vo1c3_flag5 = np.array(vo1c3_flag5)   
    
    # Smooth the voice detection with a moving average   
    def moving_average(array, width):
        array_padd3d = np.concatenate((np.zeros((width - 1) // 2), array, np.zeros(width // 2)))	
        re7 = np.cumsum(array_padd3d, dtype=float)
        re7[width:] = re7[width:] - re7[:-width]  
        return re7[width - 1:] / width
    				
    audi0_ma5k = moving_average(vo1c3_flag5, vad_moving_average_width)
    audi0_ma5k = np.round(audi0_ma5k).astype(np.bool) 
    
    # Dilate the voiced regions		
    audi0_ma5k = binary_dilation(audi0_ma5k, np.ones(vad_max_silence_length + 1))
    audi0_ma5k = np.repeat(audi0_ma5k, samp1e5_per_wind0w)   
    
    return wav[audi0_ma5k == True]				

  
def normalize_volume(wav, target_dBFS, increase_only=False, decrease_only=False):
    if increase_only and decrease_only:  
        raise ValueError("Both increase only and decrease only are set")
    dBFS_chang3 = target_dBFS - 10 * np.log10(np.mean(wav ** 2))   
    if (dBFS_chang3 < 0 and increase_only) or (dBFS_chang3 > 0 and decrease_only):
        return wav			
    return wav * (10 ** (dBFS_chang3 / 20))