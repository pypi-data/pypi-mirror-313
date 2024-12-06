import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def build_network():
    # Create the main window
    root = tk.Tk()
    root.title("NeuroConn")  # Set the window title
    root.geometry("1000x600")  # Set the window size (width x height)

    # add figure to tkinter window
    plot_frame = ttk.Frame(root)
    plot_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Create a figure and a plot
    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    # remove axes
    # hide ax spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # remove y axis
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)

    # Embed the figure in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(relx=0.4, rely=0, anchor="nw")  # Top-right quadrant

    # Define number of timesteps in text entry box
    label = tk.Label(root, text="Run time (ms)", font=("Arial", 12))
    label.pack(pady=10)
    label.place(x=10, y=430)

    # text entry for number of timesteps
    num_steps = tk.Entry(root, width=12)
    num_steps.pack(pady=5)
    num_steps.place(x=10, y=455)

    # Dropdown for stimulation layer
    label = tk.Label(root, text="Stimulation layer", font=("Arial", 16))
    label.pack(pady=10)
    label.place(x=10, y=485)

    # Create a Tkinter variable
    tkvar1 = tk.StringVar(root)

    # Dictionary with options
    choices1 = {'Layer 1', 'Layer 2', 'Layer 3', 'Layer 4', 'Layer 5'}
    tkvar1.set('Layer 4') # set the default option

    popupMenu1 = tk.OptionMenu(root, tkvar1, *choices1)
    popupMenu1.pack(pady=10)
    popupMenu1.place(x=10, y=510)

    # Text entry box for stimulation intensity
    label = tk.Label(root, text="Stimulation intensity (0-100)", font=("Arial", 16))
    label.pack(pady=10)
    label.place(x=150, y=485)

    # text entry for stimulation intensity
    stim_intensity = tk.Entry(root, width=8)
    stim_intensity.pack(pady=5)
    stim_intensity.place(x=150, y=510)



    # Define layer sizes text box
    label = tk.Label(root, text="Define layer sizes", font=("Arial", 16))
    label.pack(pady=10)
    label.place(x=10, y=10)

    # layer 1
    layer1_label = tk.Label(root, text="Layer 1", font=("Arial", 12))
    layer1_label.pack(pady=10)
    layer1_label.place(x=10, y=40)
    # text entry for layer 1 
    layer1_size = tk.Entry(root, width=10)
    layer1_size.pack(pady=5)
    layer1_size.place(x=60, y=40)

    # layer 2
    layer2_label = tk.Label(root, text="Layer 2", font=("Arial", 12))
    layer2_label.pack(pady=10)
    layer2_label.place(x=10, y=70)
    # text entry for layer 2
    layer2_size = tk.Entry(root, width=10)
    layer2_size.pack(pady=5)
    layer2_size.place(x=60, y=70)

    # layer 3
    layer3_label = tk.Label(root, text="Layer 3", font=("Arial", 12))
    layer3_label.pack(pady=10)
    layer3_label.place(x=10, y=100)
    # text entry for layer 3
    layer3_size = tk.Entry(root, width=10)
    layer3_size.pack(pady=5)
    layer3_size.place(x=60, y=100)

    # layer 4
    layer4_label = tk.Label(root, text="Layer 4", font=("Arial", 12))
    layer4_label.pack(pady=10)
    layer4_label.place(x=10, y=130)
    # text entry for layer 4
    layer4_size = tk.Entry(root, width=10)
    layer4_size.pack(pady=5)
    layer4_size.place(x=60, y=130)

    # layer 5
    layer5_label = tk.Label(root, text="Layer 5", font=("Arial", 12))
    layer5_label.pack(pady=10)
    layer5_label.place(x=10, y=160)
    # text entry for layer 5
    layer5_size = tk.Entry(root, width=10)
    layer5_size.pack(pady=5)
    layer5_size.place(x=60, y=160)

    # Define layer connectivity text box
    label = tk.Label(root, text="Define layer connectivity (0-100)", font=("Arial", 16))
    label.pack(pady=10)
    label.place(x=10, y=190)

    # layer 1
    layer1_label = tk.Label(root, text="Layer 1", font=("Arial", 12))
    layer1_label.pack(pady=10)
    layer1_label.place(x=10, y=240)
    layer1_label = tk.Label(root, text="Layer 1", font=("Arial", 12))
    layer1_label.pack(pady=10)
    layer1_label.place(x=60, y=220)
    # text entry for layer 1
    layer11_connectivity = tk.Entry(root, width=4)
    layer11_connectivity.pack(pady=5)
    layer11_connectivity.place(x=60, y=240)

    # Layer 2
    layer2_label = tk.Label(root, text="Layer 2", font=("Arial", 12))
    layer2_label.pack(pady=10)
    layer2_label.place(x=10, y=270)
    layer2_label = tk.Label(root, text="Layer 2", font=("Arial", 12))
    layer2_label.pack(pady=10)
    layer2_label.place(x=110, y=220)
    # text entry for layer 2
    layer22_connectivity = tk.Entry(root, width=4)
    layer22_connectivity.pack(pady=5)
    layer22_connectivity.place(x=110, y=270)

    # Layer 3
    layer3_label = tk.Label(root, text="Layer 3", font=("Arial", 12))
    layer3_label.pack(pady=10)
    layer3_label.place(x=10, y=300)
    layer3_label = tk.Label(root, text="Layer 3", font=("Arial", 12))
    layer3_label.pack(pady=10)
    layer3_label.place(x=160, y=220)
    # text entry for layer 3
    layer33_connectivity = tk.Entry(root, width=4)
    layer33_connectivity.pack(pady=5)
    layer33_connectivity.place(x=160, y=300)

    # Layer 4
    layer4_label = tk.Label(root, text="Layer 4", font=("Arial", 12))
    layer4_label.pack(pady=10)
    layer4_label.place(x=10, y=330)
    layer4_label = tk.Label(root, text="Layer 4", font=("Arial", 12))
    layer4_label.pack(pady=10)
    layer4_label.place(x=210, y=220)
    # text entry for layer 4
    layer44_connectivity = tk.Entry(root, width=4)
    layer44_connectivity.pack(pady=5)
    layer44_connectivity.place(x=210, y=330)

    # Layer 5
    layer5_label = tk.Label(root, text="Layer 5", font=("Arial", 12))
    layer5_label.pack(pady=10)
    layer5_label.place(x=10, y=360)
    layer5_label = tk.Label(root, text="Layer 5", font=("Arial", 12))
    layer5_label.pack(pady=5)
    layer5_label.place(x=260, y=220)
    # text entry for layer 5
    layer55_connectivity = tk.Entry(root, width=4)
    layer55_connectivity.pack(pady=5)
    layer55_connectivity.place(x=260, y=360)

    # Layer 1 - 2 box
    layer12_connectivity = tk.Entry(root, width=4)
    layer12_connectivity.pack(pady=5)
    layer12_connectivity.place(x=60, y=270)

    # Layer 1 - 3 box
    layer13_connectivity = tk.Entry(root, width=4)
    layer13_connectivity.pack(pady=5)
    layer13_connectivity.place(x=60, y=300)

    # Layer 1 - 4 box
    layer14_connectivity = tk.Entry(root, width=4)
    layer14_connectivity.pack(pady=5)
    layer14_connectivity.place(x=60, y=330)

    # Layer 1 - 5 box
    layer15_connectivity = tk.Entry(root, width=4)
    layer15_connectivity.pack(pady=5)
    layer15_connectivity.place(x=60, y=360)

    # Layer 2 - 1 box
    layer21_connectivity = tk.Entry(root, width=4)
    layer21_connectivity.pack(pady=5)
    layer21_connectivity.place(x=110, y=240)

    # Layer 2 - 3 box
    layer23_connectivity = tk.Entry(root, width=4)
    layer23_connectivity.pack(pady=5)
    layer23_connectivity.place(x=110, y=300)

    # Layer 2 - 4 box
    layer24_connectivity = tk.Entry(root, width=4)
    layer24_connectivity.pack(pady=5)
    layer24_connectivity.place(x=110, y=330)

    # Layer 2 - 5 box
    layer25_connectivity = tk.Entry(root, width=4)
    layer25_connectivity.pack(pady=5)
    layer25_connectivity.place(x=110, y=360)

    # Layer 3 - 1 box
    layer31_connectivity = tk.Entry(root, width=4)
    layer31_connectivity.pack(pady=5)
    layer31_connectivity.place(x=160, y=240)

    # Layer 3 - 2 box
    layer32_connectivity = tk.Entry(root, width=4)
    layer32_connectivity.pack(pady=5)
    layer32_connectivity.place(x=160, y=270)

    # Layer 3 - 4 box
    layer34_connectivity = tk.Entry(root, width=4)
    layer34_connectivity.pack(pady=5)
    layer34_connectivity.place(x=160, y=330)

    # Layer 3 - 5 box
    layer35_connectivity = tk.Entry(root, width=4)
    layer35_connectivity.pack(pady=5)
    layer35_connectivity.place(x=160, y=360)

    # Layer 4 - 1 box
    layer41_connectivity = tk.Entry(root, width=4)
    layer41_connectivity.pack(pady=5)
    layer41_connectivity.place(x=210, y=240)

    # Layer 4 - 2 box
    layer42_connectivity = tk.Entry(root, width=4)
    layer42_connectivity.pack(pady=5)
    layer42_connectivity.place(x=210, y=270)

    # Layer 4 - 3 box
    layer43_connectivity = tk.Entry(root, width=4)
    layer43_connectivity.pack(pady=5)
    layer43_connectivity.place(x=210, y=300)

    # Layer 4 - 5 box
    layer45_connectivity = tk.Entry(root, width=4)
    layer45_connectivity.pack(pady=5)
    layer45_connectivity.place(x=210, y=360)

    # Layer 5 - 1 box
    layer51_connectivity = tk.Entry(root, width=4)
    layer51_connectivity.pack(pady=5)
    layer51_connectivity.place(x=260, y=240)

    # Layer 5 - 2 box
    layer52_connectivity = tk.Entry(root, width=4)
    layer52_connectivity.pack(pady=5)
    layer52_connectivity.place(x=260, y=270)

    # Layer 5 - 3 box
    layer53_connectivity = tk.Entry(root, width=4)
    layer53_connectivity.pack(pady=5)
    layer53_connectivity.place(x=260, y=300)

    # Layer 5 - 4 box
    layer54_connectivity = tk.Entry(root, width=4)
    layer54_connectivity.pack(pady=5)
    layer54_connectivity.place(x=260, y=330)

    # Add description of layer size
    label = tk.Label(root, text="Parameters", font=("Arial", 20))
    label.pack(pady=10)
    label.place(x=450, y=375)

    # Add description of layer size
    label = tk.Label(root, text="Layer sizes", font=("Arial bold", 12))
    label.pack(pady=10)
    label.place(x=450, y=410)

    label = tk.Label(root, text="number of neurons in each layer", font=("Arial", 12))
    label.pack(pady=10)
    label.place(x=580, y=410)

    # Add description of layer connectivity
    label = tk.Label(root, text="Layer connectivity ", font=("Arial bold", 12))
    label.pack(pady=10)
    label.place(x=450, y=425)

    label = tk.Label(root, text="Percentage of neurons in layer X connected to neurons in Layer Y", font=("Arial", 12))
    label.pack(pady=10)
    label.place(x=580, y=425)

    # Add descripton of run time
    label = tk.Label(root, text="Run time", font=("Arial bold", 12))
    label.pack(pady=10)
    label.place(x=450, y=440)

    label = tk.Label(root, text="Number of time steps to run the simulation", font=("Arial", 12))
    label.pack(pady=10)
    label.place(x=580, y=440)

    # Add description of stimulation layer
    label = tk.Label(root, text="Stimulation layer", font=("Arial bold", 12))
    label.pack(pady=10)
    label.place(x=450, y=455)

    label = tk.Label(root, text="Layer that recieves persitant stimulation", font=("Arial", 12))
    label.pack(pady=10)
    label.place(x=580, y=455)

    # Add description of stimulation intensity
    label = tk.Label(root, text="Stimulation intensity", font=("Arial bold", 12))
    label.pack(pady=10)
    label.place(x=450, y=470)

    label = tk.Label(root, text="Percentage of neurons in the stimulation layer that recieve a stimulus", font=("Arial", 12))
    label.pack(pady=10)
    label.place(x=580, y=470)

    # Add a progress bar
    progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=370, mode='determinate')
    progress.place(relx=0.535, rely=0.55, anchor="nw")

    def on_button_click():
        global error_label
        global error_label1
        global error_label2
        # check if any of the inputs are empty
        if (layer1_size.get() == "" or layer2_size.get() == "" or layer3_size.get() == "" or layer4_size.get() == "" or layer5_size.get() == "" or
            layer11_connectivity.get() == "" or layer12_connectivity.get() == "" or layer13_connectivity.get() == "" or layer14_connectivity.get() == "" or layer15_connectivity.get() == "" or
            layer21_connectivity.get() == "" or layer22_connectivity.get() == "" or layer23_connectivity.get() == "" or layer24_connectivity.get() == "" or layer25_connectivity.get() == "" or
            layer31_connectivity.get() == "" or layer32_connectivity.get() == "" or layer33_connectivity.get() == "" or layer34_connectivity.get() == "" or layer35_connectivity.get() == "" or
            layer41_connectivity.get() == "" or layer42_connectivity.get() == "" or layer43_connectivity.get() == "" or layer44_connectivity.get() == "" or layer45_connectivity.get() == "" or
            layer51_connectivity.get() == "" or layer52_connectivity.get() == "" or layer53_connectivity.get() == "" or layer54_connectivity.get() == "" or layer55_connectivity.get() == "" or 
            num_steps.get() == "" or stim_intensity.get() == ""):
            
            # create error label
            try:
                error_label.destroy()
            except:
                pass
            error_label = tk.Label(root, text="ERROR: please fill all text boxes", font=("Arial", 12))
            error_label.pack(pady=10)
            error_label.place(x=400, y=350)    
            return  
        else:  
            # check if error label exists and destroy it
            try:
                error_label.destroy()
            except:
                pass
        
        # check if all inputs can be converted to their respective types
        try:
            int(layer1_size.get())
            int(layer2_size.get())
            int(layer3_size.get())
            int(layer4_size.get())
            int(layer5_size.get())
            float(layer11_connectivity.get())
            float(layer12_connectivity.get())
            float(layer13_connectivity.get())
            float(layer14_connectivity.get())
            float(layer15_connectivity.get())
            float(layer21_connectivity.get())
            float(layer22_connectivity.get())
            float(layer23_connectivity.get())
            float(layer24_connectivity.get())
            float(layer25_connectivity.get())
            float(layer31_connectivity.get())
            float(layer32_connectivity.get())
            float(layer33_connectivity.get())
            float(layer34_connectivity.get())
            float(layer35_connectivity.get())
            float(layer41_connectivity.get())
            float(layer42_connectivity.get())
            float(layer43_connectivity.get())
            float(layer44_connectivity.get())
            float(layer45_connectivity.get())
            float(layer51_connectivity.get())
            float(layer52_connectivity.get())
            float(layer53_connectivity.get())
            float(layer54_connectivity.get())
            float(layer55_connectivity.get())
            int(num_steps.get())
            int(stim_intensity.get())
            # remove error label if previously created
            try:
                error_label3.destroy()
            except:
                pass
        except:
            # create error label
            try:
                error_label3.destroy()
            except:
                pass
            error_label3 = tk.Label(root, text="ERROR: please enter valid numbers", font=("Arial", 12))
            error_label3.pack(pady=10)
            error_label3.place(x=400, y=350)    
            return
        
        # build connectivity matrix 
        connectivity_matrix = np.array([[float(layer11_connectivity.get())/100,float(layer21_connectivity.get())/100,float(layer31_connectivity.get())/100,float(layer41_connectivity.get())/100,float(layer51_connectivity.get())/100],
                                                    [float(layer12_connectivity.get())/100,float(layer22_connectivity.get())/100,float(layer32_connectivity.get())/100,float(layer42_connectivity.get())/100,float(layer52_connectivity.get())/100],
                                                    [float(layer13_connectivity.get())/100,float(layer23_connectivity.get())/100,float(layer33_connectivity.get())/100,float(layer43_connectivity.get())/100,float(layer53_connectivity.get())/100],
                                                    [float(layer14_connectivity.get())/100,float(layer24_connectivity.get())/100,float(layer34_connectivity.get())/100,float(layer44_connectivity.get())/100,float(layer54_connectivity.get())/100],
                                                    [float(layer15_connectivity.get())/100,float(layer25_connectivity.get())/100,float(layer35_connectivity.get())/100,float(layer45_connectivity.get())/100,float(layer55_connectivity.get())/100]])
        # check if connectivity values are between 0 and 100
        if (np.any(connectivity_matrix < 0) or np.any(connectivity_matrix > 1)):
            try:
                error_label1.destroy()
            except:
                pass
            # create error label
            error_label1 = tk.Label(root, text="ERROR: connectivity values must be between 0 and 100", font=("Arial", 12))
            error_label1.pack(pady=10)
            error_label1.place(x=400, y=350)          
            return
        else:
            # check if error label exists and destroy it
            try:
                error_label1.destory()
            except:
                pass
        
        # Check if stimulation intesnity is between 0 and 100
        if (int(stim_intensity.get()) < 0 or int(stim_intensity.get()) > 100):
            # create error label
            try:
                error_label2.destroy()
            except:
                pass
            error_label2 = tk.Label(root, text="ERROR: stimulation intensity must be between 0 and 100", font=("Arial", 12))
            error_label2.pack(pady=10)
            error_label2.place(x=400, y=350)          
            return
        else:
            # check if error label exists and destroy it
            try:
                error_label2.pack_forget()
            except:
                pass

        # run simulation
        # reset progress bar
        progress['value'] = 0
        # reset plot
        ax.clear()
        ax.xaxis.set_visible(False)
        ax.spines['bottom'].set_visible(False)

        canvas.draw()
        net, all_spikes, all_voltages = run_simulation(root, progress, int(num_steps.get()),
                    int(layer1_size.get()),
                    int(layer2_size.get()),
                    int(layer3_size.get()),
                    int(layer4_size.get()),
                    int(layer5_size.get()),
                    connectivity_matrix,
                    driving_layer = int(tkvar1.get()[-1]) - 1,
                    driving_neuron_nums = int(stim_intensity.get()))
        plot_raster(ax,root, progress,net,all_spikes,int(num_steps.get()))
        canvas.draw()
        

    def clear_connectivity():
        # Clear any existing content of all text boxes
        layer1_size.delete(0, tk.END)
        layer2_size.delete(0, tk.END)
        layer3_size.delete(0, tk.END)
        layer4_size.delete(0, tk.END)
        layer5_size.delete(0, tk.END)
        layer11_connectivity.delete(0, tk.END)
        layer12_connectivity.delete(0, tk.END)
        layer13_connectivity.delete(0, tk.END)
        layer14_connectivity.delete(0, tk.END)
        layer15_connectivity.delete(0, tk.END)
        layer21_connectivity.delete(0, tk.END)
        layer22_connectivity.delete(0, tk.END)
        layer23_connectivity.delete(0, tk.END)
        layer24_connectivity.delete(0, tk.END)
        layer25_connectivity.delete(0, tk.END)
        layer31_connectivity.delete(0, tk.END)
        layer32_connectivity.delete(0, tk.END)
        layer33_connectivity.delete(0, tk.END)
        layer34_connectivity.delete(0, tk.END)
        layer35_connectivity.delete(0, tk.END)
        layer41_connectivity.delete(0, tk.END)
        layer42_connectivity.delete(0, tk.END)
        layer43_connectivity.delete(0, tk.END)
        layer44_connectivity.delete(0, tk.END)
        layer45_connectivity.delete(0, tk.END)
        layer51_connectivity.delete(0, tk.END)
        layer52_connectivity.delete(0, tk.END)
        layer53_connectivity.delete(0, tk.END)
        layer54_connectivity.delete(0, tk.END)
        layer55_connectivity.delete(0, tk.END)

    #Add a button to fill the text box
    def default_connectivity_1():
        # clear connectivity 
        clear_connectivity()
        # Insert predefined text
        layer1_size.insert(0, 1000)
        layer2_size.insert(0, 1000)
        layer3_size.insert(0, 1000)
        layer4_size.insert(0, 1000)
        layer5_size.insert(0, 1000)
        layer11_connectivity.insert(0, 0) 
        layer22_connectivity.insert(0, 0.1)
        layer33_connectivity.insert(0, 1)
        layer44_connectivity.insert(0, 0)
        layer55_connectivity.insert(0, 0)
        layer12_connectivity.insert(0, 0.1)
        layer13_connectivity.insert(0, 0.1)
        layer14_connectivity.insert(0, 1)
        layer15_connectivity.insert(0, 0.1)
        layer21_connectivity.insert(0, 2)
        layer23_connectivity.insert(0, 0.1)
        layer24_connectivity.insert(0, 1)
        layer25_connectivity.insert(0, 0.1)
        layer31_connectivity.insert(0, 2)
        layer32_connectivity.insert(0, 0)
        layer34_connectivity.insert(0, 1)
        layer35_connectivity.insert(0, 1)
        layer41_connectivity.insert(0, 2)
        layer42_connectivity.insert(0, 0.1)
        layer43_connectivity.insert(0, 0)
        layer45_connectivity.insert(0, 0.1)
        layer51_connectivity.insert(0, 1)
        layer52_connectivity.insert(0, 1)
        layer53_connectivity.insert(0, 0.1)
        layer54_connectivity.insert(0, 1)
        
    # Add default button
    fill_button = tk.Button(root, text="Default Connectivity", command=default_connectivity_1)
    fill_button.pack(pady=10)
    fill_button.place(x=10, y=390)

    # Add clear connectivity button
    clear_button = tk.Button(root, text="Clear Connectivity", command=clear_connectivity)
    clear_button.pack(pady=10)
    clear_button.place(x=170, y=390)

    # Add a button to run simulation
    button = tk.Button(root, text="Run Stimulation", command=on_button_click)
    button.pack(pady=20)
    button.place(x=400, y=320)

    # Run the Tkinter event loop
    root.mainloop()

    return