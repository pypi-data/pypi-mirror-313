import argparse
from pathlib import Path
from typing import Dict, Union, Callable, Any, List

import numpy as np
import pandas as pd
import torch
from safetensors.torch import load_file
from torch.utils.data import Dataset, default_collate, DataLoader


class AudioData(Dataset):
    def __init__(self, safetensors_path: Path, guider: Path, filter_func: Callable[[pd.DataFrame], pd.DataFrame] = lambda x :x):
        self.safetensors_path: Path = safetensors_path
        if not safetensors_path.exists():
            raise FileNotFoundError(f"Audio path {safetensors_path} does not exist")
        if not safetensors_path.is_dir():
            raise ValueError("Audio path must be a dir")
        if not guider.exists():
            raise FileNotFoundError(f"Guider path {guider} does not exist")
        if not guider.is_file():
            raise ValueError("Guider path must be a file")
        self.guider = pd.read_csv(guider, index_col= 0, header=0).dropna(axis=0)
        self.filtered_guider: Union[pd.DataFrame, None] = None
        self.filter_func: Callable[[pd.DataFrame], pd.DataFrame] = filter_func

    def change_filter(self, filter_func: Callable[[pd.DataFrame], pd.DataFrame]):
        self.filter_func = filter_func
        self.filtered_guider = self.filter_func(self.guider)
        
    def apply_filter(self):
        self.filtered_guider = self.filter_func(self.guider)
    def __len__(self):
        if self.filtered_guider is None:
            self.apply_filter()
        return len(self.filtered_guider)

    def __process_record_meta(self, record: pd.Series) -> Dict[str, Any]:
        # load audio filename is index of record
        transcribe = record['transcribe']
        word = record['word']
        task = record['task']
        return {
            "name": str(record.name),
            "transcribe" : transcribe,
            "word": word,
            "task" : task
        }

    def __getitem__(self, idx: Union[torch.Tensor, int]):
        if torch.is_tensor(idx):
            idx.tolist()
        record: pd.Series = self.filtered_guider.iloc[idx, :]
        file_name = str(record.name)
        struct = load_file(self.safetensors_path / file_name)
        meta = self.__process_record_meta(record)

        return (struct['audio_tensor'], meta), f'-{"-".join(meta["transcribe"])}-'

    @staticmethod
    def collate_function(batch_data: List):
        x_batch = [item[0] for item in batch_data]
        y_batch = [item[1] for item in batch_data]
        x_ts: List[np.ndarray] = [item[0] for item in x_batch]
        x_meta = [item[1] for item in x_batch]
        # get maximum length of x_ts
        pad_ts = torch.nn.utils.rnn.pad_sequence(x_ts, batch_first=True)
        # TODO Return Padding information
        # TODO Convert x_ts to torch Tensor before sent to rnn
        collated_x_meta = default_collate(x_meta)
        collated_y = default_collate(y_batch)
        return (pad_ts, collated_x_meta), collated_y


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--safetensors_path", type=str, required=True)
    args.add_argument("--guider", type=str, required=True)

    args = args.parse_args()
    safetensors_path = Path(args.safetensors_path)
    guider = Path(args.guider)
    data_loader = AudioData(safetensors_path, guider)
    dl = DataLoader(data_loader, batch_size=10, collate_fn=AudioData.collate_function)
    print(next(iter(dl)))