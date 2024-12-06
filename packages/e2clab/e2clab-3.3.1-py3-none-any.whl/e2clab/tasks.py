"""
This module serves as an interface between the CLI and the Experiment object.
Creating/Reloading the experimentfrom a pickle file thanks to the 'enostask' wrapper
"""

import logging
from functools import wraps
from pathlib import Path
from typing import Optional
from uuid import UUID

import click
from enoslib.task import enostask

import e2clab.experiment as e2c_exp
from e2clab.constants import WorkflowTasks
from e2clab.experiment import Experiment
from e2clab.log import get_logger

logger = get_logger(__name__, ["TASK"])

ENV_ERROR_MSG = "Error in env, exiting..."
EXPERIMENT = "experiment"


class TaskError(click.Abort):
    """Makes click abort correctly and exit"""

    pass


def e2ctask(new: bool = False):
    """
    Returns a decorator to manage experiment instance creation, storage and retrieval
    i.e. tasks.

    The decorated function must be called with an "env" argument pointing to the dir
    where the 'env' pickle object is/should be stored, and a "exp" argument if
    new is not True to recieve the loaded experiment instance.

    Usage:
    ```python
    # Creating an experiment
    @e2ctask(new=True)
    def new_init_task(...) -> Experiment:
        exp = Experiment(...)
        return exp


    # Retrieving the experiment
    @e2ctask()
    def new_task(exp):
        # call your Experiment method
        exp.task()
    ```

    Then you can call your tasks from the cli per exmple:
    ```python
    import e2clab.tasks as task

    task.new_init_task(env="path/to/dir")
    task.new_task(env="path/to/dir")
    ```

    Args:
        new (bool, optional): Creates a new environment.
            If True decorated function must return an `e2clab.Experiment` instance.
            Defaults to False.
    """

    def decorator(fn):
        # Disable specific enoslib task logger
        logging.getLogger("enoslib.task").setLevel(logging.ERROR)

        @enostask(new=new, symlink=False)
        @wraps(fn)
        def wrapper(*args, **kwargs):
            env = kwargs["env"]
            kwargs.pop("env")
            try:
                if not new:
                    # Must retrieve exp from env
                    exp: Experiment = env[EXPERIMENT]
                    check_is_exp(exp)
                    # Pass experiment object to kwargs
                    kwargs["exp"] = exp
                r = fn(*args, **kwargs)
                if new:
                    # Function must return new exp instance
                    check_is_exp(r)
                    exp = r
                # Storing after
                env[EXPERIMENT] = exp
                return r
            except Exception as e:
                logger.exception(e)
                raise TaskError()

        def check_is_exp(exp):
            # Using Experiment type like this because of testing
            # https://stackoverflow.com/questions/11146725/isinstance-and-mocking
            if not isinstance(exp, e2c_exp.Experiment):
                logger.error(f"Error: {exp} in not instance of Experiment. Exiting ...")
                raise Exception()

        return wrapper

    return decorator


@e2ctask(new=True)
def infra(
    scenario_dir: Path,
    artifacts_dir: Path,
    optimization_config=None,
    optimization_id: Optional[UUID] = None,
) -> Experiment:
    exp = Experiment(
        scenario_dir=scenario_dir,
        artifacts_dir=artifacts_dir,
        optimization_config=optimization_config,
        optimization_id=optimization_id,
    )
    exp.initiate()
    exp.infrastructure()
    return exp


@e2ctask()
def network(exp: Experiment) -> None:
    exp.network()


@e2ctask()
def app(exp: Experiment, task: WorkflowTasks, app_conf: Optional[str] = None) -> None:
    exp.application(task=task, app_conf=app_conf)


@e2ctask()
def finalize(exp: Experiment, app_conf: Optional[str] = None, destroy: bool = False):
    exp.finalize(app_conf=app_conf, destroy=destroy)


@e2ctask()
def destroy(exp: Experiment):
    exp.destroy()


@e2ctask()
def ssh(exp: Experiment, **kwargs):
    exp.ssh(**kwargs)


@e2ctask()
def get_output_dir(exp: Experiment):
    exp.get_output_dir()


@e2ctask(new=True)
def deploy(
    scenario_dir: Path,
    artifacts_dir: Path,
    duration: int,
    repeat: int = 0,
    app_conf_list: list[str] = [],
    is_prepare: bool = True,
    optimization_id: Optional[UUID] = None,
    destroy_on_finish: bool = False,
) -> Experiment:
    for current_repeat in range(repeat + 1):
        exp = Experiment(
            scenario_dir=scenario_dir,
            artifacts_dir=artifacts_dir,
            optimization_id=optimization_id,
            app_conf_list=app_conf_list,
            repeat=current_repeat,
        )
        exp.deploy(
            duration=duration,
            is_prepare=is_prepare,
            destroy_on_finish=destroy_on_finish,
        )
    return exp
