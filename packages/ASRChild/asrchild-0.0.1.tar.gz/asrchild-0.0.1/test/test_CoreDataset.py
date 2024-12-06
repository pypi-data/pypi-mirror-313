import logging
import os
import sys
from pathlib import Path
from unittest import TestCase

import pandas as pd
from icecream import ic
from torch.utils.data import DataLoader

from src.ASRChild.Dataset.DataPipeline.CoreDataset import CoreDataset


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


class TestCoreDataset(LogTester):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio_dir = Path(os.environ["AUDIO_DIR"])
        self.data_file = pd.read_csv(Path(os.environ["DATA_FILE"]))

    def test_a_getitem(self):
        self.logger.info("Test getitem with batch size 10")
        dataset = CoreDataset(self.data_file, self.audio_dir)
        dl = DataLoader(dataset, batch_size=10, collate_fn=CoreDataset.collate_function_generator())
        ic(len(dataset))
        ic(len(dl))
        self.assertTrue(len(dl) > 0)
        self.logger.info("Test Finished")
