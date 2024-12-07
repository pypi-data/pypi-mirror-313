import torch
import librosa
import numpy as np
import soundfile
import os

from models import PyanNet
from utils import VAD_wave2wave, load_model_config

class VAD:
    def __init__(self, model_config_path="./recipes/pyannote_v2.json", checkpoint_path="./checkpoints/ERI_VAD.pth" , device=None):
        # Set device for model computation
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Load model configuration and model
        self.vad_configs = load_model_config(model_config_path)
        self.vad = PyanNet(self.vad_configs).to(self.device)
        
        # Load the pre-trained model
        checkpoint = torch.load(checkpoint_path)
        self.vad.load_state_dict(checkpoint)
        
        self.vad.eval()
        
        # VAD pipeline initialization
        self.model = VAD_wave2wave(self.vad, self.vad_configs, pre_proc_sensitivity_ms=300)
    
    def process_audio(self, path_audio: str, save_path: str = None, sr: int = 16000, batch_size: int = 32):
        sig, sr = librosa.load(path_audio, sr=sr, dtype='float32')
        print(f"Read the signal: {sig.shape}, main_sr: {sr} \n")
        
        chunk_size = sr * 10
        sig_l = len(sig)
        chunk_n = sig_l // chunk_size

        padded_sig = np.zeros(((chunk_n + 1) * chunk_size,), dtype='float32')
        padded_sig[:sig_l] = sig

        chunked_sig = padded_sig.reshape(-1, chunk_size)
        voiced_chunked_sig = np.zeros_like(chunked_sig)

        self.model.eval()

        torch.cuda.empty_cache()
        with torch.no_grad():
            for batch in range(0, chunked_sig.shape[0], batch_size):
                voice_files = self.model(torch.from_numpy(chunked_sig[batch:batch + batch_size]).to(self.device))
                voiced_chunked_sig[batch:batch + batch_size, :voice_files.shape[-1]] = voice_files

        voiced_chunked_sig = voiced_chunked_sig.reshape(-1, )[:sig_l]
        # removing non-speech
        voiced_chunked_sig = voiced_chunked_sig[voiced_chunked_sig != 0]

        if save_path:
            soundfile.write(save_path, voiced_chunked_sig, sr)
        else:
            soundfile.write(path_audio[:-4] + "_voice_detected.mp3", voiced_chunked_sig, sr)

        return voiced_chunked_sig
