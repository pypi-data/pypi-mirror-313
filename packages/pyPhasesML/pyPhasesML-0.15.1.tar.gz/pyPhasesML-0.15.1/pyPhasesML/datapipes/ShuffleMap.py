import random
from pyPhasesML.datapipes.DataPipe import DataPipe


class ShuffleMap(DataPipe):
    def __init__(self, datapipe, seed=None) -> None:
        super().__init__(datapipe)
        if seed is not None:
            random.seed(seed)
        self.indices = list(range(len(datapipe)))
        random.shuffle(self.indices)

    def __getitem__(self, index):
        original_index = self.indices[index]
        return self.datapipe[original_index]

