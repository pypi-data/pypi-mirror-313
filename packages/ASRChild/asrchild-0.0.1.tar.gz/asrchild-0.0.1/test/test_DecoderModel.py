import logging
import sys
from unittest import TestCase

import torch

from src.ASRChild.Model.ASRModel.DecoderModel import (WrappedCasualSelfAttention, WrappedCasualCrossAttention,
                                                      DecoderLayer, gen_self_attention_mask, gen_cross_attention_mask,
                                                      Decoder)


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

class TestWarpedCasualSelfAttention(LogTester):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.b, self.t, self.emb = 2, 10, 64

    def generate_model(self):
        return WrappedCasualSelfAttention(
            embed_dim=64,
            query_ratio=2,
            kv_heads=2
        )

    def generate_input(self, t=None):
        if t is None:
            t = self.t
        return torch.randn(self.b, t, self.emb)

    def test_forward(self):
        self.logger.info("Test Wrapped Casual Self Attention without a mask")
        model = self.generate_model()
        x = self.generate_input()

        output = model(x)
        # print (output.shape) for test case
        self.logger.info(output.shape)
        self.assertEqual(output.shape, (self.b, self.t, self.emb))
        self.logger.info("Test Finished")

    def test_fw_mask(self):
        self.logger.info("Test Wrapped Casual Self Attention with a mask")
        model = self.generate_model()
        x = self.generate_input()
        mask = torch.ones_like(x).bool()[..., 0]
        mask = gen_self_attention_mask(mask)
        output = model(x, mask)
        # print (output.shape) for test case
        self.logger.info(output.shape)
        self.assertEqual(output.shape, (self.b, self.t, self.emb))
        self.logger.info("Test Finished")

class TestWrappedCasualCrossAttention(TestWarpedCasualSelfAttention):

    def generate_model(self):
        return WrappedCasualCrossAttention(
            embed_dim=64,
            query_ratio=2,
            kv_heads=2
        )

    def test_forward(self):
        self.logger.info("Test Wrapped Cross Attention without masks")
        model = self.generate_model()
        x = self.generate_input()
        c = self.generate_input(3)

        output = model(x, c)
        # print (output.shape) for test case
        self.logger.info(output.shape)
        self.assertEqual(output.shape, (self.b, self.t, self.emb))
        self.logger.info("Test Finished")

    def test_fw_mask(self):
        self.logger.info("Test Wrapped Cross Attention with masks")
        model = self.generate_model()
        x = self.generate_input()
        c = self.generate_input(3)
        mask_x = torch.ones_like(x).bool()[..., 0]
        mask_c = torch.ones_like(c).bool()[..., 0]
        cross_att_mask = gen_cross_attention_mask(mask_x, mask_c)
        output = model(x, c, mask=cross_att_mask)
        # print (output.shape) for test case
        self.logger.info(output.shape)
        self.assertEqual(output.shape, (self.b, self.t, self.emb))
        self.logger.info("Test Finished")


class TestDecoderLayer(LogTester):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.embed_dim = 64
        self.query_ratio = 2
        self.kv_heads = 2
        self.d_ff = 128

    def generate_model(self):
        return DecoderLayer(
            embed_dim=self.embed_dim,
            query_ratio=self.query_ratio,
            kv_heads=self.kv_heads,
            d_ff=self.d_ff
        )

    def test_forward(self):
        self.logger.info("Test Decoder Layer without masks")
        model = self.generate_model()
        x = torch.randn(2, 10, self.embed_dim)
        c = torch.randn(2, 3, self.embed_dim)
        output = model(x, c)
        # print (output.shape) for test case
        self.logger.info(output.shape)
        self.assertEqual(output.shape, (2, 10, self.embed_dim))
        self.logger.info("Test Finished")

    def test_fw_mask(self):
        self.logger.info("Test Decoder Layer with masks")
        model = self.generate_model()
        x = torch.randn(2, 10, self.embed_dim)
        c = torch.randn(2, 3, self.embed_dim)
        mask_x = torch.ones_like(x).bool()[..., 0]
        mask_c = torch.ones_like(c).bool()[..., 0]
        self_att_mask = gen_self_attention_mask(mask_x)
        cross_att_mask = gen_cross_attention_mask(mask_x, mask_c)
        output = model(x, c, self_attention_mask=self_att_mask, cross_attention_mask=cross_att_mask)
        # print (output.shape) for test case
        self.logger.info(output.shape)
        self.assertEqual(output.shape, (2, 10, self.embed_dim))
        self.logger.info("Test Finished")


class TestDecoder(TestDecoderLayer):

    def __init__(self, *args, **kwargs):
        self.num_layer = 3
        super().__init__(*args, **kwargs)

    def generate_model(self):
        return Decoder(
            num_layer=self.num_layer,
            decoder_layer_config={
                "embed_dim": self.embed_dim,
                "query_ratio": self.query_ratio,
                "kv_heads": self.kv_heads,
                "d_ff": self.d_ff
            }
        )

    def test_forward(self):
        self.logger.info("Test Decoder without masks")
        model = self.generate_model()
        x = torch.randn(2, 10, self.embed_dim)
        c = torch.randn(2, 3, self.embed_dim)
        output = model(x, c)
        # print (output.shape) for test case
        self.logger.info(output.shape)
        self.assertEqual(output.shape, (2, 10, self.embed_dim))
        self.logger.info("Test Finished")

    def test_fw_mask(self):
        self.logger.info("Test Decoder with masks")
        model = self.generate_model()
        x = torch.randn(2, 10, self.embed_dim)
        c = torch.randn(2, 3, self.embed_dim)
        mask_x = torch.ones_like(x).bool()[..., 0]
        mask_c = torch.ones_like(c).bool()[..., 0]
        output = model(x, c, x_mask=mask_x, contextual_mask=mask_c)
        # print (output.shape) for test case
        self.logger.info(output.shape)
        self.assertEqual(output.shape, (2, 10, self.embed_dim))
        self.logger.info("Test Finished")
