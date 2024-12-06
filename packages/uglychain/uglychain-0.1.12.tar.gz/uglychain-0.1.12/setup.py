# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uglychain',
 'uglychain.chains',
 'uglychain.chains.llm',
 'uglychain.llm',
 'uglychain.llm.instructor',
 'uglychain.llm.provider',
 'uglychain.retrievers',
 'uglychain.storage',
 'uglychain.tools',
 'uglychain.tools.languages',
 'uglychain.utils',
 'uglychain.worker']

package_data = \
{'': ['*']}

install_requires = \
['docstring-parser>=0.15,<0.16',
 'loguru>=0.7.2,<0.8.0',
 'openai>=1.1.0,<2.0.0',
 'pathos>=0.3.1,<0.4.0',
 'pydantic-yaml>=1.2.1,<2.0.0',
 'pydantic>=2.0.2,<3.0.0',
 'python-frontmatter>=1.1.0,<2.0.0',
 'pyyaml>=6.0.1,<7.0.0',
 'requests>=2.31.0,<3.0.0',
 'tenacity>=8.2.3,<9.0.0']

extras_require = \
{'bm25': ['jieba-fast[bm25]>=0.53,<0.54'],
 'chatglm': ['zhipuai[chatglm]>=2.0.1,<3.0.0'],
 'dashscope': ['dashscope[dashscope]>=1.14.1,<2.0.0'],
 'gemini': ['google-generativeai[gemini]>=0.3.2,<0.4.0'],
 'ipython': ['ipykernel[ipython]>=6.26.0,<7.0.0'],
 'llama-index:python_full_version >= "3.8.1" and python_version < "3.12"': ['llama-index-core[llama-index]>=0.10.1,<0.11.0',
                                                                            'llama-index-embeddings-openai[llama-index]>=0.1.0,<0.2.0'],
 'ollama': ['ollama[ollama]>=0.1.6,<0.2.0'],
 'sparkapi': ['websockets[sparkapi]>=12.0,<13.0']}

