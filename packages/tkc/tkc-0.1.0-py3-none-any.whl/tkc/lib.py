import os

from litellm import (
    token_counter as litellm_token_counter,
    cost_per_token as litellm_cost_per_token,
)
import anthropic
from dataclasses import dataclass

from functools import lru_cache

os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
import transformers

llama3_tokenizer = transformers.AutoTokenizer.from_pretrained(
    "baseten/Meta-Llama-3-tokenizer"
)


@dataclass
class InputPromptStats:
    model: str
    tokens: int
    price: float
    price_cached: float

    def __str__(self):
        return f"{self.model} n={self.tokens} (${self.price:.2f}, ${self.price_cached:.2f} cached)"


class TokenCounter:
    def __init__(self, text: str):
        self.text = text
        self._msg = {"role": "user", "content": self.text}

    @lru_cache
    def _count_anthropic_claude_3(self) -> int:
        client = anthropic.Anthropic()
        response = client.beta.messages.count_tokens(
            model="claude-3-5-sonnet-20241022", messages=[self._msg]
        )
        return response.input_tokens

    @lru_cache
    def _count_openai_cl200k_base(self) -> int:
        return litellm_token_counter(model="gpt-4o", messages=[self._msg])

    @lru_cache
    def _count_openai_cl100k_base(self) -> int:
        return litellm_token_counter(model="gpt-4-turbo", messages=[self._msg])

    @lru_cache
    def _count_llama(self) -> int:
        return len(llama3_tokenizer.tokenize(self.text))

    @lru_cache
    def _count_gemini(self) -> int:
        return litellm_token_counter(model="gemini-1.5-pro-002", messages=[self._msg])

    def _with_provider(model: str, provider: str):
        return f"{provider}/{model}"

    def for_model(
        self, model: str, provider: str | None = "together_ai"
    ) -> InputPromptStats:
        if any(map(model.startswith, ("claude", "anthropic"))):
            count = self._count_anthropic_claude_3()
        elif model.startswith("gpt-4o") or model.startswith("o1"):
            count = self._count_openai_cl200k_base()
        elif model.startswith("gpt-4"):
            count = self._count_openai_cl100k_base()
        elif model.startswith("gemini"):
            count = self._count_gemini()
            model = f"gemini/{model}"
        elif model.startswith("llama") or model.startswith("meta-llama"):
            count = self._count_llama()
            model = f"{provider}/{model}"
        else:
            raise ValueError(f"Unsupported model: {model}")

        price, _ = litellm_cost_per_token(model=model, prompt_tokens=count)
        cached, _ = litellm_cost_per_token(
            model=model, prompt_tokens=count, cache_read_input_tokens=count
        )
        return InputPromptStats(model, count, price, cached)


if __name__ == "__main__":
    token_counter = TokenCounter("Hello, world!")
    print(token_counter.for_model("gpt-4o"))
    print(token_counter.for_model("claude-3-5-sonnet-20241022"))
