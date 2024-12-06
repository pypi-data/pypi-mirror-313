"""
@author:cmcc
@file: report.py
@time: 2024/9/1 20:50
"""
import json
import re
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Iterable
import numpy as np
import pandas as pd
from llmbench.common.constants import METRICS
from llmbench.utils import flatten_dict, convert_numpy
import plotly.express as px
import plotly.io as pio


class Report:

    def __init__(self, model: str, output_dir: str, **kwargs):
        self.model = model
        filename = re.sub(r"-{2,}", "-",
                          re.sub(r"[^\w\d-]+", "-", f"{model}_token_benchmark"))
        if output_dir is None or len(output_dir) == 0:
            output_dir = os.getcwd() + "/results/" + filename + "/" + datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            output_dir += "/" + filename + "/" + datetime.now().strftime("%Y%m%d%H%M%S")
        results_dir = Path(output_dir)
        self.result_dir = results_dir
        if not results_dir.exists():
            results_dir.mkdir(parents=True)
        elif not results_dir.is_dir():
            raise ValueError(f"{results_dir} is not a directory")
        self.filename = results_dir / f"{model}_token_benchmark.jsonl"
        self.filename_summary = results_dir / f"{model}_token_benchmark_summary.json"
        self.token_df = None
        self.report_df = None
        self.report_info = {}
        self.print_exec_info: bool = True if os.environ.get("print_exec_info", "on") == "on" else False
        self.start_t = kwargs.get("start_t")

    def save_result(self, results: List[Dict]):
        if not results:
            return
        data = []
        for result in results:
            data.append(json.dumps(flatten_dict(result), ensure_ascii=False))
        with open(self.filename, "a+", encoding="utf-8") as f:
            data = "\n".join(data) + "\n"
            f.write(data)
        self.calc_summary()

    def calc_summary(self):
        def flatten(item):
            for sub_item in item:
                if isinstance(sub_item, Iterable) and not isinstance(sub_item, str):
                    yield from flatten(sub_item)
                else:
                    yield sub_item
        df = pd.read_json(self.filename, orient="records", lines=True)
        start_time = df[METRICS.START_TIME_M].min()
        end_time = df[METRICS.END_TIME_M].max()
        df_without_errored_req = df[df[METRICS.ERROR_CODE].isna()]
        # 分位数
        df_calc = df_without_errored_req[[
            METRICS.TTFT, METRICS.INTER_TOKEN_LAT, METRICS.E2E_LAT,
            METRICS.REQ_OUTPUT_THROUGHPUT, METRICS.NUM_INPUT_TOKENS, METRICS.NUM_OUTPUT_TOKENS]]
        df_calc.loc[:, :] = df_calc.replace('', np.nan)
        df_calc = df_calc.apply(pd.to_numeric, errors='coerce')
        quantiles = [0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
        quantiles_df = df_calc.quantile(quantiles).transpose()
        quantiles_df.columns = [f'P{int(q * 100)}' for q in quantiles]
        # 计算其他统计量
        stats = {
            'mean': df_calc.mean(),
            'std': df_calc.std(),
            'max': df_calc.max(),
            'min': df_calc.min()
        }
        stats_df = pd.DataFrame(stats)
        # 合并所有统计量到一个表格
        df_result = pd.concat([stats_df, quantiles_df], axis=1)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_columns', None)
        if self.print_exec_info:
            print("==" * 80)
            print(df_result)

        self.token_df = df_result

        ret = {}
        for index, row in df_result.iterrows():
            for col in df_result.columns:
                ret[f"{index}_{col}"] = row[col]
        ret[METRICS.NUM_REQ_STARTED] = df.shape[0]
        ret[METRICS.TOTAL_COST_TIME] = end_time - start_time
        if self.print_exec_info:
            print("=="*80)
            print(f"model name: {self.model}")
            print(f"start_time: {df['start_time'].min()}")
            print(f"end_time: {df['end_time'].max()}")
            print(f"total cost time: {end_time - start_time}")
        error_codes = df[METRICS.ERROR_CODE].dropna()
        num_errors = len(error_codes)
        ret[METRICS.ERROR_RATE] = num_errors / df.shape[0] if df.shape[0] else 0
        ret[METRICS.NUM_ERRORS] = num_errors
        if self.print_exec_info:
            print(f"Number Of Errored Requests: {num_errors}")
        error_code_frequency = dict(error_codes.value_counts())
        if num_errors:
            error_code_frequency = dict(error_codes.value_counts())
            print("Error Code Frequency")
            print(convert_numpy(error_code_frequency))
        ret[METRICS.ERROR_CODE_FREQ] = convert_numpy(error_code_frequency)
        overall_output_throughput = df_without_errored_req[METRICS.NUM_OUTPUT_TOKENS].sum() / (end_time - start_time)
        ret[METRICS.OUTPUT_THROUGHPUT] = overall_output_throughput
        num_completed_requests = len(df_without_errored_req)
        num_completed_requests_per_min = (num_completed_requests / (end_time - start_time) * 60)
        if self.print_exec_info:
            print(f"Overall Output Throughput: {overall_output_throughput}")
            print(f"Number Of Completed Requests: {num_completed_requests}")
            print(f"Completed Requests Per Minute: {num_completed_requests_per_min}")
            print("==" * 80)
        ret[METRICS.NUM_COMPLETED_REQUESTS] = num_completed_requests
        ret[METRICS.COMPLETED_REQUESTS_PER_MIN] = num_completed_requests_per_min

        with open(self.filename_summary, "w") as f:
            f.write(json.dumps(flatten_dict(convert_numpy(ret)), indent=4, ensure_ascii=False))

        self.report_info.update({
            "测试模型": [self.model], "开始时间": [df['start_time'].min()], "结束时间": [df['end_time'].max()],
            "总时间花费(s)": [end_time - start_time], "错误请求数": [num_errors],
            "总体输出吞吐量(token)": [overall_output_throughput],
            "完成请求的数量": [num_completed_requests],
            "每分钟的请求数": [num_completed_requests_per_min],
            "执行总耗时(s)": [time.time() - self.start_t]
        })
        self.report_df = pd.DataFrame(self.report_info)


class HtmlReport:
    """
    生成html，性能测试报告
    """
    def __init__(self, report: Report):
        self.report = report
        self.token_jsonl_file = self.report.filename  # path to the individual responses json file
        self.output_dir = self.report.result_dir
        df = pd.read_json(self.token_jsonl_file, encoding="utf-8", lines=True)
        self.valid_df = df[(df["error_code"].isna())]
        self.input_output_token_info = ""
        self.ttfts_pic = None
        self.latency_pic = None

    def make_report(self):
        self.pic_to_ttft()
        self.pic_to_token_latencies()
        token_df = self.report.token_df.rename(
            index={"ttft_s": "首Token延迟(s)", "inter_token_latency_s": "内token延迟(s)", "end_to_end_latency_s": "端到端延迟(s)",
                   "number_input_tokens": "输入token量", "request_output_throughput_token_per_s": "token吞吐量(tps)",
                   "number_output_tokens": "输出token量"})
        self.report.report_df.set_index("测试模型", inplace=True)
        summary_df = self.report.report_df.T

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>llmbench report</title>
        </head>
        <body>
            <div>
                <h1 style='text-align:center;'>LlmBench 性能测试报告</h1> 
                <h5 style='text-align:center;'>CMRI TestTeam</h5> 
            </div>
            <h1>概览：</h1>
            <hr />
            <div id="desc">
                <h2> 本次测试信息 </h2>
                {summary_df.to_html()}
            </div>
            </br>
            <div id="desc">
                {token_df.to_html()}
            <div>
                <h4>{self.input_output_token_info}</h5>
            </div>
                <h6>注:</br>
                    内token延迟(s): 可能表示在两个标记之间（token）的网络延迟，这有助于了解数据在网络中的传输速度。</br>
                    端到端延迟(s): 是端到端的总延迟，它包括了所有传输和处理的时间，是衡量整个通信链路性能的重要指标。</br>
                    输入token量: 指的是输入到系统中的数据量(token)。</br>
                    输出token量: 则是系统输出的数据量(token)。</br>
                    token吞吐量(tps)：吞吐量，即每秒针对所有请求生成的 token 数。以上六个指标都针对单个请求，而吞吐量是针对所有并发请求的。
                </h6>
            </div>
            <h1>详情：</h1>
            <hr />
            <div>
                <h3>首Token延迟:</h3>
                <h6>注：即从输入到输出第一个token的延迟。在在线的流式应用中，TTFT 是最重要的指标，因为它决定了用户体验。</h6>
                {pio.to_html(self.ttfts_pic, full_html=False)}
            </div>
            <div>
                <h3>延迟:</h3>
                <h6>注：即从输入到输出最后一个token的延迟。 Latency = (TTFT) + (TPOT) * (the number of tokens to be generated). Latency 可以转换为 Tokens Per Second (TPS)：TPS = (the number of tokens to be generated) / Latency。</h6>
                {pio.to_html(self.latency_pic, full_html=False)}
            </div>
        </body>""" + """
        <style>
            .dataframe {border-collapse: collapse !important;}
        </style>
        </html>
        """
        with open(os.path.join(self.output_dir, "report.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

    def pic_to_ttft(self):
        final_df = pd.DataFrame()
        final_df["number_input_tokens"] = self.valid_df["number_input_tokens"]
        final_df["number_output_tokens"] = self.valid_df["number_output_tokens"]
        final_df["ttft_s"] = self.valid_df["ttft_s"]
        final_df["end_to_end_latency_s"] = self.valid_df["end_to_end_latency_s"]
        final_df["generation_throughput"] = self.valid_df["request_output_throughput_token_per_s"]

        mean_tokens_in = final_df["number_input_tokens"].mean()
        mean_tokens_out = self.valid_df["number_output_tokens"].mean()
        self.input_output_token_info = f"平均输入token数: {mean_tokens_in}.</br> 平均输出token数: {mean_tokens_out}."
        self.ttfts_pic = px.scatter(final_df, x="number_input_tokens", y="ttft_s")

    def pic_to_token_latencies(self):
        all_token_latencies = self.valid_df['end_to_end_latency_s'].apply(pd.Series).stack()
        all_token_latencies = all_token_latencies.reset_index(drop=True)
        self.latency_pic = px.scatter(all_token_latencies)

