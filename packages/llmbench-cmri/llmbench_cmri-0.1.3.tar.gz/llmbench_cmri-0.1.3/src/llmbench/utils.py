import math
import os
import time
import jwt
import random
import subprocess
import functools
import tiktoken
from typing import Tuple, List
import numpy as np

from llmbench.data import get_file_lines


def generate_token(apikey: str, exp_seconds: int):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)

    payload = {
        "api_key": id,
        "exp": int(round(time.time())) + exp_seconds,
        "timestamp": int(round(time.time())),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "type": "JWT", "sign_type": "SIGN"},
    )


@functools.lru_cache(maxsize=128)
def get_token_length():
    """
    Get the token length of the tokenizer.
    :return:
    """
    tokenizer = tiktoken.get_encoding("cl100k_base")
    return lambda text: len(tokenizer.encode(text))


def upload_to_s3(results_path: str, s3_path: str) -> None:
    """Upload the results to s3.

    Args:
        results_path: The path to the results file.
        s3_path: The s3 path to upload the results to.

    """

    command = ["aws", "s3", "sync", results_path, f"{s3_path}/"]
    result = subprocess.run(command)
    if result.returncode == 0:
        print("Files uploaded successfully!")
    else:
        print("An error occurred:")
        print(result.stderr)


def seq_sample_sonnet_lines_prompt(dataset: str) -> List[Tuple[str, int]]:
    """按顺序获取文件所有prompt"""
    _get_token_length = get_token_length()
    sonnet_lines = get_file_lines(dataset)
    result = []
    for line in sonnet_lines:
        result.append((line, _get_token_length(line)))
    return result


def randomly_sample_sonnet_lines_prompt(
    dataset: str,
    prompt_tokens_mean: int = 550,
    prompt_tokens_stddev: int = 250,
    expect_output_tokens: int = 150
) -> Tuple[str, int]:
    """Generate a prompt that randomly samples lines from a the shakespeare sonnet at sonnet.txt.

    Args:
        prompt_length_mean: The mean length of the prompt to generate.
        prompt_len_stddev: The standard deviation of the length of the prompt to generate.
        expect_output_tokens: The number of tokens to expect in the output. This is used to
        determine the length of the prompt. The prompt will be generated such that the output
        will be approximately this many tokens.

    Note:
        tokens will be counted from the sonnet using the Llama tokenizer. Using one tokenizer
        ensures a fairer comparison across different LLMs. For example, if gpt 3.5 tokenizes
        a prompt in less tokens than Llama2, then this will be reflected in the results since
        they will be fed identical prompts.

    Returns:
        A tuple of the prompt and the length of the prompt.
    """
    _get_token_length = get_token_length()

    prompt = (
        "Randomly stream lines from the following text "
        f"with {expect_output_tokens} output tokens. "
        "Don't generate eos tokens:\n\n"
    )
    # get a prompt length that is at least as long as the base
    num_prompt_tokens = sample_random_positive_int(
        prompt_tokens_mean, prompt_tokens_stddev
    )
    while num_prompt_tokens < _get_token_length(prompt):
        num_prompt_tokens = sample_random_positive_int(
            prompt_tokens_mean, prompt_tokens_stddev
        )
    remaining_prompt_tokens = num_prompt_tokens - _get_token_length(prompt)

    sonnet_lines = get_file_lines(dataset)
    random.shuffle(sonnet_lines)
    sampling_lines = True
    while sampling_lines:
        for line in sonnet_lines:
            line_to_add = line
            if remaining_prompt_tokens - _get_token_length(line_to_add) < 0:
                # This will cut off a line in the middle of a word, but that's ok since an
                # llm should be able to handle that.
                line_to_add = line_to_add[: int(math.ceil(remaining_prompt_tokens))]
                sampling_lines = False
                prompt += line_to_add
                break
            prompt += line_to_add
            remaining_prompt_tokens -= _get_token_length(line_to_add)
    return prompt, num_prompt_tokens


def sample_random_positive_int(mean: int, stddev: int) -> int:
    """Sample random numbers from a gaussian distribution until a positive number is sampled.

    Args:
        mean: The mean of the gaussian distribution to sample from.
        stddev: The standard deviation of the gaussian distribution to sample from.

    Returns:
        A random positive integer sampled from the gaussian distribution.
    """
    ret = -1
    while ret <= 0:
        ret = int(random.gauss(mean, stddev))
    return ret


def flatten_dict(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def convert_numpy(obj):
    """Convert numpy objects to native python objects.
    Args:
        obj: The object to convert.

    Returns:
        The converted object.
    """
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(v) for v in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    else:
        return obj


@functools.lru_cache(maxsize=128)
def get_token_length():
    """
    Get the token length of the tokenizer.
    :return:
    """
    tokenizer = tiktoken.get_encoding("cl100k_base")
    return lambda text: len(tokenizer.encode(text))


def load_env(current_path: str):
    print('LOAD ENV...')
    pth = os.path.join(current_path, ".env")
    if not os.path.isfile(pth):
        print(f'Did not detect the .env file at {pth}, failed to load. ')

    from dotenv import dotenv_values
    values = dotenv_values(pth)
    for k, v in values.items():
        if v is not None and len(v):
            os.environ[k] = v

def get_input_content(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        result = []
        for item in content:
            result.append(item.get("content"))
        return "\n".join(result)
