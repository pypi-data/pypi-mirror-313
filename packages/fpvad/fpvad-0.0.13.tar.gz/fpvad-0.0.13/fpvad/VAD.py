import torch
import librosa
import numpy as np
import soundfile
import os
import json

import torch
import torch.nn as nn

from asteroid_filterbanks.enc_dec import Filterbank, Encoder
from asteroid_filterbanks.param_sinc_fb import ParamSincFB

class SincNet(nn.Module):
    """Filtering and convolutional part of Pyannote

    Arguments
    ---------
    n_filters : list, int
        List consist of number of each convolution kernel
    stride_ : in 
        Stride of ParamSincFB fliltering.

    Returns
    -------
    Sincnet model: class

    """
    
    def __init__(self, 
                 n_filters = [80,60,60],
                 stride_ = 10,
                 ):
        super(SincNet,self).__init__()
        

        sincnet_list = nn.ModuleList(
            [
                nn.InstanceNorm1d(1, eps=1e-05, momentum=0.1, affine=True, track_running_stats=False),
                Encoder(ParamSincFB(n_filters=n_filters[0], kernel_size=251, stride=stride_)),
                nn.MaxPool1d(kernel_size=3, stride=3, padding=0, dilation=1, ceil_mode=False),
                nn.InstanceNorm1d(n_filters[0], eps=1e-05, momentum=0.1, affine=True, track_running_stats=False),
            ]
        )
        for counter in range(len(n_filters) - 1):
            sincnet_list.append(nn.Conv1d(n_filters[counter], n_filters[counter+1], kernel_size=(5,), stride=(1,)))
            sincnet_list.append(nn.MaxPool1d(kernel_size=3, stride=3, padding=0, dilation=1, ceil_mode=False))
            sincnet_list.append(nn.InstanceNorm1d(n_filters[counter+1], eps=1e-05, momentum=0.1, affine=True, track_running_stats=False))

        self.sincnet_layer = nn.Sequential(*sincnet_list)

    def forward(self, x):
        """This method should implement forwarding operation in the SincNet model.

        Arguments
        ---------
        x : float (Tensor)
            The input of SincNet model.

        Returns
        -------
        out : float (Tensor)
            The output of SincNet model.
        """
        out = self.sincnet_layer(x)
        return out



class PyanNet(nn.Module):
    """Pyannote model

    Arguments
    ---------
    model_config : dict, str
        consist of model parameters

    Returns
    -------
    Pyannote model: class

    """
    def __init__(self,
                 model_config,
                 ):
        super(PyanNet,self).__init__()

        self.model_config = model_config

        sincnet_filters = model_config["sincnet_filters"]
        sincnet_stride = model_config["sincnet_stride"]
        linear_blocks = model_config["linear_blocks"]

        self.sincnet = SincNet(n_filters=sincnet_filters, stride_ = sincnet_stride)

        if model_config["sequence_type"] == "lstm":
            self.sequence_blocks = nn.LSTM(sincnet_filters[-1],
                                           model_config["sequence_neuron"],
                                           num_layers=model_config["sequence_nlayers"],
                                           batch_first=True,
                                           dropout=model_config["sequence_drop_out"],
                                           bidirectional=model_config["sequence_bidirectional"],
                                           )
        elif model_config["sequence_type"] == "gru":
            self.sequence_blocks = nn.GRU(sincnet_filters[-1],
                                          model_config["sequence_neuron"],
                                          num_layers=model_config["sequence_nlayers"],
                                          batch_first=True,
                                          dropout=model_config["sequence_drop_out"],
                                          bidirectional=model_config["sequence_bidirectional"],
                                          )
        elif model_config["sequence_type"] == "attention":
            self.sequence_blocks = nn.TransformerEncoderLayer(d_model=sincnet_filters[-1],
                                                              dim_feedforward=model_config["sequence_neuron"],
                                                              nhead=model_config["sequence_nlayers"],
                                                              batch_first=True,
                                                              dropout=model_config["sequence_drop_out"])
        else:
            raise ValueError("Model type is not valid!!!")


        if model_config["sequence_bidirectional"]:
            last_sequence_block = model_config["sequence_neuron"] * 2
        else:
            last_sequence_block = model_config["sequence_neuron"]


        linear_blocks = [last_sequence_block] + linear_blocks
        linears_list = nn.ModuleList()
        for counter in range(len(linear_blocks) - 1):
            linears_list.append(
                nn.Linear(
                    in_features=linear_blocks[counter],
                    out_features=linear_blocks[counter+1],
                    bias=True,
                )
            )
        linears_list.append(nn.Sigmoid())
        self.linears = nn.Sequential(*linears_list)


    def forward(self, x):
        """This method should implement forwarding operation in the Pyannote model.

        Arguments
        ---------
        x : float (Tensor)
            The input of Pyannote model.

        Returns
        -------
        out : float (Tensor)
            The output of Pyannote model.
        """
        x = torch.unsqueeze(x, 1)
        x = self.sincnet(x)
        x = x.permute(0,2,1)

        if self.model_config["sequence_type"] == "attention":
            x = self.sequence_blocks(x)
        else:
            x = self.sequence_blocks(x)[0]

        out = self.linears(x)
        return out



def load_model_config(config_path):
    """Load model config

    Arguments
    ---------
    config_path : str
        Path of config

    Returns
    -------
    configs : dict, str
        Loaded config

    """
    with open(config_path, "r") as f:
        configs = json.load(f)
    return configs

