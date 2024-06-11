import os

from kfp import Client, compiler, dsl


@dsl.component
def say_hello() -> str:
    hello_text = f'Hello!'
    print(hello_text)
    return hello_text


@dsl.pipeline
def hello_pipeline() -> str:
    hello_task = ((say_hello().set_env_variable('http_proxy', os.getenv('http_proxy')))
                  .set_env_variable('https_proxy', os.getenv('http_proxy')).set_env_variable('no_proxy', os.getenv('no_proxy')))
    return hello_task.output


compiler.Compiler().compile(hello_pipeline, 'hello_pipeline.yaml')

client = Client(host='http://127.0.0.1:8080')
run = client.create_run_from_pipeline_package(
    'hello_pipeline.yaml', run_name="(hello_pipeline_run", experiment_name="(hello_pipeline_exp", enable_caching=False
)
