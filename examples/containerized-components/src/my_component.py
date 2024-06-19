from kfp import dsl
from math_utils import add_numbers


@dsl.component
def add(a: int, b: int) -> int:
    return add_numbers(a, b)


@dsl.component(base_image='python:3.8',
               target_image='my-component:v1')
def add(a: int, b: int) -> int:
    return add_numbers(a, b)
