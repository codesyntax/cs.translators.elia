from cs.translators.elia.utility import _cache_key_translate_content
from cs.translators.elia.utility import ELIATranslationService
from plone.base.utils import safe_bytes
from unittest.mock import Mock
from uuid import uuid4

import hashlib
import json
import pytest
import time


PREFIX = "cs.translators.elia.e_l_i_a_control_panel"

RECORDS = {
    f"{PREFIX}.api_base_url": "https://api.example.com",
    f"{PREFIX}.api_id": "test-id",
    f"{PREFIX}.api_key": "test-key",
    f"{PREFIX}.timeout": 5,
    f"{PREFIX}.translation_engine": "nmt",
    f"{PREFIX}.enabled": True,
    f"{PREFIX}.order": 30,
    f"{PREFIX}.source_languages": [],
    f"{PREFIX}.target_languages": [],
}


class FakeResponse:
    def __init__(self, body: bytes):
        self._body = body

    def read(self) -> bytes:
        return self._body


@pytest.fixture
def registry(monkeypatch):
    """Patch the registry access to a plain in-memory mapping."""

    def fake_get_registry_record(name, *args, **kwargs):
        try:
            return RECORDS[name]
        except KeyError:
            raise KeyError(name) from None

    monkeypatch.setattr(
        "plone.api.portal.get_registry_record", fake_get_registry_record
    )
    return RECORDS


@pytest.fixture
def http(monkeypatch):
    """Patch urlopen, recording every call and returning a fixed body."""
    calls = []

    def fake_urlopen(req, timeout=None):
        calls.append((req, timeout))
        body = json.dumps({"translated_text": "kaixo"}).encode("utf-8")
        return FakeResponse(body)

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    return calls


class TestIsAvailable:
    def test_enabled_by_default(self, registry):
        assert ELIATranslationService.is_available() is True

    def test_disabled(self, registry, monkeypatch):
        monkeypatch.setitem(RECORDS, f"{PREFIX}.enabled", False)
        assert ELIATranslationService.is_available() is False

    def test_missing_record(self, monkeypatch):
        monkeypatch.setattr(
            "plone.api.portal.get_registry_record",
            Mock(side_effect=KeyError("missing")),
        )
        assert ELIATranslationService.is_available() is False


class TestOrder:
    def test_order(self, registry):
        assert ELIATranslationService.order == 30


class TestAvailableLanguages:
    def test_pairs_are_lowercased_and_skip_same_language(self, monkeypatch):
        records = {
            f"{PREFIX}.source_languages": ["eu", "es"],
            f"{PREFIX}.target_languages": ["eu", "fr"],
        }
        monkeypatch.setattr(
            "plone.api.portal.get_registry_record",
            lambda name, *a, **kw: records[name],
        )
        assert ELIATranslationService.available_languages() == [
            ("eu", "fr"),
            ("es", "eu"),
            ("es", "fr"),
        ]

    def test_all_languages_when_empty(self, monkeypatch):
        records = {
            f"{PREFIX}.source_languages": [],
            f"{PREFIX}.target_languages": [],
        }
        monkeypatch.setattr(
            "plone.api.portal.get_registry_record",
            lambda name, *a, **kw: records[name],
        )
        assert ELIATranslationService.available_languages() == []

    @pytest.mark.xfail(
        reason=(
            "source/target languages are compared before being lowercased"
            " (utility.py available_languages), so ES/es yields a same-language pair"
        ),
        strict=False,
    )
    def test_same_language_different_case(self, monkeypatch):
        records = {
            f"{PREFIX}.source_languages": ["ES"],
            f"{PREFIX}.target_languages": ["es"],
        }
        monkeypatch.setattr(
            "plone.api.portal.get_registry_record",
            lambda name, *a, **kw: records[name],
        )
        assert ELIATranslationService.available_languages() == []


class TestTranslateContent:
    def test_request_payload_and_response(self, registry, http):
        content = f"hello-{uuid4().hex}"
        result = ELIATranslationService.translate_content(content, "es", "eu")

        assert result == "kaixo"
        assert len(http) == 1

        req, timeout = http[0]
        assert req.full_url == "https://api.example.com/translate_string"
        assert req.get_method() == "POST"
        assert timeout == 5
        assert json.loads(req.data.decode("utf-8")) == {
            "api_id": "test-id",
            "api_key": "test-key",
            "translation_engine": "nmt",
            "language_pair": "es-eu",
            "content_type": "html",
            "text": content,
        }
        assert req.headers["Content-type"] == "application/json"
        assert req.headers["Accept"] == "application/json"

    def test_missing_translated_text_returns_empty_string(self, registry, monkeypatch):
        def fake_urlopen(req, timeout=None):
            return FakeResponse(b"{}")

        monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
        content = f"hello-{uuid4().hex}"
        assert ELIATranslationService.translate_content(content, "es", "eu") == ""

    def test_result_is_cached(self, registry, http):
        content = f"hello-{uuid4().hex}"
        first = ELIATranslationService.translate_content(content, "es", "eu")
        second = ELIATranslationService.translate_content(content, "es", "eu")

        assert first == second == "kaixo"
        assert len(http) == 1


class TestCacheKey:
    def test_cache_key_format(self, monkeypatch):
        monkeypatch.setattr(time, "time", lambda: 5 * 3600)
        content = "hello world"
        digest = hashlib.sha512(safe_bytes(content)).hexdigest()
        assert (
            _cache_key_translate_content(None, None, content, "es", "eu")
            == f"elia-translate-es-eu-{digest}-5"
        )

    def test_cache_key_changes_with_content(self, monkeypatch):
        monkeypatch.setattr(time, "time", lambda: 5 * 3600)
        first = _cache_key_translate_content(None, None, "one", "es", "eu")
        second = _cache_key_translate_content(None, None, "two", "es", "eu")
        assert first != second
