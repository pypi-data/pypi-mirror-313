import logging
import os
import sys
from pathlib import Path
from unittest import TestCase

import torch

from src.ASRChild.Model.ASRModel.ExternalLM import ExternalLMFactory, LoraModelFactory


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


class TestExternalLM(LogTester):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tokenizer = None
        self.string_input_ids = None
        self.list_string_input_ids = None

    def setUp(self):
        self.logger.info("Setting up Tokenizer and inputs")
        self.string_input = "This is a test"
        self.list_string_input = ["This is a test", "This is another test pad"]
        self.get_tokenizer()
        self.string_input_ids: torch.Tensor = self.tokenizer(self.string_input, padding=True, return_tensors="pt",
                                               truncation=True).input_ids
        self.list_string_input_ids = self.tokenizer(self.list_string_input, padding=True, return_tensors="pt",
                                                    truncation=True).input_ids

    def generate_model(self, quantization_config=None):

        return ExternalLMFactory(weight_path=Path(os.environ["LLAMA_WEIGHT_PATH"]),
                                 quantization_config=quantization_config).get_model()

    def get_tokenizer(self):
        if self.tokenizer is None:
            self.tokenizer = ExternalLMFactory(
                weight_path=Path(os.environ["LLAMA_WEIGHT_PATH"])).get_tokenizer()

    def get_lora_model(self, model):
        if model is None:
            model = self.generate_model()
        return LoraModelFactory(model=model, lora_config={
            "r": 8,
            "lora_alpha": 16,
            "target_modules": ["q_proj", "v_proj"],
            "lora_dropout": 0.1
        }).get_lora_model()

    def test_a_tokenizer(self):
        self.logger.info("Test Tokenizer with string input")
        self.logger.info(self.string_input_ids.shape)
        self.assertEqual(self.string_input_ids.shape, (1, 5))
        self.logger.info("Test Tokenizer with list of strings input")
        self.logger.info(self.list_string_input_ids.shape)
        self.assertEqual(self.list_string_input_ids.shape, (2, 6))
        self.logger.info("Test Finished")

    def test_b_model_without_quant(self):
        self.logger.info("Test ExternalLM without quantization")
        model = self.generate_model()
        output = model(input_ids=self.string_input_ids).last_hidden_state
        self.logger.info(output.shape)
        self.assertTrue((output.shape[0] == self.string_input_ids.shape[0]) and
                        (output.shape[1] == self.string_input_ids.shape[1]) and
                        (output.shape[2] == 4096))

    def test_c_lora_without_quant(self):
        self.logger.info("Test ExternalLM with lora")
        model = self.generate_model()
        lora_model = self.get_lora_model(model)
        output = lora_model(input_ids=self.string_input_ids).last_hidden_state
        self.logger.info(output.shape)
        self.assertTrue((output.shape[0] == self.string_input_ids.shape[0]) and
                        (output.shape[1] == self.string_input_ids.shape[1]) and
                        (output.shape[2] == 4096))
        self.logger.info("Test Finished")
