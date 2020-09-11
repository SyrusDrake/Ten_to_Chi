import math as m
import shelve
from pathlib import Path

ybp = 0
matches = {}
norma_markers = {}
debug = open("debug.txt", "w+")


# filename = Path.cwd() / "Test_Cassiopeia" / "test.smp"
filename = Path.cwd() / "Test_Cassiopeia" / "full.smp"
star_distances = shelve.open(str(filename))['distances']
star_angles = shelve.open(str(filename))['angles']
normd_star = shelve.open(str(filename))['normalized_distances']
norma_star = shelve.open(str(filename))['normalized_angles']

filename = Path.cwd() / "Patterns" / "gemini.ptn"
# filename = Path.cwd() / "cassiopeia.ptn"
markers = shelve.open(str(filename))['marker_list']

def calculate_marker_distances(**markers):
    distances = {}
    x1 = markers[list(markers.keys())[0]]['x']
    y1 = markers[list(markers.keys())[0]]['y']
    for point in markers:  # Goes through all markers except the first
        x2 = markers[point]['x']
        y2 = markers[point]['y']
        ID = point
        dis = m.sqrt((x2-x1)**2+(y2-y1)**2)  # calculates the distances
        if dis == 0:
            pass
        else:
            distances[ID] = dis
    distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}  # sorts the dictionary entries by value
    return distances


def normalize(**values):
    normalized_values = {}
    ref_values = list(values.values())[0]  # Takes the first entry in the list of values
    for i in values:  # Iterates through the entire list and divides all values by the chosen reference values.
        normalized_values[i] = (values[i]/ref_values)
    return normalized_values  # returns a new list of normalized values


def calculate_marker_bearings(**markers):
    angles = {}
    x1 = markers['1']['x']
    y1 = markers['1']['y']

    for i in range(2, len(markers)+1):
        x2 = markers[str(i)]['x']
        y2 = markers[str(i)]['y']
        ang = 180-m.degrees(m.atan2(x2-x1, y2-y1))
        angles[str(i)] = ang

    return angles


marker_bearings = calculate_marker_bearings(**markers)

marker_distances = calculate_marker_distances(**markers)

normd_markers = normalize(**marker_distances)

temp_dict = {}
b1 = marker_bearings[list(normd_markers)[0]]  # uses nearest neighbour as "normalizer" for bearings
temp_dict[list(normd_markers)[0]] = 0.0
del marker_bearings[list(normd_markers)[0]]  # removes "normalizer" from bearings list so it isn't used again

# Calculates angles between markers based on their bearings
for i in marker_bearings:
    b2 = marker_bearings[i]
    ang = b1 - b2
    if ang > 180:
        ang = ang-360
    elif ang < -180:
        ang += 360
    temp_dict[i] = ang

# Sorts the normalized angles not on their values but on the values of the distances
for k in list(normd_markers.keys()):
    norma_markers[k] = temp_dict[k]

print(norma_markers)

for a in normd_star:
    # matches[f'{a}'] = {}
    # matches[f'{a}']['Matches'] = 0
    for n in normd_star[a]:
        mid = f'{a}-{n}'
        matches[mid] = {}
        matches[mid]['Matches'] = 0
        for t in normd_star[a][n]:
            compd_star = normd_star[a][n][t]
            compa_star = norma_star[a][n][t]
            for i in list(normd_markers.keys())[1:]:
                compd_markers = normd_markers[i]
                compa_markers = norma_markers[i]
                diff_d = compd_star-compd_markers
                diff_a = compa_star-compa_markers
                if a == '33018' and n == '34693' and (t == '36850' or t == '32246' or t == '36046' or t == '36962' or t == '37826' or t == '30343' or t == '35550' or t == '34088' or t == '29655' or t == '30883' or t == '37740' or t == '28734'):
                    print(f'Master: {a}, Normalizer: {n}, Target: {t}, Difference distance: {diff_d}, Difference angle: {diff_a}, Marker: {i}')
                if abs(diff_d) < 0.35 and abs(diff_a) < 3:
                    if matches[mid]['Matches'] == 0:
                        debug.write(f'Master: {a}, Normalizer: {n}, Target: {t}, Difference distance: {diff_d}, Difference angle: {diff_a}, Marker: {i}\r\n')
                        matches[mid]['Matches'] += 1
                        matches[mid]['Marker 1'] = a
                        matches[mid][f'Marker {list(normd_markers.keys())[0]}'] = n
                        matches[mid][f'Marker {i}'] = t
                    elif f'Marker {i}' not in list(matches[mid].keys()):
                        debug.write(f'Master: {a}, Normalizer: {n}, Target: {t}, Difference distance: {diff_d}, Difference angle: {diff_a}, Marker: {i}\r\n')
                        matches[mid]['Matches'] += 1
                        matches[mid][f'Marker {i}'] = t

for k, v in list(matches.items()):
    if v['Matches'] < len(list(normd_markers))-1:
        del matches[k]

print(matches)
