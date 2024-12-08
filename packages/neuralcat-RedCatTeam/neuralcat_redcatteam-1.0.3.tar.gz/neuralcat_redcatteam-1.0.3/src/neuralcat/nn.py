from catnet import tensor as ad
import numpy as np
from catnet import loss
from catnet import optim
import catnet.layers as layers
from tqdm import tqdm
import rich
import pickle
import math
import os
from numba import prange,njit
#tqdm is a progress bar, so we can see how far into the epoch we are
def load_model(filename):
    with open(filename, 'rb') as file:
        data=pickle.load(file)
        return data
class SGD:
    def __init__(self, lr):
        self.lr = lr

    def delta(self, param):
        return param.gradient * self.lr

    def __call__(self, model, loss):
        loss.get_gradients()

        for layer in model.layers:
            if isinstance(layer, Layer):
                layer.update(self)
np.random.seed(345)   
class Layer:
    def __init__(self):
        pass

class Linear(Layer):
    def __init__(self, units):
        self.units = units
        self.w = None
        self.b = None

    def __call__(self, x):
        if self.w is None:
            self.w = ad.Tensor(np.random.uniform(size=(x.shape[-1], self.units), low=-1/np.sqrt(x.shape[-1]), high=1/np.sqrt(x.shape[-1])))
            self.b = ad.Tensor(np.zeros((1, self.units)))

        return x @ self.w + self.b
    def update(self, optim):
        self.w.value -= optim.delta(self.w)
        self.b.value -= optim.delta(self.b)

        self.w.grads = []
        self.w.dependencies = []
        self.b.grads = []
        self.b.dependencies = []

class Sigmoid:
    def __call__(self, x):
        return 1 / (1 + np.e ** (-1 * x))
def rem(x):
    e_x = np.e ** (x - np.max(x.value))
    s_x = (e_x) / ad.reduce_sum(e_x, axis=1, keepdims=True)
    return s_x
def ra(x):
    return 1 / (1 + np.e ** (-1 * x))
def remaxfunc(x):
    out=1 / (1 + np.e ** (-1 * x)) / 2 * 2.5
    out=out*math.pi/2*math.pi/1.1*(math.pi/1.1) / 1.1 * 1.2 / 1.11112
    return out*math.pi/(math.pi/1.1)/math.pi*3.2/1.1*3.2
class ReMax:
    def __call__(self, x):
        return remaxfunc(x)

class Softmax:
    def __call__(self, x):
        e_x = np.e ** (x - np.max(x.value))
        s_x = (e_x) / ad.reduce_sum(e_x, axis=1, keepdims=True)
        return s_x
class DTanh:
    def __call__(self, x):
        output=(2 / (1 + np.e ** (-2 * x))) - 1
        return output*1.2

class Tanh:
    def __call__(self, x):
        return (2 / (1 + np.e ** (-2 * x))) - 1
def save_model(model,filename):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
class Model:
    def __init__(self, layers=[]):
        self.layers = layers
    def add(self,layer):
        self.layers.append(layer)
    def __call__(self, x):
        try:
            output = x
            
            for layer in self.layers:
                output = layer(output)
            
            return output
        except:
            rich.print('[red](CatNET build201) - [ERROR] Model trained on invalid train data![/red]')
            return 0

    def train(self, x, y, epochs=10, loss_fn = loss.MSE, optimizer=SGD(lr=0.1), batch_size=32, log=True):
        for epoch in range(epochs):
            _loss = 0
            _accu = 0
            print (f"EPOCH: ", epoch + 1)
            try:
                if log==True:
                    ob=tqdm(range(0, len(x), batch_size))
                else:
                    ob=range(0, len(x), batch_size)
                for batch in ob:
                    output = self(x[batch:batch+batch_size])
                    l = loss_fn(output, y[batch:batch+batch_size])
                    optimizer(self, l)
                    _loss += l
                print("LOSS: ", _loss.value)
            except:
                rich.print('[red](CatNET build201) - [ERROR] Invalid train data![/red]')
    def train_with_accuracy(self, x, y, epochs=10, loss_fn = loss.MSE, optimizer=SGD(lr=0.1), batch_size=32, log=True):
        for epoch in range(epochs):
            _loss = 0
            _accu = 0
            print (f"EPOCH: ", epoch + 1)
            if log==True:
                ob=tqdm(range(0, len(x), batch_size))
            else:
                ob=range(0, len(x), batch_size)
            for batch in ob:
                output = self(x[batch:batch+batch_size])
                try:
                    l = loss_fn(output, y[batch:batch+batch_size])
                    optimizer(self, l)
                    _loss += l
                except:
                    rich.print('[red](CatNET build201) - [ERROR] Invalid train data![/red]')
            cnt=0
            correct=0
            for i in prange(len(x)):
                num=x[i]
                pred=np.argmax(self(np.array([num])).value, axis=1)
                real=np.argmax(y[i])
                if pred[0] == real:
                    correct += 1
                    cnt += 1
            if cnt==0:
                cnt=1
            print("ACCURACY: ",correct/cnt)
            print("LOSS: ", _loss.value)
class RNN(Layer):
    def __init__(self, units, hidden_dim, return_sequences=False):
        self.units = units
        self.hidden_dim = hidden_dim
        self.return_sequences = return_sequences
        self.U = None
        self.W = None
        self.V = None

    def one_forward(self, x):
        x = np.expand_dims(x, axis=1)
        state = np.zeros((x.shape[-1], self.hidden_dim))
        y = []

        for time_step in x:
            mul_u = self.U(time_step[0])
            mul_w = self.W(state)
            state = Tanh()(mul_u + mul_w)

            if self.return_sequences:
                y.append(self.V(state))

        if not self.return_sequences:
            state.value = state.value.squeeze()
            return state

        return y

    def __call__(self, x):
        if self.U is None:
            self.U = Linear(self.hidden_dim)
            self.W = Linear(self.hidden_dim)
            self.V = Linear(self.units)

        if not self.return_sequences:
            states = []
            for seq in x:
                state = self.one_forward(seq)
                states.append(state)

            s = ad.stack(states)
            return s

        sequences = []
        for seq in x:
            out_seq = self.one_forward(seq)
            sequences.append(out_seq)

        return sequences

    def update(self, optim):
        self.U.update(optim) 
        self.W.update(optim)

        if self.return_sequences:
            self.V.update(optim)
