from typing import AsyncGenerator, Iterable
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from openai import OpenAI
from config import Config
from typing import Callable
from models.chat_record import ChatRecordSchema, ChatRole


class OpenAiService:
    client = OpenAI(api_key=Config.OPEN_AI_KEY)
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=Config.OPEN_AI_KEY
    )

    gpt = ChatOpenAI(model="gpt-4o", api_key=Config.OPEN_AI_KEY)

    async def stream_chat_completion(
        self,
        user_message: str,
        message_history: list[dict] = [],
        model="gpt-4o",
        callback_function: Callable[[str, str, ChatRole], None] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Basic stream chat completion from OpenAI

        Args:
            user_message (ChatCompletionMessageParam): user's new message
            message_history (list[ChatRecordSchema], optional): previous chat messages. Defaults to [].
            model (str, optional): openAI model used to in the chat. Defaults to "gpt-4o".
            callback_function (Callable[[str], None], optional): callback function to handle the open ai completed response. Defaults to None.

        Yields:
            AsyncGenerator[str, None]: Streamed chat completion

        """
        print([{"role": "user", "content": user_message}] + message_history)
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}] + message_history,
            model=model,
            stream=True,
        )

        ai_response = ""
        for chunk in response:
            response = chunk.choices[0].delta.content
            if response is not None:
                ai_response += response or ""
                yield response or ""

        if callback_function is not None:
            callback_function(ai_response, ChatRole.ASSISTANT)
