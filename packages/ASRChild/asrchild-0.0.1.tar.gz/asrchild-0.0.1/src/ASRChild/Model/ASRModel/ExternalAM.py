from pathlib import Path

from transformers import HubertModel


class ExternalAMFactory:
    def __init__(self, weight_path: Path):
        self.model = None
        self.weight_path = weight_path

    def get_model(self) -> HubertModel:
        if self.model is None:
            self.model = HubertModel.from_pretrained(self.weight_path)
            for param in self.model.parameters():
                param.requires_grad = False
        return self.model
