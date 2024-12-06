from sourcestack.client import Client

client = Client(api_key="fake-api-key")


def test_client_api_key():
    assert client.api_key == "fake-api-key"


def test_client_base_url():
    assert client.base_url == "https://sourcestack-api.com"


def test_client_session():
    assert client.session.headers["X-API-KEY"] == "fake-api-key"
