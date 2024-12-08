import numpy as np
import catnet.loss as loss
import catnet.optim as optim
from numba import njit
np.random.seed(0)
@njit(cache=True)
def csigmoid(x):
    out=1 / (1 + np.exp(-x))
    out=np.round(out,2)
    return out
def sigmoid(x):
    x=np.tanh(x)
    out=1 / (1 + np.exp(-x))
    return out
@njit
def ssigmoid(x):
    out=np.maximum(0,x)
    out=np.maximum(out,0)*1.1
    return out
def sg(x):
    x=np.maximum(x,0)
    return np.dot(x,1.2)
class Activation:
    def __init__(self):
        pass

class Layer:
    def __init__(self):
        pass

class Model: 
    def __init__(self, layers):
        self.layers = layers

    def __call__(self, x):
        output = x
        for layer in self.layers:
            output = layer(output)

        return output

class Linear(Layer):
    def get(self):
        return 'linear'
    def getunits(self):
        return self.units
    def __init__(self, units):
        self.units = units
        self.initialized = False

    def __call__(self, x):
        self.input = x
        if not self.initialized:
            self.w = np.random.rand(self.input.shape[-1], self.units)
            self.b = np.random.rand(self.units)
            self.initialized = True

        return self.input @ self.w + self.b

    def backward(self, grad):
        self.w_gradient = self.input.T @ grad
        self.b_gradient = np.sum(grad, axis=0)
        return grad @ self.w.T

class Sigmoid(Activation):
    def __init__(self,count=0):
        self.c=count
    def get(self):
        return self.c
    def alg(self):
        return 'sigmoid'
    def __call__(self, x):
        self.output = 1 / (1 + np.exp(-x))

        return self.output

    def backward(self, grad):
        return grad * (self.output * (1 - self.output))

class CSIG(Activation):
    def __init__(self,count=0):
        self.c=count
    def get(self):
        return self.c
    def alg(self):
        return 'csig'
    def __call__(self, x):
        self.output = csigmoid(x)
        return self.output

    def backward(self, grad):
        return grad * (self.output * (1 - self.output))
class MRELU(Activation):
    def __init__(self,count=0):
        self.c=count
    def get(self):
        return self.c
    def __call__(self, x):
        self.output = ssigmoid(x)
        return self.output
    def alg(self):
        return 'mrelu'
    def backward(self, grad):
        return grad * np.clip(self.output, 0, 1)

class Relu(Activation):
    def __init__(self,count=0):
        self.c=count
    def get(self):
        return self.c
    def alg(self):
        return 'relu'
    def __call__(self, x):
        self.output = np.maximum(0, x)   
        return self.output

    def backward(self, grad):
        return grad * np.clip(self.output, 0, 1)

class Softmax(Activation):
    def __init__(self,count=0):
        self.c=count
    def get(self):
        return self.c
    def alg(self):
        return 'soft'
    def __call__(self, x):
        exps = np.exp(x - np.max(x))
        self.output = exps / np.sum(exps, axis=1, keepdims=True)
        return self.output

    def backward(self, grad):
        m, n = self.output.shape
        p = self.output
        tensor1 = np.einsum('ij,ik->ijk', p, p)
        tensor2 = np.einsum('ij,jk->ijk', p, np.eye(n, n))
        dSoftmax = tensor2 - tensor1
        dz = np.einsum('ijk,ik->ij', dSoftmax, grad) 
        return dz

class Tanh(Activation):
    def __init__(self,count=0):
        self.c=count
    def alg(self):
        return 'tanh'
    def get(self):
        return self.c
    def __call__(self, x):
        self.output = np.tanh(x)

        return self.output

    def backward(self, grad):
        return grad * (1 - self.output ** 2)

class Model: 
    def __init__(self, layers=[]):
        self.layers = layers
        lrs=[]
        for layer in self.layers:
            if layer.get()!='linear':
                if layer.get()>0:
                    lrs.append(Linear(layer.get()))
                if layer.alg()=='soft':
                    lrs.append(Softmax())
                elif layer.alg()=='relu':
                    lrs.append(Relu())
                elif layer.alg()=='mrelu':
                    lrs.append(MRELU())
                elif layer.alg()=='csig':
                    lrs.append(CSIG())
                elif layer.alg()=='tanh':
                    lrs.append(Tanh())
            else:
                lrs.append(Linear(layer.getunits()))
        self.layers=lrs
    def add(self,layer):
        self.layers.append(layer)
        lrs=[]
        for layer in self.layers:
            if layer.get()!='linear':
                lrs.append(Linear(layer.get()))
                if layer.alg()=='soft':
                    lrs.append(Softmax())
                elif layer.alg()=='relu':
                    lrs.append(Relu())
                elif layer.alg()=='mrelu':
                    lrs.append(MRELU())
                elif layer.alg()=='csig':
                    lrs.append(CSIG())
                elif layer.alg()=='tanh':
                    lrs.append(Tanh())
            else:
                lrs.append(Linear(layer.getunits()))
        self.layers=lrs

    def __call__(self, x):
        output = x
        for layer in self.layers:
            output = layer(output)
        return output

    def train(self, x, y, optim = optim.SGD(0.01), loss=loss.MSE(), epochs=10):
        for epoch in range(1, epochs + 1):
            pred = self.__call__(x)
            l = loss(pred, y)
            optim(self, loss)
            print (f"Epoch {epoch} ended. Loss: {l}")
