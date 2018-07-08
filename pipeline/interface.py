from abc import ABC, abstractmethod
from git import Repo, GitCommandError
from subprocess import check_call
from distutils.version import StrictVersion
from configparser import ConfigParser
from io import StringIO
from functools import reduce, wraps


def stage_decorator(f):
    @wraps(f)
    def wrapped(*args, **kwds):
        print("\nStarting stage ({})".format(f.__name__))
        f(*args, **kwds)
        print("Stage ({}) complete\n".format(f.__name__))
    return wrapped


class AbstractExecutor(ABC):
    """
    Defines a single method which acts as the entrypoint to 
    any pipeline process.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def execute(self):
        pass


class AbstractSteps(ABC):
    """
    Opinionated pipeline steps.
    """

    def __init__(self, repo_path):
        super().__init__()
        self.repo = Repo(repo_path)

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def version(self):
        pass

    @abstractmethod
    def deploy(self):
        pass
