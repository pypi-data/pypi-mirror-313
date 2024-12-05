from ml3_platform_sdk.client import ML3PlatformClient


# NB DON'T CHANGE THIS TEST ORDER BECAUSE OF SINGLETON NOT REINITIALIZED
def test_client_not_initialized():
    client: ML3PlatformClient = ML3PlatformClient('', '')
    assert client is not None
    assert client.connection is None


def test_base_initialization():
    client: ML3PlatformClient = ML3PlatformClient(
        api_key="api_key",
        url="url",
    )
    assert client is not None
    assert client.connection is not None and client.connection.initialized is True


def test_inizialization_multiclient():
    client1: ML3PlatformClient = ML3PlatformClient(
        api_key="api_key",
        url="url",
    )
    client2: ML3PlatformClient = ML3PlatformClient(
        api_key="api_key2",
        url="url2",
    )
    assert client1 is not None
    assert client1.connection is not None and client1.connection.initialized is True
    assert client2 is not None
    assert client2.connection is not None and client2.connection.initialized is True
