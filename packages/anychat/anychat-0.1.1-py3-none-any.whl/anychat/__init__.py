from anychat.model import AnyChat

__all__ = ["AnyChat"]


class ChatModelCenter:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def get_chat_model(self, model_name: str, temperature: float = 0.95) -> AnyChat:
        return AnyChat(
            model_name=model_name,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=temperature,
        )
