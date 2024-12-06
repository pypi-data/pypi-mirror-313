import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from neural_classes import neural_net

def run_simulation(root, progress, num_steps,
                    layer_1_size,
                    layer_2_size,
                    layer_3_size,
                    layer_4_size,
                    layer_5_size,
                    connectivity_matrix = np.array([[0,0,0.02,0.02,0.01],
                                                    [0.001,0.001,0,0.001,0.01],
                                                    [0.001,0.001,0.01,0,0.001],
                                                    [0.01,0.01,0.01,0,0.01],
                                                    [0.001,0.001,0.01,0.001,0]]),
                                                    driving_layer = 3,
                                                    driving_neuron_nums = 50):
    """
    Purpose: Build the neural network then the simulation of the network over time
             with a given stimulus
    Inputs:
        root: tkinter root object
        progress: tkinter progress bar object
        num_steps: int, number of time steps to run the simulation
        layer_sizes: int, number of neurons in layer
        connectivity_matrix: 2D array of floats, matrix of connection strengths between layers
        driving_layer: int, layer number to add stimulus to
        driving_neuron_nums: int, percentage of neurons to add stimulus to
    Returns:
        net: neural_net object
        all_spikes: time x layer x neuron matrix, spikes of each neuron in the network
        all_voltages: time x layer x neuron matrix, voltages of each neuron in the network
    """
    # set up network parameters 
    num_layers = 5
    dt = 0.001

    # Set progress bar to 0
    progress['value'] = 0  # Increment progress bar

    # Create network
    net = neural_net(num_layers, [layer_1_size,
                                layer_2_size,
                                layer_3_size,
                                layer_4_size,
                                layer_5_size],
                                connectivity_matrix)

    # save voltages over time
    all_voltages = []
    all_spikes = []

    # Define random neruons in stimulus layer to recieve the driving stimulus
    driving_neurons = np.random.randint(0,len(net.layers[driving_layer].neurons),int(np.round(len(net.layers[driving_layer].neurons)*driving_neuron_nums/100)))
    
    # run network over time
    for i in range(num_steps):
        # update progress bar
        progress['value'] = 50 * i / num_steps

        # Refresh the GUI
        root.update_idletasks()  
        
        #Check which neurons in the network spiked at previous time step
        spiked = []
        for layer_num in range(num_layers):
            spiked.append([x > -30 for x in net.layers[layer_num].voltages()])

        # reset voltages to resting potential for neurons that spiked
        net.reset_potentials(spiked)

        # Update neuron potentials based on input spikes of presynaptic connections
        net.feed_forward([[int(value) for value in test_i] for test_i in spiked])

        # add a stimulus to driving layer
        net.layers[driving_layer].driving_stimulus(driving_neurons)
        
        # Iterate neurons timestep for LIF model
        for layer_num in range(num_layers):
            for neuron_num in range(len(net.layers[layer_num].neurons)):
                net.layers[layer_num].neurons[neuron_num].update_potential(dt)
        
        # save voltages
        all_voltages.append(net.voltages())
        all_spikes.append([[int(value) for value in test_i] for test_i in spiked])

    return net, all_spikes, all_voltages

def plot_raster(ax, root, progress, net,all_spikes,t):
    """
    Purpose: Plot the raster plot of the network over time
    Inputs:
        ax: matplotlib axis object
        root: tkinter root object
        progress: tkinter progress bar object
        net: neural_net object
        all_spikes: matrix time x layer x neuron matrix, spikes of each neuron in the network
        t: int, time to run the simulation
    """

    # count total neurons in network
    total_neurons = sum([len(net.layers[i].neurons) for i in range(len(net.layers))])
    
    # itialize counter for progress bar
    counter = 0

    # iterate over layers
    for l in range(len(net.layers)):
        # iterate over neurons
        color_i = l/len(net.layers)
        for n in range(len(net.layers[l].neurons)):
            progress['value'] = 50 + 50 * (counter) / total_neurons # update progress bar
            root.update_idletasks()  # Refresh the GUI
            curr_spikes = [all_spikes[i][l][n] for i in range(len(all_spikes))] # get spikes for current neuron in current layer over time
            ax.scatter(np.linspace(0,t,t), [i+counter for i in np.ones(t)], s = curr_spikes,color = [0,color_i,color_i])
            counter += 1

    # add verticle bars to represent layers
    ax.plot([0,0],[0+10,len(net.layers[0].neurons)-10],color = 'black')
    ax.plot([0,0], [len(net.layers[0].neurons)+10,len(net.layers[0].neurons)+len(net.layers[1].neurons)-10],color = 'black')
    ax.plot([0,0], [len(net.layers[0].neurons)+len(net.layers[1].neurons)+10,len(net.layers[0].neurons)+len(net.layers[1].neurons)+len(net.layers[2].neurons)-10],color = 'black')
    ax.plot([0,0], [len(net.layers[0].neurons)+len(net.layers[1].neurons)+len(net.layers[2].neurons)+10,len(net.layers[0].neurons)+len(net.layers[1].neurons)+len(net.layers[2].neurons)+len(net.layers[3].neurons)-10],color = 'black')
    ax.plot([0,0], [len(net.layers[0].neurons)+len(net.layers[1].neurons)+len(net.layers[2].neurons)+len(net.layers[3].neurons)+10,len(net.layers[0].neurons)+len(net.layers[1].neurons)+len(net.layers[2].neurons)+len(net.layers[3].neurons)+len(net.layers[4].neurons)-10],color = 'black')
    
    # add text next to bars to distiniush layers
    ax.text(-8, len(net.layers[0].neurons)/2, 'Layer 1', ha='right', va='center',fontsize = 8)
    ax.text(-8, len(net.layers[0].neurons)+len(net.layers[1].neurons)/2, 'Layer 2', ha='right', va='center',fontsize = 8)
    ax.text(-8, len(net.layers[0].neurons)+len(net.layers[1].neurons)+len(net.layers[2].neurons)/2, 'Layer 3', ha='right', va='center',fontsize = 8)
    ax.text(-8, len(net.layers[0].neurons)+len(net.layers[1].neurons)+len(net.layers[2].neurons)+len(net.layers[3].neurons)/2, 'Layer 4', ha='right', va='center', fontsize = 8)
    ax.text(-8, len(net.layers[0].neurons)+len(net.layers[1].neurons)+len(net.layers[2].neurons)+len(net.layers[3].neurons)+len(net.layers[4].neurons)/2, 'Layer 5', ha='right', va='center', fontsize = 8)

    # formatting
    ax.spines['bottom'].set_visible(True)
    ax.xaxis.set_visible(True)
    ax.set_xlabel('Time (ms)')
    ax.xaxis.set_label_coords(1, 0)
    
    # set x axis labels
    ax.set_xticks(np.arange(0,t,t/5))
    ax.set_xticklabels(np.round(np.arange(0,t,t/5)))
    