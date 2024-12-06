import logging
import os
import sys
from pathlib import Path
from unittest import TestCase

from icecream import ic

from src.ASRChild.Dataset.DataPipeline.DataFactory import DataFactoryModule


class LogTester(TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a custom logger
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.INFO)
        logging.basicConfig(level=logging.DEBUG)
        # Create handler (stdout)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        # Create formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # mp.set_start_method("spawn")
        # Add the handler to the logger
        os.environ['TOKENIZERS_PARALLELISM'] = 'false'
        if not cls.logger.hasHandlers():
            cls.logger.addHandler(handler)


class TestDataFactoryModule(LogTester):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.safetensor_dir = Path(os.environ["SAFETENSOR_DIR"])
        self.transcribe_label_dir = Path(os.environ["TRANSCRIBE_LABEL_DIR"])
        self.temp_data_saving_dir = Path(os.environ["TEMP_DATA_SAVING_DIR"])
        self.word_data_dir = Path(os.environ["WORD_DATA_DIR"])
        self.llama_weight_path = Path(os.environ["LLAMA_WEIGHT_PATH"])
        self.tokenized_context_dir = Path(os.environ["TOKENIZED_CONTEXT_DIR"])
        self.training_ratio = 0.8
        self.batch_size = 10
        self.data_factory = None

    def setUp(self):
        self.logger.info("Setting up DataFactoryModule")
        self.data_factory = DataFactoryModule(safetensor_dir=self.safetensor_dir,
                                              transcribe_label_dir=self.transcribe_label_dir,
                                              temp_data_saving_dir=self.temp_data_saving_dir,
                                              word_data_dir=self.word_data_dir,
                                              llama_weight_path=self.llama_weight_path,
                                              tokenized_context_dir=self.tokenized_context_dir,
                                              training_ratio=self.training_ratio,
                                              batch_size=self.batch_size)

    # def test_a_prepare(self):
    #     self.logger.info("Test prepare with no desired time, no force regenerate, not checking hash")
    #     self.data_factory.prepare_data()
    #     self.assertTrue(self.data_factory.version_control.exists())
    #     self.assertTrue((self.data_factory.temp_data_saving_dir / "data.csv").exists())
    #     self.logger.info("Test Finished")

    # def test_b_prepare(self):
    #     self.logger.info("Test prepare with no desired time, no force regenerate, checking_hash")
    #     self.data_factory.prepare_data()
    #     self.assertTrue(self.data_factory.version_control.exists())
    #     self.assertTrue((self.data_factory.temp_data_saving_dir / "data.csv").exists())
    #     self.logger.info("Test Finished")

    def test_c_dataloaders(self):
        self.logger.info("Test training and validation dataloaders")
        self.data_factory.setup()
        training_dataloader = self.data_factory.train_dataloader()
        validation_dataloader = self.data_factory.val_dataloader()
        training_data_next = next(iter(training_dataloader))
        validation_data_next = next(iter(validation_dataloader))
        ic(len(training_dataloader))
        ic(len(validation_dataloader))
        self.assertEqual(len(training_data_next), 2)
        self.assertEqual(len(validation_data_next), 2)
        self.assertEqual(len(training_data_next[0]), 4)
        self.assertEqual(len(training_data_next[1]), 3)
        self.assertEqual(training_data_next[0][0].shape[0], self.batch_size)
        ic(training_data_next[1][2])
        self.logger.info("Test Finished")
