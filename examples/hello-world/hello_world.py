import os
from kfp import Client, compiler, dsl
from get_no_proxy_var import get_no_proxy_var


http_proxy=os.getenv('http_proxy')
https_proxy=os.getenv('https_proxy')
no_proxy=os.getenv('no_proxy') + "," + get_no_proxy_var("https://127.0.0.1:6443", ["default", "kubeflow"])
ml_pipeline_host = os.getenv('http://127.0.0.1:8080')


@dsl.component(
    base_image="python:3.8"
)
def say_hello():
    hello_text = 'Hello!'
    print(hello_text)


@dsl.pipeline
def hello_pipeline():
    say_hello().set_env_variable('http_proxy',http_proxy).set_env_variable('https_proxy',https_proxy).set_env_variable('no_proxy',no_proxy)


compiler.Compiler().compile(hello_pipeline, 'hello_pipeline.yaml')

client = Client(host=ml_pipeline_host)
run = client.create_run_from_pipeline_package(
    'hello_pipeline.yaml', run_name="hello_pipeline_run2", experiment_name="hello_pipeline_exp2", enable_caching=False
)
