# Overview: 
This package generates a simple spiking network model with a leaky integrate and fire (LIF) approach. The spiking model can be customized and outputs spiking activity over time of each neuron in the form of a raster plot. Additionally, membrane potential voltages are stored for each neuron at each step of the simulation.

# Features:
The model is customizable with the aid of a user friendly interface. The model consists of 5 layers where the user defines the following:
- number of neurons in each layer
- connectivity matrix of each layer to itself and other layers
- stimulation layer
- percent of neurons in stimulation layer reciving stimulation
- run time of stimulation in miliseconds

# Setup and installation 
Dependencies:
To use the package, first install the following pacakges and make sure you are using python version 3.11 or later:
```
pip install numpy
pip install matplotlib
pip install tk
```

Install the package:
```
pip install build_a_brain
```

# User guide:
To use the interactive interface, the function can be ran in either the command line or in a jupyter notebook:
```
build_a_brain.build_network_interface()
```
To output the network object, spikes over time, and voltages over time, it is reccomended to use a jupyter notbook. Below is an example of a neural network that can be generated.
```
net, spikes, voltages = run_simulation(-1, -1, num_steps = 100,
                    layer1_size = 1000,
                    layer2_size = 1000,
                    layer3_size = 1000,
                    layer4_size = 1000,
                    layer5_size = 1000,
                    connectivity_matrix = np.array([[0,0,0.02,0.02,0.01],
                                                    [0.001,0.001,0,0.001,0.01],
                                                    [0.001,0.001,0.01,0,0.001],
                                                    [0.01,0.01,0.01,0,0.01],
                                                    [0.001,0.001,0.01,0.001,0]]),
                    driving_layer = 3,
                    driving_neuron_nums = 20)
```
