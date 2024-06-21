from kfp import dsl
from math_utils import add_numbers


@dsl.component(base_image='python:3.8',
               target_image='localhost/my-component:v5')
def add(a: int, b: int) -> int:
    return add_numbers(a, b)
