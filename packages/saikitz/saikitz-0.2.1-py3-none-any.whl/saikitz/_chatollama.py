import requests

from openai import NOT_GIVEN, NotGiven
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat import ChatCompletionMessageParam
from typing import Iterable
from pathlib import Path

from saikitz.utils import img_to_base64

class ollamachat(object):
    def __init__(self, base_url:str = "http://localhost:11434/",
                 system_prompt:str|None = None,
                 tools:Iterable[ChatCompletionToolParam]|NotGiven = NOT_GIVEN):
        self.__url = base_url
        if system_prompt is None :
            self.__messages = []
        else :
            self.__messages = [{"role": "system", "content": system_prompt}]
        self.__tools = tools
    def chat(self, model:str,
             message:str|Iterable[ChatCompletionMessageParam], 
             image:Path|str|list[Path|str]|None = None,
             temperature:float = 0.3,
             top_p:float = 1.0,
             max_token:int = 1024,
             stream:bool = True,
             tools:Iterable[ChatCompletionToolParam]|NotGiven|None = None) -> str :
        if tools is not None :
            self.__tools = tools
        if image is None :
            if isinstance(message, str) :
                self.__messages.append({"role": "user", "content": message})
            else :
                self.__messages.extend(message)
        else:
            if isinstance(image, Iterable) and not isinstance(image, str):
                ximages = [img_to_base64(i) for i in image]
            else :
                ximages = [img_to_base64(image)]
            if isinstance(message, str) :
                self.__messages.append({"role": "user", "content": message, "images":ximages})
            else :
                message[-1]["images"] = ximages
                self.__messages.extend(message)
        r = requests.post(
            "{}api/chat".format(self.__url),
            json={"model": model, "messages": self.__messages, "stream": stream,
                  "tools":[] if self.__tools is NOT_GIVEN else self.__tools,
                  "options": {"temperature": temperature, "top_p": top_p, "num_ctx": max_token}},
            stream=stream)
        r.raise_for_status()
        return r.iter_lines()
    