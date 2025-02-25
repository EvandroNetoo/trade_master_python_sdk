import os
from abc import ABC
from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Dict, Literal, Optional, Type, TypeVar
from urllib.parse import urljoin

from requests import Response, request

from trade_master_api.access_token import AcessToken

from .exceptions import raise_for_status


class BaseTradeMasterAPI(ABC):
    PRODUCTION_BASE_URL = 'https://apigateway.trademaster.com.br/v2/agreement/'
    DEBUG_BASE_URL = 'https://apigateway.hml.trademaster.com.br/v2/agreement/'

    DEBUG = os.environ.get('DEBUG', '1') == '1'

    CLIENT_ID = os.environ.get('TRADE_MASTER_CLIENT_ID', '')
    CLIENT_SECRET = os.environ.get('TRADE_MASTER_CLIENT_SECRET', '')

    BASE_ENDPOINT: str

    @classmethod
    def get_base_url(cls) -> str:
        if cls.DEBUG:
            return cls.DEBUG_BASE_URL
        return cls.PRODUCTION_BASE_URL

    @classmethod
    def _mount_url(cls, extra_endpoint: str = '') -> str:
        url = urljoin(cls.get_base_url(), cls.BASE_ENDPOINT)

        if extra_endpoint:
            url = urljoin(url, extra_endpoint)

        return url.strip('/')

    @classmethod
    def _send_request(  # noqa: PLR0913
        cls,
        *,
        method: Literal['GET', 'POST', 'PUT', 'DELETE'] = 'GET',
        extra_endpoint: str = '',
        headers: dict[str, str] = None,
        params: dict[str, str] = None,
        data: dict = None,
        json: dict | list = None,
        authenticate: bool = True,
    ) -> Response:
        if not isinstance(headers, dict):
            headers = {}
        if not isinstance(params, dict):
            params = {}
        if not isinstance(data, dict):
            data = None
        if not isinstance(json, (dict, list)):
            json = None

        url = cls._mount_url(extra_endpoint)

        request_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json; charset=utf-8',
        }
        if headers:
            request_headers.update(headers)
        if authenticate:
            request_headers['Authorization'] = f'Bearer {AcessToken()}'

        response = request(
            method=method,
            url=url,
            headers=request_headers,
            params=params,
            data=data,
            json=json,
            timeout=10,
        )

        raise_for_status(response)

        return response


@dataclass
class BaseConsult:
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None


@dataclass
class BaseConsultResponse:
    totalCount: int
    pageNumber: int
    pageSize: int
    data: list[dict]


T = TypeVar('T')  # Tipo genérico para representar qualquer dataclass


def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
    """Converte um dicionário para uma instância de uma dataclass, incluindo atributos que são outras dataclasses ou listas delas."""
    if not is_dataclass(cls):
        raise ValueError(f'{cls} não é uma dataclass')

    processed_data: Dict[str, Any] = {}

    for field in fields(cls):  # Obtém os campos da dataclass
        key = field.name
        field_type = field.type

        if key in data:
            value = data[key]

            if is_dataclass(
                field_type
            ):  # Se for outra dataclass, chamar recursivamente
                processed_data[key] = from_dict(field_type, value)

            elif (
                hasattr(field_type, '__origin__')
                and field_type.__origin__ is list
                and is_dataclass(field_type.__args__[0])
            ):  # Lista de dataclasses
                processed_data[key] = [
                    from_dict(field_type.__args__[0], item) for item in value
                ]

            else:  # Qualquer outro tipo de dado (int, str, etc.)
                processed_data[key] = value

    return cls(**processed_data)
