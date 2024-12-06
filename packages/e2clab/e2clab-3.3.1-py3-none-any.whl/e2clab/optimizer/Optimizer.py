import glob
import os
import shutil
import uuid
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Optional

from e2clab.constants import Command
from e2clab.errors import E2clabError
from e2clab.experiment import Experiment
from e2clab.log import get_logger
from e2clab.utils import is_valid_setup


class Optimizer:
    """E2Clab class API for optimization loops.
    Inherit from this class to define your Optimization

    :param scenario_dir: Path to your ``SCENARIO_DIR``
    :type scenario_dir: Path
    :param artifacts_dir: Path to your ``ARTIFACTS_DIR``
    :type artifacts_dir: Path
    :param duration: Duration of your 'deployment', defaults to 0
    :type duration: int, optional
    :param repeat: Number of 'deployment' repreats, defaults to 0
    :type repeat: int, optional

    :raises Exception: If supplied invalid ``e2clab`` configuration
    """

    __metaclass__ = ABCMeta

    def __init__(
        self,
        scenario_dir: Path,
        artifacts_dir: Path,
        duration: int = 0,
        repeat: int = 0,
    ):
        self.logger = get_logger(__name__, ["OPT"])

        if not is_valid_setup(
            scenario_dir=scenario_dir,
            artifacts_dir=artifacts_dir,
            command=Command.DEPLOY,
        ):
            self.logger.error("Invalid setup for Optimizer deployment")
            raise E2clabError("Invalid setup")

        self.scenario_dir = scenario_dir.resolve()
        self.artifacts_dir = artifacts_dir.resolve()

        self.duration = duration
        self.repeat = repeat
        self.optimization_dir: Optional[Path] = None
        self.result_dir = None
        self.optimization_id: Optional[str] = None
        self.logger = get_logger(__name__, ["OPT"])

    @abstractmethod
    def run(self):
        """Setup your training: Implement the logic of your optimization."""
        pass

    def prepare(self) -> Path:
        """Creates a new directory ``optimization_dir`` for optimization run.
        Copies experiment definition files (yaml files) into ``optimization_dir``.
        The optimization run will be launched from this ``optimization_dir``.

        Returns:
            optimization_dir (Path): Optimization run's SCENARIO_DIR
        """
        self.optimization_id = uuid.uuid4().hex
        self.optimization_dir = self.scenario_dir / self.optimization_id

        os.mkdir(self.optimization_dir)
        # Copy experiment defintion into the new optimization dir
        self._copy_experiment_to_opt()
        os.chdir(self.optimization_dir)

        return self.optimization_dir

    def launch(self, optimization_config: Optional[dict] = None) -> Path:
        """Deploys the configurations defined by the search algorithm.
        It runs the following E2Clab commands automatically:
        - layers_services
        - network
        - workflow (prepare, launch, finalize)
        - finalize

        Args:
            optimization_config (dict, optional): "config" dictionary, defaults to None
                Passed to your workflow in ``{{ optimization_config }}``

        Returns:
            result_dir (Path): output folder of your optimization experiment run,
        """
        for current_repeat in range(self.repeat + 1):
            self.exp = Experiment(
                scenario_dir=self.optimization_dir,
                artifacts_dir=self.artifacts_dir,
                repeat=current_repeat,
                optimization_config=optimization_config,
                optimization_id=self.optimization_id,
            )
            self.exp.deploy(duration=self.duration)
        self.result_dir = self.exp.get_exp_dir()
        return self.result_dir

    def finalize(self) -> None:
        """Destroys optimization run computing resources"""
        self.exp.destroy()

    def _copy_experiment_to_opt(self):
        """Copy the experiment definition to the new optimization dir"""
        files = glob.iglob(os.path.join(self.scenario_dir, "*.yaml"))
        for file in files:
            if os.path.isfile(file):
                shutil.copy2(file, self.optimization_dir)
