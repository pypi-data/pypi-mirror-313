
class DataPipe:
    def __init__(self, datapipe: "DataPipe") -> None:
        self.datapipe = datapipe

    def __getitem__(self, index):
        return self.datapipe[index]

    def __len__(self):
        return len(self.datapipe)
    
    def __iter__(self) -> int:
        for i in range(len(self)):
            yield self[i]

    def close(self):
        pass