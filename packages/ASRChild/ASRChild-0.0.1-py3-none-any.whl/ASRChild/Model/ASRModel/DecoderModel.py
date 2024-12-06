from typing import Optional
from typing import TypedDict

import torch
import torch.nn as nn
from torch import Tensor
from torchtune import modules


class SwiGLU(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.swishB_linear = nn.Linear(hidden_dim, hidden_dim)
        self.GLU_linear = nn.Linear(hidden_dim, hidden_dim)
        # Beta is a learnable scaler
        self.beta = nn.Parameter(torch.ones(1))

    def forward(self, x):
        x_1 = self.swishB_linear(x)
        swish_b = x_1 * torch.sigmoid(x_1 * self.beta)
        x_2 = self.GLU_linear(x)
        return x_2 * swish_b


class FFN(nn.Module):
    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(d_model, d_ff),
            SwiGLU(d_ff),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model)
        )
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.norm(x + self.model(x))


class WrappedCasualSelfAttention(nn.Module):
    """
    Wrap Casual Self Attention, include projection layer and positional encoding and everything
    """

    def __init__(self, embed_dim: int,
                 query_ratio: int,
                 kv_heads: int,
                 max_seq_len: int = 16392,
                 attn_dropout: float = 0.0, **kwargs):
        super().__init__(**kwargs)
        num_heads = kv_heads * query_ratio
        self.q_proj = nn.Linear(embed_dim, embed_dim * num_heads)
        self.k_proj = nn.Linear(embed_dim, embed_dim * kv_heads)
        self.v_proj = nn.Linear(embed_dim, embed_dim * kv_heads)
        self.output_proj = nn.Linear(embed_dim * num_heads, embed_dim)
        self.pos = modules.RotaryPositionalEmbeddings(embed_dim, max_seq_len=max_seq_len)
        self.attn = modules.MultiHeadAttention(
            embed_dim=embed_dim * num_heads, # num_heads * head_dim
            num_heads=num_heads,
            num_kv_heads=kv_heads,
            head_dim=embed_dim, # head dim input
            attn_dropout=attn_dropout,
            max_seq_len=max_seq_len,
            q_proj=self.q_proj,
            k_proj=self.k_proj,
            v_proj=self.v_proj,
            pos_embeddings=self.pos,
            output_proj=self.output_proj,
        )
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x: Tensor, mask: Optional[Tensor] = None) -> Tensor:
        # Use Checkpoint to save memory
        # x_attn = deepspeed.checkpointing.checkpoint(partial(self.attn, mask=mask), x, x)
        # Direct call for debugging
        # map mask to [b, s, s] for causal attention if mask is not None
        x_attn = self.attn(x, x, mask=mask)
        return self.norm(x + x_attn)


class WrappedCasualCrossAttention(nn.Module):

    def __init__(self, embed_dim: int,
                 query_ratio: int,
                 kv_heads: int,
                 max_seq_len: int = 16392,
                 attn_dropout: float = 0.0, **kwargs):
        super().__init__(**kwargs)
        num_heads = kv_heads * query_ratio
        self.q_proj = nn.Linear(embed_dim, embed_dim * num_heads)
        self.k_proj = nn.Linear(embed_dim, embed_dim * kv_heads)
        self.v_proj = nn.Linear(embed_dim, embed_dim * kv_heads)
        self.output_proj = nn.Linear(embed_dim * num_heads, embed_dim)
        self.pos = modules.RotaryPositionalEmbeddings(embed_dim, max_seq_len=max_seq_len)
        self.attn = modules.MultiHeadAttention(
            embed_dim=embed_dim * num_heads,  # num_heads * head_dim
            num_heads=num_heads,
            num_kv_heads=kv_heads,
            head_dim=embed_dim,  # head dim input
            attn_dropout=attn_dropout,
            max_seq_len=max_seq_len,
            q_proj=self.q_proj,
            k_proj=self.k_proj,
            v_proj=self.v_proj,
            pos_embeddings=self.pos,
            output_proj=self.output_proj,
        )
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self,
                x: Tensor,
                contextual: Tensor,
                mask: Optional[Tensor] = None) -> Tensor:
        # Use Checkpoint to save memory
        # x_attn = deepspeed.checkpointing.checkpoint(partial(self.attn, mask=mask), x, x)
        # Direct call for debugging
        x_attn = self.attn(x, contextual, mask=mask)
        return self.norm(x + x_attn)


