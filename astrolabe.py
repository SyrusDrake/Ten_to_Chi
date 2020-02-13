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
marker_list = [{'ID': 1, 'x': 239, 'y': 315}, {'ID': 2, 'x': 478, 'y': 376}, {'ID': 3, 'x': 553, 'y': 252}, {'ID': 4, 'x': 752, 'y': 291}, {'ID': 5, 'x': 799, 'y': 134}]

star_distances = shelve.open('star_save_test')['distances']
normalized_star_distances = {}

# Calculates distances from a master marker to all other points


def calculate_marker_distances(*markers):
    distances = {}
    master = markers[0]
    x1 = master['x']
    y1 = master['y']
    for marker in marker_list[1:]:  # Goes through all markers except the first
        x2 = marker['x']
        y2 = marker['y']
        dis = m.sqrt((x2-x1)**2+(y2-y1)**2)  # calculates the distances
        distances[f"mdis_{marker['ID']}"] = dis  # adds the result to the list of distances
    distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}  # sorts the dictionary entries by value
    return distances


# Normalizes all distances so that one is 1.0 and all others are fractions of that
def normalize(**distances):
    normalized_distances = {}
    ref_distance = list(distances.values())[0]  # Takes the first entry in the list of distances
    for i in distances:  # Iterates through the entire list and divides all distances by the chosen reference distance.
        normalized_distances[i] = (distances[i]/ref_distance)
    return normalized_distances  # returns a new list of normalized distances


for i in star_distances:
    normalized_star_distances[i] = normalize(**star_distances[i])

marker_distances = calculate_marker_distances(*marker_list)
normalized_marker_distances = normalize(**marker_distances)

print(star_distances)
print(normalized_star_distances)
print(marker_distances)
print(normalized_marker_distances)
