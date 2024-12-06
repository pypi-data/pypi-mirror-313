# LLMBench

A Tool for evaulation the performance of LLM APIs.

# Installation
```bash
git clone ...
cd LLMBench
pip install -e .
```

# Basic Usage


### Example
```bash
llmbench_tokenmark 
--model test                                # 模型客户端
--num_concurrent_requests 10
--dataset test                              # 数据集
--timeout 60                                # 性能测试时长
--max_request_sample_num -1                        # 最大请求数，-1：不限制，跟数据集个数及测试时长有关， 100： 即使用数据集中100个用例
--results-dir /aaa/bbb/ccc/outpu_dir        # 测试结果路径
--extra_params '{}'                         # 额外参数，供客户端使用
```

# 简介

```
该项目是为了测试大模型接口性能（token 吞吐量）
```

### 客户端

```python
import json
import os
import time
import requests
from llmbench.common.constants import METRICS
from llmbench.inference.clients.client_abc import Client


class OpenAIChatCompletionsClient(Client):
    """Client for OpenAI Chat Completions API."""
    Model_Name = "openai"

    def __init__(self, **kwargs):
        pass

    def make_request(self, request_config):
        prompt = request_config.prompt
        prompt, prompt_len = prompt

        message = [
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt},
        ]
        model = request_config.model
        body = {
            "model": model,
            "messages": message,
            "stream": True,
        }
        sampling_params = request_config.sampling_params
        body.update(sampling_params or {})
        time_to_next_token = []
        tokens_received = 0
        ttft = 0
        error_response_code = -1
        generated_text = ""
        error_msg = ""
        output_throughput = 0
        total_request_time = 0

        metrics = {METRICS.ERROR_CODE: None, METRICS.ERROR_MSG: ""}

        start_time = time.monotonic()
        most_recent_received_token_time = time.monotonic()
        address = os.environ.get("OPENAI_API_BASE")
        if not address:
            raise ValueError("the environment variable OPENAI_API_BASE must be set.")
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError("the environment variable OPENAI_API_KEY must be set.")
        headers = {"Authorization": f"Bearer {key}"}
        if not address:
            raise ValueError("No host provided.")
        if not address.endswith("/"):
            address = address + "/"
        address += "chat/completions"
        try:
            with requests.post(
                    address,
                    json=body,
                    stream=True,
                    timeout=180,
                    headers=headers,
            ) as response:
                if response.status_code != 200:
                    error_msg = response.text
                    error_response_code = response.status_code
                    response.raise_for_status()
                for chunk in response.iter_lines(chunk_size=None):
                    chunk = chunk.strip()

                    if not chunk:
                        continue
                    stem = "data: "
                    chunk = chunk[len(stem):]
                    if chunk == b"[DONE]":
                        continue
                    tokens_received += 1
                    data = json.loads(chunk)

                    if "error" in data:
                        error_msg = data["error"]["message"]
                        error_response_code = data["error"]["code"]
                        raise RuntimeError(data["error"]["message"])

                    delta = data["choices"][0]["delta"]
                    if delta.get("content", None):
                        if not ttft:
                            ttft = time.monotonic() - start_time
                            time_to_next_token.append(ttft)
                        else:
                            time_to_next_token.append(
                                time.monotonic() - most_recent_received_token_time
                            )
                        most_recent_received_token_time = time.monotonic()
                        generated_text += delta["content"]

            total_request_time = time.monotonic() - start_time
            output_throughput = tokens_received / total_request_time

        except Exception as e:
            metrics[METRICS.ERROR_MSG] = error_msg
            metrics[METRICS.ERROR_CODE] = error_response_code
            print(f"Warning Or Error: {e}")
            print(error_response_code)

        metrics[METRICS.INTER_TOKEN_LAT] = sum(
            time_to_next_token)  # This should be same as metrics[metrics.E2E_LAT]. Leave it here for now
        metrics[METRICS.TTFT] = ttft
        metrics[METRICS.E2E_LAT] = total_request_time
        metrics[METRICS.REQ_OUTPUT_THROUGHPUT] = output_throughput
        metrics[METRICS.NUM_TOTAL_TOKENS] = tokens_received + prompt_len
        metrics[METRICS.NUM_OUTPUT_TOKENS] = tokens_received
        metrics[METRICS.NUM_INPUT_TOKENS] = prompt_len

        return metrics, generated_text, request_config

```

### 获取token长度的函数（在utils.py 脚本中，如有需要可进行调用）

```python
import functools
import tiktoken


@functools.lru_cache(maxsize=128)
def get_token_length():
    """
    Get the token length of the tokenizer.
    :return:
    """
    tokenizer = tiktoken.get_encoding("cl100k_base")
    return lambda text: len(tokenizer.encode(text))
```

## 线下测试

```python
# 使用pytest 框架驱动 test/test_bench.py
from pathlib import Path
import os
from llmbench.inference.token_benchmark import TokenBenchmark

current_path = os.path.dirname(__file__)
eval_client_path = str(Path(current_path, "../eval_client"))
llmbench_client_path = str(Path(current_path, "../llmbench_client"))


class TestBenchmark:

    def test_self_client(self):
        """
        llmbench 内部的客户端
        """
        TokenBenchmark("eduction", 5, 60, "test").run_token_benchmark()

    def test_evals_client(self):
        """
        evals 的客户端   模型/引擎
        """
        TokenBenchmark("test", 5, 60, "test/all").run_token_benchmark()

    def test_evals_client_by_path(self):
        """
        evals  model是客户端路径
        """
        TokenBenchmark("test", 5, 60,
                       r"D:\code\evals_code\evals\src\evals\clients\client_cmri_test.py").run_token_benchmark()

    def test_outer_client_by_path_for_llmbench(self):
        """
        llmbench 外部客户端，需指定client_path， 仅在测试时使用extra_params，真实环境使用.env进行设置客户端路径
        """
        TokenBenchmark("test", 5, 60, "outer_llmbench",
                       extra_params={"client_path": llmbench_client_path}).run_token_benchmark()

    def test_outer_client_by_path_for_evals(self):
        """
        eval 外部客户端，需指定client_path， 仅在测试时使用extra_params，真实环境使用.env进行设置客户端路径
        """
        TokenBenchmark("test", 5, 60, "outer_eval",
                       extra_params={"client_path": eval_client_path}).run_token_benchmark()

    def test_client_for_multi_engine(self):
        """
        evals 默认支持模型名/引擎 这种方式，这里只举例了llmbench 也支持模型名加引擎方式。 除了evals内部的客户端外，其他客户端都用Model_Name指定模型名即可
        """
        TokenBenchmark("test", 1, 60, "openai_multi/gpt3.5",
                       extra_params={"client_path": llmbench_client_path}).run_token_benchmark()

```

### 数据集
```python
# llmbench/data 目录即存放数据集（jsonl）
# 由于本工具主要是测试性能， 跟期望关系不大，所以数据集中可以不写期望。
# 如下：
{"input": [{"role": "system", "content": "图片里描述了什么？", "file_path": "files/flower.png"}], "ideal": "花朵"}  # 这里的ideal 可以不写，如客户端需要，加上即可
```


