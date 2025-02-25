from trade_master_api.api_modules.authentication import AuthenticationAPI
from trade_master_api.api_modules.authorization import AuthorizationAPI
from trade_master_api.api_modules.credit_limit import CreditLimitAPI
from trade_master_api.api_modules.operation import OperationAPI
from trade_master_api.base import BaseTradeMasterAPI


class TradeMasterAPI:
    @classmethod
    def get_debug(cls) -> bool:
        return BaseTradeMasterAPI.DEBUG

    @classmethod
    def set_debug(cls, debug: bool) -> None:
        BaseTradeMasterAPI.DEBUG = debug

    @classmethod
    def get_client_id(cls) -> dict:
        return BaseTradeMasterAPI.CLIENT_ID

    @classmethod
    def set_client_id(cls, client_id: str) -> None:
        BaseTradeMasterAPI.CLIENT_ID = client_id

    @classmethod
    def get_client_secret(cls) -> dict:
        return BaseTradeMasterAPI.CLIENT_SECRET

    @classmethod
    def set_client_secret(cls, client_secret: str) -> None:
        BaseTradeMasterAPI.CLIENT_SECRET = client_secret

    credit_limit = CreditLimitAPI()
    authentication = AuthenticationAPI()
    authorization = AuthorizationAPI()
    operation = OperationAPI()
