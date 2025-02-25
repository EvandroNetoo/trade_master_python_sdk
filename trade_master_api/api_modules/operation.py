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


class InvoiceType(Enum):
    PRODUCT = 'produto'
    SERVICE = 'servico'


class ContentType(Enum):
    XML = 'xml'
    PDF = 'pdf'


@dataclass
class PostOperationProcessRequest:
    @dataclass
    class Invoice:
        @dataclass
        class Content:
            type: ContentType
            value: str

        type: InvoiceType
        invoiceDate: str
        amount: float
        discount: float
        content: list
        validationKey: str
        extendedDays: Optional[int]

    @dataclass
    class Ticket:
        amount: float
        dueDate: str
        installmentNumber: int
        discount: float | None = None
        ticketNumber: str | None = None
        operationalExternalNumber: str | None = None

    authorizationCode: str
    buyerDocument: str
    sellerDocument: str
    invoices: list[Invoice]
    tickets: list[Ticket]


@dataclass
class PostOperationProcessResponse:
    @dataclass
    class Ticket:
        installmentNumber: int
        dueDate: str
        ticketNumber: str
        amount: float
        discount: float

    operationCode: str
    tickets: list[Ticket]


@dataclass
class GetOperationProcessRequest(BaseConsult):
    operationCode: str | None = None
    authorizationCode: str | None = None
    sellerDocument: str | None = None
    createdAt: str | None = None


@dataclass
class GetOperationProcessResponse(BaseConsultResponse):
    @dataclass
    class Operation:
        class Invoice:
            type: InvoiceType | None = None
            number: str | None = None
            series: str | None = None
            validationCode: str | None = None

        class Ticket:
            installmentNumber: int | None = None
            dueDate: str | None = None
            ticketNumber: str | None = None
            amount: float | None = None
            discount: float | None = None

            def __post_init__(self):
                if isinstance(self.dueDate, str):
                    self.dueDate = datetime.fromisoformat(self.dueDate)

        operationCode: str | None = None
        buyerDocument: str | None = None
        sellerDocument: str | None = None
        invoices: list[Invoice] | None = None
        authorizationCode: str | None = None
        createdAt: datetime | None = None
        tickets: list[Ticket] | None = None

    data: list[Operation] | None = None


class OperationAPI(BaseTradeMasterAPI):
    BASE_ENDPOINT = 'operation'

    @classmethod
    def process(cls, data: PostOperationProcessRequest):
        json = asdict(data)
        response = cls._send_request(method='POST', json=json)
        return from_dict(PostOperationProcessResponse, response.json())

    @classmethod
    def consult(cls, params: GetOperationProcessRequest = None):
        params = {} if params is None else asdict(params)
        response = cls._send_request(method='GET', params=params)
        return from_dict(GetOperationProcessResponse, response.json())
