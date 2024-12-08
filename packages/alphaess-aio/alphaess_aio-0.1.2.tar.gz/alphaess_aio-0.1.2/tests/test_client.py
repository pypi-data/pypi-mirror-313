from unittest import mock
import pytest
from alphaessaio import client

# values taken from docs
MY_TEST_SECRET = "c2d2ef6c047c49678e2c332fb2d74c3c"
MY_TEST_APP_ID = "alphaef7900ee81dbbce9"


@pytest.fixture
def mocked_response(request):
    status, data = request.param
    mocked_client_response = mock.MagicMock(spec=client.aiohttp.ClientResponse)
    mocked_client_response.status = status
    mocked_client_response.json.return_value = data

    return mocked_client_response


@pytest.fixture
def auth() -> client.AlphaEssAuth:
    return client.AlphaEssAuth(appid=MY_TEST_APP_ID, appsecret=MY_TEST_SECRET)


@pytest.fixture
def alphaess_api(auth: client.AlphaEssAuth, mocker) -> client.AlphaEssAPI:
    return client.AlphaEssAPI(auth)


def test_create_headers_works(auth: client.AlphaEssAuth, mocker):
    mocked_timestamp = "1676353875"
    mocker.patch("alphaessaio.client.time.time", return_value=mocked_timestamp)
    assert auth.create_headers() == {
        "appId": MY_TEST_APP_ID,
        "timeStamp": mocked_timestamp,
        "sign": "0f023c2287b8f6b21b0994947465f8e"
        "9de0e1542567b1735bdc6c427336b9b6406285cd9"
        "4f9215c3e9af958df37fb11c2c9fe792713d8afbdb8c463359a1add8",
    }


@pytest.mark.parametrize(
    "mocked_response",
    [(200, {"data": "something", "code": 200})],
    indirect=True,
)
@pytest.mark.asyncio
async def test_evaluate_response_valid(mocked_response):
    assert await client.AlphaEssAPI._evaluate_response(mocked_response) == {
        "data": "something",
        "code": 200,
    }


@pytest.mark.parametrize(
    "mocked_response",
    [
        (200, {"data": "something"}),
        (200, {"data": "something", "code": 400}),
        (400, {"data": "something", "code": 400}),
    ],
    indirect=True,
)
@pytest.mark.asyncio
async def test_evaluate_response_invalid(mocked_response):
    with pytest.raises(client.AlphaEssRequestError):
        await client.AlphaEssAPI._evaluate_response(mocked_response)


@pytest.mark.asyncio
async def test_get_called_correctly(alphaess_api, mocker):
    class MockResponse:
        def __init__(self, url, text, status):
            self.url = url
            self._text = text
            self.status = status

        async def text(self):
            return self._text

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def __aenter__(self):
            return self

        async def json(self):
            return self._text

    mocker.patch.object(
        client.aiohttp.ClientSession,
        "get",
        return_value=MockResponse("bla", {"data": "xyz", "code": 200}, 200),
    )

    await alphaess_api._get("bla", "blub")


def test_post_called_correctly():
    pass
