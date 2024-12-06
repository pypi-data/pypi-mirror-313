from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path
from typing import Union, Dict

import yaml
from icecream import ic

from ..Model.ASRModel.ContextualASR import ContextualASR
from ..Model.ASRModel.DecoderModel import Decoder, DecoderLayer
from ..Model.ASRModel.ExternalLM import LoraModelFactory, ExternalLMFactory


def save_yaml(data: Union[ContextualASR.ContextualASRConfig, Dict], path: Path):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
    print(f"Saved to {path}")


def main(audio_weight_path: Path, base_lm_weight_path: Path,
         run_path: Path, model_save_path: Path, checkpoint_path: Path,
         safetensor_dir: Path, transcribe_label_dir: Path, temp_data_saving_dir: Path,
         word_data_dir: Path, tokenized_context_dir: Path,
         model_config_path: Path, model_saves_path: Path, data_path: Path,
         desired_time: datetime):
    # model parameters that we define, hubert path, llama path
    model_config = ContextualASR.ContextualASRConfig(
        output_dim=39,
        lora_config=LoraModelFactory.LoraFactoryConfig(
            r=8,
            lora_alpha=16,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.1
        ),
        decoder_config=Decoder.DecoderConfig(
            num_layer=2,
            decoder_layer_config=DecoderLayer.DecoderLayerConfig(
                embed_dim=64,
                query_ratio=2,
                kv_heads=2,
                d_ff=128
            )
        ),
        audio_weight_path=str(audio_weight_path),
        base_lm_weight_path=str(base_lm_weight_path),
        audio_output_dim=1024,
        lm_output_dim=4096,
        quantization_config=ExternalLMFactory.ExternalQuantizationConfig(
            load_in_8bit=True,
            load_in_4bit=False
        ),
    )

    # run folder, model save folder, checkpoint etc
    model_saves = {
        "run_path": str(run_path),
        "model_save_path": str(model_save_path),
        "checkpoint_path": str(checkpoint_path)
    }

    # data
    data_dir = {
        "desired_time": desired_time.strftime("%Y-%m-%d %H:%M:%S %Z %z"),
        "safetensor_dir": str(safetensor_dir),
        "transcribe_label_dir": str(transcribe_label_dir),
        "temp_data_saving_dir": str(temp_data_saving_dir),
        "word_data_dir": str(word_data_dir),
        "llama_weight_path": str(base_lm_weight_path),
        "tokenized_context_dir": str(tokenized_context_dir)
    }

    ic(model_config)
    save_yaml(model_config, model_config_path)
    save_yaml(model_saves, model_saves_path)
    save_yaml(data_dir, data_path)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--model_config", type=str, required=True, default="model_config.yaml")
    parser.add_argument("--model_saves", type=str, required=True, default="model_saves.yaml")
    parser.add_argument("--data_path", type=str, required=True, default="data_path.yaml")
    parser.add_argument("--audio_weight_path", type=str, required=True)
    parser.add_argument("--base_lm_weight_path", type=str, required=True)
    parser.add_argument("--run_path", type=str, required=True)
    parser.add_argument("--model_save_path", type=str, required=True)
    parser.add_argument("--checkpoint_path", type=str, required=True)
    parser.add_argument("--safetensor_dir", type=str, required=True)
    parser.add_argument("--transcribe_label_dir", type=str, required=True)
    parser.add_argument("--temp_data_saving_dir", type=str, required=True)
    parser.add_argument("--word_data_dir", type=str, required=True)
    parser.add_argument("--tokenized_context_dir", type=str, required=True)
    parser.add_argument("--desired_time", type=str, required=False,
                        default=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z %z"))
    args = parser.parse_args()
    main(Path(args.audio_weight_path), Path(args.base_lm_weight_path),
         Path(args.run_path), Path(args.model_save_path), Path(args.checkpoint_path),
         Path(args.safetensor_dir), Path(args.transcribe_label_dir), Path(args.temp_data_saving_dir),
         Path(args.word_data_dir), Path(args.tokenized_context_dir),
         Path(args.model_config), Path(args.model_saves), Path(args.data_path),
         datetime.strptime(args.desired_time, "%Y-%m-%d %H:%M:%S %Z %z"))
