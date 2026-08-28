import pytest

from anvil.models import RuntimeConfig, normalize_model_identifier


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("  qwen3.5:35b  ", "qwen3.5:35b"),
        ("NVFP4 / Qwen  30B", "NVFP4 / Qwen 30B"),
        ("\u00a0Qwen\t30B\n", "Qwen 30B"),
        ("a/b:c-d.e/\u03bb", "a/b:c-d.e/\u03bb"),
    ],
)
def test_normalize_model_identifier(value, expected):
    assert normalize_model_identifier(value) == expected


@pytest.mark.parametrize("value", ["", " \t\n", None, 1, True, False])
def test_normalize_model_identifier_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        normalize_model_identifier(value)


def test_runtime_config_normalizes_environment_model(monkeypatch):
    monkeypatch.setenv("ANVIL_MODEL", "  NVFP4 / Qwen  30B  ")

    assert RuntimeConfig.from_environment().model == "NVFP4 / Qwen 30B"


@pytest.mark.parametrize("setting", ["ANVIL_SAMPLES", "ANVIL_CONCURRENCY"])
@pytest.mark.parametrize("value", ["0", "-1", "not-an-integer"])
def test_runtime_config_rejects_invalid_environment_counts(monkeypatch, setting, value):
    monkeypatch.setenv(setting, value)

    with pytest.raises(ValueError, match="positive integer"):
        RuntimeConfig.from_environment()


@pytest.mark.parametrize("field", ["samples", "concurrency"])
@pytest.mark.parametrize("value", [True, False, 1.0, "4", 0, -2])
def test_runtime_config_rejects_non_positive_integer_counts(field, value):
    with pytest.raises(ValueError, match="positive integer"):
        RuntimeConfig(**{field: value})


def test_runtime_config_preserves_valid_values_and_routing(monkeypatch):
    monkeypatch.setenv("ANVIL_ENDPOINT", "http://example.test/v1")
    monkeypatch.setenv("ANVIL_MODEL", "NVFP4/Qwen3-30B-A3B-Instruct-2507-FP4")
    monkeypatch.setenv("ANVIL_SAMPLES", "3")
    monkeypatch.setenv("ANVIL_CONCURRENCY", "2")

    config = RuntimeConfig.from_environment()

    assert config.samples == 3
    assert config.concurrency == 2
    assert config.endpoint == "http://example.test/v1"
    assert config.model == "NVFP4/Qwen3-30B-A3B-Instruct-2507-FP4"
