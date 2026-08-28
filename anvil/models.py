from dataclasses import dataclass
import os


def _validate_positive_int(name: str, value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be a positive integer")
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _environment_positive_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a positive integer") from None
    return _validate_positive_int(name, value)


def normalize_model_identifier(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Input must be a string")

    normalized = " ".join(value.split())

    if not normalized:
        raise ValueError("Empty normalized value")

    return normalized


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
    protocol: str = "openai"

    def __post_init__(self) -> None:
        _validate_positive_int("concurrency", self.concurrency)
        _validate_positive_int("samples", self.samples)

    @classmethod
    def from_environment(cls) -> "RuntimeConfig":
        think = os.getenv("ANVIL_THINK")
        return cls(
            endpoint=os.getenv("ANVIL_ENDPOINT", cls.endpoint),
            model=normalize_model_identifier(os.getenv("ANVIL_MODEL", cls.model)),
            timeout_seconds=float(os.getenv("ANVIL_TIMEOUT", cls.timeout_seconds)),
            output_tokens=int(os.getenv("ANVIL_OUTPUT_TOKENS", cls.output_tokens)),
            temperature=float(os.getenv("ANVIL_TEMPERATURE", cls.temperature)),
            concurrency=_environment_positive_int("ANVIL_CONCURRENCY", cls.concurrency),
            samples=_environment_positive_int("ANVIL_SAMPLES", cls.samples),
            api_key=os.getenv("ANVIL_API_KEY"),
            think=None if think is None else think.lower() in {"1", "true", "yes", "on"},
            protocol=os.getenv("ANVIL_PROTOCOL", "openai"),
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
