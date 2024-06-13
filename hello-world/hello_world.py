import os

from kfp import Client, compiler, dsl


@dsl.component(
    base_image="python:3.8"
)
def say_hello():
    hello_text = 'Hello!'
    print(hello_text)


@dsl.pipeline
def hello_pipeline():
    say_hello().set_env_variable('http_proxy', 'http://10.32.230.10:3128').set_env_variable('https_proxy','http://10.32.230.10:3128').set_env_variable('no_proxy','10.96.0.1,kubernetes,metadata-envoy-service,cache-server,metadata-grpc-service,mysql,ml-pipeline,minio-service,0.0.0.0,localhost,127.0.0.1')


compiler.Compiler().compile(hello_pipeline, 'hello_pipeline.yaml')

client = Client(host='http://127.0.0.1:8080')
run = client.create_run_from_pipeline_package(
    'hello_pipeline.yaml', run_name="hello_pipeline_run2", experiment_name="hello_pipeline_exp2", enable_caching=False
)
