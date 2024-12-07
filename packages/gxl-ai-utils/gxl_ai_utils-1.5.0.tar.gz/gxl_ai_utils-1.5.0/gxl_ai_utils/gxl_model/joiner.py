import torch
from torch import nn


class Joiner(nn.Module):
    def __init__(self, input_size, output_size):
        super(Joiner, self).__init__()
        self.input_size = input_size
        self.output_linear = nn.Linear(input_size, output_size)

    def forward(self, encoder_out, decoder_out):
        assert encoder_out.ndim == decoder_out.ndim == 3, f"encoder out dim: {encoder_out.ndim}, decoder out dim: {decoder_out.ndim}"
        assert encoder_out.size(0) == decoder_out.size(0), f"encoder_out.size(0): {encoder_out.size(0)}, decoder_out.size(0): {decoder_out.size(0)}"
        assert encoder_out.size(2) == decoder_out.size(2), f"encoder_out.size(2): {encoder_out.size(2)}, decoder_out.size(2): {decoder_out.size(2)}"
        encoder_out = encoder_out.unsqueeze(2)
        decoder_out = decoder_out.unsqueeze(1)
        logits = encoder_out + decoder_out
        logits = nn.functional.relu(logits)
        output = self.output_linear(logits)
        return output


def test_joiner():
    model = Joiner(80, 1024)
    input_encoder = torch.randn(3, 93, 80)
    input_decoder = torch.randn(3, 12, 80)
    output = model(input_encoder, input_decoder)
    print(output.size())
