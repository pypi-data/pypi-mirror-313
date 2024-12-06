import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class neuron():
    def __init__(self,tau):
        self.v = -70
        self.v0 = -70
        self.tau = tau
        self.spiked = False
        self.refractory = 0
    
    def update_potential(self, dt):
        # update LIF neuron potential
        self.dv = -(self.v - self.v0) / self.tau
        self.v += self.dv * dt
        if self.refractory > 0:
            self.refractory -= 1
        else:
            self.spiked = False

    def add_noise(self, input):
        if self.spiked == False:
            self.v += input

    def set_inital_potential(self, input):
        self.v = input

    def input_spikes(self, spike):
        if self.spiked == False:
            self.v += spike*5

    def reset_potential(self):
        self.v = -110
        self.spiked = True
        self.refractory = 5

class neural_layer():
    def __init__(self, num_neurons,layer_id, weights):
        self.layer_id = layer_id
        self.neurons = [neuron(np.random.randint(1, 5)) for _ in range(num_neurons)]
        self.weights = weights

    def set_inital_potential(self, inputs):
        self.inputs = inputs
        for i in range(len(inputs)):
            self.neurons[i].set_inital_potential(inputs[i])
            
    def feed_forward(self, inputs,in_layer_id):
        self.inputs = inputs
        for i in range(len(inputs)):
            curr_spike = inputs[i]
            curr_connects = self.weights[in_layer_id][self.layer_id][i]
            for conn in curr_connects:
                self.neurons[conn].input_spikes(curr_spike)
    
    def add_noise(self,inputs):
        self.inputs = inputs
        for i in range(len(inputs)):
            self.neurons[i].add_noise(inputs[i])

    def driving_stimulus(self,drive_neurons):
        for i in drive_neurons:
            self.neurons[i].add_noise(np.random.randint(20))

    def reset_potentials(self,inputs):
        self.inputs = inputs
        for i in range(len(inputs)):
            curr_reset = inputs[i]
            if curr_reset == True:
                self.neurons[i].reset_potential()

    def voltages(self):
        return [neuron.v for neuron in self.neurons]

class neural_net():
    def __init__(self, num_layers, layer_sizes, connectivity):
        self.connectivity = connectivity   
        self.weights = []
    
        # iterare through each network layer
        for lay_a in range(num_layers):
            layer_connectivity = []
            # iterate through the connecting layers
            for lay_b in range(num_layers):
                temp_connectivity = []
                # define layer a connectivity to layer b scaled by number of neurons in layer b
                layer_ab_connectivity = int(connectivity[lay_a,lay_b]*layer_sizes[lay_b])
                for neuron_layer_a in range(layer_sizes[lay_a]):
                    # Get connectivity of this neuron to layer b neurons
                    temp_connectivity.append(np.random.randint(0, layer_sizes[lay_b], size=(1, layer_ab_connectivity))[0].tolist())
                layer_connectivity.append(temp_connectivity)
            self.weights.append(layer_connectivity)
     
        # create the layers with defined connectivity to other layers
        self.layers = [neural_layer(layer_sizes[i],i, self.weights) for i in range(num_layers)]


    def set_inital_potential(self, inputs):
        for i in range(0, len(self.layers)):
            self.layers[i].set_inital_potential(inputs[i])

    def feed_forward(self, inputs):
        for i in range(0, len(self.layers)):
            for j in range(0, len(self.layers)):
                self.layers[i].feed_forward(inputs[j],j)
    
    def add_noise(self,inputs):
        for i in range(0, len(self.layers)):
            self.layers[i].add_noise(inputs[i])
            
    def reset_potentials(self,inputs):
        for i in range(0, len(self.layers)):
            self.layers[i].reset_potentials(inputs[i])
            
    def voltages(self):
        return [layer.voltages() for layer in self.layers]
    
    def weights(self):
        return [layer.weights() for layer in self.layers]
        