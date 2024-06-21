from kfp import Client, compiler, dsl
from examples import http_proxy, https_proxy, no_proxy, ML_PIPELINE_HOST


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

client = Client(host=ML_PIPELINE_HOST)
run = client.create_run_from_pipeline_package(
    'hello_pipeline.yaml', run_name="hello_pipeline_run2", experiment_name="hello_pipeline_exp2", enable_caching=False
)
