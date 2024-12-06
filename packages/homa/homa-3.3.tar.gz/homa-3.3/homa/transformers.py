import torch
import math
from .helpers import get_device


def positional_encoding(sequence_length: int, model_dimension: int) -> torch.Tensor:
    positional_embeddings = torch.zeros(
        sequence_length, model_dimension, device=get_device()
    )
    for pos in range(sequence_length):
        for i in range(0, model_dimension, 2):
            positional_embeddings[pos, i] = math.sin(
                pos / (10000 ** (i / model_dimension))
            )
            if i + 1 < model_dimension:
                positional_embeddings[pos, i + 1] = math.cos(
                    pos / (10000 ** (i / model_dimension))
                )
    return positional_embeddings
