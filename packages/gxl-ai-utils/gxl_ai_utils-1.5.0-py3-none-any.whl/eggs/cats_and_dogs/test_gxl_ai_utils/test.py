import torch

from gxl_ai_utils.model_warehouse.transformer.transformer import Transformer

if __name__ == '__main__':
    model = Transformer(1000, 100, 1000, 100)
    input = torch.randint(0,1000,(2, 10))
    input_len = torch.randint(0,11,(2,1))
    output, encoder_self_attn, decoder_self_attn, decoder_context_attn = model(input, input_len, input, input_len)
    print(output.shape)

