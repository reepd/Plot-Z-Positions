# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:23:45 2024

@author: reepd

code to find heights of images

Import necessary modules: os for directory operations and re for regular expressions.
Define a function extract_numbers_from_filenames that takes the folder path as an argument.
Compile a regular expression pattern to match the numbers between "_Z" and "_ref_GFP.tif".
Iterate through the files in the specified folder and search for matches using the pattern.
Extract the numbers and convert them to integers.
Sort the numbers in descending order and return the list.

"""

import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def extract_numbers_and_subfolders_from_filenames(folder_path):
    numbers = []
    subfolders = []
    filenames = []
    pattern = re.compile(r'_Z(\d+\.\d+)_GFP-ref\.tif') #unique to SCaMP file name

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            match = pattern.search(filename)
            if match:
                number = float(match.group(1))
                subfolder = os.path.relpath(root, folder_path).split(os.sep)[0].split('_')[0]
                numbers.append((number, subfolder))
                filenames.append(filename)
                
    return numbers, filenames

def create_swarm_and_box_plot(numbers_and_subfolders, filenames):
    df = pd.DataFrame(numbers_and_subfolders, columns=['Number', 'Subfolder'])
    
    # Assign colors based on the subfolder groups
    unique_subfolders = df['Subfolder'].unique()
    base_colors = ['k'] + ['g' if i % 2 == 0 else 'b' for i in range(1, len(unique_subfolders))]
    color_map = {subfolder: base_colors[i] for i, subfolder in enumerate(unique_subfolders)}
    
    plt.figure(figsize=(12, 6))
    
    # Create swarm plot with open circles and 50% transparency
    #sns.stripplot(x='Subfolder', y='Number', data=df, palette=color_map, size=5, jitter=True, marker='o', alpha=0.5, s=5)
    
    # Overlay box and whisker plot without the maximum and minimum range bars
    sns.boxplot(x='Subfolder', y='Number', data=df, palette=color_map, showcaps=True, boxprops={'facecolor':'None'}, showfliers=False, whiskerprops={'visible': False})
    
    # Customize markers based on filename content
    for i in range(len(filenames)):
        if '-A' in filenames[i] or '-B' in filenames[i]:
            lighter_color = 'lightgreen' if color_map[df['Subfolder'][i]] == 'g' else 'lightblue'
            plt.scatter(df['Subfolder'][i], df['Number'][i], marker='o', color=lighter_color, alpha=0.5, s=5)
        elif '-G' in filenames[i] or '-H' in filenames[i]:
            darker_color = 'darkgreen' if color_map[df['Subfolder'][i]] == 'g' else 'darkblue'
            plt.scatter(df['Subfolder'][i], df['Number'][i], marker='o', color=darker_color, alpha=0.5, s=5)
        else:
            darker_color = 'green' if color_map[df['Subfolder'][i]] == 'g' else 'blue'
            plt.scatter(df['Subfolder'][i], df['Number'][i], marker='o', color=darker_color, alpha=0.5, s=5)
    
    plt.title('Z distances for 2024-03-04 Imaging Week')
    plt.xlabel('Plate', fontsize=10)
    plt.ylabel('Z Values (μm)')
    plt.xticks(rotation=45, ha='right', fontsize=8)
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='k', markersize=5, label='doNotAnalyze'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen', markersize=5, label='A or B (rig2)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=5, label='A or B (rig1)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='darkgreen', markersize=5, label='G or H (rig2)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='darkblue', markersize=5, label='G or H (rig1)')
    ]
    
    plt.legend(handles=legend_elements, title='Legend')
    
    plt.show()

# Example usage

folder_path = r'\\prfs.hhmi.org\genie\GECIScreenData\GECI_Imaging_Data\SCaMP\20240304_SCaMP_raw'
numbers_and_subfolders, filenames = extract_numbers_and_subfolders_from_filenames(folder_path)
print(f"All extracted numbers and subfolders: {numbers_and_subfolders}")  # Print all extracted numbers and subfolders
create_swarm_and_box_plot(numbers_and_subfolders, filenames)