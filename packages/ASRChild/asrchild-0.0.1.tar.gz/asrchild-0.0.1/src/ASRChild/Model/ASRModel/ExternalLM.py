from pathlib import Path
from typing import Optional
from typing import TypedDict

import peft
import transformers
from peft import get_peft_model
from transformers import LlamaModel, PreTrainedTokenizerFast, BitsAndBytesConfig


class ExternalLMFactory:
    class ExternalQuantizationConfig(TypedDict, total=False):
        load_in_8bit: bool
        load_in_4bit: bool

    def __init__(self,
                 weight_path: Path,
                 quantization_config: Optional[ExternalQuantizationConfig] = None
                 ):
        self.model = None
        self.weight_path = weight_path
        self.tokenizer = None
        self.pad_token = None
        self.quantization_config = BitsAndBytesConfig(
            **quantization_config) if quantization_config is not None else None

    def get_model(self) -> LlamaModel:
        if self.model is None:
            dict_config = {
                "pretrained_model_name_or_path": self.weight_path
            }
            if self.quantization_config is not None:
                dict_config["quantization_config"] = self.quantization_config
            self.model = LlamaModel.from_pretrained(**dict_config)
            for param in self.model.parameters():
                param.requires_grad = False
        return self.model

    def get_tokenizer(self) -> PreTrainedTokenizerFast:
        """
        finetune right pad id is 128004
        """
        if self.tokenizer is None:
            self.tokenizer = transformers.AutoTokenizer.from_pretrained(self.weight_path)
            self.tokenizer.pad_token = "<|finetune_right_pad_id|>" if self.pad_token is None else self.pad_token
        return self.tokenizer


class LoraModelFactory:
    """
    Factory to create LoRA model from the original model,
    the original model weights are frozen from gradient updates
    """

    class LoraFactoryConfig(TypedDict, total=True):
        r: int
        lora_alpha: int
        target_modules: list[str]
        lora_dropout: float

    def __init__(self,
                 model: LlamaModel,
                 lora_config: LoraFactoryConfig
                 ):
        """
        :param model: Model with frozen weights
        :param lora_config:
        """
        self.model = model
        self.lora_config = peft.LoraConfig(**lora_config)
        self.lora_model = None

    def get_lora_model(self) -> LlamaModel:
        if self.lora_model is None:
            self.lora_model = get_peft_model(self.model, self.lora_config)
        return self.lora_model
