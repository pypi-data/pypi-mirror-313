import json
from unittest import mock

import aws4.key_pair
import httpcore
import httpx
import pytest

from neosctl import http
from neosctl.http import Method, NeosClient


@pytest.fixture
def client():
    return NeosClient(token="token", key_pair=None, partition="ksa", service="dummy")


@pytest.fixture
def signature_client():
    return NeosClient(
        token=None,
        key_pair=aws4.key_pair.KeyPair("access-key", "access-secret"),
        partition="ksa",
        service="dummy",
    )


class TestNeosClient:
    @pytest.mark.parametrize(
        ("method", "params", "json_payload", "headers"),
        [
            (Method.GET, None, None, None),
            (Method.GET, None, None, {"auth": "token"}),
            (Method.GET, {"a": "b", "c": "d"}, None, {"auth": "token"}),
            (Method.POST, None, None, None),
            (Method.POST, None, None, {"auth": "token"}),
            (Method.POST, None, {"a": "b", "c": "d"}, {"auth": "token"}),
            (Method.PUT, None, None, None),
            (Method.PUT, None, None, {"auth": "token"}),
            (Method.PUT, None, {"a": "b", "c": "d"}, {"auth": "token"}),
            (Method.DELETE, None, None, None),
            (Method.DELETE, None, None, {"auth": "token"}),
            (Method.DELETE, None, {"a": "b", "c": "d"}, {"auth": "token"}),
        ],
    )
    def test_request(self, client, httpx_mock, method, params, json_payload, headers):
        url = "http://host"
        query = "?{}".format("&".join([f"{k}={v}" for k, v in params.items()])) if params else ""
        body = f"{json.dumps(json_payload)}".encode() if json_payload else None
        httpx_mock.add_response(
            url=f"{url}{query}",
            match_content=body,
            json={"hello": "world"},
            headers=headers,
        )

        r = client.request(
            url=url,
            method=method,
            params=params,
            headers=headers,
            json=json_payload,
        )

        assert r.json() == {"hello": "world"}

    @pytest.mark.parametrize(
        ("method", "params", "json_payload", "headers"),
        [
            (Method.GET, None, None, None),
            (Method.GET, None, None, {"auth": "token"}),
            (Method.GET, {"a": "b", "c": "d"}, None, {"auth": "token"}),
            (Method.POST, None, None, None),
            (Method.POST, None, None, {"auth": "token"}),
            (Method.POST, None, {"a": "b", "c": "d"}, {"auth": "token"}),
            (Method.PUT, None, None, None),
            (Method.PUT, None, None, {"auth": "token"}),
            (Method.PUT, None, {"a": "b", "c": "d"}, {"auth": "token"}),
            (Method.DELETE, None, None, None),
            (Method.DELETE, None, None, {"auth": "token"}),
            (Method.DELETE, None, {"a": "b", "c": "d"}, {"auth": "token"}),
        ],
    )
    def test_signed_request(self, signature_client, httpx_mock, method, params, json_payload, headers):
        url = "http://host"
        query = "?{}".format("&".join([f"{k}={v}" for k, v in params.items()])) if params else ""
        body = f"{json.dumps(json_payload)}".encode() if json_payload else None
        httpx_mock.add_response(
            url=f"{url}{query}",
            match_content=body,
            json={"hello": "world"},
            headers=headers,
        )

        r = signature_client.request(url, method, params, headers, json_payload)

        assert r.json() == {"hello": "world"}

    def test_token_request_generates_bearer_auth(self, client, monkeypatch):
        httpx_client = mock.MagicMock()
        mock_client = mock.Mock()
        httpx_client.__enter__.return_value = mock_client
        monkeypatch.setattr(http.httpx, "Client", mock.MagicMock(return_value=httpx_client))

        client.request("url", Method.GET)

        assert mock_client.request.call_args == mock.call(
            url="url",
            method="GET",
            params=None,
            json=None,
            headers=None,
            auth=http.NeosBearerClientAuth("token"),
        )

    def test_empty_token_request_excludes_auth(self, monkeypatch):
        client = NeosClient(token="", key_pair=None, service="dummy", partition="ksa")
        httpx_client = mock.MagicMock()
        mock_client = mock.Mock()
        httpx_client.__enter__.return_value = mock_client
        monkeypatch.setattr(http.httpx, "Client", mock.MagicMock(return_value=httpx_client))

        client.request("url", Method.GET)

        assert mock_client.request.call_args == mock.call(
            url="url",
            method="GET",
            params=None,
            json=None,
            headers=None,
            auth=None,
        )

    def test_signed_request_generates_signature_auth(self, signature_client, monkeypatch):
        httpx_client = mock.MagicMock()
        mock_client = mock.Mock()
        httpx_client.__enter__.return_value = mock_client
        monkeypatch.setattr(http.httpx, "Client", mock.MagicMock(return_value=httpx_client))

        signature_client.request("url", Method.GET)

        assert mock_client.request.call_args == mock.call(
            url="url",
            method="GET",
            params=None,
            json=None,
            headers=None,
            auth=http.HttpxAWS4Auth(
                aws4.key_pair.KeyPair("access-key", "access-secret"),
                "ksa",
                "service",
                http.NEOSAuthSchema,
            ),
        )

    def test_request_handles_connect_timeout(self, client, httpx_mock):
        httpx_mock.add_exception(httpcore.ConnectTimeout("Timed out"))
        with pytest.raises(http.RequestException):
            client.request("url", method=Method.GET)

    def test_request_handles_read_timeout(self, client, httpx_mock):
        httpx_mock.add_exception(httpcore.ReadTimeout("Timed out"))
        with pytest.raises(http.RequestException):
            client.request("url", method=Method.GET)

    def test_request_handles_connect_error(self, client, httpx_mock):
        httpx_mock.add_exception(httpx.ConnectError("Unable to connect"))
        with pytest.raises(http.RequestException):
            client.request("url", method=Method.GET)
