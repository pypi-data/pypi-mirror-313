from pathlib import Path

COMMON_MODEL_PATH = Path.home() / ".cache" / "huggingface" / "hub"
TOKENIZER_MODEL_PATH = COMMON_MODEL_PATH / "models--hf-internal-testing--llama-tokenizer"


class TOKENIZER_MODEL:
    """# 0: openai tiktoken 1: models--hf-internal-testing--llama-tokenizer"""
    tiktoken = 0
    llama = 1


default_tokenizer_model = TOKENIZER_MODEL.tiktoken


class METRICS:
    START_TIME = "start_time"
    END_TIME = "end_time"
    START_TIME_M = "start_time_m"
    END_TIME_M = "end_time_m"
    INTER_TOKEN_LAT = "inter_token_latency_s"
    TTFT = "ttft_s"
    E2E_LAT = "end_to_end_latency_s"
    NUM_INPUT_TOKENS = "number_input_tokens"
    NUM_OUTPUT_TOKENS = "number_output_tokens"
    NUM_TOTAL_TOKENS = "number_total_tokens"
    REQ_OUTPUT_THROUGHPUT = "request_output_throughput_token_per_s"
    ERROR_MSG = "error_msg"
    ERROR_CODE = "error_code"
    ERROR_CODE_FREQ = "error_code_frequency"
    NUM_ERRORS = "number_errors"
    OUTPUT_THROUGHPUT = "mean_output_throughput_token_per_s"
    NUM_COMPLETED_REQUESTS = "num_completed_requests"
    COMPLETED_REQUESTS_PER_MIN = "num_completed_requests_per_min"
    ERROR_RATE = "error_rate"
    NUM_REQ_STARTED = "num_requests_started"
    TOTAL_COST_TIME = "total_cost_time_s"
    REQUEST_CONTENT = "request_content"
    RESPONSE_CONTENT = "response_content"
    EXTRA_DATA = "extra_data"
