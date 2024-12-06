import argparse
import os
from llmbench.inference.token_benchmark import TokenBenchmark


def main():
    from llmbench.utils import load_env
    current_path = os.getcwd()
    load_env(current_path)
    args = argparse.ArgumentParser(
        description="Run a token throughput and latency benchmark."
    )
    args.add_argument("--model", type=str, help="The model to use for this load test.")
    args.add_argument("--dataset", type=str, default="sonnet", help="The model to use for this load test.")
    args.add_argument(
        "--num-concurrent-requests",
        type=int,
        default=10,
        help=("The number of concurrent requests to send (default: %(default)s)"),
    )
    args.add_argument(
        "--timeout",
        type=int,
        default=90,
        help="The amount of time to run the load test for. (default: %(default)s)",
    )
    args.add_argument(
        "--results-dir",
        type=str,
        default="",
        help=(
            "The directory to save the results to. "
            "(`default: %(default)s`) No results are saved)"
        ),
    )
    args.add_argument(
        "--extra_params",
        type=str,
        default="{}",
        help=(
            "The extra_params to use for the llm api.  "
        ),
    )
    args.add_argument(
        "--max_request_sample_num",
        type=int,
        default=-1,
        help=(
            "The maximum request number for llm api.  "
            "   -1：No limit, depending on the amount of data in the dataset"
        ),
    )
    args = args.parse_args()
    TokenBenchmark(
        model=args.model,
        dataset=args.dataset,
        max_request_sample_num=args.max_request_sample_num,
        test_timeout=args.timeout,
        num_concurrent_requests=args.num_concurrent_requests,
        extra_params=args.extra_params,
        result_dir=args.results_dir,
    ).run_token_benchmark()


if __name__ == "__main__":
    main()
