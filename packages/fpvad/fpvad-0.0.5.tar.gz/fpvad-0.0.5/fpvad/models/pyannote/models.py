import torch
import torch.nn as nn

from models.pyannote.layers import SincNet


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