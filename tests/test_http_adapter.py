"""Tests for HttpMemoryAdapter against a disposable, generic local HTTP fixture.

None of these tests contact mem0, fidelis, or any real memory store — the
fixture in tests/http_fixture.py is a stdlib HTTP server started and torn
down within each test.
"""

from __future__ import annotations

from zer0lint.http_adapter import HttpMemoryAdapter, _normalize_results

from .http_fixture import generic_http_memory_fixture


def test_add_then_search_round_trip():
    with generic_http_memory_fixture(response_shape="mem0") as (add_url, search_url):
        adapter = HttpMemoryAdapter(add_url, search_url, user_id="roundtrip-user")
        adapter.add("The API runs on port 8421.")

        response = adapter.search("port 8421", user_id="roundtrip-user")
        results = response["results"]

        assert len(results) == 1
        assert "8421" in results[0]["memory"]


def test_search_isolates_by_user_id():
    with generic_http_memory_fixture(response_shape="mem0") as (add_url, search_url):
        adapter = HttpMemoryAdapter(add_url, search_url)
        adapter.add("fact for user A", user_id="user-a")
        adapter.add("fact for user B", user_id="user-b")

        response = adapter.search("fact", user_id="user-a")

        assert len(response["results"]) == 1
        assert "user A" in response["results"][0]["memory"]


def test_search_handles_list_response_shape():
    with generic_http_memory_fixture(response_shape="list") as (add_url, search_url):
        adapter = HttpMemoryAdapter(add_url, search_url, user_id="u")
        adapter.add("plain list shape fact")

        response = adapter.search("fact", user_id="u")

        assert response["results"] == [{"memory": "plain list shape fact"}]


def test_search_handles_hits_response_shape():
    with generic_http_memory_fixture(response_shape="hits") as (add_url, search_url):
        adapter = HttpMemoryAdapter(add_url, search_url, user_id="u")
        adapter.add("elasticsearch-style fact")

        response = adapter.search("fact", user_id="u")

        assert response["results"] == [
            {"text": "elasticsearch-style fact", "memory": "elasticsearch-style fact"}
        ]


def test_add_raises_on_server_error():
    with generic_http_memory_fixture() as (_, search_url):
        error_add_url = search_url.replace("/search", "/error")
        adapter = HttpMemoryAdapter(error_add_url, search_url, user_id="u")

        try:
            adapter.add("this will fail")
            raise AssertionError("expected RuntimeError")
        except RuntimeError as e:
            assert "500" in str(e)


def test_default_user_id_is_generated_and_isolated():
    a = HttpMemoryAdapter("http://example.invalid/add", "http://example.invalid/search")
    b = HttpMemoryAdapter("http://example.invalid/add", "http://example.invalid/search")

    assert a.default_user_id.startswith("zer0lint_")
    assert a.default_user_id != b.default_user_id


def test_normalize_results_empty_and_unknown_shapes():
    assert _normalize_results({}) == []
    assert _normalize_results(None) == []
    assert _normalize_results({"unexpected": "shape"}) == []
