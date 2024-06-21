import os
from .utils.proxy import get_no_proxy_var

http_proxy=os.getenv('http_proxy')
https_proxy=os.getenv('https_proxy')
no_proxy=os.getenv('no_proxy') + "," + get_no_proxy_var("https://127.0.0.1:6443", ["default", "kubeflow"])
ML_PIPELINE_HOST = os.getenv('http://127.0.0.1:8080')