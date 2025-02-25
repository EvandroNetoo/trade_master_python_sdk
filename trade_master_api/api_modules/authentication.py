from requests import Response

from trade_master_api.base import BaseTradeMasterAPI


class AuthenticationAPI(BaseTradeMasterAPI):
    BASE_ENDPOINT = (
        '/auth/realms/api-management/protocol/openid-connect/token/'
    )

    @classmethod
    def get_access_token(cls) -> Response:
        data = {
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET,
            'scope': 'convenio-api/.default',
            'grant_type': 'client_credentials',
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return cls._send_request(
            method='POST',
            headers=headers,
            data=data,
            authenticate=False,
        )
