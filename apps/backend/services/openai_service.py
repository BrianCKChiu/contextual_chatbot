from typing import AsyncGenerator
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from openai import OpenAI
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from config import Config


class OpenAiService:
    client = OpenAI(api_key=Config.OPEN_AI_KEY)
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=Config.OPEN_AI_KEY
    )

    gpt = ChatOpenAI(model="gpt-4o", api_key=Config.OPEN_AI_KEY)

    async def stream_chat_completion(
        self,
        user_message: str,
        message_history: list[ChatCompletionMessageParam] = [],
        model="gpt-4o",
    ) -> AsyncGenerator[str, None]:
        """
        Basic stream chat completion from OpenAI

        Args:
            user_message (ChatCompletionMessageParam): user's new message
            message_history (list[ChatCompletionMessageParam], optional): user's previous message. Defaults to [].
            model (str, optional): openAI model used to in the chat. Defaults to "gpt-4o".

        Yields:
            AsyncGenerator[str, None]: Streamed chat completion

        """
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}, *message_history],
            model=model,
            stream=True,
        )

        for c in response:
            choice = c.choices[0]
            delta = choice.delta.content
            yield delta or ""
