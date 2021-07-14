import tensorflow as tf
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from collections import deque


class PuyoPuyoAgent():
    def __init__(self,memoryBufferSize=10000,epsilon =0):
        self.model= Sequential([Dense(32, input_dim=5,activation='relu', ),Dense(32,activation='relu', ), Dense(1 ,activation='linear',)])#input_shape=(12,6) input_shape=(24,10),Flatten(input_shape=(24,0),),
        self.model.compile(loss="mse",optimizer=Adam(lr=0.001),metrics=['accuracy'])
        self.epsilon = epsilon
        self.memory = deque(maxlen=memoryBufferSize)
        self.epsilonMin = 0
        self.epsilonDecay = 0.002


    def bestMoves(self, states):
        maxqvalue =  None
        best_moves = None
        counter=0
        if random.uniform(0,1)<self.epsilon:
            counter = random.randint(0,len(states)-1)
            return counter, list(states)[counter]
        else:
            for state in states:
                qValue= self.model.predict(np.reshape(state,[1,5]))[0]
                if not maxqvalue or qValue > maxqvalue:
                    maxqvalue = qValue
                    best_moves = counter
                    bestState = state
                counter+=1
            return best_moves, bestState


    def addToMovesMemory(self,state,bestFutureState,score, gameOver):
        self.memory.append((state,bestFutureState,score,gameOver))

    def train(self, batchSize = 32, epochs=3):
        if len(self.memory)>batchSize and len(self.memory)>= 5000:
            batchToTrainOn = random.sample(self.memory,batchSize)
            nextStates = np.array([x[1] for x in batchToTrainOn])
            nextQs = [x[0] for x in self.model.predict(nextStates)]
            x = []
            y = []

            for i,(state,futureState, score, gameOver) in enumerate(batchToTrainOn):
                if not gameOver:
                    newQ = score + 0.95 * nextQs[i]
                else:
                    newQ = score
                x.append(state)
                y.append(newQ)
            self.model.fit(np.array(x),np.array(y),batch_size=batchSize, epochs=epochs,verbose=0)

            if self.epsilon>self.epsilonMin:
                self.epsilon-=self.epsilonDecay



