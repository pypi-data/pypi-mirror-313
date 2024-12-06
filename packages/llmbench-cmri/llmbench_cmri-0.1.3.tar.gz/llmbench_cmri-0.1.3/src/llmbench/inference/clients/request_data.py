from dataclasses import dataclass, field
from typing import List, Optional, Dict, Union, Any


@dataclass(frozen=True)
class Request:
    """
    A `Request` specifies how to query a language model (given a prompt,
    complete it).  It is the unified representation for communicating with
    various APIs (e.g., GPT-3, Jurassic).
    """

    model: str = "openai/text-davinci-002"
    """Which model to query"""

    prompt: Any = None
    """What prompt do condition the language model on"""

    temperature: float = 1.0
    """Temperature parameter that governs diversity"""

    num_completions: int = 1
    """Generate this many completions (by sampling from the model)"""

    top_k_per_token: int = 1
    """Take this many highest probability candidates per token in the completion"""

    max_tokens: int = 100
    """Maximum number of tokens to generate (per completion)"""

    stop_sequences: List[str] = field(default_factory=list)
    """Stop generating once we hit one of these strings."""

    echo_prompt: bool = False
    """Should `prompt` be included as a prefix of each completion? (e.g., for
    evaluating perplexity of the prompt)"""

    top_p: float = 1
    """Same from tokens that occupy this probability mass (nucleus sampling)"""

    presence_penalty: float = 0
    """Penalize repetition (OpenAI only)"""

    frequency_penalty: float = 0
    """Penalize repetition (OpenAI only)"""

    random: Optional[str] = None
    """Used to control randomness. Expect different responses for the same
    request but with different values for `random`."""

    api_base: Optional[str] = None

    api_key: Optional[str] = None

    url: str = ""

    auth: str = ""
