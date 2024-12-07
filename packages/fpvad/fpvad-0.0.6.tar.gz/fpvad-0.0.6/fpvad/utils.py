import torch
import torch.nn as nn
import json

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
