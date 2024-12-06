import logging
import os
import sys
from pathlib import Path
from unittest import TestCase

import torch

from src.ASRChild.Model.ASRModel.ExternalAM import ExternalAMFactory


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


class TestExternalAM(LogTester):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.b, self.t = 2, 24000
        self.t_set = [24000, 28000, 32000, 32001]
        self.model_factory = None
        self.weight_path = os.environ["HUBERT_WEIGHT_PATH"]

    def generate_model(self):
        if self.model_factory is None:
            self.model_factory = ExternalAMFactory(
                weight_path=Path(self.weight_path))

    def generate_input(self, t=None):
        if t is None:
            t = self.t
        return torch.randint(low=-10000, high=10000, size=(self.b, t), dtype=torch.float32)

    def test_forward(self):
        self.logger.info("Test ExternalAM")
        self.generate_model()
        model = self.model_factory.get_model()
        for t in self.t_set:
            x = self.generate_input(t=t)
            output = model(input_values=x).last_hidden_state
            self.logger.info("Test for sequence length: %d" % t)
            self.logger.info(output.shape)
            # it is supposed to be input_seq_len/320, but 24000 provides 74, 32000 provides 99
            shape_lower = t // 320 - 1
            shape_upper = t // 320 + 1
            self.assertTrue((output.shape[0] == self.b) and
                            (shape_lower <= output.shape[1] <= shape_upper) and
                            (output.shape[2] == 1024))
        self.logger.info("Test Finished")
