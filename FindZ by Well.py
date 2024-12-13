# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:11:16 2024

@author: reepd

z-locations by well

Loops through folder_path = \\prfs.hhmi.org\\genie\\GECIScreenData\\GECI_Imaging_Data\\SCaMP\\20240304_SCaMP_raw
to search all subfolders for file names that contain "_GFP-ref"
In those filenames, extract three things:
The plate name, which are the first 13 characters of the file name.
The well position, which is in each file name as the three characters prior to the string "_165dot"
The Z position, between the strings "_Z" and "_GFP-ref"

Then it plots the Z position against the well position as a swarm plot.
On a separate plot, it shows the Z position against the plate name as a swarm plot.
"""
import os
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define the folder path
folder_path = r'\\prfs.hhmi.org\\genie\\GECIScreenData\\GECI_Imaging_Data\\SCaMP\\20240304_SCaMP_raw'

# Lists to store extracted data
plate_names = []
well_positions = []
z_positions = []

# Loop through the folder and subfolders
for root, dirs, files in os.walk(folder_path):
    # Skip folders with 'doNotAnalyze' in their names
    if 'doNotAnalyze' in root:
        continue
    for file in files:
        if '_GFP-ref' in file:
            # Extract plate name, well position, and Z position using regex
            plate_name = file[:13]
            well_position_match = re.search(r'(\w{3})_165dot', file)
            z_position_match = re.search(r'_Z([\d.]+)_GFP-ref', file)
            
            if well_position_match and z_position_match:
                well_position = well_position_match.group(1)
                z_position = int(float(z_position_match.group(1)))  # Convert to float first, then to int
                
                # Append the extracted data to the lists
                plate_names.append(plate_name)
                well_positions.append(well_position)
                z_positions.append(z_position)

# Create a DataFrame from the extracted data
data = pd.DataFrame({
    'Plate Name': plate_names,
    'Well Position': well_positions,
    'Z Position': z_positions
})

# Ensure Plate Name is a string
data['Plate Name'] = data['Plate Name'].astype(str)

# Separate data into odd and even based on the third character of Plate Name
data_odd = data[data['Plate Name'].str[2].astype(int) % 2 != 0]
data_even = data[data['Plate Name'].str[2].astype(int) % 2 == 0]

# Function to create swarm plot with linear regression line and angled X axis labels
def create_swarmplot(data, x_col, y_col, title, add_hline=None):
    plt.figure(figsize=(12, 6))
    sorted_order = sorted(data[x_col].unique(), reverse=False)
    sns.swarmplot(x=x_col, y=y_col, data=data, order=sorted_order)
    sns.regplot(x=pd.Categorical(data[x_col], categories=sorted_order).codes, y=data[y_col], scatter=False)
    plt.title(title)
    plt.xticks(rotation=45, fontsize=8)
    if add_hline:
        plt.axhline(y=add_hline, color='r', linestyle='--')
    plt.show()

# Function to create swarm plot without linear regression line and angled X axis labels
def create_swarmplot_no_reg(data, x_col, y_col, title, add_hline=None):
    plt.figure(figsize=(12, 6))
    sorted_order = sorted(data[x_col].unique())
    sns.swarmplot(x=x_col, y=y_col, data=data, order=sorted_order)
    plt.title(title)
    plt.xticks(rotation=45, fontsize=8)
    if add_hline:
        plt.axhline(y=add_hline, color='r', linestyle='--')
    plt.show()

# Plot Z position against Well position as a swarm plot for odd Plate Names with horizontal line at 8267
create_swarmplot(data_odd, 'Well Position', 'Z Position', 'Z vs Well, Rig 1, 20240304', add_hline=8267)

# Plot Z position against Well position as a swarm plot for even Plate Names with horizontal line at 8578
create_swarmplot(data_even, 'Well Position', 'Z Position', 'Z vs Well, Rig 2, 20240304', add_hline=8578)

# Plot Z position against Plate name as a swarm plot for odd Plate Names with horizontal line at 8267 (no regression line)
create_swarmplot_no_reg(data_odd, 'Plate Name', 'Z Position', 'Z vs Plate, Rig 1, 20240304', add_hline=8267)

# Plot Z position against Plate name as a swarm plot for even Plate Names with horizontal line at 8578 (no regression line)
create_swarmplot_no_reg(data_even, 'Plate Name', 'Z Position', 'Z vs Plate, Rig 2, 20240304', add_hline=8578)