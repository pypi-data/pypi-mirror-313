import openai
from typing import List, Dict, Any

from .base import ModelBase

class OpenAI(ModelBase):
    def __init__(
            self,
            api_key: str = None,
            endpoint: str = None,
            headers: Dict[str, Any] = None,
            timeout: float = 600,
            retry: int = 2
    ):
        super().__init__(
            api_key=api_key,
            endpoint=endpoint,
            headers=headers,
            timeout=timeout,
            retry=retry
        )

        self.client = openai.OpenAI(
            default_headers=self.headers,
            api_key=self.api_key,
            base_url=self.endpoint,
            timeout=self.timeout,
            max_retries=self.retry
        )


    def _non_stream_response(
        self,
        model,
        temperature,
        top_p,
        max_tokens,
        messages,
        response_format,
        tools,
        tool_choice
    ):
        response = self.client.chat.completions.create(
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            messages=messages,
            response_format=response_format,
            tools=tools,
            tool_choice=tool_choice,
            stream=False
        )
        return response

    def _stream_response(
        self,
        model,
        temperature,
        top_p,
        max_tokens,
        messages,
        response_format,
        tools,
        tool_choice
    ):
        response = self.client.chat.completions.create(
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            messages=messages,
            response_format=response_format,
            tools=tools,
            tool_choice=tool_choice,
            stream=True
        )
        for chunk in response:
            yield chunk
