import json

from gevent import monkey

monkey.patch_all()
import gevent
from gevent import queue, pool
import traceback
import time
from typing import Optional, Dict, Any, List
from tqdm import tqdm
import logging
from llmbench.data import get_file_lines
from llmbench.report import Report, HtmlReport
from llmbench.inference.general_client import GeneralClient

logger = logging.getLogger(__name__)


class TokenBenchmark(object):

    def __init__(
            self,
            dataset: str,
            num_concurrent_requests: int,
            test_timeout: int,
            model: str,  # 模型名称或模型路径
            max_request_sample_num: int = 10000,  # 最大请求样本数，默认-1, 无限制
            result_dir: str = None,  # 结果保存路径
            need_calc_token: bool = False,
            extra_params: Optional[Dict[str, Any]] = None,
    ):
        self.pool = pool.Pool(num_concurrent_requests)
        self.dataset = dataset
        self.duration = test_timeout
        self.model = model
        if extra_params is None:
            extra_params = {}
        if isinstance(extra_params, str) and extra_params.startswith("{"):
            extra_params = json.loads(extra_params)
        self.extra_params = extra_params
        self.max_request_sample_num = max_request_sample_num if max_request_sample_num != -1 else max_request_sample_num
        self.report = Report(model.replace("/", "_"), result_dir, **{"start_t": time.time()})
        self.num_concurrent_requests = num_concurrent_requests
        self.max_queue_size = num_concurrent_requests * 1000
        self.job_queue = queue.Queue(maxsize=self.max_queue_size)
        self.report_queue = queue.Queue()
        self.client = GeneralClient(self.model, self.extra_params)
        self.need_calc_token = need_calc_token

    def get_prompt_data(self, max_line_num: int = 5000):
        """获取测试数据"""
        data_lines = get_file_lines(self.dataset, max_line_num)
        return data_lines

    def send_data(self, prompt, **kwargs):
        return self.client.send_data(prompt, **kwargs)

    def clac_report(self):
        """计算报告"""
        start_time = time.time()
        output_time = time.time()
        report_list = []
        while time.time() - start_time < self.duration + 10:
            try:
                if self.report_queue.empty():
                    gevent.sleep(2)
                    continue
                report = self.report_queue.get_nowait()
                if report:
                    report_list.append(report)
                if time.time() - output_time > 10:
                    output_time = time.time()
                    self.report.save_result(report_list)
                    report_list.clear()
            except Exception as e:
                logger.error(traceback.format_exc())
                gevent.sleep(2)
        if len(report_list) > 0:
            self.report.save_result(report_list)

    def worker(self):
        """工作线程"""
        start_time = time.time()
        while time.time() - start_time < self.duration:
            try:
                if self.job_queue.empty():
                    gevent.sleep()
                    continue
                task = self.job_queue.get_nowait()
                if task:
                    result = self.send_data(task)
                    if result:
                        self.report_queue.put_nowait(result)
            except (Exception, queue.Empty) as e:
                logger.error(traceback.format_exc())
                gevent.sleep()

    def producer(self):
        """生产者线程"""
        start_time = time.time()
        iter_num = 0
        prompt = self.get_prompt_data(self.max_request_sample_num)
        max_line_num = self.max_request_sample_num if len(prompt) >= self.max_request_sample_num else len(prompt)
        while time.time() - start_time < self.duration:
            try:
                if not self.job_queue.full():
                    iter_num += 1
                    self.job_queue.put_nowait(prompt[iter_num % max_line_num])
                else:
                    gevent.sleep()  # 等待队列有空间
            except queue.Full:
                gevent.sleep()  # 等待队列有空间

    def wait_all_task(self, tasks: List[gevent.Greenlet]):
        """等待所有任务完成"""
        gevent.joinall(tasks)

    def start_all_task(self) -> List[gevent.Greenlet]:
        job_events = []
        try:
            # 生产线程
            job_events.append(gevent.spawn(self.producer))

            # 报告线程
            job_events.append(gevent.spawn(self.clac_report))

            # 工作线程
            job_events.extend(
                [gevent.spawn(self.worker) for _ in range(self.num_concurrent_requests)])

        except Exception as e:
            logger.error(traceback.format_exc())
        return job_events

    def start_process_monitor(self):
        """进度监控"""

        def update_process(pbar, process):
            pbar.n = int(process)
            pbar.refresh()

        start_time = time.time()
        with tqdm(total=self.duration, desc="执行进度") as pbar:
            while time.time() - start_time < self.duration:
                gevent.sleep(5)
                update_process(pbar, time.time() - start_time)
            update_process(pbar, time.time() - start_time)

    def run_token_benchmark(self):
        tasks = self.start_all_task()
        # 启动进度监听
        self.start_process_monitor()
        # 等待所用任务完成
        self.wait_all_task(tasks)
        HtmlReport(self.report).make_report()

