"""Per-provider call throttle tests (anthropic input-TPM). Zero API budget."""

import probe_runner


def _reset() -> None:
    probe_runner._last_call_start.clear()


def test_first_call_never_sleeps(monkeypatch):
    """No prior call to space against → no wait, even for a capped provider."""
    _reset()
    slept: list[float] = []
    monkeypatch.setattr(probe_runner.time, "monotonic", lambda: 1000.0)
    monkeypatch.setattr(probe_runner.time, "sleep", lambda s: slept.append(s))

    probe_runner.throttle("anthropic")

    assert slept == []


def test_second_call_within_interval_sleeps_remainder(monkeypatch):
    """A capped provider called 10s after the last start waits the rest of 60s."""
    _reset()
    slept: list[float] = []
    clock = {"t": 1000.0}
    monkeypatch.setattr(probe_runner.time, "monotonic", lambda: clock["t"])
    monkeypatch.setattr(probe_runner.time, "sleep", lambda s: slept.append(s))

    probe_runner.throttle("anthropic")  # records start at t=1000
    clock["t"] = 1010.0  # 10s of other work elapsed
    probe_runner.throttle("anthropic")

    assert slept == [50.0]


def test_no_sleep_when_interval_already_elapsed(monkeypatch):
    """A call that itself outlasts the interval incurs no extra wait."""
    _reset()
    slept: list[float] = []
    clock = {"t": 1000.0}
    monkeypatch.setattr(probe_runner.time, "monotonic", lambda: clock["t"])
    monkeypatch.setattr(probe_runner.time, "sleep", lambda s: slept.append(s))

    probe_runner.throttle("anthropic")
    clock["t"] = 1075.0  # big agentic call took 75s > 60s interval
    probe_runner.throttle("anthropic")

    assert slept == []


def test_uncapped_provider_never_sleeps(monkeypatch):
    """Providers absent from PROVIDER_MIN_INTERVAL_S are not throttled."""
    _reset()
    assert "gemini" not in probe_runner.PROVIDER_MIN_INTERVAL_S
    slept: list[float] = []
    clock = {"t": 1000.0}
    monkeypatch.setattr(probe_runner.time, "monotonic", lambda: clock["t"])
    monkeypatch.setattr(probe_runner.time, "sleep", lambda s: slept.append(s))

    probe_runner.throttle("gemini")
    clock["t"] = 1000.1
    probe_runner.throttle("gemini")

    assert slept == []
