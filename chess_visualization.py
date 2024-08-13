import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors


def create_heatmap(matrix, title_str): # creates a heatmap of the chess board based on whatever 8x8 matrix is provided
    y_labels = ["8", "7", "6", "5", "4", "3", "2", "1"]
    x_labels = ["a", "b", "c", "d", "e", "f", "g", "h"]
    fig, ax = plt.subplots()
    im = ax.imshow(matrix)
    plt.grid(False)
    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(x_labels)), labels=x_labels)
    ax.set_yticks(np.arange(len(y_labels)), labels=y_labels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            text = ax.text(j, i, matrix[i, j],
                           ha="center", va="center", color="w")

    ax.set_title(title_str)
    fig.tight_layout()
    plt.show()

def castling_chart(matrix, title_str): #visualizes the castling matrix
    y_labels = ["1-0", "1/2-1/2", "0-1"]
    x_labels = ["white first", "same time", "black first"]

    # Define a custom color map that does not relate to the data values
    colors = [
    "#ffffff", "#ffffff", "#ffffff", 
    "#ffffff", "#ffffff", "#ffffff",
    "#ffffff", "#ffffff", "#ffffff"
    ]  
    
    cmap = mcolors.ListedColormap(colors)
    
    fig, ax = plt.subplots()
    im = ax.imshow(matrix, cmap=cmap)
    plt.grid(False)
    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(x_labels)), labels=x_labels)
    ax.set_yticks(np.arange(len(y_labels)), labels=y_labels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            text = ax.text(j, i, f'{matrix[i, j]:,}', ha="center", va="center", color="black")

    ax.set_title(title_str)
    fig.tight_layout()
    plt.show()

"""
# testing display with sample values
matrix = np.array([
    [691214, 222798, 757545],
    [118376, 38168, 131066],
    [627963, 201797, 688526]
])

castling_chart(matrix, "Castling Matrix")
"""