# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:33:53 2024

@author: go29lap
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv('Z Parameter Table 8.csv')

# Quick look at the data (optional)
print(data.head())

# Plot the data (assuming 'x_column' and 'y_column' exist in your CSV)
plt.plot(data['x_column'], data['y_column'])

# Customize the plot (optional)
plt.xlabel('X Axis Label')
plt.ylabel('Y Axis Label')
plt.title('Your Plot Title')

# Show the plot
plt.show()
