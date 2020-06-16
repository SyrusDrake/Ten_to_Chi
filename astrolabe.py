# Florian Fruehwirth
# Does all the maths stuff and comparisons
# Last change: 16.06.2020

import math as m
import shelve
from tkinter import filedialog
from pathlib import Path

marker_list = {'1': {'x': 261, 'y': 207}, '2': {'x': 329, 'y': 340}, '3': {'x': 441, 'y': 343}, '4': {'x': 497, 'y': 476}, '5': {'x': 626, 'y': 397}}
# filename = filedialog.askopenfilename(filetypes=[('Patterns', '*.ptn')])
# marker_list = shelve.open(filename)['marker_list']
# filename.close()
# filename = filedialog.askopenfilename(filetypes=[('Maps', '*.smp')])
filename = Path.cwd() / "Map_47N" / "Map_0BP.smp"
star_distances = shelve.open(str(filename))['distances']
star_angles = shelve.open(str(filename))['angles']

normalized_star_distances = {}
normalized_star_angles = {}
dis_dif = {}
ang_dif = {}
dis_dif_comb = {}
ang_dif_comb = {}
total_comb = {}
marker_num = len(marker_list)


# Calculates distances from a master marker to all other points
def calculate_marker_distances(**markers):
    distances = {}
    x1 = markers[list(markers.keys())[0]]['x']
    y1 = markers[list(markers.keys())[0]]['y']
    for point in markers:  # Goes through all markers except the first
        x2 = markers[point]['x']
        y2 = markers[point]['y']
        dis = m.sqrt((x2-x1)**2+(y2-y1)**2)  # calculates the distances
        if dis == 0:
            pass
        else:
            distances[point] = dis
    distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}  # sorts the dictionary entries by value
    return distances


# Calculates angles between Marker1-Marker2 and Marker1-MarkerX
def calculate_marker_angles(**markers):
    angles = {}
    # Extraxts the x and y values of the first two points in the list
    m1 = markers[list(markers.keys())[0]]['x']
    m2 = markers[list(markers.keys())[0]]['y']
    s1 = markers[list(markers.keys())[1]]['x']
    s2 = markers[list(markers.keys())[1]]['y']
    d = m.atan2(s2-m2, s1-m1)  # Saves the first part of the equation as a constant so it doesn't have to be repeated

    # Repeats the calculations for all points in the list except the first two
    for i in range(2, len(markers)):
        x1 = markers[list(markers.keys())[i]]['x']
        x2 = markers[list(markers.keys())[i]]['y']
        ang = m.degrees(m.atan2(x2-m2, x1-m1) - d)
        # Adds 360 to negative values to only return positive angles
        if ang < 0:
            ang += 360
        angles[list(markers.keys())[i]] = ang
    return angles


# Normalizes all values so that one is 1.0 and all others are fractions of that
def normalize(**values):
    normalized_values = {}
    ref_values = list(values.values())[0]  # Takes the first entry in the list of values
    for i in values:  # Iterates through the entire list and divides all values by the chosen reference values.
        normalized_values[i] = (values[i]/ref_values)
    return normalized_values  # returns a new list of normalized values


# <cf> Normalizes all values and puts them in a new dictionary
for i in star_distances:
    normalized_star_distances[i] = normalize(**star_distances[i])

for i in star_distances:
    normalized_star_angles[i] = normalize(**star_angles[i])

marker_distances = calculate_marker_distances(**marker_list)
normalized_marker_distances = normalize(**marker_distances)
marker_angles = calculate_marker_angles(**marker_list)
normalized_marker_angles = normalize(**marker_angles)

# </cf> Normalizes all values and puts them in a new dictionary


# <cf> Compares normalized marker and star values
for d in normalized_star_distances:
    dis_dif[d] = {}
    for (s, n) in zip(normalized_star_distances[d], normalized_marker_distances):
        dis_dif[d][s] = normalized_star_distances[d][s] - normalized_marker_distances[n]

for d in normalized_star_angles:
    ang_dif[d] = {}
    for (s, n) in zip(normalized_star_angles[d], normalized_marker_angles):
        ang_dif[d][s] = normalized_star_angles[d][s] - normalized_marker_angles[n]

# </cf> Compares normalized marker and star values

# <cf> Makes a new list with the sums of the differences between marker and star distances/angles. Quick way to see which master star might be the best match.
for d in dis_dif:
    sum = 0
    for i in dis_dif[d]:
        sum = sum + abs(dis_dif[d][i])
        dis_dif_comb[d] = sum

for d in ang_dif:
    sum = 0
    for i in ang_dif[d]:
        sum = sum + abs(ang_dif[d][i])
        ang_dif_comb[d] = sum
# </cf> Makes a new list with the sums of the differences between marker and star distances/angles. Quick way to see which master star might be the best match.

# Sorts dis_dif_comb by values to see which master star has the least deviation from the marker pattern

dis_dif_comb = {k: v for k, v in sorted(dis_dif_comb.items(), key=lambda item: abs(item[1]))}
ang_dif_comb = {k: v for k, v in sorted(ang_dif_comb.items(), key=lambda item: abs(item[1]))}

for i in dis_dif_comb:
    x = dis_dif_comb[i] + ang_dif_comb[i]
    total_comb[i] = x

# Prints the HIP ID of the star with the least deviation.
print(list(dis_dif_comb.keys())[0])
print(list(ang_dif_comb.keys())[0])
print(list(total_comb.keys())[0])


# Analytics code to compare expected and actual results
# x = list(total_comb.keys())[0]
# print(f"{x} ({total_comb[x]}) -> {total_comb[x]}")
# print(total_comb['8886'])
