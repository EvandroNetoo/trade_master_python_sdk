import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional


@dataclass
class AcessTokenDataclass:
    access_token: str
    expires_at: int

    def is_valid(self) -> bool:
        return time.time() < self.expires_at

    def __bool__(self) -> bool:
        return self.is_valid()


class AcessToken(str):
    file_dir = Path(__file__).parent.resolve()
    file_name = 'access_token.json'
    file_path = file_dir / file_name

    def _get(self) -> Optional[AcessTokenDataclass]:
        if not self.file_path.exists():
            return None

        with self.file_path.open('r') as file:
            data = json.load(file)
        return AcessTokenDataclass(**data)

    def _set(self, access_token: AcessTokenDataclass):
        data = asdict(access_token)
        with self.file_path.open('w') as file:
            json.dump(data, file)
        return data

    def _generate(self) -> AcessTokenDataclass:
        from .api_modules.authentication import (  # noqa: PLC0415
            AuthenticationAPI,
        )

        response = AuthenticationAPI.get_access_token()
        data = response.json()
        access_token = AcessTokenDataclass(
            access_token=data['access_token'],
            expires_at=time.time() + data['expires_in'],
        )
        self._set(access_token)
        return access_token

    def _get_valid(self) -> str:
        access_token = self._get()
        if access_token:
            return access_token.access_token

        access_token = self._generate()
        return access_token.access_token

    def __str__(self):
        return self._get_valid()
