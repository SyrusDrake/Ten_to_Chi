# Florian Fruehwirth
# Does all the maths stuff and comparisons
# Last change: 07.02.2020

import math as m

# wildcard
# marker_list = [{'ID': 1, 'x': 162, 'y': 435}, {'ID': 2, 'x': 192, 'y': 465}, {'ID': 3, 'x': 211, 'y': 434}, {'ID': 4, 'x': 248, 'y': 450}, {'ID': 5, 'x': 241, 'y': 396}]
# random
# marker_list = [{'ID': 1, 'x': 180, 'y': 538}, {'ID': 2, 'x': 223, 'y': 542}, {'ID': 3, 'x': 160, 'y': 48}, {'ID': 4, 'x': 182, 'y': 50}, {'ID': 5, 'x': 189, 'y': 223}]
# check
marker_list = [{'ID': 1, 'x': 239, 'y': 315}, {'ID': 2, 'x': 478, 'y': 376}, {'ID': 3, 'x': 553, 'y': 252}, {'ID': 4, 'x': 752, 'y': 291}, {'ID': 5, 'x': 799, 'y': 134}]
stars = [{'hip': 4427, 'mag': 2.15, 'ra': 14.17708808, 'de': 60.71674966, 'pm_ra': 7.130699999999999e-06, 'pm_de': -1.06196e-06, 'cal_ra': 14.39100908, 'cal_de': 60.684890859999996, 'dis_3179': 4.679132022843306, 'dis_746': 6.147565179199756, 'dis_6686': 3.6154859678780737, 'dis_8886': 7.326465552975556}, {'hip': 3179, 'mag': 2.24, 'ra': 10.12661349, 'de': 56.53740928, 'pm_ra': 1.4000079999999999e-05, 'pm_de': -8.94326e-06, 'cal_ra': 10.54661589, 'cal_de': 56.26911148, 'dis_4427': 4.679132022843306, 'dis_746': 4.916157800415676, 'dis_6686': 6.98066709787243, 'dis_8886': 11.57559683497648}, {'hip': 746, 'mag': 2.28, 'ra': 2.29204036, 'de': 59.15021814, 'pm_ra': 0.00014550242, 'pm_de': -5.015675999999999e-05, 'cal_ra': 6.657112959999999, 'cal_de': 57.64551534, 'dis_4427': 6.147565179199756, 'dis_3179': 4.916157800415676, 'dis_6686': 9.694935407428709, 'dis_8886': 13.261054531148202}, {'hip': 6686, 'mag': 2.66, 'ra': 21.45251267, 'de': 60.23540347, 'pm_ra': 8.263272e-05, 'pm_de': -1.375822e-05, 'cal_ra': 23.93149427, 'cal_de': 59.82265687, 'dis_4427': 3.6154859678780737, 'dis_3179': 6.98066709787243, 'dis_746': 9.694935407428709, 'dis_8886': 4.799727548960269}, {'hip': 8886, 'mag': 3.35, 'ra': 28.59868107, 'de': 63.67014686, 'pm_ra': 8.89044e-06, 'pm_de': -5.187479999999999e-06, 'cal_ra': 28.865394270000003, 'cal_de': 63.51452246, 'dis_4427': 7.326465552975556, 'dis_3179': 11.57559683497648, 'dis_746': 13.261054531148202, 'dis_6686': 4.799727548960269}]
star1 = {'hip': 8886, 'mag': 3.35, 'ra': 28.59868107, 'de': 63.67014686, 'pm_ra': 8.89044e-06, 'pm_de': -5.187479999999999e-06, 'cal_ra': 28.865394270000003, 'cal_de': 63.51452246, 'dis_4427': 7.326465552975556, 'dis_3179': 11.57559683497648, 'dis_746': 13.261054531148202, 'dis_6686': 4.799727548960269}

# Calculates distances from a master marker to all other points
def calculate_marker_distances():
    global marker_list
    distances = {}
    master = marker_list[0]
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


# Extracts the distances from a single star dictionary
def extract_distances(**star):
    distances = {}
    for i in star:
        if 'dis_' in i:
            distances[i] = star[i]
    distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}  # Sorts by size of value
    return distances


# Goes through the entire list of star dictionaries
for i in stars:
    d = extract_distances(**i)
    normalized_star_distances = (normalize(**d))
    print(f"{i['hip']}: {normalized_star_distances}; {sum(normalized_star_distances.values())}")
    # print(f"{i['hip']}: {sum(normalized_star_distances.values())}.")


marker_distances = calculate_marker_distances()
normalized_marker_distances = normalize(**marker_distances)
print(f"{normalized_marker_distances}; {sum(normalized_marker_distances.values())}")
