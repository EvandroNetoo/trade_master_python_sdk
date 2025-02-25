from requests import Response


class TradeMasterAPIError(Exception):
    def __init__(self, response: Response) -> None:
        self.response = response
        self.url = response.url
        self.status_code = response.status_code
        self.reason = response.reason
        self.text = response.text

    def __str__(self) -> str:
        return f'{self.url} {self.status_code} - {self.reason} - {self.text}'


def raise_for_status(response: Response) -> None:
    if response.ok:
        return
    raise TradeMasterAPIError(response)
