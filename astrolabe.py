import math as m
import shelve
from pathlib import Path

ybp = 0
matches = {}
norma_markers = {}


filename = Path.cwd() / "Test_Cassiopeia" / "test.smp"
star_distances = shelve.open(str(filename))['distances']
star_angles = shelve.open(str(filename))['angles']

filename = Path.cwd() / "cassiopeia.ptn"
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
print(marker_distances)

normd_markers = normalize(**marker_distances)

temp_dict = {}
b1 = marker_bearings[list(normd_markers)[0]]  # uses nearest neighbour as "normalizer" for bearings
temp_dict[list(normd_markers)[0]] = 0.0
del marker_bearings[list(normd_markers)[0]]  # removes "normalizer" from bearings list so it isn't used again

# Calculates angles between markers based on their bearings
for i in marker_bearings:
    b2 = marker_bearings[i]
    if b1 >= b2:
        ang = b1 - b2
    else:
        ang = b2 - b1
    temp_dict[i] = ang

# Sorts the normalized angles not on their values but on the values of the distances
for k in list(normd_markers.keys()):
    norma_markers[k] = temp_dict[k]

normd_star = {}

for i in star_distances:
    normd_star[i] = {}
    for d in star_distances[i]:
        normd_star[i][d] = {}
        divisor = star_distances[i][d]
        for x in star_distances[i]:
            normalized = star_distances[i][x]/divisor
            normd_star[i][d][x] = normalized

norma_star = {}

for i in star_angles:
    norma_star[i] = {}
    for s in star_angles[i]:
        norma_star[i][s] = {}
        minuend = star_angles[i][s]
        for x in star_angles[i]:
            normalized = minuend-star_angles[i][x]
            norma_star[i][s][x] = normalized


for a in normd_star:
    matches[f'{a}'] = {}
    matches[f'{a}']['Matches'] = 0
    for n in normd_star[a]:
        for t in normd_star[a][n]:
            compd_star = normd_star[a][n][t]
            compa_star = norma_star[a][n][t]
            for i in list(normd_markers.keys())[1:]:
                compd_markers = normd_markers[i]
                compa_markers = norma_markers[i]
                diff_d = compd_star-compd_markers
                diff_a = compa_star-compa_markers
                print(f'Master: {a}, Normalizer: {n}, Target: {t}, Difference distance: {diff_d}, Difference angle: {diff_a}, Marker: {i}')
                if abs(diff_d) < 0.5 and abs(diff_a) < 1:
                    matches[a]['Matches'] += 1
                    if matches[a]['Matches'] == 1:
                        matches[a]['Marker 1'] = a
                        matches[a][f'Marker {list(normd_markers.keys())[0]}'] = n
                        matches[a][f'Marker {i}'] = t
                    else:
                        matches[a][f'Marker {i}'] = t

for k, v in list(matches.items()):
    if v['Matches'] < len(list(normd_markers))-1:
        del matches[k]

print(matches)


# for i in star_distances:
#     master = i
#     target1, target2 = list(star_distances[i].keys())[0:2]
#     print(f'Master: {i}, Target 1: {target1}, Target 2: {target2}')
#
#     m1 = 1
#     m2 = (star_distances[master][target2])/star_distances[master][target1]
#     # wan_dis = (star_distances[target1][target2])/star_distances[master][target1]
#     ang = m.radians(star_angles[master][target1]-star_angles[master][target2])
#     dist = m.sqrt(m1*m1+m2*m2-2*m1*m2*m.cos(ang))
#     print(dist)


# Distance 8886-6686: 4.799
# Distance 8886-4427: 7.32
# Angle: 25
# ?: 3.597
#
# Distance 8886-6686: 1
# Distance 8886-4427: 1.525
# Angle: 25
# ?: 0.749
