from dataclasses import dataclass

import numpy as np


def softmax(values: np.ndarray, axis: int = -1) -> np.ndarray:
    shifted = values - np.max(values, axis=axis, keepdims=True)
    exps = np.exp(shifted)
    return exps / np.sum(exps, axis=axis, keepdims=True)


def gelu(values: np.ndarray) -> np.ndarray:
    return 0.5 * values * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (values + 0.044715 * values**3)))


def sinusoidal_positions(sequence_length: int, model_dim: int) -> np.ndarray:
    positions = np.arange(sequence_length)[:, None]
    div_terms = np.exp(np.arange(0, model_dim, 2) * (-np.log(10000.0) / model_dim))
    encodings = np.zeros((sequence_length, model_dim))
    encodings[:, 0::2] = np.sin(positions * div_terms)
    encodings[:, 1::2] = np.cos(positions * div_terms)
    return encodings


@dataclass
class TransformerConfig:
    vocab_size: int
    max_seq_len: int = 32
    model_dim: int = 32
    num_heads: int = 4
    ff_dim: int = 64
    num_layers: int = 2
    seed: int = 0

    def __post_init__(self) -> None:
        if self.model_dim % self.num_heads != 0:
            raise ValueError("model_dim must be divisible by num_heads")


class Linear:
    def __init__(self, in_features: int, out_features: int, rng: np.random.Generator, scale: float = 0.02):
        self.weight = rng.normal(0.0, scale, size=(in_features, out_features))
        self.bias = np.zeros(out_features)

    def __call__(self, inputs: np.ndarray) -> np.ndarray:
        return inputs @ self.weight + self.bias


class LayerNorm:
    def __init__(self, model_dim: int, eps: float = 1e-5):
        self.gamma = np.ones(model_dim)
        self.beta = np.zeros(model_dim)
        self.eps = eps

    def __call__(self, inputs: np.ndarray) -> np.ndarray:
        mean = np.mean(inputs, axis=-1, keepdims=True)
        variance = np.var(inputs, axis=-1, keepdims=True)
        normalized = (inputs - mean) / np.sqrt(variance + self.eps)
        return self.gamma * normalized + self.beta


class MultiHeadSelfAttention:
    def __init__(self, config: TransformerConfig, rng: np.random.Generator):
        self.num_heads = config.num_heads
        self.model_dim = config.model_dim
        self.head_dim = config.model_dim // config.num_heads
        self.query = Linear(config.model_dim, config.model_dim, rng)
        self.key = Linear(config.model_dim, config.model_dim, rng)
        self.value = Linear(config.model_dim, config.model_dim, rng)
        self.out = Linear(config.model_dim, config.model_dim, rng)

    def _split_heads(self, inputs: np.ndarray) -> np.ndarray:
        batch_size, sequence_length, _ = inputs.shape
        reshaped = inputs.reshape(batch_size, sequence_length, self.num_heads, self.head_dim)
        return np.transpose(reshaped, (0, 2, 1, 3))

    def _merge_heads(self, inputs: np.ndarray) -> np.ndarray:
        batch_size, _, sequence_length, _ = inputs.shape
        transposed = np.transpose(inputs, (0, 2, 1, 3))
        return transposed.reshape(batch_size, sequence_length, self.model_dim)

    def __call__(self, inputs: np.ndarray, causal_mask: bool = True) -> tuple[np.ndarray, np.ndarray]:
        queries = self._split_heads(self.query(inputs))
        keys = self._split_heads(self.key(inputs))
        values = self._split_heads(self.value(inputs))

        scores = np.matmul(queries, np.transpose(keys, (0, 1, 3, 2))) / np.sqrt(self.head_dim)
        if causal_mask:
            sequence_length = inputs.shape[1]
            mask = np.triu(np.ones((sequence_length, sequence_length), dtype=bool), k=1)
            scores = np.where(mask[None, None, :, :], -1e9, scores)

        weights = softmax(scores, axis=-1)
        attended = np.matmul(weights, values)
        merged = self._merge_heads(attended)
        return self.out(merged), weights


