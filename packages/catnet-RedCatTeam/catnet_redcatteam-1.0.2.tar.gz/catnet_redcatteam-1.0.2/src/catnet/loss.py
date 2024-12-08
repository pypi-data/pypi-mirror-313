import numpy as np
from catnet import tensor as ad

class MSE:
    def __call__(self, pred, y):
        self.error = pred - y
        return np.mean(self.error ** 2)

    def backward(self):
        return 2 * (1 / self.error.shape[-1]) * self.error 

def CategoricalCrossentropy(pred, real):
    loss = -1 * ad.reduce_mean(real * ad.log(pred))

    return loss
