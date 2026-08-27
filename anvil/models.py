from dataclasses import dataclass
import os


@dataclass(frozen=True)
class RuntimeConfig:
    endpoint: str = "http://127.0.0.1:8010/v1"
    model: str = "NVFP4/Qwen3-30B-A3B-Instruct-2507-FP4"
    timeout_seconds: float = 60.0
    output_tokens: int = 160
    temperature: float = 0.0
    concurrency: int = 4
    samples: int = 8
    api_key: str | None = None
    think: bool | None = None

    @classmethod
    def from_environment(cls) -> "RuntimeConfig":
        think = os.getenv("ANVIL_THINK")
        return cls(
            endpoint=os.getenv("ANVIL_ENDPOINT", cls.endpoint),
            model=os.getenv("ANVIL_MODEL", cls.model),
            timeout_seconds=float(os.getenv("ANVIL_TIMEOUT", cls.timeout_seconds)),
            output_tokens=int(os.getenv("ANVIL_OUTPUT_TOKENS", cls.output_tokens)),
            temperature=float(os.getenv("ANVIL_TEMPERATURE", cls.temperature)),
            concurrency=int(os.getenv("ANVIL_CONCURRENCY", cls.concurrency)),
            samples=int(os.getenv("ANVIL_SAMPLES", cls.samples)),
            api_key=os.getenv("ANVIL_API_KEY"),
            think=None if think is None else think.lower() in {"1", "true", "yes", "on"},
        )


@dataclass(frozen=True)
class InferenceResponse:
    text: str
    actual_model: str
    prompt_tokens: int | None
    output_tokens: int | None
    reasoning_tokens: int | None
    total_tokens: int | None
    finish_reason: str | None
    raw_response: dict[str, object]
