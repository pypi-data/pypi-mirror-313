import torch
from torch import nn

from gxl_ai_utils.audio_model.s2t.modules.ctc_decoder import CTCDecoder
from gxl_ai_utils.audio_model.s2t.modules.subsampling import Conv2dSubsampling4Pure
import torch.nn.utils.rnn as rnn
import torch.nn.functional as F


class CRNNEncoder(nn.Module):
    def __init__(self,
                 feat_size,
                 dict_size,
                 num_rnn_layers=4,
                 rnn_size=1024,
                 rnn_direction='forward',
                 num_fc_layers=2,
                 fc_layers_size_list=None,
                 num_conv_layers=2,
                 use_gru=False):
        super().__init__()
        if fc_layers_size_list is None:
            fc_layers_size_list = [512, 256]
        self.num_conv_layers = num_conv_layers
        self.rnn_size = rnn_size
        self.feat_size = feat_size  # 161 for linear
        self.dict_size = dict_size
        self.num_rnn_layers = num_rnn_layers
        self.num_fc_layers = num_fc_layers
        self.rnn_direction = rnn_direction
        self.fc_layers_size_list = fc_layers_size_list
        self.use_gru = use_gru
        self.conv = Conv2dSubsampling4Pure(feat_size, 32, dropout_rate=0.0)

        self.output_dim = self.conv.output_dim

        i_size = self.conv.output_dim
        self.rnn = nn.ModuleList()
        self.layernorm_list = nn.ModuleList()
        self.fc_layers_list = nn.ModuleList()
        if rnn_direction == 'bidirect' or rnn_direction == 'bidirectional':
            layernorm_size = 2 * rnn_size
        elif rnn_direction == 'forward':
            layernorm_size = rnn_size
        else:
            raise Exception("Wrong rnn direction")
        for i in range(0, num_rnn_layers):
            if i == 0:
                rnn_input_size = i_size
            else:
                rnn_input_size = layernorm_size
            if use_gru is True:
                self.rnn.append(
                    nn.GRU(
                        input_size=rnn_input_size,
                        hidden_size=rnn_size,
                        num_layers=1,
                        bidirectional=rnn_direction == 'bidirectional',
                    )
                )
            else:
                self.rnn.append(
                    nn.LSTM(
                        input_size=rnn_input_size,
                        hidden_size=rnn_size,
                        num_layers=1,
                        bidirectional=rnn_direction == 'bidirectional'))
                self.layernorm_list.append(nn.LayerNorm(layernorm_size))
                self.output_dim = layernorm_size

                fc_input_size = layernorm_size
                for i in range(self.num_fc_layers):
                    self.fc_layers_list.append(
                        nn.Linear(fc_input_size, fc_layers_size_list[i]))
                    fc_input_size = fc_layers_size_list[i]
                    self.output_dim = fc_layers_size_list[i]

    @property
    def output_size(self):
        return self.output_dim

    def forward(self, x, x_lens, init_state_h_box=None, init_state_c_box=None):
        """Compute Encoder outputs

        Args:
            x (Tensor): [B, T, D]
            x_lens (Tensor): [B]
            init_state_h_box(Tensor): init_states h for RNN layers: [num_rnn_layers * num_directions, batch_size, hidden_size]
            init_state_c_box(Tensor): init_states c for RNN layers: [num_rnn_layers * num_directions, batch_size, hidden_size]
        Return:
            x (Tensor): encoder outputs, [B, T, D]
            x_lens (Tensor): encoder length, [B]
            final_state_h_box(Tensor): final_states h for RNN layers: [num_rnn_layers * num_directions, batch_size, hidden_size]
            final_state_c_box(Tensor): final_states c for RNN layers: [num_rnn_layers * num_directions, batch_size, hidden_size]
        """
        if init_state_h_box is not None:
            init_state_list = None

            if self.use_gru is True:
                init_state_h_list = torch.split(
                    init_state_h_box, self.num_rnn_layers, dim=0)
                init_state_list = init_state_h_list
            else:
                init_state_h_list = torch.split(
                    init_state_h_box, init_state_h_box.shape[0] // self.num_rnn_layers, dim=0)
                init_state_c_list = torch.split(
                    init_state_c_box, init_state_c_box.shape[0] // self.num_rnn_layers, dim=0)
                init_state_list = [(init_state_h_list[i], init_state_c_list[i])
                                   for i in range(self.num_rnn_layers)]
        else:
            init_state_list = [None] * self.num_rnn_layers

        x, x_lens = self.conv(x, x_lens)
        final_chunk_state_list = []
        for i in range(0, self.num_rnn_layers):
            """
            在使用self.lstm(x, init_state_list,)时,如果有x_lens数据，需要先对x进行填充和打包，这样LSTM层就可以根
            据x_lens忽略掉填充部分，只处理有效部分。这样做可以提高计算效率和准确性，避免填充部分对结果产生影响。
            x_lens 为0,1,2时, 经过4倍降采样得到的是-1,只有当x_lens大于等于7时,经过4倍下采样得到的值才为1.
            """
            device_temp = x.device
            temp_lens = torch.where(x_lens <= 0, 1, x_lens)
            temp_lens = temp_lens.to(torch.device('cpu')).to(torch.int64)
            x = rnn.pack_padded_sequence(x, temp_lens, batch_first=True, enforce_sorted=False)
            output, final_state = self.rnn[i](x, init_state_list[i],
                                              )  # [B, T, D]
            output, x_lens = rnn.pad_packed_sequence(output, batch_first=True)
            x = output
            final_chunk_state_list.append(final_state)
            x = self.layernorm_list[i](x)

        for i in range(self.num_fc_layers):
            x = self.fc_layers_list[i](x)
            x = F.relu(x)

        if self.use_gru is True:
            final_chunk_state_h_box = torch.concat(final_chunk_state_list, dim=0)
            final_chunk_state_c_box = init_state_c_box
        else:
            final_chunk_state_h_list = [
                final_chunk_state_list[i][0] for i in range(self.num_rnn_layers)
            ]
            final_chunk_state_c_list = [
                final_chunk_state_list[i][1] for i in range(self.num_rnn_layers)
            ]
            final_chunk_state_h_box = torch.concat(
                final_chunk_state_h_list, dim=0)
            final_chunk_state_c_box = torch.concat(
                final_chunk_state_c_list, dim=0)

        return x, x_lens, final_chunk_state_h_box, final_chunk_state_c_box

    def forward_chunk_by_chunk(self, x, x_lens, decoder_chunk_size=8):
        """Compute Encoder outputs

        Args:
            x (Tensor): [B, T, D]
            x_lens (Tensor): [B]
            decoder_chunk_size: The chunk size of decoder
        Returns:
            eouts_list (List of Tensor): The list of encoder outputs in chunk_size: [B, chunk_size, D] * num_chunks
            eouts_lens_list (List of Tensor): The list of  encoder length in chunk_size: [B] * num_chunks
            final_state_h_box(Tensor): final_states h for RNN layers: [num_rnn_layers * num_directions, batch_size, hidden_size]
            final_state_c_box(Tensor): final_states c for RNN layers: [num_rnn_layers * num_directions, batch_size, hidden_size]
        """
        subsampling_rate = self.conv.subsampling_rate
        receptive_field_length = self.conv.receptive_field_length
        chunk_size = (decoder_chunk_size - 1
                      ) * subsampling_rate + receptive_field_length
        chunk_stride = subsampling_rate * decoder_chunk_size
        max_len = x.shape[1]
        assert (chunk_size <= max_len)

        eouts_chunk_list = []
        eouts_chunk_lens_list = []
        if (max_len - chunk_size) % chunk_stride != 0:
            padding_len = chunk_stride - (max_len - chunk_size) % chunk_stride
        else:
            padding_len = 0
        padding = torch.zeros((x.shape[0], padding_len, x.shape[2]))
        padded_x = torch.concat([x, padding], dim=1)
        num_chunk = (max_len + padding_len - chunk_size) / chunk_stride + 1
        num_chunk = int(num_chunk)
        chunk_state_h_box = None
        chunk_state_c_box = None
        for i in range(0, num_chunk):
            start = i * chunk_stride
            end = start + chunk_size
            x_chunk = padded_x[:, start:end, :]
            # 剩余的长度
            x_len_left = torch.where(x_lens - i * chunk_stride < 0,
                                     torch.zeros_like(x_lens),
                                     x_lens - i * chunk_stride)
            x_chunk_len_tmp = torch.ones_like(x_lens) * chunk_size
            # 在当前chunk的长度
            x_chunk_lens = torch.where(x_len_left < x_chunk_len_tmp,
                                       x_len_left, x_chunk_len_tmp)

            eouts_chunk, eouts_chunk_lens, chunk_state_h_box, chunk_state_c_box = self.forward(
                x_chunk, x_chunk_lens, chunk_state_h_box, chunk_state_c_box)

            eouts_chunk_list.append(eouts_chunk)
            eouts_chunk_lens_list.append(eouts_chunk_lens)
        final_state_h_box = chunk_state_h_box
        final_state_c_box = chunk_state_c_box
        return eouts_chunk_list, eouts_chunk_lens_list, final_state_h_box, final_state_c_box


class DeepSpeech2Model(nn.Module):
    def __init__(
            self,
            feat_size,
            dict_size,
            num_conv_layers=2,
            num_rnn_layers=4,
            rnn_size=1024,
            rnn_direction='forward',
            num_fc_layers=2,
            fc_layers_size_list=None,
            use_gru=False,
            blank_id=0,
            ctc_grad_norm_type=None, ):
        super().__init__()
        if fc_layers_size_list is None:
            fc_layers_size_list = [512, 256]
        self.encoder = CRNNEncoder(
            feat_size=feat_size,
            dict_size=dict_size,
            num_conv_layers=num_conv_layers,
            num_rnn_layers=num_rnn_layers,
            rnn_direction=rnn_direction,
            num_fc_layers=num_fc_layers,
            fc_layers_size_list=fc_layers_size_list,
            rnn_size=rnn_size,
            use_gru=use_gru)

        self.decoder = CTCDecoder(
            odim=dict_size,  # <blank> is in  vocab
            enc_n_units=self.encoder.output_size,
            blank_id=blank_id,
            dropout_rate=0.0,
            reduction=True,  # sum
        )

    def forward(self, audio, audio_len, text, text_len):
        """Compute Model loss

        Args:
            audio (Tensor): [B, T, D]
            audio_len (Tensor): [B]
            text (Tensor): [B, U]
            text_len (Tensor): [B]

        Returns:
            loss (Tensor): [1]
        """
        eouts, eouts_len, final_state_h_box, final_state_c_box = self.encoder(
            audio, audio_len, None, None)
        loss = self.decoder(eouts, eouts_len, text, text_len)
        return loss

    @torch.no_grad()
    def decode(self, audio, audio_len):
        # decoders only accept string encoded in utf-8
        # Make sure the decoder has been initialized
        eouts, eouts_len, final_state_h_box, final_state_c_box = self.encoder(
            audio, audio_len, None, None)
        probs = self.decoder.softmax(eouts)
        res = self.decoder.decode_batch_beam_search_offline(probs, eouts_len, None)
        return res[0]

    @classmethod
    def from_config(cls, config):
        """Build a DeepSpeec2Model from config
        Parameters

        config: yacs.config.CfgNode
            config
        Returns
        -------
        DeepSpeech2Model
            The model built from config.
        """
        model = cls(
            feat_size=config.input_dim,
            dict_size=config.output_dim,
            num_conv_layers=config.num_conv_layers,
            num_rnn_layers=config.num_rnn_layers,
            rnn_size=config.rnn_layer_size,
            rnn_direction=config.rnn_direction,
            num_fc_layers=config.num_fc_layers,
            fc_layers_size_list=config.fc_layers_size_list,
            use_gru=config.use_gru,
            blank_id=config.blank_id,
            ctc_grad_norm_type=config.get('ctc_grad_norm_type', None), )
        return model


class DeepSpeech2InferModel(DeepSpeech2Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def forward(self,
                audio_chunk,
                audio_chunk_lens,
                chunk_state_h_box=None,
                chunk_state_c_box=None):
        if self.encoder.rnn_direction == "forward":
            eouts_chunk, eouts_chunk_lens, final_state_h_box, final_state_c_box = self.encoder(
                audio_chunk, audio_chunk_lens, chunk_state_h_box,
                chunk_state_c_box)
            probs_chunk = self.decoder.softmax(eouts_chunk)
            return probs_chunk, eouts_chunk_lens, final_state_h_box, final_state_c_box
        elif self.encoder.rnn_direction == "bidirect":
            eouts, eouts_len, _, _ = self.encoder(audio_chunk, audio_chunk_lens)
            probs = self.decoder.softmax(eouts)
            return probs, eouts_len
        else:
            raise Exception("wrong model type")


if __name__ == '__main__':
    """"""
    model = CRNNEncoder(
        feat_size=64,
        dict_size=50000,
        num_rnn_layers=3,
        rnn_size=1024,
        rnn_direction='forward',
        num_fc_layers=2,
        fc_layers_size_list=None,
        use_gru=False
    )
    whole_model = DeepSpeech2Model(
        feat_size=64,
        dict_size=50000,
        num_conv_layers=2,
        num_rnn_layers=4,
        rnn_size=1024,
        rnn_direction='forward',
        num_fc_layers=2,
        fc_layers_size_list=None,
        use_gru=False
    )
    print('output_size:' + str(model.output_size))
    input = torch.randn(123, 1000, 64)
    x_lens = torch.randint(600, 1001, (123,))
    target = torch.randint(50000, (123, 100))
    target_len = torch.randint(10, 101, (123,))
    loss = whole_model(input, x_lens, target, target_len)
    print(loss)