def cal_frame_sample_pyannote(wav_length,
                              sinc_step=10,
                              sinc_filter=251,
                              n_conv=2,
                              conv_filter= 5,
                              max_pool=3):
    """Define the number and the length of frames according to Pyannote model

    Arguments
    ---------
    wav_length : int
        Length of wave
    sinc_step : int
        Frame shift
    sinc_filter : int
        Length of sincnet filter
    n_conv : int
        Number of convolutional layers
    conv_filter : int
        Length of convolution filter
    max_pool : int
        Lenght of maxpooling
    
    Returns
    -------
    n_frame : float
        The number of frames according to Pyannote model
    sample_per_frame : float
        The length of frames according to Pyannote model

    """

    n_frame = (wav_length - (sinc_filter - sinc_step)) // sinc_step
    n_frame = n_frame // max_pool

    for _ in range(n_conv):
        n_frame = n_frame - (conv_filter - 1)
        n_frame = n_frame // max_pool

    sample_per_frame = wav_length // n_frame

    return n_frame, sample_per_frame

def changed_index(ind, step = 0):
    ind_bool = ind < ind.min() - 1
    if step == -1 :
        ind_bool[1:] = (ind+1)[:-1] == ind[1:] 
    else:
        ind_bool[:-1] = (ind-step)[1:] == ind[:-1]
    
    ind_bool = ~ind_bool
    return ind_bool

def post_processing_VAD(vad_out, goal = 1, len_frame_ms = 20, sensitivity_ms = 200):
    """Post-processing of VAD models to change 0 label0 with 1 labels according to a sensitivity.

    Arguments
    ---------
        vad_out : float (Tensor)
            Output of the VAD model.
        goal : int (Tensor)
            The goal of change.
        len_frame_ms : float 
            Length of decision frame.
        sensitivity_ms : float 
            Threshold to change labels that are less than it.

    Returns
    -------
        vad_out : float (Tensor)
            The pre-processed output.

    """

    Th = max(int(sensitivity_ms // len_frame_ms), 1)
    ind0,ind1 = torch.where(vad_out== goal)
    
    if len(ind0) != 0:
        ind1_max = vad_out.shape[-1] - 1
        ind0_last_bool = changed_index(ind0.clone())

        ind0_last = torch.where(ind0_last_bool)[0]
        ind0_first = torch.zeros_like(ind0_last)
        ind0_first[1:] = ind0_last[:-1] + 1
        ind0_first[0] = 0

        ind1_l1_bool = changed_index(ind1.clone(), step = 1)
        ind1_l1_bool[ind0_last] = False

        ind1_f1_bool = changed_index(ind1.clone(), step = -1)
        ind1_f1_bool[ind0_first] = False


        dif_bool = ind1[ind1_f1_bool] - ind1[ind1_l1_bool] > Th + 1
        l1_bool_temp = ind1_l1_bool[ind1_l1_bool].clone()
        l1_bool_temp[dif_bool] = False
        ind1_l1_bool[ind1_l1_bool.clone()] = l1_bool_temp

        f1_bool_temp = ind1_f1_bool[ind1_f1_bool].clone()
        f1_bool_temp[dif_bool] = False
        ind1_f1_bool[ind1_f1_bool.clone()] = f1_bool_temp


        second_ind = ind1[ind1_l1_bool].clone()
        for i in range(1,Th+1):
            second_ind = torch.clip(ind1[ind1_l1_bool]+i,0,ind1_max)
            desired_out = (second_ind < ind1[ind1_f1_bool])
            temp_b = vad_out[ind0[ind1_l1_bool], second_ind].clone()
            temp_b[desired_out] = goal
            vad_out[ind0[ind1_l1_bool], second_ind] = temp_b.clone()
    
    return vad_out


class VAD_wave2wave(nn.Module):
    def __init__(self,
                 vad,
                 vad_configs,
                 pre_proc_sensitivity_ms = 200,
                 ):
        super(VAD_wave2wave, self).__init__()

        self.vad = vad
        self.sensitivity_ms = pre_proc_sensitivity_ms
        self.vad_configs = vad_configs
            
    def forward(self, speechfiles):

        len_sp = speechfiles.shape[-1]
        num_frame , len_frame = cal_frame_sample_pyannote(len_sp,
                                                         sinc_step= self.vad_configs["sincnet_stride"]
                                                         )
        vad_predict = self.vad(speechfiles)
        vad_predict = (vad_predict > 0.5).int()
        vad_predict = vad_predict[...,0]
        l_fr_ms = len_frame/16

        vad_predict = post_processing_VAD(vad_predict, goal = 1, len_frame_ms = l_fr_ms,
                                       sensitivity_ms = self.sensitivity_ms)
        
        sample_label = torch.repeat_interleave(torch.tensor(vad_predict), len_frame, dim = -1)
        len_vad = sample_label.shape[-1]
        if len_sp > len_vad:
            speechfiles = speechfiles[...,:len_vad]
        else:
            sample_label = sample_label[...,:len_sp]
        voice_files = sample_label * speechfiles
        
        return voice_files.cpu().numpy() 



class VAD:
    def __init__(self, model_config_path=".pyannote_v2.json", checkpoint_path=".ERI_VAD.pth" , device=None):
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
