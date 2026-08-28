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
