from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from trade_master_api.base import (
    BaseConsult,
    BaseConsultResponse,
    BaseTradeMasterAPI,
    from_dict,
)


class AuthorizationStatus(Enum):
    CANCELLED = 'CANCELLED'
    AUTHORIZED = 'AUTHORIZED'
    CAPTURED = 'CAPTURED'


@dataclass
class Authorization:
    sellerDocument: str
    amount: float
    isSplit: bool


@dataclass
class RequestAuthorization:
    buyerDocument: str
    authorizations: list[Authorization]


@dataclass
class ConsultAuthorization(BaseConsult):
    authorizationCode: Optional[str] = None
    sellerDocument: Optional[str] = None


@dataclass
class DetailedAuthorization:
    amount: float
    createdAt: str
    authorizationCode: str
    isConfirmed: bool
    isSplit: bool
    status: AuthorizationStatus


@dataclass
class DetailedConsultAuthorization:
    buyerDocument: str
    authorizations: list[DetailedAuthorization]


@dataclass
class ConsultAuthorizationResponse(BaseConsultResponse):
    data: list[DetailedConsultAuthorization]


@dataclass
class AuthorizationExtensionResponse:
    authorizationCode: str
    newExpireDate: str
    oldExpireDate: str
    dateCreated: str

    def __post_init__(self):
        if isinstance(self.newExpireDate, str):
            self.newExpireDate = datetime.strptime(
                self.newExpireDate, '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        if isinstance(self.oldExpireDate, str):
            self.oldExpireDate = datetime.strptime(
                self.oldExpireDate, '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        if isinstance(self.dateCreated, str):
            self.dateCreated = datetime.strptime(
                self.dateCreated, '%Y-%m-%dT%H:%M:%S.%fZ'
            )


class AuthorizationAPI(BaseTradeMasterAPI):
    BASE_ENDPOINT = 'authorization/'

    @classmethod
    def request(cls, request_authorization: RequestAuthorization):
        """Solicitar reserva do saldo disponível."""
        json = asdict(request_authorization)
        response = cls._send_request(method='POST', json=json)
        data = response.json()
        return data

    @classmethod
    def consult(cls, params: RequestAuthorization = None):
        """Consultar Limite reservado da autorização ou cliente."""
        params = {} if params is None else asdict(params)
        response = cls._send_request(method='GET', params=params)
        data = response.json()
        return from_dict(ConsultAuthorizationResponse, data)

    @classmethod
    def reverse(cls, authorization_code: str):
        """Solicitar estorno de reserva, quando pedido for cancelado ou modificado para valor maior."""
        json = [{'authorizationCode': authorization_code}]
        cls._send_request(
            method='POST',
            extra_endpoint='reverse',
            json=json,
        )

    @classmethod
    def extend(cls, authorization_code: str):
        """Estender a data de validade de uma autorização."""
        json = {'authorizationCode': authorization_code}
        response = cls._send_request(
            method='POST',
            extra_endpoint='extension',
            json=json,
        )
        return from_dict(AuthorizationExtensionResponse, response.json())
