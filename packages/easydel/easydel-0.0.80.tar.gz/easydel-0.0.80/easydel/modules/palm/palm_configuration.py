# Copyright 2023 The EASYDEL Author @erfanzar (Erfan Zare Chavoshi).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional

from jax.sharding import PartitionSpec

from easydel.modules.factory import register_config
from easydel.modules.modeling_utils import EasyDeLBaseConfig


@register_config("palm")
class PalmConfig(EasyDeLBaseConfig):
	def __init__(
		self,
		vocab_size: Optional[int] = 32000,
		hidden_size: Optional[int] = 4096,
		dim_head: Optional[int] = None,
		num_hidden_layers: Optional[int] = 32,
		num_attention_heads: Optional[int] = 32,
		up_inner_dim: Optional[int] = 4,
		eps: Optional[float] = 1e-5,
		max_length: int = 8196,  # Easydel trained palm with length of 8196
		bos_token_id: int = 0,
		eos_token_id: int = 1,
		gradient_checkpointing="nothing_saveable",
		use_tie_word_embedding: bool = True,
		**kwargs,
	):
		dim_head = dim_head if dim_head is not None else hidden_size // num_attention_heads
		self.dim_head = dim_head
		self.up_inner_dim = up_inner_dim
		self.gradient_checkpointing = gradient_checkpointing
		self.num_attention_heads = num_attention_heads
		self.use_tie_word_embedding = use_tie_word_embedding
		self.num_hidden_layers = num_hidden_layers
		self.hidden_size = hidden_size
		self.vocab_size = vocab_size
		self.eps = eps
		self.max_length = max_length
		super().__init__(bos_token_id=bos_token_id, eos_token_id=eos_token_id, **kwargs)

	@staticmethod
	def _set_config_defaults(config, config_defaults):
		for k, v in config_defaults.items():
			if k not in config:
				config[k] = v
		return config

	@staticmethod
	def get_partition_rules(fully_sharded_data_parallel: bool = False):
		return (
			(
				("wi/kernel", PartitionSpec("fsdp")),
				("attn_wo/kernel", PartitionSpec("fsdp", "dp")),
				("ff_wo/kernel", PartitionSpec("fsdp", "dp")),
				("wte/embedding", PartitionSpec("fsdp", "dp")),
				("lm_head/kernel", PartitionSpec("fsdp")),
				("post_norm/kernel", PartitionSpec("fsdp")),
				("norm/kernel", PartitionSpec("fsdp", "dp")),
				(".*", PartitionSpec(("fsdp", "sp"))),
			)
			if not fully_sharded_data_parallel
			else (
				("wi/kernel", PartitionSpec("fsdp")),
				("attn_wo/kernel", PartitionSpec("fsdp")),
				("ff_wo/kernel", PartitionSpec("fsdp")),
				("wte/embedding", PartitionSpec("fsdp")),
				("lm_head/kernel", PartitionSpec("fsdp")),
				("post_norm/kernel", PartitionSpec("fsdp")),
				("norm/kernel", PartitionSpec("fsdp")),
				(".*", PartitionSpec("fsdp")),
			)
		)

	def add_jax_args(
		self,
		**kwargs,
	): ...
