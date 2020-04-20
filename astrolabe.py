# Florian Fruehwirth
# Does all the maths stuff and comparisons
# Last change: 07.02.2020

import math as m
import shelve

# wildcard
# marker_list = [{'ID': 1, 'x': 162, 'y': 435}, {'ID': 2, 'x': 192, 'y': 465}, {'ID': 3, 'x': 211, 'y': 434}, {'ID': 4, 'x': 248, 'y': 450}, {'ID': 5, 'x': 241, 'y': 396}]
# random
# marker_list = [{'ID': 1, 'x': 180, 'y': 538}, {'ID': 2, 'x': 223, 'y': 542}, {'ID': 3, 'x': 160, 'y': 48}, {'ID': 4, 'x': 182, 'y': 50}, {'ID': 5, 'x': 189, 'y': 223}]
# check
marker_list = {'1': {'x': 261, 'y': 207}, '2': {'x': 329, 'y': 340}, '3': {'x': 441, 'y': 343}, '4': {'x': 497, 'y': 476}, '5': {'x': 626, 'y': 397}}

star_distances = shelve.open('star_save_test')['distances']
normalized_star_distances = {}
dis_dif = {}
dis_dif_comb = {}
marker_num = len(marker_list)
print(star_distances)


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

# Calculates angles between Star1-Star2 and Star1-StarX
def calculate_marker_angles(**markers):
    angles = {}
    # Extraxts the x and y values of the first two points in the list
    m1 = markers[list(markers.keys())[0]]['x']
    m2 = markers[list(markers.keys())[0]]['y']
    s1 = markers[list(markers.keys())[1]]['x']
    s2 = markers[list(markers.keys())[1]]['y']
    d = m.atan2(s2-m2, s1-m1) # Saves the first part of the equation as a constant so it doesn't have to be repeated

    # Repeats the calculations for all points in the list except the first two
    for i in range(2, len(markers)):
        x1 = markers[list(markers.keys())[i]]['x']
        x2 = markers[list(markers.keys())[i]]['y']
        ang = m.degrees(d - m.atan2(x2-m2, x1-m1))
        # Adds 360 to negative values to only return positive angles
        if ang < 0:
            ang += 360
        angles[list(markers.keys())[i]] = ang
    return angles


# Normalizes all distances so that one is 1.0 and all others are fractions of that
def normalize(**values):
    normalized_distances = {}
    ref_distance = list(values.values())[0]  # Takes the first entry in the list of distances
    for i in values:  # Iterates through the entire list and divides all distances by the chosen reference distance.
        normalized_distances[i] = (values[i]/ref_distance)
    return normalized_distances  # returns a new list of normalized distances


# Normalizes all star distances and puts them in a new dictionary
for i in star_distances:
    normalized_star_distances[i] = normalize(**star_distances[i])


marker_distances = calculate_marker_distances(**marker_list)
normalized_marker_distances = normalize(**marker_distances)
marker_angles = calculate_marker_angles(**marker_list)
normalized_marker_angles = normalize(**marker_angles)


# Compares normalized marker and star distances
for d in normalized_star_distances:
    dis_dif[d] = {}
    for (s, n) in zip(normalized_star_distances[d], normalized_marker_distances):
        dis_dif[d][s] = normalized_star_distances[d][s] - normalized_marker_distances[n]

# Makes a new list with the sums of the differences between marker and star distances. Quick way to see which master star might be the best match.
for d in dis_dif:
    sum = 0
    for i in dis_dif[d]:
        sum = sum + abs(dis_dif[d][i])
        dis_dif_comb[d] = sum

# Sorts dis_dif_comb by values to see which master star has the least deviation from the marker pattern
dis_dif_comb = {k: v for k, v in sorted(dis_dif_comb.items(), key=lambda item: abs(item[1]))}

# Prints the HIP ID of the star with the least deviation.
print(list(dis_dif_comb.keys())[0])


# Analytics code to compare expected and actual results
# x = list(dis_dif_comb.keys())[0]
# print(f"{x} ({dis_dif_comb[x]}) -> {dis_dif[x]}")
# print(dis_dif['8886'])
