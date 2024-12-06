import logging
import os
import sys
from pathlib import Path
from unittest import TestCase

import torch

from src.ASRChild.Model.ASRModel.ContextualASR import ContextualASR
from src.ASRChild.Model.ASRModel.DecoderModel import Decoder, DecoderLayer
from src.ASRChild.Model.ASRModel.ExternalLM import LoraModelFactory


class LogTester(TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a custom logger
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.INFO)

        # Create handler (stdout)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        # Create formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        if not cls.logger.hasHandlers():
            cls.logger.addHandler(handler)


class TestContextualASR(LogTester):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = ContextualASR.ContextualASRConfig(
            output_dim=43,
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
            audio_weight_path=Path(os.environ["AUDIO_WEIGHT_PATH"]),
            base_lm_weight_path=Path(os.environ["BASE_LM_WEIGHT_PATH"]),
            audio_output_dim=1024,
            lm_output_dim=4096,
            quantization_config=None,
        )

    def setUp(self):
        self.logger.info("creating model ...")
        self.model = ContextualASR(**self.config)

    def test_a_hubert_new_mask(self):
        self.logger.info("Test Hubert with new mask")
        x = torch.randn(2, 24000)
        margin = torch.randint(1, 23999, (1,))[0]
        x_mask = torch.cat((torch.ones((2, margin)), torch.zeros((2, 24000 - margin))), dim=1).bool()
        output = self.model.get_hubert_output(x, x_mask)
        new_mask = self.model.get_new_x_mask_after_hubert(x_mask, output)
        self.logger.debug(type(self.model.audio_model))
        # ic(self.model.audio_model)
        self.logger.debug(output.shape)
        self.logger.debug(new_mask.shape)
        self.assertTrue(output.shape[0] == 2 and output.shape[2] == 1024 and new_mask.shape[1] == output.shape[1])
        self.logger.info("Test Finished")

    def test_b_forward(self):
        self.logger.info("Test Decoder forward")
        x = torch.randn(2, 24000)
        margin = torch.randint(1, 23999, (1,))[0]
        x_mask = torch.cat((torch.ones((2, margin)), torch.zeros((2, 24000 - margin))), dim=1).bool()
        contextual = torch.randint(1, 12800, (2, 100))
        contextual_margin = torch.randint(1, 99, (1,))[0]
        contextual_mask = torch.cat((torch.ones((2, contextual_margin)), torch.zeros((2, 100 - contextual_margin)),),
                                    dim=1).bool()
        output = self.model(x, contextual, x_mask, contextual_mask)
        self.logger.debug(output.shape)
        self.assertTrue(output.shape[0] == 2 and output.shape[-1] == self.config["output_dim"])
        self.logger.info(output)
        self.logger.info("Test Finished")
