from pathlib import Path
from typing import TypedDict, Optional, List, Union, cast

import torch
from torch import nn
from transformers import BatchEncoding

from .DecoderModel import Decoder
from .ExternalAM import ExternalAMFactory
from .ExternalLM import LoraModelFactory, ExternalLMFactory


class ContextualASR(nn.Module):
    class ContextualASRConfig(TypedDict, total=True):
        lora_config: LoraModelFactory.LoraFactoryConfig
        decoder_config: Decoder.DecoderConfig
        audio_weight_path: Union[str, Path]
        base_lm_weight_path: Union[str, Path]
        quantization_config: Optional[ExternalLMFactory.ExternalQuantizationConfig]
        audio_output_dim: int
        lm_output_dim: int
        output_dim: int

    def __init__(self,
                 output_dim: int,
                 lora_config: LoraModelFactory.LoraFactoryConfig,
                 decoder_config: Decoder.DecoderConfig,
                 audio_weight_path: Union[str, Path],
                 base_lm_weight_path: Union[str, Path],
                 audio_output_dim: int,
                 lm_output_dim: int,
                 quantization_config: Optional[ExternalLMFactory.ExternalQuantizationConfig] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.audio_model = ExternalAMFactory(weight_path=Path(audio_weight_path)).get_model()
        self.base_lm = ExternalLMFactory(weight_path=Path(base_lm_weight_path),
                                         quantization_config=quantization_config).get_model()
        self.contextual_lora_model = LoraModelFactory(model=self.base_lm, lora_config=lora_config).get_lora_model()
        self.decoder = Decoder(**decoder_config)
        self.tokenizer = ExternalLMFactory(weight_path=Path(base_lm_weight_path)).get_tokenizer()
        self.lm_linear_adj = nn.Linear(lm_output_dim, decoder_config['decoder_layer_config']['embed_dim'])
        self.am_linear_adj = nn.Linear(audio_output_dim, decoder_config['decoder_layer_config']['embed_dim'])
        self.output_layer = nn.Linear(decoder_config["decoder_layer_config"]["embed_dim"], output_dim)

    def get_hubert_output(self, x: torch.Tensor, audio_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        return self.audio_model.forward(input_values=x, attention_mask=audio_mask).last_hidden_state

    # potential problem found while constructing test: "Text Encode Input must be Union[TextInputSequence, Tuple[InputSequence, InputSequence]]"
    def get_tokenized_output(self, x: Union[str, List[str], List[List[str]]]) -> BatchEncoding:
        return self.tokenizer(x, padding=True, return_tensors="pt", truncation=True)

    def get_contextual_output(self, x: torch.LongTensor, text_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        return self.contextual_lora_model.forward(input_ids=x, attention_mask=text_mask).last_hidden_state

    def get_new_x_mask_after_hubert(self, x_mask: torch.Tensor, output: torch.Tensor) -> torch.Tensor:
        # downsample_rate = original_input.size(1) // output.size(1)
        # # new_mask = torch.nn.MaxPool1d(kernel_size=downsample_rate, stride=downsample_rate, ceil_mode=True)(x_mask).bool()
        # new_mask = torch.nn.functional.max_pool1d(x_mask[..., torch.newaxis].float(), kernel_size=downsample_rate, stride=downsample_rate, ceil_mode=True).bool()
        # return torch.squeeze(new_mask[:, :output.size(1)], dim= -1).bool()
        x_mask: torch.LongTensor = cast(torch.LongTensor, x_mask)
        return self.audio_model._get_feature_vector_attention_mask(output.shape[1], x_mask)

    def forward(self, x: torch.Tensor,
                contextual: torch.LongTensor,
                x_mask: Optional[torch.Tensor] = None,
                contextual_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        audio_embedding = self.get_hubert_output(x, audio_mask=x_mask)
        audio_compress = self.am_linear_adj(audio_embedding)
        x_mask_hubert = self.get_new_x_mask_after_hubert(x_mask, audio_embedding) if x_mask is not None else None
        contextual_embedding = self.get_contextual_output(x=contextual, text_mask=contextual_mask)
        contextual_compress = self.lm_linear_adj(contextual_embedding)
        audio_x = self.decoder(x=audio_compress, contextual=contextual_compress, x_mask=x_mask_hubert,
                               contextual_mask=contextual_mask)
        return self.output_layer(audio_x)
