import torch
from torch import nn

from ...Dataset.DataPipeline.CoreDataset import get_char_map_table


class GreedyCTCDecoder(nn.Module):
    def __init__(self, blank: int = 0):
        super().__init__()
        self.blank = blank
        self.char_map_table = get_char_map_table()
        self.labels = [""] * len(self.char_map_table)
        for k, v in self.char_map_table.items():
            self.labels[k] = v

    def forward(self, emission: torch.Tensor) -> list:
        """
        Decodes a batch of emission tensors using greedy CTC decoding with vectorized operations.

        Args:
            emission (torch.Tensor): Tensor of shape (batch_size, time_steps, num_classes).

        Returns:
            list: A list of decoded strings, one for each sequence in the batch.
        """
        argmax_indices = torch.argmax(emission, dim=-1)
        shifted_indices = torch.zeros_like(argmax_indices)
        shifted_indices[:, 1:] = argmax_indices[:, :-1]
        mask = argmax_indices != shifted_indices
        unique_indices = argmax_indices * mask.long()
        unique_indices = unique_indices.masked_fill(unique_indices == self.blank, -1)
        unique_indices_list = unique_indices.tolist()
        decoded_batch = [
            "".join([self.labels[idx] for idx in seq if idx != -1]).replace(".", "")
            for seq in unique_indices_list
        ]

        return decoded_batch
