from gigachat import GigaChat

from . import GigaChatEntryPoint


class GigaPlusEntryPoint(GigaChatEntryPoint):
    def __init__(self, client_id: str, client_secret: str) -> None:
        super().__init__(client_id, client_secret)
        self._model = GigaChat(
            credentials=self._creds,
            base_url="https://gigachat.devices.sberbank.ru/api/v1",
            scope="GIGACHAT_API_CORP",
            model="GigaChat-Plus",
            verify_ssl_certs=False,
            profanity_check=False,
        )
