import tempfile
from kfp import Client, dsl, compiler
from examples.containerized_components.my_component import add
from examples import ML_PIPELINE_HOST
from examples.utils.proxy import add_proxy_env_vars


@dsl.pipeline
def addition_pipeline(x: int, y: int) -> int:
    task1 = add(a=x, b=y)
    add_proxy_env_vars(task1)
    task2 = add(a=task1.output, b=x)
    add_proxy_env_vars(task2)
    return task2.output


# Create a temporary file
with tempfile.NamedTemporaryFile(suffix=".yaml", delete=True) as temp:
    # Compile the pipeline to the temporary file
    compiler.Compiler().compile(addition_pipeline, temp.name)

    # Read the contents of the file and print them
    with open(temp.name, 'r') as f:
        print(f.read())

    arguments = {'x': 1, 'y': 2}

    client = Client(host=ML_PIPELINE_HOST)
    # Run the pipeline from the temporary file
    run = client.create_run_from_pipeline_package(
        temp.name, arguments=arguments, run_name="addition_pipeline_run1", experiment_name="addition_pipeline_exp1",
        enable_caching=False
    )
