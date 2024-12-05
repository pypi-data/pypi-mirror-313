from openai import OpenAI,NOT_GIVEN
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from typing import Iterable
from pathlib import Path
import os
import json

from saikitz.utils import printmd,lastoflistdict
from saikitz._chatollama import ollamachat

KEYPLACE = Path(__file__).absolute().parent

DEFAULT_PROMPT = """你是一个机智的智能信息助理，名叫 saikitz。可以帮助用户回答问题，查询资料。"""

class aiSearcher(object) :
    __all__ = ["chat","set_system_prompt","set_model"]
    def __init__(self, api_key:str|Path|None = None, 
                 base_url:str|None = None,
                 search_web:bool= False,
                 system_prompt:str|Path|None = None,
                 max_dialogue_turns:int = 20) -> None:
        """
        aiSearcher is a class for chatting with AI.
        api_key : str|Path|None ，支持三种方式：1.环境变量（AISEARCKER_API_KEY）
                                               2.文件读取
                                               3.直接输入
        base_url : str|None ，支持两种方式：1.指定渠道名：kimi、qwen、ollama
                                           2.自定义url
        search_web : bool ，是否使用LLM自带的网络搜索工具，默认为False。目前仅有Kimi和qwen有自带网络搜索。
        system_prompt : str ，默认为None，不设置则使用默认prompt
        max_dialogue_turns : int ，默认为20，最大历史对话轮次，超过则删除最旧的记录，设定0或负值，则不删除历史记录
        
        特别说明：
        1. 使用搜索工具会带来较大的TPM，如果账号初始设立，可能会出现超TPM的错误返回信息。
        """
        match base_url:
            case "kimi" :
                self.__channel = "kimi"
                self.__model = "moonshot-v1-auto"
                url = "https://api.moonshot.cn/v1"
            case "qwen" :
                self.__channel = "qwen"
                if search_web :
                    self.__model = "qwen-plus"
                else:
                    self.__model = "qwen2.5-72b-instruct"
                url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
            case "ollama" :
                self.__channel = "ollama"
                self.__model = "llama3.2:latest"
                url = 'http://localhost:11434'
            case None :
                self.__channel = "kimi"
                self.__model = "moonshot-v1-auto"
                url = "https://api.moonshot.cn/v1"
            case _ :
                self.__channel = "custom"
                self.__model = None
                url = base_url
        if api_key is None :
            if self.__channel == "ollama" :
                aikey = "ollama"
            else:
                aikey = os.environ.get("AISEARCH_API_KEY")
            if aikey is None :
                raise ValueError("AISEARCH_API_KEY is not set!!")
        elif isinstance(api_key, Path) :
            aikey = api_key.read_text()
        else :
            aikey = api_key
        if self.__channel == "ollama" :
            self.__client = ollamachat()
        self.__client = OpenAI(
            api_key = aikey,
            base_url = url,)
        self.__max_history = max_dialogue_turns
        self.__turns = 0
        if system_prompt is None :
            prompt = DEFAULT_PROMPT
        else :
            prompt = system_prompt
        self.__system_prompt = {"role": "system", "content": prompt}
        self.__history = [self.__system_prompt]
        self.__prefix = ""
        self.__search_web = search_web
    def set_system_prompt(self, system_prompt:str|Path) -> None:
        """
        设置系统提示语
        system_prompt : str|Path ，支持两种方式：
                                    1.固定系统设定：default、langPrompt、chi、runse、trans；
                                    2.直接输入。
        其中：
        default : 默认提示语，专业的信息检索人员。
        chi : 专业的中文信息辅助者。
        """
        if isinstance(system_prompt, Path) :
            prompt = system_prompt.read_text(encoding="utf-8")
        else:
            match system_prompt:
                case "default" :
                    prompt = DEFAULT_PROMPT
                case "longPrompt":
                    prompt = (KEYPLACE/"prompts/sysprompt.txt").read_text(encoding="utf-8")
                case "chi" :
                    prompt = (KEYPLACE/"prompts/chiprompt.txt").read_text(encoding="utf-8")
                case "runse" :
                    prompt = (KEYPLACE/"prompts/opmprompt.txt").read_text(encoding="utf-8")
                case "trans" :
                    prompt = (KEYPLACE/"prompts/transprompt.txt").read_text(encoding="utf-8")
                case _ :
                    prompt = system_prompt
        self.__system_prompt = {"role": "system", "content": prompt}
        self.__history = [self.__system_prompt]
    def set_model(self, model:str) -> None :
        """使用自定义API链接时才需要先设定所需模型"""
        self.__model = model
    def _chat_create(self, model,messages,temp,maxtn,topp,tools, **kwargs) :
        if self.__channel == "ollama" :
            caht_info = self.__client.chat(model=model,
                message=messages, temperature=temp, max_token=maxtn,
                top_p=topp, stream=False, tools=tools)
            output = ""
            for i in caht_info :
                tmpx = json.loads(i)["message"]
                if "tool_calls" in tmpx.keys():
                    return {"role":"tool","tool_calls":tmpx["tool_calls"]}
                else :
                    output += json.loads(i)["message"]["content"]
            return {"role":"assistant","content":output}
        else :
            caht_info = self.__client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temp, max_tokens=maxtn,
                top_p=topp, tools=tools, **kwargs)
            output = ''
            while caht_info.choices[0].finish_reason == "length":
                output += caht_info.choices[0].message.content
                self.__history.append({"role": "assistant", "content": output, "partial": True})
                caht_info = self.__client.chat.completions.create(
                            model=model,
                            messages=messages,
                            temperature=temp, max_tokens=maxtn,
                            top_p=topp, tools=tools, **kwargs)
            self.__prefix = output
            return caht_info.choices[0]
    def _optimizing_history_(self) -> None :
        if self.__max_history > 0 :
            if self.__max_history == 1 :
                self.__history = [self.__system_prompt]
            elif self.__max_history <= 4 :
                if self.__turns > self.__max_history :
                    ind = lastoflistdict(self.__history, "role", "user")
                    self.__history = [self.__system_prompt] + self.__history[ind:]
            else :
                self.__history.append({"role": "user", 
                                       "content": "请总结之前所有对话的主要信息，并以'之前对话主要内容为：'开头。"})
                chatres = self._chat_create(self.__model,self.__history,
                                            0.7,2048,1,NOT_GIVEN)
                summ = chatres["content"] if self.__channel == "ollama" else chatres.message.content
                self.__history = [
                    self.__system_prompt,
                    {"role": "assistant", "content": summ}
                ]
    def _calling(self, tem, topp, maxtn, ctools) :
        ot = [] if ctools is NOT_GIVEN else ctools
        add_args = {}
        if self.__search_web :
            if self.__channel == "kimi":
                tools = [
                    {
                        "type": "builtin_function",
                        "function": {
                            "name": "$web_search",
                        },
                    },
                ] + ot
            if self.__channel == "qwen" :
                add_args = {"extra_body":{"enable_search": True}}
                tools = NOT_GIVEN if ot else ot
        else:
            tools = NOT_GIVEN if ot else ot
        completion = self._chat_create(self.__model,self.__history,tem,maxtn,topp,tools, **add_args)
        return completion
    def _useFile(self,tfile:Path) -> None :
        file_object = self.__client.files.create(file=tfile, 
                                                 purpose="file-extract")
        if self.__channel == "kimi" :
            file_content = self.__client.files.content(file_id=file_object.id).text
        elif self.__channel == "qwen" :
            file_content = f"fileid://{file_object.id}"
        else :
            file_content = None
            print("Not supported yet!")
        if file_content is not None :
            self.__history.append({"role": "system", "content": file_content})
    def _get_max_token(self, input:str|int) -> int :
        if isinstance(input,int) :
            return input
        else :
            match input:
                case "auto":
                    return 1024
                case "long":
                    return 4096
                case "max" :
                    return 8192
                case _ :
                    raise ValueError("Undefined Names!")
    def chat(self, message:str, 
             temperature:float = 0.3,
             top_p:float = 1.0,
             max_tokens:int|str = "auto",
             tools:Iterable[ChatCompletionToolParam]|None = None,
             file:Path|str|None = None,
             show:bool = True) -> str|None :
        if self.__model is None :
            raise ValueError("Model is not set!! Use set_model() first!")
        self._optimizing_history_()
        if file is not None :
            self._useFile(Path(file))
        self.__history.append({"role": "user", "content": message})
        finished = None
        calledTools = False
        while finished is None or finished == "tool_calls":
            choice = self._calling(temperature, top_p, 
                                   self._get_max_token(max_tokens), tools)
            if self.__channel == "ollama" :
                finished = "tool_calls" if "tool_calls" in choice.message.model_dump().keys() else None
            if self.__channel == "qwen" :
                finished = "tool_calls" if choice.message.tool_calls is not None else None
            else :
                finished = choice.finish_reason
            if finished == "tool_calls":
                calledTools = True
                self.__prefix += choice.message.content
                if self.__channel == "ollama" :
                    self.__history.append(choice)
                else :
                    self.__history.append(choice.message)
                    for tool_call in choice.message.tool_calls:
                        tool_call_name = tool_call.function.name
                        tool_call_arguments = json.loads(tool_call.function.arguments)
                        if tool_call_name == "$web_search":
                            tool_result = tool_call_arguments
                        else:
                            tool_result = eval(tool_call_name)(**tool_call_arguments)
                        self.__history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call_name,
                            "content": json.dumps(tool_result),
                        })
        if self.__prefix != "" :
            if calledTools :
                xCatRes = self._chat_create(
                    self.__model,
                    {"role":"user","content":"请整理以下语句，是表达更清晰明确：/n{}".format(self.__prefix)},
                    0.7,2048,1,NOT_GIVEN)
                result = xCatRes.message.content
            else :
                result = self.__prefix + choice.message.content
            self.__prefix = ""
        else :
            result = choice["content"] if self.__channel == "ollama" else  choice.message.content
        self.__history.append({"role": "assistant","content": result})
        self.__turns += 1
        if show :
            printmd(result)
        else :
            return result