import pandas as pd
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import random
# data = pd.read_fwf(r"C:\Users\ayush\Desktop\minor project\VisDrone_Dataset\VisDrone2019-DET-train\VisDrone2019-DET-train\labels\0000084_02139_d_0000007.txt")
 
 
 
input_file = r"D:\Projects\UAV comm\server\0000085_00001_d_0000008.txt"
output_file = "output.txt"
 
with open(input_file, "r") as f:
    content = f.read()
    content_with_commas = content.replace(" ", ",")
 
with open(output_file, "w") as f:
    f.write(content_with_commas)
 
#print("Commas inserted successfully.")
 
 
 
 
data = pd.read_csv(r"D:\Projects\UAV comm\server\output.txt")
 
 
filtered_data = data[(data['0'] == 1) | (data['0'] == 0)]
 
filtered_data['0.7074074074074075'] = 1 - filtered_data['0.7074074074074075']
filtered_data = filtered_data.reset_index(drop=True)
 
 
 
 
import pandas as pd
import math
 
rows = []
vis = set([])
# Sample data
for i in range(50):
    def find_closest_rows(filtered_data, num_iterations):
        # Start from row 0
 
 
        current_row_index = i
        closest_rows = [current_row_index]
        visited_rows = set([current_row_index])
 
        for _ in range(num_iterations):
            current_row = filtered_data.iloc[current_row_index]
            distances = []
 
            # Calculate Euclidean distance from the current row to unvisited rows
            for index, row in filtered_data.iterrows():
                if index != current_row_index and index not in visited_rows:
                    euclidean_distance = math.sqrt((current_row['0.190625'] - row['0.190625'])**2 + (current_row['0.7074074074074075'] - row['0.7074074074074075'])**2)
                    distances.append((index, euclidean_distance))
 
            if not distances:
                # All remaining rows are visited
                break
 
            # Find the row with the minimum Euclidean distance
            min_distance_row = min(distances, key=lambda x: x[1])
            if min_distance_row[1]>0.09:
                #print("Exceeded threshold")
                break
            current_row_index = min_distance_row[0]
            closest_rows.append(current_row_index)
            visited_rows.add(current_row_index)
 
            #print(f"Minimum distance at iteration {_ + 1}: {min_distance_row[1]}")
 
        if len(closest_rows)==6:
 
            l = 0  # Initialize l
 
            while l < len(closest_rows):
                if closest_rows[l] in vis:
                    closest_rows.pop(l)
                else:
                    l += 1
 
 
            for l in range(len(closest_rows)):
                vis.add(closest_rows[l])
            if len(closest_rows)>2:
                rows.append(closest_rows)
 
 
        return closest_rows
 
    # Usage example
    closest_rows = find_closest_rows(filtered_data, 5)
    #print("Closest rows:", closest_rows)
 
 
print(len(rows))

 
# Open the image using Pillow
image = Image.open(r"D:\Projects\UAV comm\server\0000085_00001_d_0000008.jpg")  # Replace with the path to your image file
 
# Get the image dimensions
image = ImageOps.flip(image)
width, height = image.size
 
# Define the rows data containing 6 lists (replace with your data)
 
 
# Create a Matplotlib figure
fig, ax = plt.subplots()
 
# Display the image on the Matplotlib axes
ax.imshow(image)
 
# Invert the y-axis
ax.invert_yaxis()
 
# Define a list of colors for each row
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'w']
 
# Plot points from each row with a different color
for i, row_index in enumerate(rows):
    color = colors[i % len(colors)]  # Get a color from the list
    x_coordinate = filtered_data['0.190625'].iloc[row_index]
    y_coordinate = filtered_data['0.7074074074074075'].iloc[row_index]
    ax.plot(x_coordinate * width, y_coordinate * height, color + ' o')  # 'ro' for red, 'go' for green, etc.
 
# Set the aspect ratio to 'auto' to prevent distortion of the image
# ax.set_aspect('auto')
 
# Show the plot
plt.savefig('result.jpg')