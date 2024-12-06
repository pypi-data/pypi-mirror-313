"""
扫描evals中的client，并返回一个client实例
扫描自身client，并返回一个client实例

俩个客户端，尽量结构一致
"""
import importlib.util
import inspect
import os
import logging
import sys
from pathlib import Path

from dacite import from_dict
from llmbench.inference.clients.request_data import Request

logger = logging.getLogger(__name__)


def import_module_by_file(file_path: str, module_name: str = ""):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    if module_name is not None:
        sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class GeneralClient:

    def __init__(self, model, extra_params):
        self.model = model
        self.extra_params = extra_params or {}
        self.client_path = os.environ.get("client_path") or self.extra_params.get("client_path") # 测试用extra_params, 真实环境用env文件
        self.client = None
        self.is_self_client = True
        self.get_client()

    def get_client(self):
        client = self._get_self_client(self.model)
        if client is None:
            if os.path.exists(self.client_path):
                load_client_info, self.is_self_client = LoadClient(self.client_path).get_file_client()
                if self.model in load_client_info:
                    client = load_client_info.get(self.model)
            # self.is_self_client = False
            # if os.path.exists(self.client_path):
            #     if "llmbench_client" in self.client_path:
            #         self.is_self_client = True
            #         client = self._get_file_client(self.model)
            #     else:
            #         client = self._get_eval_client(self.model)
        if client is None:
            raise ValueError(f"Could not find client for Model_Name[{self.model}], or file_path:{self.client_path}")
        logger.info(f"current model is :{client}, is llmbench model: {self.is_self_client}")
        if self.is_self_client:
            self.client = client(**self.extra_params)
        else:
            self.client = client(model_extra_options=self.extra_params)

    # def find_client_class(self, super_classes):
    #     super_class_names = [i.__name__ for i in super_classes]
    #     if "Client" in super_class_names and "ABC" in super_class_names:
    #         return True
    #     return False

    # def _get_file_object(self, client_file_path: str, module_name: str):
    #     module = import_module_by_file(client_file_path, module_name)
    #     for name, obj in inspect.getmembers(module):
    #         if inspect.isclass(obj) and obj.__name__ != "Client" and self.find_client_class(inspect.getmro(obj)):
    #             return obj
    #     return None

    # def _get_file_client(self, client_file_path: str):
    #     client_dir, module_name = os.path.split(client_file_path)
    #     client = self._get_file_object(client_file_path, module_name)  # 文件形式加载
    #     if client is None:
    #         logger.warning(f"Could not find client for model: {client_file_path} "
    #                        f"file_path: {client_file_path}, try to load by driver")
    #     else:
    #         client = client
    #     return client

    def _get_self_client(self, model: str):
        self.is_self_client = True
        load_client_info, _ = LoadClient().get_file_client()
        if model in load_client_info:
            client = load_client_info.get(model)
            return client

    def _get_eval_client(self, model):
        try:
            from evals.clients.client_auto import Model_Client
        except ImportError:
            logger.warning(f"Could not find client for model in evals: {model}")
            return
        if "/" in model:
            model_name, engine = model.split("/")
            if model_name in Model_Client:
                for _client in Model_Client[model_name]:
                    if engine in _client.get("engine", []):
                        client = _client.get("client")
                        return client

    def send_data(self, prompt, **kwargs):
        if self.is_self_client:
            result = self.client.make_request(from_dict(Request, {
                "model": self.model,
                "prompt": prompt,
                **kwargs
            }))
            result = result[0]
        else:
            result = self.client.make_request(from_dict(Request, {
                "model": self.model,
                "prompt": prompt,
                **kwargs
            }))
            if result:
                result = result.raw_response
        return result


class LoadClient:
    """
    根据模型自身定义的属性查找client,并返回映射关系
    """
    def __init__(self, client_file_path=None):
        self.client_file_path = client_file_path

    def _get_file_object(self, client_file_path: str, module_name: str):
        module = import_module_by_file(client_file_path, module_name)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and hasattr(obj, "Model_Name"):
                return {obj.Model_Name: obj}

    def get_file_client(self):
        is_self_client = True
        if not self.client_file_path:
            self.client_file_path = os.path.join(os.path.dirname(__file__), "clients")
        else:
            if self.client_file_path.endswith("eval_client"):
                is_self_client = False

        client_mapping = {}
        for client_file in os.listdir(self.client_file_path):
            tmp_client = Path(client_file)
            if tmp_client.stem.startswith("client") and tmp_client.suffix == ".py":
                map_info = self._get_file_object(os.path.join(self.client_file_path, client_file), client_file)
                if map_info:
                    client_mapping.update(**map_info)
        if not client_mapping:
            logger.warning(f"Could not find client by Model_Name.")
        return client_mapping, is_self_client
