import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .neural_classes import neuron, neural_layer, neural_net
from .neural_simulator import run_simulation
from .interface import build_network