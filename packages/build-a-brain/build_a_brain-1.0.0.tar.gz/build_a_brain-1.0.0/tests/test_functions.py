import os
import sys
import unittest
from unittest.mock import patch
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from build_a_brain.neural_classes import neural_net, neuron, neural_layer
from build_a_brain.neural_simulator import run_simulation,plot_raster
from build_a_brain.interface import build_network

class TestNueronGeneration(unittest.TestCase):

    def test_intital_voltage(self):
        self.assertEqual(neuron(tau=1).v, -70)
    
    def test_resting_potential(self):
        self.assertEqual(neuron(tau=1).v0, -70)

    def test_time_constant(self):
        self.assertEqual(neuron(tau=1).tau, 1)

    def test_spiked(self):
        self.assertEqual(neuron(tau=1).spiked, False)

    def test_refractory(self):
        self.assertEqual(neuron(tau=1).refractory, 0)

class TestNeuronFunctions(unittest.TestCase):

    def test_update_potential(self):
        n = neuron(tau=1)
        n.update_potential(dt=0.1)
        self.assertEqual(n.v, -70)

    def test_add_noise(self):
        n = neuron(tau=1)
        n.add_noise(input=10)
        self.assertEqual(n.v, -60)

    def test_set_inital_potential(self):
        n = neuron(tau=1)
        n.set_inital_potential(input=10)
        self.assertEqual(n.v, 10)

    def test_input_spikes(self):
        n = neuron(tau=1)
        n.input_spikes(spike=1)
        self.assertEqual(n.v, -65)

    def test_reset_potential(self):
        n = neuron(tau=1)
        n.add_noise(10)
        n.reset_potential()
        self.assertEqual(n.v, -110)
        self.assertTrue(n.spiked, True)
        self.assertEqual(n.refractory, 5)

class TestNeuralLayerGeneration(unittest.TestCase):
    
    def test_num_neurons(self):
        layer = neural_layer(100,1,[1,2,3])
        self.assertEqual(len(layer.neurons), 100)

    def test_weights(self):
        layer = neural_layer(100,1,[1,2,3])
        self.assertEqual(layer.weights, [1,2,3])
        
class TestNeuralLayerFunctions(unittest.TestCase):

    def test_voltages(self):
        layer = neural_layer(100,1,[1,2,3])
        self.assertEqual(layer.voltages(), [-70]*100)

    def test_set_inital_potentials(self):
        layer = neural_layer(100,1,[1,2,3])
        # list of 100 values of 10
        input = np.ones(100)*100
        layer.set_inital_potential(input)
        self.assertEqual(layer.voltages()[0], input[0])
    
    def test_add_layer_noise(self):
        layer = neural_layer(100,1,[1,2,3])
        input = np.random.random(100)*100
        layer.add_noise(input)
        self.assertEqual(layer.voltages(), [i-70 for i in input])

    def test_reset_potentials(self):
        layer = neural_layer(100,1,[1,2,3])
        layer.add_noise(np.ones(100)*100)
        layer.reset_potentials([True]*100)
        self.assertEqual(layer.voltages(), [-110]*100)

class TestNetworkGeneration(unittest.TestCase):

    def test_num_layers(self):
        connectivity = np.array([[0,0,0.02,0.02,0.01],
                                 [0.001,0.001,0,0.001,0.01],
                                 [0.001,0.001,0.01,0,0.001],
                                 [0.01,0.01,0.01,0,0.01],
                                 [0.001,0.001,0.01,0.001,0]])
        net = neural_net(5,[100,100,100,100,100],connectivity)
        self.assertEqual(len(net.layers), 5)

    def test_layer_sizes(self):
        connectivity = np.array([[0,0,0.02,0.02,0.01],
                                 [0.001,0.001,0,0.001,0.01],
                                 [0.001,0.001,0.01,0,0.001],
                                 [0.01,0.01,0.01,0,0.01],
                                 [0.001,0.001,0.01,0.001,0]])
        net = neural_net(5,[100,100,100,100,100],connectivity)
        self.assertEqual([len(layer.neurons) for layer in net.layers], [100]*5)

    def test_initial_potentials(self):
        connectivity = np.array([[0,0,0.02,0.02,0.01],
                                 [0.001,0.001,0,0.001,0.01],
                                 [0.001,0.001,0.01,0,0.001],
                                 [0.01,0.01,0.01,0,0.01],
                                 [0.001,0.001,0.01,0.001,0]])
        net = neural_net(5,[100,100,100,100,100],connectivity)
        net.set_inital_potential([[10]*100]*5)
        self.assertEqual(net.voltages()[0][0], 10)

    def test_feed_forward(self):
        connectivity = np.array([[100,100,100,100,100],
                                 [100,100,100,100,100],
                                 [100,100,100,100,100],
                                 [100,100,100,100,100],
                                 [100,100,100,100,100]])
        
        layer_sizes = [100,100,100,100,100]
        net = neural_net(5,layer_sizes,connectivity)
        net.feed_forward(np.ones([5,100]))
        self.assertGreater(net.voltages()[0][0], -70)

    def test_reset_potentials(self):
        connectivity = np.array([[100,100,100,100,100],
                                 [100,100,100,100,100],
                                 [100,100,100,100,100],
                                 [100,100,100,100,100],
                                 [100,100,100,100,100]])
        
        layer_sizes = [100,100,100,100,100]
        net = neural_net(5,layer_sizes,connectivity)
        net.reset_potentials([[True]*100]*5)
        self.assertEqual(net.voltages()[0][0], -110)

class TestNeuralSimulation(unittest.TestCase):

    def test_run_simulation(self):
        connectivity = np.array([[0,0,0.02,0.02,0.01],
                                 [0.001,0.001,0,0.001,0.01],
                                 [0.001,0.001,0.01,0,0.001],
                                 [0.01,0.01,0.01,0,0.01],
                                 [0.001,0.001,0.01,0.001,0]])
        time_steps = 5
        net, all_spikes, all_voltages = run_simulation(-1,-1,time_steps,100,100,100,100,100,connectivity,2,10)
        self.assertEqual(len(all_voltages), time_steps)
        self.assertEqual(len(all_spikes), time_steps)
        self.assertEqual(len(all_voltages[0]), 5)
        self.assertEqual(len(all_spikes[0]), 5)
        self.assertEqual(len(all_voltages[0][0]), 100)
        self.assertEqual(len(all_spikes[0][0]), 100)
        self.assertEqual(net.voltages(), all_voltages[-1])

if __name__ == '__main__':
    unittest.main()