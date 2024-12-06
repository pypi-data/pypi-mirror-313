from typing import Union, TypedDict, Optional

import lightning as L
import torch
import torchmetrics
from deepspeed.ops.adam import FusedAdam
from torch.optim.lr_scheduler import StepLR

from ..Model.ASRModel.CTCDecoder import GreedyCTCDecoder
from ..Model.ASRModel.ContextualASR import ContextualASR


class ContextualASRWrap(L.LightningModule):
    class ContextualASRWrapConfig(TypedDict, total=True):
        lr: float
        step_reduce: int
        step_gamma: float

    def __init__(self, model: Union[ContextualASR, torch.nn.Module],
                 lr: float = 1e-5, step_reduce: int = 100,
                 step_gamma: float = 0.1, **kwargs):
        super().__init__()
        self.model: ContextualASR = model
        self.lr, self.step_reduce, self.step_gamma = lr, step_reduce, step_gamma
        self.criterion = torch.nn.CTCLoss(blank=0, zero_infinity=True)
        self.train_metrics = torchmetrics.MetricCollection(
            {
                "wer": torchmetrics.text.WordErrorRate(),
            },
            prefix="train_",
        )
        self.valid_metrics = self.train_metrics.clone(prefix="valid_")
        self.decoder = GreedyCTCDecoder()

    def forward(self, x: torch.Tensor,
                contextual: torch.LongTensor,
                x_mask: Optional[torch.Tensor] = None,
                contextual_mask: Optional[torch.Tensor] = None) -> torch.Tensor:

        return self.model.forward(x=x, contextual=contextual, x_mask=x_mask, contextual_mask=contextual_mask)

    def _shared_step(self, batch, batch_idx, stage='train'):
        x, y = batch
        audio_data, tokenized_context, audio_data_mask, content_mask = x
        tokenized_transcribe, ctc_target_length, transcribe = y
        y_hat: torch.Tensor = self.model(audio_data, tokenized_context, audio_data_mask, content_mask)
        ctc_input_length = self.model.get_new_x_mask_after_hubert(audio_data_mask, y_hat).sum(dim=-1)
        log_prob = torch.nn.functional.log_softmax(y_hat.to(dtype=torch.float32), dim=-1)
        log_prob = log_prob.permute(1, 0, 2)
        loss = self.criterion(log_probs=log_prob,
                              targets=tokenized_transcribe,
                              input_lengths=ctc_input_length,
                              target_lengths=ctc_target_length)
        with torch.no_grad():
            decoded = self.decoder(log_prob)
            if stage == 'train':
                metrics = self.train_metrics(decoded, transcribe)
                metrics["train_loss"] = loss
            if stage == 'valid':
                metrics = self.valid_metrics(decoded, transcribe)
                metrics["valid_loss"] = loss
        return metrics

    def on_train_epoch_end(self) -> None:
        self.train_metrics.reset()

    def on_validation_epoch_end(self) -> None:
        self.log("valid_full_wer", self.valid_metrics.compute()["valid_wer"])
        self.valid_metrics.reset()

    def training_step(self, batch, batch_idx):
        metrics = self._shared_step(batch, batch_idx, 'train')
        self.log_dict(metrics, on_step=True, on_epoch=True, prog_bar=True)
        return metrics["train_loss"]

    def validation_step(self, batch, batch_idx):
        metrics = self._shared_step(batch, batch_idx, 'valid')
        self.log_dict(metrics, on_step=False, on_epoch=True, prog_bar=True)
        return metrics["valid_loss"]

    def configure_optimizers(self):
        # TODO figure out which adam to use, also pair with deepspeed
        opti = FusedAdam(self.model.parameters(), lr=self.lr)
        scheduler = StepLR(opti, step_size=self.step_reduce, gamma=self.step_gamma)
        return [opti], [
            {
                'scheduler': scheduler,
                'interval': 'epoch',
            }
        ]
