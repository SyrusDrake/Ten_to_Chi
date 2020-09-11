# Florian Fruehwirth
# Testmap: Functionally the same as starmap but creates simpler output files for testing purposes
# Last change: 16.06.2020
# Longitude = right ascension
# Latitude = declination

# Polaris 11767
# Sirius 32349
# Vega 91262
# γ Lyr 93194
# Deneb 102098
# γ Cyg 100453

import math as m
import time
import shelve
from pathlib import Path
import os

# hip = open('hip_main.dat')
hip = open('hip_test.dat')
lines = hip.readlines()  # Puts every line of the catalog in an list item
stars = []  # Empty list of stars
distances = {}
angles = {}
temp_dict = {}
calculations = 0
latitude = 47  # Latitde of the observer
ybp = 0  # Years before present
step_size = 5000
ybp_max = 0
deg_per_mas = 0.000000278  # conversion factor from miliarcseconds to degrees
dec_limit = -(90 - latitude)  # Declination limit based on observer latitude
mag_limit = 5.3
neighbours = 100
norm_dist = {}
norm_ang = {}
# 6.5 is limit of visibility. 4.8 is 1025 stars. 3.4 seems to return the best results for now.

# get all star
def chop(line):
    choppedline = []
    list_with_space = line.rsplit('|')
    for item in list_with_space:
        choppedline.append(item.strip())    # Removes whitepsaces (?)
    return choppedline


# <cf> Function to calculate new coordinates based on proper motion
def calculate_new_coordinates(ra, de, pm_ra, pm_de, ybp):
    if (pm_ra * ybp >= 360):
        new_ra = ra + ((pm_ra * ybp) % 360)
    else:
        new_ra = ra + ((pm_ra * ybp))

    if ((pm_de * ybp) >= 360):
        new_de = de + ((pm_de * ybp) % 360)
    else:
        new_de = de + ((pm_de * ybp))

    if new_ra >= 360:
        new_ra = new_ra - 360
    if new_ra < 0:
        new_ra = new_ra + 360

    if new_de > 90:
        new_de = 180 - new_de
        if new_ra >= 180:
            new_ra = new_ra - 180
        if new_ra < 180:
            new_ra = new_ra + 180

    return new_ra, new_de
# </cf>


# Function to calculate angular distance between stars
def calculate_angular_distance(active_entry, target_entry):  # Takes HIP IDs as input

    ra1 = active_entry['ra']
    dec1 = active_entry['de']
    ra2 = target_entry['ra']
    dec2 = target_entry['de']

    ra1 = m.radians(ra1)
    dec1 = m.radians(dec1)

    ra2 = m.radians(ra2)
    dec2 = m.radians(dec2)

    ang = m.degrees(m.acos((m.sin(dec1) * m.sin(dec2)) + (m.cos(dec1) * m.cos(dec2) * m.cos(ra1 - ra2))))
    return ang


for ybp in range(ybp, ybp_max+1, step_size):
    stars = []  # Empty list of stars
    distances = {}
    angles = {}
    temp_dict = {}

# <cf> Creates list of star dictionary
for line in lines:
    # div by '|'
    chopdline = chop(line)
    try:
        newstar = {}
        newstar['hip'] = int(chopdline[1])
        newstar['mag'] = float(chopdline[5])
        newstar['ra'] = float(chopdline[8])
        newstar['de'] = float(chopdline[9])
        newstar['pm_ra'] = float(chopdline[12]) * deg_per_mas
        newstar['pm_de'] = float(chopdline[13]) * deg_per_mas
        newstar['cal_ra'], newstar['cal_de'] = calculate_new_coordinates(newstar['ra'], newstar['de'], newstar['pm_ra'], newstar['pm_de'], ybp)

        if newstar['cal_de'] > dec_limit and newstar['mag'] <= mag_limit:  # Checks if star is visible at position and due to brightness. Otherwise skips it.
            # Adds dictionary items
            stars.append(newstar)

    except ValueError:
        # data missing
        pass
# </cf>

# Creates an empty dictionary of dictionaries since creating nested entries from scratch seems to be impossible.
for i in stars:
    distances[f"{i['hip']}"] = {}
    angles[f"{i['hip']}"] = {}

# <cf> Creates distances-list
startTime = time.time()
for a in stars:
    active_hip = f"{a['hip']}"
    for t in stars:
        target_hip = f"{t['hip']}"
        if target_hip in distances and active_hip in distances[target_hip]:  # Checks if the calculation has already been done in reverse
            pass
        elif (a != t):  # Avoids calculating distances of 0
            ang = calculate_angular_distance(a, t)
            distances[active_hip][target_hip] = distances[target_hip][active_hip] = ang
            calculations += 1
            # print(f"{calculations}/{todo}")  # Shows how many calculations have been done already vs how many are necessary

for a in distances:
    distances[a] = {k: v for k, v in sorted(distances[a].items(), key=lambda item: item[1])}
    del_list = list(distances[a].keys())[neighbours:]
    for i in del_list:
        del distances[a][i]

for i in distances:
    norm_dist[i] = {}
    for d in distances[i]:
        norm_dist[i][d] = {}
        divisor = distances[i][d]
        for x in distances[i]:
            normalized = distances[i][x]/divisor
            norm_dist[i][d][x] = normalized

# </cf>

# <cf> Calculates angles between stars
for master in stars:
    active_hip = f"{master['hip']}"
    for t in distances[active_hip]:
        target = next(item for item in stars if item["hip"] == int(t))
        m_ra = m.radians(master['cal_ra'])
        m_dec = m.radians(master['cal_de'])
        t_ra = m.radians(target['cal_ra'])
        t_dec = m.radians(target['cal_de'])
        x = m.cos(t_dec) * m.sin(t_ra-m_ra)
        y = m.cos(m_dec) * m.sin(t_dec) - m.sin(m_dec) * m.cos(t_dec) * m.cos(t_ra-m_ra)
        ang = m.degrees(m.atan2(x, y))
        angles[active_hip][t] = -ang

for i in angles:
    norm_ang[i] = {}
    for s in angles[i]:
        norm_ang[i][s] = {}
        secondary = angles[i][s]
        for x in angles[i]:
            normalized = secondary-angles[i][x]
            if normalized > 180:
                normalized = normalized-360
            elif normalized < -180:
                normalized += 360
            norm_ang[i][s][x] = normalized

# </cf> Calculates angles between stars


# <cf> Saving data

# folder_path = Path.cwd() / f"Map_{latitude}N"
# save_file = Path.cwd() / f"Map_{latitude}N" / f"Map_{ybp}BP.smp"

folder_path = Path.cwd() / "Test_Cassiopeia"
# save_file = Path.cwd() / "Test_Cassiopeia" / f"Map_{ybp}BP.smp"
# save_file = Path.cwd() / "Test_Cassiopeia" / "full.smp"
save_file = Path.cwd() / "Test_Cassiopeia" / "test.smp"

if not os.path.exists(folder_path):
    os.mkdir(folder_path)
else:
    pass

save_data = shelve.open(str(save_file), "n")
save_data['mag_limit'] = mag_limit
save_data['angles'] = angles
save_data['distances'] = distances
save_data['normalized_angles'] = norm_ang
save_data['normalized_distances'] = norm_dist
save_data.close()

# </cf> Saving data
