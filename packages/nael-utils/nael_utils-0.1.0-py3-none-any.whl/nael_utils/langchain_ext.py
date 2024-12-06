# nael_utils/your_module.py

import os
from typing import Optional, Type
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers.pydantic import TBaseModel
from langchain_openai.chat_models import ChatOpenAI


def call_gpt_with_prompt_model(prompt: str, pydantic_object: Optional[Type[TBaseModel]]):
    """
    Generic function to ask for GPT's inference. Return value will be in pydantic_object
    :param prompt:
    :param pydantic_object:
    :return:
    """
    chat = ChatOpenAI(model="gpt-4o", api_key=os.environ["OPENAI_API_KEY"])
    parser = JsonOutputParser(pydantic_object=pydantic_object)
    format_instructions = parser.get_format_instructions()
    _prompt = f"Answer the user query.\n{format_instructions}\n{prompt}\n"
    messages = [
        HumanMessage(
            content=[
                {"type": "text", "text": _prompt},
            ]
        )
    ]

    text_result = chat.invoke(messages)
    return parser.invoke(text_result)
