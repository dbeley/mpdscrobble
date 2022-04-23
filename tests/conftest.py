import pylast
import pytest


@pytest.fixture(autouse=True)
def no_httpx(monkeypatch):
    """Remove httpx.Client for all tests."""
    monkeypatch.delattr("httpx.Client")


class MockSessionKeyGenerator:
    @staticmethod
    def get_session_key(self, *args, **kwargs):
        return "1234"


@pytest.fixture()
def mock_pylast_session_key_generator(monkeypatch):
    def mock_session_key_generator(*args, **kwargs):
        return MockSessionKeyGenerator()

    monkeypatch.setattr(pylast, "SessionKeyGenerator", mock_session_key_generator)