class FeedForward:
    def __init__(self, config: TransformerConfig, rng: np.random.Generator):
        self.in_proj = Linear(config.model_dim, config.ff_dim, rng)
        self.out_proj = Linear(config.ff_dim, config.model_dim, rng)

    def __call__(self, inputs: np.ndarray) -> np.ndarray:
        return self.out_proj(gelu(self.in_proj(inputs)))


class TransformerBlock:
    def __init__(self, config: TransformerConfig, rng: np.random.Generator):
        self.attention_norm = LayerNorm(config.model_dim)
        self.attention = MultiHeadSelfAttention(config, rng)
        self.ffn_norm = LayerNorm(config.model_dim)
        self.feed_forward = FeedForward(config, rng)

    def __call__(self, inputs: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        normalized_inputs = self.attention_norm(inputs)
        attention_output, attention_weights = self.attention(normalized_inputs)
        hidden = inputs + attention_output
        feed_forward_input = self.ffn_norm(hidden)
        return hidden + self.feed_forward(feed_forward_input), attention_weights


class TinyTransformer:
    def __init__(self, config: TransformerConfig):
        self.config = config
        self.rng = np.random.default_rng(config.seed)
        self.token_embedding = self.rng.normal(0.0, 0.02, size=(config.vocab_size, config.model_dim))
        self.position_embedding = sinusoidal_positions(config.max_seq_len, config.model_dim)
        self.blocks = [TransformerBlock(config, self.rng) for _ in range(config.num_layers)]
        self.final_norm = LayerNorm(config.model_dim)
        self.lm_head = Linear(config.model_dim, config.vocab_size, self.rng)

    def embed(self, token_ids: np.ndarray) -> np.ndarray:
        batch_size, sequence_length = token_ids.shape
        if sequence_length > self.config.max_seq_len:
            raise ValueError("sequence_length exceeds max_seq_len")
        token_vectors = self.token_embedding[token_ids]
        position_vectors = np.broadcast_to(
            self.position_embedding[:sequence_length],
            (batch_size, sequence_length, self.config.model_dim),
        )
        return token_vectors + position_vectors

    def forward(self, token_ids: np.ndarray, return_attentions: bool = False) -> tuple[np.ndarray, list[np.ndarray]]:
        if token_ids.ndim != 2:
            raise ValueError("token_ids must have shape (batch_size, sequence_length)")
        hidden = self.embed(token_ids.astype(np.int64, copy=False))
        attention_maps = []
        for block in self.blocks:
            hidden, attention_weights = block(hidden)
            if return_attentions:
                attention_maps.append(attention_weights)
        logits = self.lm_head(self.final_norm(hidden))
        return logits, attention_maps

    def predict_next(self, token_ids: np.ndarray) -> np.ndarray:
        logits, _ = self.forward(token_ids)
        return np.argmax(logits[:, -1, :], axis=-1)

    def generate(self, prompt: list[int], steps: int) -> list[int]:
        generated = list(prompt)
        for _ in range(steps):
            window = np.array([generated[-self.config.max_seq_len :]], dtype=np.int64)
            next_token = int(self.predict_next(window)[0])
            generated.append(next_token)
        return generated


if __name__ == "__main__":
    config = TransformerConfig(vocab_size=20, max_seq_len=8, model_dim=16, num_heads=4, ff_dim=32, num_layers=2)
    model = TinyTransformer(config)

    sample_tokens = np.array(
        [
            [1, 5, 7, 2, 0, 0, 0, 0],
            [3, 4, 9, 6, 2, 1, 0, 0],
        ],
        dtype=np.int64,
    )

    logits, attention_maps = model.forward(sample_tokens, return_attentions=True)
    print("logits shape:", logits.shape)
    print("attention map shapes:", [weights.shape for weights in attention_maps])
    print("greedy next tokens:", model.predict_next(sample_tokens))