# Running the python sdk tests
## Create the virtual environment
Create a virtual environment and install the required packages
```bash
python3.10 -m venv .venv
source .venv/bin/activate
cd sdk/python
pip install .
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install uritemplate deprecated fire jsonschema
```
## Run the tests
```bash
pytest --ignore=kfp/deprecated --ignore=tests
```

## Run an individual test in PyCharm
When running individual tests in PyCharm, you need to specify the containing module and select the test
case using pytests `-k` option:
* Set `script` to the module. For example `pipelines/sdk/python/kfp/local/pipeline_orchestrator_test.py`
* Add command line option `-k` to specify the test case to run. For example `-k test_all_param_io`. See also [here](https://docs.pytest.org/en/latest/example/markers.html#using-k-expr-to-select-tests-based-on-their-name)

## Debug tests that use subprocesses
Some of the test use subprocess to create virtual environments. To debug these tests you need to disable
the option to also debug sub processes in Pycharm as described [here](https://youtrack.jetbrains.com/issue/PY-52864/Cannot-debug-python-Poetry#focus=Comments-27-5748162.0-0)
Otherwise an error like
```
stdout = b'unknown option --port\nusage: /tmp/tmpkdgwaqmu/bin/python [option] ... [-c cmd | -m mod | file | -] [arg] ...\nTry `...\\\'pip\\\']\\nrunpy.run_module("pip", run_name="__main__", alter_sys=True)\\n\']\' returned non-zero exit status 2.\n'
```
might occur (`unknown option --port` is the error message in this case).




