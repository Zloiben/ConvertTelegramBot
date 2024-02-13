from typing import runtime_checkable, Protocol, Optional

from httpx import AsyncClient, ConnectTimeout, HTTPStatusError, RequestError

from src.сore.const import SERVICE_UNAVAILABLE_503, INTERNAL_SERVER_ERROR_500
from src.сore.enum import HTTPMethods
from src.сore.error import AppException

__all__ = (
    'AsyncHTTPClientProtocol',
    'HTTPXClient'
)


@runtime_checkable
class AsyncHTTPClientProtocol(Protocol):

    async def send_request(
            self,
            url: str,
            method: HTTPMethods,
            body: Optional[dict] = None,
            params: Optional[dict] = None
    ) -> dict:
        ...


class HTTPXClient:

    def __init__(self, timeout: float = 10.0):
        self._client = AsyncClient(timeout=timeout)

    async def send_request(
            self,
            url: str,
            method: HTTPMethods = HTTPMethods.GET,
            body: Optional[dict] = None,
            params: Optional[dict] = None
    ) -> dict:
        try:
            response = await self._client.request(method.value, url, json=body, params=params)
            response.raise_for_status()
            return response.json()
        except ConnectTimeout as e:
            raise AppException(status_code=SERVICE_UNAVAILABLE_503, message='Сервис временно не доступен')
        except HTTPStatusError as e:
            raise AppException(
                status_code=e.response.status_code, content=e.response.json(), message='Проблема при обработке'
            )
        except RequestError as e:
            raise AppException(
                status_code=INTERNAL_SERVER_ERROR_500, content={'error': str(e)}, message='Проблема при обработке'
            )
