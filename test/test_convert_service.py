import pytest

from src.service.base import HTTPXClient
from src.service.сurrency_сonvert import ConvertService
from src.сore.error import AppException


@pytest.mark.asyncio
async def test_convert_service_ok():
    httpx_client = HTTPXClient()
    convert_service = ConvertService(httpx_client)
    await convert_service.convert(amount=100, from_currency='USD', to_currency='RUB')


@pytest.mark.asyncio
async def test_convert_service_error_in_currency():
    httpx_client = HTTPXClient()
    convert_service = ConvertService(httpx_client)
    with pytest.raises(AppException):
        await convert_service.convert(amount=100, from_currency='UasdasdsdSD', to_currency='RUB')
