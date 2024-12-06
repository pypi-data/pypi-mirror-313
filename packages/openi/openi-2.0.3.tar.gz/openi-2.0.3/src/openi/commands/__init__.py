from abc import ABC, abstractmethod
from argparse import _SubParsersAction


class BaseOpeniCLICommand(ABC):
    @staticmethod
    @abstractmethod
    def register_subcommand(parser: _SubParsersAction):
        raise NotImplementedError()

    @abstractmethod
    def run(self):
        raise NotImplementedError()
