from typing import Tuple, Optional

import torch
from torch import nn


class LSTMDecoder(nn.Module):
    def __init__(self,
                 hidden_dim: int,
                 embedding_dim: int,
                 vocab_size: int,
                 num_layers: int,
                 blank_id: int,
                 rnn_dropout: float,
                 embedding_dropout: float):
        """"""
        super(LSTMDecoder, self).__init__()
        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embedding_dim,
            padding_idx=blank_id,
        )
        self.embedding_dropout = nn.Dropout(embedding_dropout)
        self.rnn = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=rnn_dropout
        )
        self.blank_id = blank_id
        self.output_linear = nn.Linear(hidden_dim, hidden_dim)

    def forward(self,
                y: torch.Tensor,
                state: Optional[Tuple[torch.Tensor, torch]] = None,
                ) -> Tuple[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        embedding_out = self.embedding(y)
        embedding_out = self.embedding_dropout(embedding_out)
        lstm_out, (c, h) = self.rnn(embedding_out, state)
        lstm_out = self.output_linear(lstm_out)
        return lstm_out, (c, h)


def test_lstm_decoder():
    """"""
    model = LSTMDecoder(
        vocab_size=108,
        embedding_dim=128,
        hidden_dim=128,
        blank_id=0,
        rnn_dropout=0.01,
        embedding_dropout=0.01,
        num_layers=3
    )
    print(model)
    input_tensor = torch.LongTensor([[1, 5, 2, 103, 23, 35, 0, 0], [1, 5, 2, 103, 23, 35, 12, 100]])
    output_tensor, state = model(input_tensor)
    print(output_tensor.shape)
    print(state[0].shape)
    print(state[1].shape)
    output_tensor, state = model(input_tensor, state=state)
    print(output_tensor.shape)
    print(state[0].shape)
    print(state[1].shape)