class DecoderLayer(nn.Module):
    class DecoderLayerConfig(TypedDict, total=False):
        embed_dim: int
        query_ratio: int
        kv_heads: int
        d_ff: int
        max_seq_len: int
        dropout: float

    def __init__(self, embed_dim: int, query_ratio: int, kv_heads: int, d_ff: int, max_seq_len: int = 16392,
                 dropout: float = 0.1, **kwargs):
        super().__init__(**kwargs)
        self.self_attn = WrappedCasualSelfAttention(embed_dim=embed_dim, query_ratio=query_ratio, kv_heads=kv_heads, max_seq_len=max_seq_len)
        self.cross_attn = WrappedCasualCrossAttention(embed_dim=embed_dim, query_ratio=query_ratio, kv_heads=kv_heads, max_seq_len=max_seq_len)
        self.ffn = FFN(d_model=embed_dim, d_ff=d_ff, dropout=dropout)

    def forward(self, x: Tensor,
                contextual: Tensor,
                self_attention_mask: Optional[Tensor] = None,
                cross_attention_mask: Optional[Tensor] = None) -> Tensor:
        x = self.self_attn(x, mask=self_attention_mask)
        x = self.cross_attn(x, contextual, mask=cross_attention_mask)
        return self.ffn(x)


def gen_self_attention_mask(x_mask: Tensor) -> Tensor:
    casual_mask = torch.tril(torch.ones(x_mask.size(-1), x_mask.size(-1), device=x_mask.device), diagonal=0).bool()
    padding_mask = x_mask.unsqueeze(-2) & x_mask.unsqueeze(-1)
    # ic(x_mask.device, padding_mask.device)
    # TODO figure out why two tensors are on different devices
    mask = torch.logical_and(casual_mask, padding_mask)
    return mask


def gen_cross_attention_mask(x_mask: Tensor, contextual_mask: Tensor) -> Tensor:
    x_mask = x_mask.unsqueeze(-1)  # [b, s_x, 1]
    mask_contextual = contextual_mask.unsqueeze(-2)  # [b, 1, s_c]
    # use broadcasting to generate the mask with boolean values
    mask = x_mask & mask_contextual  # [b, s_x, s_c]
    return mask


class Decoder(nn.Module):
    class DecoderConfig(TypedDict, total=True):
        num_layer: int
        decoder_layer_config: DecoderLayer.DecoderLayerConfig

    def __init__(self, num_layer: int, decoder_layer_config: DecoderLayer.DecoderLayerConfig, **kwargs):
        super().__init__(**kwargs)
        self.layers = nn.ModuleList([DecoderLayer(**decoder_layer_config) for _ in range(num_layer)])

    def forward(self, x: Tensor,
                contextual: Tensor,
                x_mask: Optional[Tensor] = None,
                contextual_mask: Optional[Tensor] = None) -> Tensor:
        # ic(x_mask, contextual_mask)
        x_mask: torch.Tensor = torch.ones_like(x[..., 0], device=x.device).bool() if x_mask is None else x_mask.bool()
        contextual_mask: torch.Tensor = torch.ones_like(
            contextual[..., 0], device=x.device).bool() if contextual_mask is None else contextual_mask.bool()
        self_attn_mask = gen_self_attention_mask(x_mask.to(x.device))
        cross_attn_mask = gen_cross_attention_mask(x_mask.to(x.device), contextual_mask.to(x.device))
        for layer in self.layers:
            x = layer(x, contextual, self_attention_mask=self_attn_mask, cross_attention_mask=cross_attn_mask)
        return x
