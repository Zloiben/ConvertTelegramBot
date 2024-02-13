from src.config import config
from src.сore.enum import HTTPMethods
from .base import AsyncHTTPClientProtocol

__all__ = (
    'ConvertService',
)


class ConvertService:
    """
    Класс для работы с сервисом конвертации валют
    """
    BASE_URL = f'https://v6.exchangerate-api.com/v6/{config.CONVERT_SERVICE_TOKEN}'

    def __init__(self, client: AsyncHTTPClientProtocol):
        self.client = client

    async def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        response = await self.client.send_request(
            url=self.BASE_URL + f'/pair/{from_currency}/{to_currency}/{amount}', method=HTTPMethods.GET
        )
        return response['conversion_result']
