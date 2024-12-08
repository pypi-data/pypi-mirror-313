from sklearn.datasets import load_digits
import numpy as np

def one_hot(n, max):
    arr = [0] * max

    arr[n] = 1

    return arr
class MNIST:
    def __init__(self,gan):
        self.act=True
        self.gan=gan
    def load(self):
        if self.act==True:
            mnist=load_digits()
            images = np.array([image.flatten() for image in mnist.images])
            targets = np.array([one_hot(n, 10) for n in mnist.target])
            if self.gan==False:
                return images, targets
            else:
                return targets, images
