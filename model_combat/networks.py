import os
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import Dense

class CriticNetwork(keras.Model):
    def __init__(self, fc1_dims=512, fc2_dims=512,
                 name='critic', chkpt_dir='tmp/ddpg'):
        super(CriticNetwork, self).__init__()
        self.fc1_dims=fc1_dims
        self.fc2_dims=fc2_dims
        self.model_name=name
        self.checkpoint_dir=chkpt_dir
        self.checkpoint_file=os.path.join(self.checkpoint_dir, self.model_name+'ddpg.h5')

        #initialize the layers
        self.fc1=Dense(self.fc1_dims, activation='relu')
        self.fc2=Dense(self.fc2_dims, activation='relu')
    
    def call_critic(self, state, action):
        action_value = self.fc1(tf.concat([state, action]), axis=1)
        action_value = self.fc2(action_value)
        q_value=self.q(action_value)
        #return critic network output
        return q_value
    
class ActorNetwork(keras.Model):
    def __init__(self, fc1_dims=512, fc2_dims=512, 
                 n_actions=14, name='actor', chkpt_dir='tmp.ddpg'):
        super(ActorNetwork, self).__init__()
        self.fc1_dims=fc1_dims
        self.fc2_dims=fc2_dims
        self.n_actions=n_actions

        self.model_name=name
        self.checkpoint_dir=chkpt_dir
        self.checkpoint_file=os.path.join(self.checkpoint_dir, self.model_name+'ddpg.h5')

        #initialize the layers
        self.fc1=Dense(self.fc1_dims, activation='relu')
        self.fc2=Dense(self.fc2_dims, activation='relu')
        self.mu=Dense(self.n_actions, activation='tanh')

    def call_actor(self, state):
        prob = self.fc1(state)
        prob = self.fc2(prob)

        mu=self.mu(prob)
        return mu