setup_kwargs = {
    'name': 'uglychain',
    'version': '0.1.12',
    'description': 'UglyChain：更好用的 LLM 应用构建工具',
    'long_description': '[![Release Notes][release-shield]][release-url]\n[![Contributors][contributors-shield]][contributors-url]\n[![Forks][forks-shield]][forks-url]\n[![Stargazers][stars-shield]][stars-url]\n[![Issues][issues-shield]][issues-url]\n[![MIT License][license-shield]][license-url]\n\n<!-- PROJECT LOGO -->\n<br />\n<div align="center">\n  <a href="https://github.com/uglyboy-tl/UglyChain">\n    <!-- <img src="images/logo.png" alt="Logo" width="80" height="80"> -->\n  </a>\n\n  <h3 align="center">UglyChain</h3>\n\n  <p align="center">\n    ⚡ UglyChain：更好用的 LLM 应用构建工具 ⚡\n    <br />\n    <a href="https://uglychain.uglyboy.cn"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="https://github.com/uglyboy-tl/UglyChain/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/uglyboy-tl/UglyChain/issues">Request Feature</a>\n  </p>\n</div>\n\n## 🤔 What is UglyChain?\n现在有很多利用大模型 LLM 进行应用构建的工具，最有名的就是 LangChain。早期的 LangChain 整个框架并不完善，很多并不直观的定义和调用方式，以及将内部功能封装得太彻底，使的难以定制化的更充分的利用大模型的能力来解决问题。所以我就开发的最初的 UglyGPT（UglyChain的原型），试图解决这个问题。\n\n到了今天，GPTs 也已经面世很长时间了，也有了越来越多的 LLM 应用构建工具。但是这些工具都有一个共同的问题：**不够直观**。\n从底层来说，现在的大模型是基于 Chat 进行接口交互的，这对于应用开发而言并不友好，因为应用开发更多的是模板化的结构化内容生成，而不是对话式的交互。所以我们需要一个对应用开发更加友好的接口，这就是 UglyChain 的初衷。\n\n## Features\n\n- 📦 对大模型接口进行封装，提供对工程化更加直观易懂的交互方式，而不是传统的对话式交互。\n  - 可以参数化 Prompt，更加方便地进行批量调用\n  - 可以对 Prompt 进行结构化返回，方便后续处理\n  - 可以对 Prompt 进行角色设置，方便模型进行角色扮演（这个过程无需操控 Message）\n- 🔗 对大模型的高级调用进行封装，提供更加方便的交互方式\n  - 提供了类似于 MapReduce 的功能，可以通过 MapChain 对多个 Prompt 进行并行调用，也可以用 ReduceChain 对多个 Prompt 进行串行调用\n  - 大模型最优质的能力之一就是拥有 ReAct 能力。我们提供了 ReActChain 便捷的实现这种能力。\n- 💾 提供了搜索引擎的封装，可以方便地进行搜索引擎的调用。\n  - 注意我们只封装了搜索过程的调用，而没有提供搜索引擎的搭建。如果要构建基于 RAG 的应用，需要利用其他的工具完成资料库的建立，而我们只提供对资料库搜索功能的封装。\n\n## Getting Started\n\nWith pip:\n\n```bash\npip install uglychain\n```\n\n## Usage\n\n### LLM\n\n> 这是最基础的模型调用类，其他的高级类也都继承和使用了这个类的基本功能。\n\n快速使用：\n\n```python\nfrom uglychain import LLM, Model\n\nllm = LLM()\nprint(llm("你是谁？")) # 与模型对话，返回字符串的回答\n```\n\n调整基础配置选项：\n\n```python\nllm = LLM(model = Model.YI) # 可以选择更多的模型，如 Model.GPT3_TURBO、Model.GPT4 等等\nllm = LLM(system_prompt = "我想让你担任职业顾问。我将为您提供一个在职业生涯中寻求指导的人，您的任务是帮助他们根据自己的技能、兴趣和经验确定最适合的职业。您还应该对可用的各种选项进行研究，解释不同行业的就业市场趋势，并就哪些资格对追求特定领域有益提出建议。") # 可以对模型设置角色，这样模型就会以这个角色的视角来回答问题。设置的内容保存在 System Message 中。\n```\n\n参数化 prompt：\n\n```python\nllm = LLM(prompt_template = "{object}的{position}是谁？")\nprint(llm(object = "《红楼梦》", position = "作者"))\nprint(llm(object = "上海市", position = "市长"))\n```\n\n对于 prompt 中只有一个参数的情况，可以直接传入参数：\n\n```python\nllm = LLM("介绍一下{object}")\nprint(llm("Transformer"))\n```\n\n结构化返回结果：\n\n```python\nclass UserDetail(BaseModel):\n    name: str\n    age: int\n\nllm = LLM(response_model=UserDetail)\nprint(llm("Extract Jason is 25 years old")) # UserDetail(name=\'Jason\', age=25)\n```\n\n### MapChain\n\n> 这是一个可以并行对同类型 Prompt 进行调用的类，可以大大提高调用效率。\n\n快速使用：\n\n```python\nfrom uglychain import MapChain\n\nllm = MapChain()\nprint(llm([\n        {"input": "How old are you?"},\n        {"input": "What is the meaning of life?"},\n        {"input": "What is the hottest day of the year?"},\n    ]))\n```\n\n类似于 LLM，也可以对 MapChain 进行更高阶的使用：\n\n```python\nclass AUTHOR(BaseModel):\n    name: str = Field(..., description="姓名")\n    introduction: str = Field(..., description="简介")\n\nllm = MapChain(prompt_template="{book}的{position}是谁？", response_model=AUTHOR, map_keys=["book",])\ninput = [\n    "《红楼梦》",\n    "《西游记》",\n    "《三国演义》",\n    "《水浒传》",\n]\nprint(llm(book=input, position="作者"))\n```\n\n## Roadmap\n\n- [x] 增加 FunctionCall 的能力\n- [ ] 增加 Memory 的能力\n\n## Contributing\n\nContributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\nIf you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".\nDon\'t forget to give the project a star! Thanks again!\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n## License\n\nDistributed under the MIT License. See `LICENSE.txt` for more information.\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[release-shield]:https://img.shields.io/github/release/uglyboy-tl/UglyChain.svg?style=for-the-badge\n[release-url]: https://github.com/uglyboy-tl/UglyChain/releases\n[contributors-shield]: https://img.shields.io/github/contributors/uglyboy-tl/UglyChain.svg?style=for-the-badge\n[contributors-url]: https://github.com/uglyboy-tl/UglyChain/graphs/contributors\n[forks-shield]: https://img.shields.io/github/forks/uglyboy-tl/UglyChain.svg?style=for-the-badge\n[forks-url]: https://github.com/uglyboy-tl/UglyChain/network/members\n[stars-shield]: https://img.shields.io/github/stars/uglyboy-tl/UglyChain.svg?style=for-the-badge\n[stars-url]: https://github.com/uglyboy-tl/UglyChain/stargazers\n[issues-shield]: https://img.shields.io/github/issues/uglyboy-tl/UglyChain.svg?style=for-the-badge\n[issues-url]: https://github.com/uglyboy-tl/UglyChain/issues\n[license-shield]: https://img.shields.io/github/license/uglyboy-tl/UglyChain.svg?style=for-the-badge\n[license-url]: https://github.com/uglyboy-tl/UglyChain/blob/master/LICENSE.txt',
    'author': 'uglyboy',
    'author_email': 'uglyboy@uglyboy.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/uglyboy-tl/uglychain',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
