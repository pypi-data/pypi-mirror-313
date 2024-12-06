# Loading env variables before anything
from dotenv import load_dotenv

ENV_FILE = ".e2c_env"
loaded_dotenv = load_dotenv(ENV_FILE)

from e2clab.optimizer import Optimizer  # noqa: E402
from e2clab.services import Service  # noqa: E402

__all__ = ["Optimizer", "Service"]
__version__ = "3.3.1"
