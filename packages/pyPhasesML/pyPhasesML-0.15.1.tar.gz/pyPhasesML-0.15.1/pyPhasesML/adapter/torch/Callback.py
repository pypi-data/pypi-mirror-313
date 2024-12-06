from pyPhasesML.Model import ModelConfig


class Callback:
    def __init__(self, config: ModelConfig, priority=100) -> None:
        self.config = config
        self.priority = priority

    def getLogPath(self):
        return f"{self.config.logPath}/"

    def trigger(self, event, *args, **kwargs):
        if event == "trainingStart":
            self.onTrainingStart(*args, **kwargs)
        elif event == "trainingEnd":
            self.onTrainingEnd(*args, **kwargs)
        elif event == "validationStart":
            self.onValidationStart(*args, **kwargs)
        elif event == "validationEnd":
            self.onValidationEnd(*args, **kwargs)
        elif event == "batchEnd":  # at the end of a batch, after backpropagation and batch scheduler
            self.onBatchEnd(*args, **kwargs)
        elif event == "shutdown":  # when a shutdown request is made
            self.onShutdown(*args, **kwargs)
        elif event == "checkpoint":  # when a checkpoint is created
            self.onCheckpoint(*args, **kwargs)
        elif event == "restore":  # when a restore checkpoint was found and the training is restored
            self.onRestore(*args, **kwargs)
        elif event == "register":  # when the callback gets registered to the model
            self.onRegister(*args, **kwargs)

    def onTrainingStart(self, model, dataset):
        pass

    def onTrainingEnd(self, model):
        pass

    def onValidationStart(self, model, validationData):
        pass

    def onValidationEnd(self, model, results, scorer):
        pass

    def onBatchEnd(self, model, batchIndex):
        pass
    
    def onShutdown(self, model):
        pass
    
    def onCheckpoint(self, model):
        pass

    def onRestore(self, model):
        pass
    
    def onRegister(self, model):
        pass
