import math as m
import shelve
from pathlib import Path
from tkinter import filedialog

ybp = 0
matches = {}
norma_markers = {}
debug = open("debug.txt", "w+")



# filename = Path.cwd() / "Test" / "test.smp"
# filename = Path.cwd() / "Test" / "full.smp"
filename = Path.cwd() / "Test" / "large.smp"
star_distances = shelve.open(str(filename))['distances']
star_angles = shelve.open(str(filename))['angles']
normd_star = shelve.open(str(filename))['normalized_distances']
norma_star = shelve.open(str(filename))['normalized_angles']

# filename = Path.cwd() / "Patterns" / "gemini.ptn"
filename = filedialog.askopenfilename(filetypes=[('Patterns', '*.ptn')])
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


for a in normd_star:
    # matches[f'{a}'] = {}
    # matches[f'{a}']['Matches'] = 0
    for n in normd_star[a]:
        mid = f'{a}-{n}'
        matches[mid] = {}
        matches[mid]['Matches'] = 0
        matches[mid]['Diff_d'] = 0
        matches[mid]['Diff_a'] = 0
        for t in normd_star[a][n]:
            compd_star = normd_star[a][n][t]
            compa_star = norma_star[a][n][t]
            for i in list(normd_markers.keys())[1:]:
                compd_markers = normd_markers[i]
                compa_markers = norma_markers[i]
                diff_d = compd_star-compd_markers
                diff_a = compa_star-compa_markers
                # if a == '57632' and n == '54879' and (t == '54872' or t == '50583' or t == '49583' or t == '49669' or t == '50335' or t == '48455' or t == '47908'):
                #     print(f'Master: {a}, Normalizer: {n}, Target: {t}, Difference distance: {diff_d}, Difference angle: {diff_a}, Marker: {i}')
                if abs(diff_d) < 0.40 and abs(diff_a) < 3:
                    if matches[mid]['Matches'] == 0:
                        debug.write(f'Master: {a}, Normalizer: {n}, Target: {t}, Difference distance: {diff_d}, Difference angle: {diff_a}, Marker: {i}\r\n')
                        matches[mid]['Matches'] += 1
                        matches[mid]['Diff_d'] += abs(diff_d)
                        matches[mid]['Diff_a'] += abs(diff_a)
                        matches[mid]['Marker 1'] = a
                        matches[mid][f'Marker {list(normd_markers.keys())[0]}'] = n
                        matches[mid][f'Marker {i}'] = t
                    elif f'Marker {i}' not in list(matches[mid].keys()):
                        debug.write(f'Master: {a}, Normalizer: {n}, Target: {t}, Difference distance: {diff_d}, Difference angle: {diff_a}, Marker: {i}\r\n')
                        matches[mid]['Matches'] += 1
                        matches[mid]['Diff_d'] += abs(diff_d)
                        matches[mid]['Diff_a'] += abs(diff_a)
                        matches[mid][f'Marker {i}'] = t

for k, v in list(matches.items()):
    if v['Matches'] < len(list(normd_markers))-1:
        del matches[k]

# for i in matches:
#     matches[i]['Diff_total'] = matches[i]['Diff_d'] + matches[i]['Diff_a']

sort_dist = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1]['Diff_d'])}
sort_ang = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1]['Diff_a'])}

del_list = list(sort_dist.keys())[30:]

for i in del_list:
    del sort_dist[i]

del_list = list(sort_ang.keys())[30:]

for i in del_list:
    del sort_ang[i]

print("Sorted by distance-deviation--------------")
for i in sort_dist:
    print(sort_dist[i])

print("Sorted by angle-deviation--------------")
for i in sort_ang:
    print(sort_ang[i])

print("In both--------------")
for i in sort_dist:
    if i in sort_ang:
        print(sort_dist[i])
