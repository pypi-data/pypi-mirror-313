# TODO: create optimizer base class

class Optimizer:
    def __init__(self, **kwargs):
        self.optimizer = None
        self.optimizer_kwargs = kwargs

    def optimize(self, **kwargs):
        raise NotImplementedError

    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    def set_optimizer_kwargs(self, **kwargs):
        self.optimizer_kwargs = kwargs

    def get_optimizer(self):
        return self.optimizer

    def get_optimizer_kwargs(self):
        return self.optimizer_kwargs

    def get_optimizer_params(self):
        return self.optimizer.get_params()

    def set_optimizer_params(self, **kwargs):
        self.optimizer.set_params(**kwargs)