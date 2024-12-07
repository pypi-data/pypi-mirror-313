import pytest
from fast_depends import inject
from good_common.dependencies import BaseProvider, AsyncBaseProvider


def test__basic_base_provider():
    class FakeClient:
        def __init__(self, host: str, port: int):
            self.host = host
            self.port = port

        def __str__(self):
            return f"{self.host}:{self.port}"

    class ClientProvider(BaseProvider[FakeClient], FakeClient):
        pass

    @inject
    def test_client(client: FakeClient = ClientProvider(host="localhost", port=8080)):
        assert client.host == "localhost"
        assert client.port == 8080

    test_client()


def test__dependency_with_runtime_config():
    class FakeClient:
        def __init__(self, host: str, port: int, db: str):
            self.host = host
            self.port = port
            self.db = db

        def __str__(self):
            return f"{self.host}:{self.port}:{self.db}"

    class ClientProvider(BaseProvider[FakeClient], FakeClient):
        def initializer(self, cls_args: tuple, cls_kwargs: dict, fn_kwargs: dict):
            if fn_kwargs.get("db"):
                cls_kwargs["db"] = fn_kwargs["db"]
            return cls_args, cls_kwargs

    @inject
    def test_client(
        db: str,
        client: FakeClient = ClientProvider(host="localhost", port=8080),
    ):
        assert client.host == "localhost"
        assert client.port == 8080
        assert client.db == "test"

    test_client(db="test")


@pytest.mark.asyncio
async def test__basic_async_base_provider():
    class FakeClient:
        def __init__(self, host: str, port: int):
            self.host = host
            self.port = port

        def __str__(self):
            return f"{self.host}:{self.port}"

    class ClientProvider(AsyncBaseProvider[FakeClient], FakeClient):
        pass

    @inject
    async def test_client(
        client: FakeClient = ClientProvider(host="localhost", port=8080),
    ):
        assert client.host == "localhost"
        assert client.port == 8080

    await test_client()
