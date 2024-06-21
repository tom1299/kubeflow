from kfp import Client, compiler, dsl
from examples import ML_PIPELINE_HOST
from examples.utils.proxy import add_proxy_env_vars


@dsl.component(
    base_image="python:3.8"
)
def say_hello():
    hello_text = 'Hello!'
    print(hello_text)


@dsl.pipeline
def hello_pipeline():
    add_proxy_env_vars(say_hello())


compiler.Compiler().compile(hello_pipeline, 'hello_pipeline.yaml')

client = Client(host=ML_PIPELINE_HOST)
run = client.create_run_from_pipeline_package(
    'hello_pipeline.yaml', run_name="hello_pipeline_run2", experiment_name="hello_pipeline_exp2", enable_caching=False
)
