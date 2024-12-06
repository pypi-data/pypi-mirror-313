import logging
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from typing import Union, List

import lightning as L
from lightning.pytorch.callbacks import RichProgressBar
from yaml import safe_load

from ..Dataset.DataPipeline.DataFactory import DataFactoryModule
from ..Model.ASRModel.ContextualASR import ContextualASR
from ..Training.TrainingWrap import ContextualASRWrap


def convert_to_paths(data):
    if isinstance(data, dict):
        return {key: convert_to_paths(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_to_paths(item) for item in data]
    elif isinstance(data, str):
        try:
            potential_path = Path(data)
            if potential_path.exists() or potential_path.is_absolute():
                return potential_path
        except:
            pass
    return data


def read_yaml(path: Union[Path, str]):
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    with open(path, "r") as f:
        config = safe_load(f)
    return config


def create_trainer(epochs: int = 100,
                   rich_progressbar: bool = False,
                   callback: List = None,
                   detect_anomaly=False,
                   **kwargs) -> L.Trainer:
    if callback is None:
        callbacks = []
    else:
        callbacks = callback.copy()
    if rich_progressbar is True:
        callbacks.append(RichProgressBar())
    # TODO figure out which stage to use
    trainer = L.Trainer(max_epochs=epochs, log_every_n_steps=10, callbacks=callbacks, detect_anomaly=detect_anomaly,
                        strategy="deepspeed_stage_2",
                        accelerator="gpu",
                        precision="32-true",
                        **kwargs)
    return trainer


def main(model_config_path: str, data_path: str):
    data_config = read_yaml(data_path)
    data_config = convert_to_paths(data_config)
    data_config["desired_time"] = datetime.strptime(data_config["desired_time"], "%Y-%m-%d %H:%M:%S %Z %z")
    data_factory = DataFactoryModule(**data_config, batch_size=4, training_ratio=0.8)
    # data_factory.prepare_data()
    # data_factory.setup()
    # training_dataloader = data_factory.train_dataloader()
    # validation_dataloader = data_factory.val_dataloader()
    model_config = read_yaml(model_config_path)
    model = ContextualASR(**model_config)
    logging.info("Model Loaded")
    # model = torch.compile(model)
    wrap = ContextualASRWrap(model=model)
    logging.info("Lightning Warp Loaded")
    trainer = create_trainer(rich_progressbar=True)
    logging.info("Trainer Loaded")
    # trainer.fit(wrap, train_dataloaders=training_dataloader, val_dataloaders=validation_dataloader)
    # TODO figure out what did they do to the batches
    trainer.fit(wrap, datamodule=data_factory)

if __name__ == "__main__":
    parser = ArgumentParser()
    logging.basicConfig(level=logging.INFO, force=True)
    logging.info("About to Start")
    parser.add_argument("--model_config_path", type=str, required=True)
    parser.add_argument("--data_path", type=str, required=True)
    args = parser.parse_args()
    main(args.model_config_path, args.data_path)
