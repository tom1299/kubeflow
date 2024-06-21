from kfp import Client, dsl, compiler
from my_component import add
from examples import http_proxy, https_proxy, no_proxy, ML_PIPELINE_HOST

@dsl.pipeline
def addition_pipeline(x: int, y: int) -> int:
    task1 = add(a=x, b=y).set_env_variable('http_proxy',http_proxy).set_env_variable('https_proxy',https_proxy).set_env_variable('no_proxy',no_proxy)
    task2 = add(a=task1.output, b=x).set_env_variable('http_proxy',http_proxy).set_env_variable('https_proxy',https_proxy).set_env_variable('no_proxy',no_proxy)
    return task2.output


compiler.Compiler().compile(addition_pipeline, 'addition_pipeline.yaml')

arguments = {'x': 1, 'y': 2 }

client = Client(host=ML_PIPELINE_HOST)
run = client.create_run_from_pipeline_package(
    'addition_pipeline.yaml', arguments=arguments, run_name="addition_pipeline_run1", experiment_name="addition_pipeline_exp1", enable_caching=False
)