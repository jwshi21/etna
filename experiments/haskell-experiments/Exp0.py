import os
import json

from benchtool.Haskell import Haskell
from benchtool.Types import ReplaceLevel, LogLevel
from Tasks import tasks
from benchtool.Experiment import Experiment

RESULTS = f'{os.getcwd()}/jwshi'

tool = Haskell(RESULTS, replace_level=ReplaceLevel.REPLACE, log_level=LogLevel.DEBUG)


class MyExperiment(Experiment):

    def skip(self, bench: str, variant: str, method: str, property: str) -> bool:
        if method == 'Size':
            return True

        if variant == 'base':
            return False

        if method != 'Correct':
            return True

        if bench in ['BST', 'RBT']:
            if property.split('_')[1] not in tasks[bench][variant]:
                return True

        return False

    def trials(self, _: str, method: str) -> int:
        return 1

    def timeout(self) -> float:
        return 5


experiment = MyExperiment(tool)
experiment.run()