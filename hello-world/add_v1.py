import os
import kfp.dsl as dsl
from kfp import compiler
from kubernetes.client.models import V1EnvVar
from kfp import Client
from kfp.components import create_component_from_func


def add(a: float, b: float) -> float:
    print(f"Adding {a} and {b} to get {a + b}")
    return a + b


add_op = create_component_from_func(
    add, output_component_file='add_component.yaml')


@dsl.pipeline(
    name='Addition pipeline',
    description='An example pipeline that performs addition calculations.'
)
def add_pipeline(
        a='1',
        b='7',
):
    first_add_task = add_op(a, 4)
    second_add_task = add_op(first_add_task.output, b)


compiler.Compiler().compile(add_pipeline, 'add_pipeline.yaml')

client = Client(host='http://127.0.0.1:8080')
run = client.create_run_from_pipeline_package(arguments={'a': '7', 'b': '10'},
                                              pipeline_file='add_pipeline.yaml',
                                              run_name="hello_pipeline_run",
                                              experiment_name="hello_pipeline_exp", enable_caching=False)
