from truefoundry.workflow import PythonTaskConfig, TaskPythonBuild, task, workflow


@task(
    task_config=PythonTaskConfig(
        image=TaskPythonBuild(
            python_version="3.9",
            pip_packages=["truefoundry[workflow]"],
        ),
        service_account="tfy-workflows-sa",
    )
)
def say_hello() -> str:
    return "Hello, World!"


@workflow
def hello_world_wf() -> str:
    res = say_hello()
    return res
