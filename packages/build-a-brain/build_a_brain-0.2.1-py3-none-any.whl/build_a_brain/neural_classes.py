import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class neuron():
    """
    Class defines a single neuron in the network
    Atrribues:
        v: float, neuron potential
        v0: float, resting potential
        tau: float, time constant
        spiked: boolean, if neuron spiked at current timestep
        refractory: int, refractory period after neuron spiked
    """
    def __init__(self,tau):
        self.v = -70
        self.v0 = -70
        self.tau = tau
        self.spiked = False
        self.refractory = 0
    
    def update_potential(self, dt):
        """""
        Purpose: Update the neuron potential decay based on the LIF model
                 sets the spiked identiy to false if refactory period is over
        Inputs:
            dt: float, time step
        """""
        self.dv = -(self.v - self.v0) / self.tau
        self.v += self.dv * dt
        if self.refractory > 0:
            self.refractory -= 1
        else:
            self.spiked = False

    def add_noise(self, input):
        """
        Purpose: Add stimulus to the neuron potential
        Inputs:
            input: float, stimulus to add to neuron potential
        """
        if self.spiked == False:
            self.v += input

    def set_inital_potential(self, input):
        """
        purpose: set the initial potential of the neuron
        inputs:
            input: float, initial potential
        """
        self.v = input

    def input_spikes(self, spike):
        """
        Purpose: Add input spikes to the neuron potential from presynaptic neurons
        Inputs:
            spike: int (0 or 1), input spike from presynaptic neuron
        """
        if self.spiked == False:
            self.v += spike*5

    def reset_potential(self):
        """
        Purpose: Reset the neuron potential to resting potential
                 set spiked identity to true 
                 set refractory period to 5
        """
        self.v = -110
        self.spiked = True
        self.refractory = 5

class neural_layer():
    """
    Class defines a single layer in the network
    Attributes:
        num_neurons: int, number of neurons in the layer
        layer_id: int, layer id
        neurons: list, list of neuron objects in the layer
        weights: list, neuron numbers in other layers that the neuons are connected to
    """
    def __init__(self, num_neurons,layer_id, weights):
        self.layer_id = layer_id
        self.neurons = [neuron(np.random.randint(1, 5)) for _ in range(num_neurons)]
        self.weights = weights

    def set_inital_potential(self, inputs):
        """
        Purpose: Set the initial potential of the neurons in the layer
        Inputs:
            inputs: list, initial potentials for each neuron in the layer
        """
        self.inputs = inputs
        for i in range(len(inputs)):
            self.neurons[i].set_inital_potential(inputs[i])
            
    def feed_forward(self, inputs,in_layer_id):
        """
        Purpose: Update the neuron potentials based on input spikes from presynaptic neurons
        Inputs:
            inputs: list, input spikes from presynaptic neurons
            in_layer_id: int, layer id of the presynaptic neurons
        """
        self.inputs = inputs
        for i in range(len(inputs)):
            curr_spike = inputs[i]
            curr_connects = self.weights[in_layer_id][self.layer_id][i]
            for conn in curr_connects:
                self.neurons[conn].input_spikes(curr_spike)
    
    def add_noise(self,inputs):
        """
        Purpose: Add stimulus to the neuron potentials
        Inputs:
            inputs: list, noise to add to neuron potentials
        """
        self.inputs = inputs
        for i in range(len(inputs)):
            self.neurons[i].add_noise(inputs[i])

    def driving_stimulus(self,drive_neurons):
        """
        Purpose: Add stimulus to the neuron potentials
        Inputs:
            drive_neurons: list, neurons to add stimulus to in this layer
        """
        for i in drive_neurons:
            self.neurons[i].add_noise(np.random.randint(20))

    def reset_potentials(self,inputs):
        """
        Purpose: Reset the neuron potentials to resting potential
        Inputs:
            inputs: list, neurons that spiked on previous timeset
        """
        self.inputs = inputs
        for i in range(len(inputs)):
            curr_reset = inputs[i]
            if curr_reset == True:
                self.neurons[i].reset_potential()

    def voltages(self):
        """
        Purpose: Get the neuron potentials
        Returns:
            list, neuron potentials
        """
        return [neuron.v for neuron in self.neurons]

class neural_net():
    """
    Class defines the network of layers
    Attributes:
        connectivity: array, connectivity matrix of the network
        weights: list, neuron numbers in other layers that the neuons are connected to
        layers: list, list of neural layer objects
    """
    def __init__(self, num_layers, layer_sizes, connectivity):
        self.connectivity = connectivity   
        self.weights = []

        # Initalize the network connectivity upon creation of the network
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
        """
        Purpose: Set the initial potential of the neurons in the network
        Inputs:
            inputs: list, initial potentials for each neuron in each layer in the network
        """
        for i in range(0, len(self.layers)):
            self.layers[i].set_inital_potential(inputs[i])

    def feed_forward(self, inputs):
        """
        Purpose: Update the neuron potentials based on input spikes from presynaptic neurons
        Inputs:
            inputs: list, input spikes from presynaptic neurons
        """
        for i in range(0, len(self.layers)):
            for j in range(0, len(self.layers)):
                self.layers[i].feed_forward(inputs[j],j)
    
    def add_noise(self,inputs):
        """
        Purpose: Add stimulus to the neuron potentials
        Inputs:
            inputs: list, noise to add to neuron potentials
        """
        for i in range(0, len(self.layers)):
            self.layers[i].add_noise(inputs[i])
            
    def reset_potentials(self,inputs):
        """
        Purpose: Reset the neuron potentials to resting potential
        Inputs:
            inputs: list, neurons that spiked on previous timeset
        """
        for i in range(0, len(self.layers)):
            self.layers[i].reset_potentials(inputs[i])
            
    def voltages(self):
        """
        Purpose: Get the neuron potentials
        Returns:
            list, neuron potentials
        """
        return [layer.voltages() for layer in self.layers]
    
    def weights(self):
        """
        Purpose: Get the weights of the network
        Returns:
            list, weights of the network
        """
        return [layer.weights() for layer in self.layers]
        