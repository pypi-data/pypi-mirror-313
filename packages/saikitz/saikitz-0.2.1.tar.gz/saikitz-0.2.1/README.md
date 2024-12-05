# saiKitz

saiKitz: Sidney Zhang's Toolkit for AI Conversations & Info Queries.

-----

一个简单的AI聊天机器人。主要是为了在Jupyter Notebook里面能快速使用，
也是为了写分析报告可以获得更多文字上的帮助，有的时候更多是查询信息上的帮助。

核心使用的时[kimi](https://kimi.moonshot.cn/)的API，
以及[qwen](https://dashscope.aliyun.com/)
和[ollama](https://ollama.com)，对于其他AI的API当然也是支持的，
前提是这些API有兼容OpenAI的API链接，当然绝对也是支持OpenAI的ChatGPT，
不过这个在国内无法直连使用，所以只作为自定义方式来支持了。

### 1.安装

```bash
$ pip install saikitz
```

### 2.快速开始

可以把你的API KEY设置到环境变量（`$AISEARCKER_API_KEY`）中，或者直接在代码中设置。

这是在环境变量中使用的方式，默认使用Kimi：

```python
from saikitz.aikit import aiSearcher

chatbot = aiSearcher()

chatttbot.chat('你好')
```

注册Kimi的[Platform](https://platform.moonshot.cn/)，就可以获得一个API KEY，
首次注册可以获得免费额度。简单实用已经完全足够了。
如果你需要大量使用Kimi的搜索插件，那还是需要充值一定金额的。

下面是`aiSearcher`的参数说明：

```bash
api_key : str|Path|None ，支持三种方式：1.环境变量（AISEARCKER_API_KEY）
                                       2.文件读取
                                       3.直接输入
base_url : str|None ，支持两种方式：1.指定渠道名：kimi（默认值）、qwen、ollama
                                   2.自定义url
no_tools : bool ，是否使用附加工具，目前只有网络搜索工具。默认为真，即不使用工具。
system_prompt : str ，默认为None，不设置则使用默认prompt
max_dialogue_turns : int ，默认为20，最大历史对话轮次，超过则删除最旧的记录，
                           设定0或负值，则不删除历史记录
```

你可以根据自己的需要对这些默认参数进行调整。

如果你不想使用默认模型，请使用 `chatbot.set_model(model_name)` 方法修改。
同样，对于默认的系统提示，也可以通过 `chatbot.set_system_prompt(prompt)` 来修改。

目前自带的系统提示有五种：

- default ： 默认的提示，很简单，适应绝大多数使用情况。
- langPrompt ： 更复杂的智能助理提示。可以帮助用户完成更复杂的任务。
- chi ： 纯中文助理，对于非国产LLM比较有用。
- runse ： 文本润色。
- trans ： 语言翻译。

### 3.其他说明

1. 使用Kimi的搜索工具会带来较大的TPM，如果账号还未充值，可能会出现超TPM的错误返回信息。
2. 使用ollama时，默认使用了`llama3.2:latest`，请注意提前`ollama pull llama3.2:latest`，完成模型下载。
3. `set_system_prompt()`可以传入一个文本文件地址，这是为了系统提示太长时所准备的方法。
4. 如果发现什么使用上的问题欢迎随时[与我联系](mailto:zly@lyzhang.me) 。
