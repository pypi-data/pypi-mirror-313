from functools import partial
from pathlib import Path
from typing import Dict, List

import pandas as pd
import torch
from safetensors.torch import load_file
from torch.utils.data import Dataset, default_collate


def get_char_map_table():
    # char_table = ['-', ' ', '.', '?', '!', '\'', '\"']
    char_table = ['-', ' ', '.']
    for i in range(26):
        char_table.append(chr(i + 97))
    for i in range(10):
        char_table.append(str(i))
    return {k: v for k, v in enumerate(char_table)}


def special_symbol_map():
    return {
        "°": " degree"
    }


def tokenize_with_char_map_table(text: str, char_mapping: Dict):
    # this is commented because torch.nn.CTCLoss requires target index cannot be blank
    # text = "-".join(text)
    indices = [char_mapping[char] for char in text]
    return torch.tensor(indices, dtype=torch.long)


def bare_collate_function(batch_data: List, audio_pad_value, LLM_pad_value, y_pad_value):
    x_batch, y_batch = (tuple(item) for item in zip(*batch_data))
    x_audio_data, x_context, audio_data_mask, content_mask = (list(item) for item in zip(*x_batch))
    y_tokenized_transcribe, ctc_target_length, transcribe = (list(item) for item in zip(*y_batch))

    # get maximum length of x_ts
    pad_audio_data = torch.nn.utils.rnn.pad_sequence(x_audio_data, batch_first=True, padding_value=audio_pad_value)
    pad_tokenized_context = torch.nn.utils.rnn.pad_sequence(x_context, batch_first=True,
                                                            padding_value=LLM_pad_value)
    pad_tokenized_transcribe = torch.nn.utils.rnn.pad_sequence(y_tokenized_transcribe, batch_first=True,
                                                               padding_value=y_pad_value)
    pad_audio_data_mask = torch.nn.utils.rnn.pad_sequence(audio_data_mask, batch_first=True, padding_value=False)
    pad_content_mask = torch.nn.utils.rnn.pad_sequence(content_mask, batch_first=True, padding_value=False)
    ctc_target_length = default_collate(ctc_target_length)
    transcribe = default_collate(transcribe)
    return (pad_audio_data, pad_tokenized_context, pad_audio_data_mask, pad_content_mask), (
        pad_tokenized_transcribe, ctc_target_length, transcribe)


class CoreDataset(Dataset):
    """
    y_pad_value: '-' is of index 0
    audio magnitude pad is 0.0
    LLM pad token is 12804
    """
    y_pad_value = 0
    audio_pad_value = 0.0
    LLM_pad_value = 12804

    def __init__(self, data_file: pd.DataFrame, audio_dir: Path):
        self.data = data_file
        self.audio_dir = audio_dir
        self.char_map_table = get_char_map_table()
        self.reversed_char_map_table = {v: k for k, v in self.char_map_table.items()}

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        """
            audio_id = row["audio_id"]
            transcribe = row["transcribe"]
            word = row["word"]
            task = row["task"]
            context_type = row["context_type"]
            context = row["context"]
            tokenized_context_dir = row["tokenized_context_dir"]
        """
        row = self.data.iloc[idx]
        audio_file_dir = self.audio_dir / row['audio_id']
        # audio magnitude safetensors have "audio_tensor" and "audio_sample_rate" two keys
        struct = load_file(audio_file_dir)
        tokenized_transcribe = tokenize_with_char_map_table(row["transcribe"], self.reversed_char_map_table)
        tokenized_context = load_file(row["tokenized_context_dir"])["input_ids"].squeeze()

        return ((struct["audio_tensor"], tokenized_context,
                 torch.ones_like(struct["audio_tensor"], dtype=torch.bool),
                 torch.ones_like(tokenized_context, dtype=torch.bool)),
                (tokenized_transcribe,
                 tokenized_transcribe.shape[0],
                 row["transcribe"]))

    @classmethod
    def collate_function_generator(cls):
        return partial(
            bare_collate_function,
            audio_pad_value=cls.audio_pad_value,
            LLM_pad_value=cls.LLM_pad_value,
            y_pad_value=cls.y_pad_value,
        )
