import json
import random
import time
import requests
from llmbench.inference.clients.client_abc import Client
from llmbench.common.constants import METRICS
from llmbench.utils import generate_token


class TestAPIClient(Client):
    """Client for OpenAI Chat Completions API."""
    Model_Name = "test"

    def __init__(self, **kwargs):
        pass

    def get_token(self, auth):
        auth = auth or {}
        apikey = auth.get("API_KEY", "65ae213bf7b40c25fbe169bb.JxNn87L/KgLO7rWGOTHOnTzW0NCnJQaK")
        return generate_token(apikey, 3600)

    def make_request(self, request_config):
        prompt = request_config.prompt
        prompt_len = random.randint(len(prompt), 100)
        jwt_token = self.get_token(request_config.auth)
        address = request_config.url or "http://127.0.0.1:5000/stream"

        body = {
            "modelId": request_config.model or "jiutian-lan",
            "prompt": prompt,
            "params": {"temperature": 0.8, "top_p": 0.95},
            "history": [],
            "stream": True
        }
        headers = {'content-type': "application/json", "Authorization": "Bearer " + jwt_token}

        time_to_next_token = []
        ttft = 0
        tokens_received = random.randint(1, 10)
        error_response_code = -1
        error_msg = ""
        generated_text = ""
        output_throughput = 0
        total_request_time = 0
        start_time = time.monotonic()
        most_recent_received_token_time = time.monotonic()

        metrics = {METRICS.ERROR_CODE: None, METRICS.ERROR_MSG: "",
                   METRICS.START_TIME: time.time(), METRICS.START_TIME_M: start_time}

        try:
            with requests.get(
                    address,
                    json=body,
                    stream=True,
                    timeout=180,
                    headers=headers,
            ) as response:
                time.sleep(random.randint(1, 3))
                if response.status_code != 200:
                    error_msg = response.text
                    error_response_code = response.status_code
                    response.raise_for_status()
                for chunk in response.iter_lines(chunk_size=None):
                    if not chunk:
                        continue

                    chunk = chunk.decode("utf-8").strip()
                    stem = "data:"
                    if not chunk.startswith(stem):
                        continue
                    chunk = chunk.split(stem)[-1]
                    try:
                        data = json.loads(chunk)
                    except Exception as e:
                        continue

                    tokens_received += 1

                    if "delta" not in data.keys():
                        error_msg = data["message"]
                        error_response_code = data["code"]
                        raise RuntimeError(data["message"])

                    delta = data["delta"]
                    if delta:
                        if not ttft:
                            time.sleep(random.random())
                            ttft = time.monotonic() - start_time
                            time_to_next_token.append(ttft)
                        else:
                            time_to_next_token.append(
                                time.monotonic() - most_recent_received_token_time
                            )
                        most_recent_received_token_time = time.monotonic()
                        generated_text += delta

            total_request_time = time.monotonic() - start_time
            output_throughput = tokens_received / total_request_time

        except Exception as e:
            metrics[METRICS.ERROR_MSG] = error_msg
            metrics[METRICS.ERROR_CODE] = error_response_code
            print(f"Warning Or Error: {e}")
            print(error_response_code)

        metrics[METRICS.END_TIME_M] = time.monotonic()
        metrics[METRICS.END_TIME] = time.time()
        # This should be same as METRICS[METRICS.E2E_LAT]. Leave it here for now
        metrics[METRICS.INTER_TOKEN_LAT] = sum(time_to_next_token)
        metrics[METRICS.TTFT] = ttft
        metrics[METRICS.E2E_LAT] = total_request_time
        metrics[METRICS.REQ_OUTPUT_THROUGHPUT] = output_throughput
        metrics[METRICS.NUM_TOTAL_TOKENS] = tokens_received + prompt_len
        metrics[METRICS.NUM_OUTPUT_TOKENS] = tokens_received
        metrics[METRICS.NUM_INPUT_TOKENS] = prompt_len
        return metrics, generated_text, request_config
