import contextlib
import json
import requests


class YandexGPTEntryPoint:
    def __init__(self, token, folder_id):
        iam_token = requests.post(
            url="https://iam.api.cloud.yandex.net/iam/v1/tokens",
            data=json.dumps({"yandexPassportOauthToken": token}),
        ).json()["iamToken"]
        self.folder_id = folder_id
        self.text_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.emb_url = "https://llm.api.cloud.yandex.net:443/foundationModels/v1/textEmbedding"
        self.doc_uri = f"emb://{self.folder_id}/text-search-doc/latest"
        self.query_uri = f"emb://{self.folder_id}/text-search-query/latest"
        self.headers = {
            "Authorization": f"Bearer {iam_token}",
            "Content-Type": "application/json",
        }
        self.DIM = 256
        self.ZEROS = [0 for _ in range(self.DIM)]
        self.ERROR_MESSAGE = ""
        self.warmup()

    def get_response(self, total_input: str) -> str:
        data = {
            "model_uri": f"gpt://{self.folder_id}/yandexgpt/latest",
            "messages": [
                {
                    "role": "user",
                    "text": total_input,
                }
            ],
        }
        with contextlib.suppress(Exception):
            response = requests.post(url=self.text_url, headers=self.headers, json=data).json()
            return response["result"]["alternatives"][0]["message"]["text"]
        return self.ERROR_MESSAGE

    def get_embeddings(self, total_input, input_is_long=False) -> list:
        data = {
            "modelUri": self.doc_uri if input_is_long else self.query_uri,
            "text": total_input,
        }
        with contextlib.suppress(Exception):
            response = requests.post(url=self.emb_url, headers=self.headers, json=data).json()
            return response["embedding"]
        return self.ZEROS

    def warmup(self) -> None:
        assert self.get_response("Прогрев") != self.ERROR_MESSAGE, "Нет доступа к ллм!"
        assert self.get_embeddings("Прогрев") != self.ZEROS, "Нет доступа к ллм!"
        assert self.get_embeddings("Прогрев", input_is_long=True) != self.ZEROS, "Нет доступа к ллм!"
