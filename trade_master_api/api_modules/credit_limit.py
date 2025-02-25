from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional

from trade_master_api.base import (
    BaseConsult,
    BaseConsultResponse,
    BaseTradeMasterAPI,
    from_dict,
)


class CreditLimitStatus(Enum):
    NEW = 'new'
    COMPLETED = 'completed'
    NEUROTECH_PENDING = 'neurotechPending'
    CANCELED = 'canceled'
    BLOCKED = 'blocked'


class CreditLimitType(Enum):
    CONCESSION = 'concession'
    REVIEW = 'review'


@dataclass
class Centralizer:
    document: Optional[str] = None


@dataclass
class SalesPerson:
    name: Optional[str] = None
    email: Optional[str] = None


@dataclass
class Address:
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    postalCode: str
    complement: Optional[str] = None
    country: Optional[str] = 'BR'


@dataclass
class FinancialHistoryItem:
    transactionNumber: str
    installmentNumber: str
    ticketNumber: str
    billingDate: str
    dueDate: str
    amount: float
    paidAmount: float
    settled: bool
    paymentDate: Optional[str] = None


@dataclass
class RequestCreditLimit:
    buyerDocument: str
    buyerName: str
    address: Address
    billingContact: str
    billingEmail: str
    businessPhone: str
    businessEmail: str
    buyerDocumentType: Literal['CPF', 'CNPJ'] = 'CNPJ'
    birthDate: Optional[str] = None
    stateRegistration: Optional[str] = None
    cityRegistration: Optional[str] = None
    suggestedCreditLimit: Optional[float] = None
    externalCustomerCode: Optional[str] = None
    branch: Optional[str] = None
    profile: Optional[str] = None
    groupCode: Optional[str] = None
    salesMan: Optional[str] = None
    regional: Optional[str] = None
    billingPhone: Optional[str] = None
    businessModel: Optional[Literal['whiteFlag', 'b2b']] = None
    centralizer: Optional[Centralizer] = None
    salesPerson: Optional[SalesPerson] = None
    financialHistory: List[FinancialHistoryItem] = None


@dataclass
class RequestCreditLimitResponse:
    id: Optional[str] = None
    buyerDocument: Optional[str] = None
    status: Optional[CreditLimitStatus] = None
    type: Optional[CreditLimitType] = None
    externalCustomerCode: Optional[str] = None
    buyerName: Optional[str] = None


@dataclass
class ConsultCreditLimit(BaseConsult):
    id: Optional[str] = None
    buyerDocument: Optional[str] = None
    status: Optional[CreditLimitStatus] = None
    externalCustomerCode: Optional[CreditLimitType] = None
    createdAt: Optional[str] = None


@dataclass
class DetailedCreditLimit(RequestCreditLimitResponse):
    result: Optional[str] = None
    reason: Optional[str] = None
    suggestedCreditLimit: Optional[float] = None
    approvedLimit: Optional[float] = None
    creditLimitApprovedAt: Optional[datetime] = None
    hasEconomicGroup: Optional[bool] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    def __post_init__(self):
        if isinstance(self.creditLimitApprovedAt, str):
            self.creditLimitApprovedAt = datetime.strptime(
                self.creditLimitApprovedAt, '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        if isinstance(self.createdAt, str):
            self.createdAt = datetime.strptime(
                self.createdAt, '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        if isinstance(self.updatedAt, str):
            self.updatedAt = datetime.strptime(
                self.updatedAt, '%Y-%m-%dT%H:%M:%S.%fZ'
            )


@dataclass
class ConsultCreditLimitResponse(BaseConsultResponse):
    data: List[DetailedCreditLimit] = None


class CreditLimitAPI(BaseTradeMasterAPI):
    BASE_ENDPOINT = 'creditLimitRequest'

    @classmethod
    def request(cls, request_credit_limit: RequestCreditLimit):
        json = asdict(request_credit_limit)
        response = cls._send_request(method='POST', json=json)
        data = response.json()
        return from_dict(RequestCreditLimitResponse, data)

    @classmethod
    def consult(cls, params: ConsultCreditLimit = None):
        params = {} if params is None else asdict(params)
        response = cls._send_request(method='GET', params=params)
        data = response.json()
        return from_dict(ConsultCreditLimitResponse, data)
