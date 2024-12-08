import catnet.loss as loss
import catnet.layers as layers
import catnet.optim as optim
import catnet.optimize as opt
import catnet.losses as losses
from catnet.layers import *
import numpy as np
from catnet.layers import *
import pickle

__version__='NeuralCAT v.1.0.3 BETA (build202)'
version='NeuralCAT v.1.0.3 BETA (build202)'
def load_model(filename):
    with open(filename, 'rb') as file:
        data=pickle.load(file)
        return data
def save_model(model,filename):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
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
    def summary(self):
        i=1
        print('-------------------------------')
        for layer in self.layers:
            print(str(i)+' - '+layer.alg())
            i=i+1
        print('-------------------------------')
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

    def train(self, x, y, acc, optim = optim.SGD(0.01), loss=losses.MSE(), epochs=10, logging=True):
        for epoch in range(1, epochs + 1):
            pred = self.__call__(x)
            l = loss(pred, y)
            optim(self, loss, logging)
            print(f"Epoch {epoch} ended .")
            print(f"Loss : {l} .")
            if acc==True:
                correct = 0
                cnt = 0
                
                for xx in x:
                    pred = np.argmax(self(np.array([xx])), axis=1)
                    real = np.argmax(y[cnt])
                    if pred[0] == real:
                        correct += 1
                    cnt += 1
                print(correct,'correct of',cnt)
                print ("Accuracy:", correct / cnt)
