from kfp import Client, dsl, compiler
from my_component import add
from examples import ML_PIPELINE_HOST
from examples.utils.proxy import add_proxy_env_vars


@dsl.pipeline
def addition_pipeline(x: int, y: int) -> int:
    task1 = add(a=x, b=y)
    add_proxy_env_vars(task1)
    task2 = add(a=task1.output, b=x)
    add_proxy_env_vars(task2)
    return task2.output


compiler.Compiler().compile(addition_pipeline, 'addition_pipeline.yaml')

arguments = {'x': 1, 'y': 2}

client = Client(host=ML_PIPELINE_HOST)
run = client.create_run_from_pipeline_package(
    'addition_pipeline.yaml', arguments=arguments, run_name="addition_pipeline_run1", experiment_name="addition_pipeline_exp1", enable_caching=False
)