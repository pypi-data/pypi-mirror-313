import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import lightning as L
import pandas as pd
import torch
from safetensors.torch import save_file, load_file
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import PreTrainedTokenizerFast

from ...Dataset.DataPipeline.CoreDataset import CoreDataset, special_symbol_map, get_char_map_table
from ...Model.ASRModel.ExternalLM import ExternalLMFactory


class DataFactoryModule(L.LightningDataModule):
    def __init__(self, safetensor_dir: Path, transcribe_label_dir: Path,
                 temp_data_saving_dir: Path, word_data_dir: Path,
                 llama_weight_path: Path, tokenized_context_dir: Path,
                 training_ratio: float, batch_size: int,
                 split_seed: Optional[int] = None,
                 desired_time: Optional[datetime] = None,
                 force_regenerate: bool = False,
                 check_hash: bool = False,
                 minimum_required_length: int = 16000,
                 maximum_length_after_hubert: int = 16384,
                 discard_abnormal_std_threshold: float = 1.e-3,
                 **kwargs):
        super().__init__()
        self.safe_tensor_dir = safetensor_dir
        self.transcribe_label_dir = transcribe_label_dir
        self.temp_data_saving_dir = temp_data_saving_dir
        self.force_regenerate = force_regenerate
        self.word_data_dir = word_data_dir
        self.llama_weight_path = llama_weight_path
        self.tokenized_context_dir = tokenized_context_dir
        self.check_hash = check_hash
        self.special_symbol_map: Dict = special_symbol_map()
        self.char_map_table: Dict = get_char_map_table()
        self.training_ratio = training_ratio
        self.split_seed = split_seed
        self.maximum_length_after_hubert = maximum_length_after_hubert
        self.batch_size = batch_size
        self.train_dataset: Optional[CoreDataset] = None
        self.validation_dataset: Optional[CoreDataset] = None
        self.pin_memory: bool = False
        self.multiprocess_load = True
        self.minimum_required_length = minimum_required_length
        self.discard_abnormal_std_threshold = discard_abnormal_std_threshold
        if not desired_time:
            self.desired_time = datetime.now(timezone.utc)
        else:
            self.desired_time = desired_time
        self.version_control = self.temp_data_saving_dir / "version.txt"

    def generation_condition(self) -> bool:
        if not self.version_control.exists():
            self.version_control.parent.mkdir(parents=True, exist_ok=True)
            return True
        with open(self.version_control, 'r') as f:
            version_datetime = datetime.strptime(f.readline(), "%Y-%m-%d %H:%M:%S %Z %z")
        if self.desired_time > version_datetime:
            return True
        return self.force_regenerate

    def save_tokenized_context(self, context_tokenized: torch.Tensor, context_file_dir: Path) -> None:
        if context_file_dir.exists():
            if self.check_hash:
                previous_tokenized = load_file(context_file_dir)
                assert torch.equal(previous_tokenized['input_ids'], context_tokenized)
        else:
            save_file({"input_ids": context_tokenized}, context_file_dir)

    def hash_and_tokenize(self, context: str, tokenizer: PreTrainedTokenizerFast) -> (torch.Tensor, Path):
        context_hash = hashlib.md5(context.encode()).hexdigest()
        context_file_dir = self.tokenized_context_dir / (context_hash + ".safetensors")
        context_tokenized = tokenizer(context, return_tensors="pt").input_ids
        return context_tokenized, context_file_dir

    def fix_transcribe(self, transcribe: str) -> str:
        transcribe = transcribe.lower()
        for k in self.special_symbol_map:
            transcribe = transcribe.replace(k, self.special_symbol_map[k])
        for char in transcribe:
            if char not in self.char_map_table.values():
                transcribe = transcribe.replace(char, "")
        return transcribe

    def exam_audio(self, audio_id) -> bool:
        audio_file_dir = self.safe_tensor_dir / audio_id
        struct = load_file(audio_file_dir)
        if (struct["audio_tensor"].shape[0] < self.minimum_required_length or
                struct['audio_std'] < self.discard_abnormal_std_threshold or
                struct["audio_tensor"].shape[0] // 320 >= self.maximum_length_after_hubert):
            return False
        return True

    def prepare_data(self) -> None:
        word_cache: Dict = {}
        tokenizer = ExternalLMFactory(weight_path=self.llama_weight_path).get_tokenizer()
        logging.info(f"Loaded tokenizer from {self.llama_weight_path} ...")
        counter = {"accepted": 0, "rejected": 0}
        if self.generation_condition():
            self.initialize_save()
            with open(self.transcribe_label_dir, 'r') as f:
                transcribe_label = json.load(f)
            column_names: List[str] = ["audio_id", "transcribe", "word", "task", "context_type", "context",
                                       "tokenized_context_dir"]
            dataframe: pd.DataFrame = pd.DataFrame(columns=column_names)
            for audio_id in tqdm(transcribe_label):
                if not self.exam_audio(audio_id):
                    logging.debug(f"Audio {audio_id} is not suitable for training")
                    counter["rejected"] += 1
                    continue
                counter["accepted"] += 1
                word = transcribe_label[audio_id]["word"]
                task = transcribe_label[audio_id]["task"]
                transcribe = transcribe_label[audio_id]["transcribe"]
                # remove non string
                if type(transcribe) != str or transcribe == "nan":
                    logging.debug(f"Transcribe for '{word}' is not a string")
                    continue
                transcribe = self.fix_transcribe(transcribe)
                if word not in word_cache:
                    word_dir = self.word_data_dir / (word.replace(" ", "_") + ".json")
                    try:
                        with open(word_dir, 'r') as f:
                            word_data = json.load(f)
                    except FileNotFoundError:
                        logging.warning(f"Word data for '{word}' : '{word_dir}' not found")
                        continue
                    word_cache[word] = word_data
                word_instance = {
                    "audio_id": audio_id,
                    "transcribe": transcribe,
                    "word": word,
                    "task": task,
                    "context_type": "question"
                }
                if task == "Definition":
                    # definition task only have one context, which is the question being asked
                    context = word_cache[word]["definition_question"]
                    context_tokenized, context_file_dir = self.hash_and_tokenize(context, tokenizer)
                    self.save_tokenized_context(context_tokenized, context_file_dir)
                    word_instance["context"] = context
                    word_instance["tokenized_context_dir"] = context_file_dir
                    dataframe = pd.concat([dataframe, pd.DataFrame([word_instance])], ignore_index=True)
                elif task == "Sentence":
                    # sentence task have two context, the question being asked and the example sentences
                    context = word_cache[word]["sentence_question"]
                    context_tokenized, context_file_dir = self.hash_and_tokenize(context, tokenizer)
                    self.save_tokenized_context(context_tokenized, context_file_dir)
                    word_instance["context"] = context
                    word_instance["tokenized_context_dir"] = context_file_dir
                    dataframe = pd.concat([dataframe, pd.DataFrame([word_instance])], ignore_index=True)
                    # adding example sentences next
                    word_instance["context_type"] = "example sentence"
                    for example_sentence in word_cache[word]["sentence_context_candidates"]:
                        context = example_sentence
                        context_tokenized, context_file_dir = self.hash_and_tokenize(context, tokenizer)
                        self.save_tokenized_context(context_tokenized, context_file_dir)
                        word_instance["context"] = example_sentence
                        word_instance["tokenized_context_dir"] = context_file_dir
                        dataframe = pd.concat([dataframe, pd.DataFrame([word_instance])], ignore_index=True)
            dataframe.to_csv(self.temp_data_saving_dir / "data.csv", index=False)
            logging.info(f"Data generation finished, {counter['accepted']} accepted, {counter['rejected']} rejected")
            del tokenizer

    def initialize_save(self):
        version_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z %z")
        logging.info(f"Generating data with version {version_time} ...")
        if self.tokenized_context_dir.exists():
            logging.info("Removing old hashed context files ...")
            for item in self.tokenized_context_dir.iterdir():
                if item.is_file():
                    item.unlink()
        else:
            logging.info("Creating hashed context directory ...")
            self.tokenized_context_dir.mkdir(parents=True, exist_ok=True)
        with open(self.version_control, 'w') as f:
            f.write(version_time)

    def split_dataframe(self, dataframe: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        shuffled_df = dataframe.sample(frac=1, random_state=self.split_seed).reset_index(drop=True)
        split_index = int(self.training_ratio * len(shuffled_df))
        return shuffled_df.iloc[:split_index, :], shuffled_df.iloc[split_index:, :]

    def setup(self, stage: str = None):
        dataframe = pd.read_csv(self.temp_data_saving_dir / "data.csv")
        training_df, validation_df = self.split_dataframe(dataframe)
        self.train_dataset = CoreDataset(data_file=training_df, audio_dir=self.safe_tensor_dir)
        self.validation_dataset = CoreDataset(data_file=validation_df, audio_dir=self.safe_tensor_dir)

    def train_dataloader(self):
        if self.train_dataset is not None:
            return DataLoader(self.train_dataset,
                              batch_size=self.batch_size,
                              num_workers=self.calculate_num_workers(),
                              collate_fn=CoreDataset.collate_function_generator(),
                              pin_memory=self.pin_memory)
        else:
            raise ValueError("train dataset not setup correctly")

    def val_dataloader(self):
        if self.train_dataset is not None:
            return DataLoader(self.validation_dataset,
                              batch_size=self.batch_size,
                              num_workers=os.cpu_count() if self.multiprocess_load else 0,
                              collate_fn=CoreDataset.collate_function_generator(),
                              pin_memory=self.pin_memory)
        else:
            raise ValueError("val dataset not setup correctly")

    def calculate_num_workers(self, max_workers: int = 32):
        if self.multiprocess_load:
            nums = int(os.getenv("SLURM_CPUS_PER_TASK", os.cpu_count()))
            return min(max_workers, nums)
        else:
            return 0


    # def test_dataloader(self):
    #     return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=self.num_workers,
    #                       collate_fn=default_collate, pin_memory=self.pin_memory)
