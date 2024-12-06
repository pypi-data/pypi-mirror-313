import contextlib
from base64 import b64encode

from gigachat.models import Embedding
from gigachat import GigaChat
from itertools import chain
from time import sleep
import concurrent

from httpx import NetworkError


class GigaChatEntryPoint:
    __slots__ = ("_creds", "_model", "_DIM", "_ZEROS", "_ERROR_MESSAGE", "_warmed_up")

    def __init__(self, client_id: str, client_secret: str, obligatory_warmup: bool = False) -> None:
        self._creds: str = b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
        self._model = GigaChat(
            credentials=self._creds,
            base_url="https://gigachat.devices.sberbank.ru/api/v1",
            scope="GIGACHAT_API_CORP",
            model="GigaChat-Pro",
            verify_ssl_certs=False,
            profanity_check=False,
        )
        self._DIM: int = 1024
        self._ZEROS: list[float] = [0.0 for _ in range(self._DIM)]
        self._ERROR_MESSAGE: str = ""
        self._warmed_up: bool = False
        if obligatory_warmup:
            self.warmup()

    def __call__(self) -> GigaChat:
        return self._model

    def get_response(self, sentence: str) -> str:
        with contextlib.suppress(Exception):
            return self._model.chat(sentence).choices[0].message.content
        return self._ERROR_MESSAGE

    def get_response_by_payload(self, payload: list[dict[str, str]]) -> str:
        """payload: [{"role": "system", "content": system}, {"role": "user", "content": replica}]"""
        with contextlib.suppress(Exception):
            return self._model.chat({"messages": payload}).choices[0].message.content
        return self._ERROR_MESSAGE

    def get_embedding(self, sentence: str) -> list[float]:
        with contextlib.suppress(Exception):
            return self._model.embeddings([sentence]).data[0].embedding
        return self._ZEROS

    def get_embeddings(self, sentences: list[str], request_limit=50) -> list[list[float]]:
        embeddings: list[list[float]] | None = None
        counter: int = 0
        while embeddings is None and counter < request_limit:
            with contextlib.suppress(Exception):
                items: list[Embedding] = self._model.embeddings(sentences).data
                embeddings = [item.embedding for item in items]
                break
            sleep(0.1)
            counter += 1
        if embeddings is not None:
            return embeddings
        return [self._ZEROS for _ in sentences]

    def get_more_embeddings(self, sentences: list[str], batch_size: int = 2, max_workers: int = 4) -> list[list[float]]:
        batches: list[list[str]] = self.make_batches(sentences, size=batch_size)
        if max_workers == 1:
            emb_batches = [self.get_embeddings(batch) for batch in batches]
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(self.get_embeddings, batch) for batch in batches]
                emb_batches = [future.result() for future in futures]
        return list(chain.from_iterable(emb_batches))

    def count_tokens(self, sentences: list[str]) -> list[int]:
        return [count.tokens for count in self._model.tokens_count(sentences)]

    @staticmethod
    def make_batches(items: list, size: int = 500) -> list[list[str]]:
        slices = [(i * size, (i + 1) * size) for i in range(len(items) // size + 1)]
        return [items[st:ed] for st, ed in slices]

    def warmup(self) -> None:
        if self.get_response("Прогрев") == self._ERROR_MESSAGE or self.get_embedding("Прогрев") == self._ZEROS:
            raise NetworkError("Нет доступа к ллм!")
        self._warmed_up = True

    def is_warmed_up(self) -> bool:
        return self._warmed_up
