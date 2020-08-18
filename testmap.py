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

# hip = open('test_stars.txt')
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
ybp_max = 20000
deg_per_mas = 0.000000278  # conversion factor from miliarcseconds to degrees
dec_limit = -(90 - latitude)  # Declination limit based on observer latitude
mag_limit = 4.5
neighbours = 100
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

    # </cf>

    # <cf> Calculates angles between stars
    for h in stars:
        # Chooses a master and a slave (star and its closest neighbour), between which a line is drawn
        master_hip = f"{h['hip']}"
        slave_hip = list(distances[master_hip].keys())[0]
        slave = next(item for item in stars if item['hip'] == int(slave_hip))
        ra1 = m.radians(h['cal_ra'])
        dec1 = m.radians(h['cal_de'])
        ra2 = m.radians(slave['cal_ra'])
        dec2 = m.radians(slave['cal_de'])
        h1 = m.atan2(m.sin(ra2-ra1)*m.cos(dec2), m.cos(dec1)*m.sin(dec2)-m.sin(dec1)*m.cos(dec2)*m.cos(ra2-ra1))
        angles[master_hip][slave_hip] = 0  # An entry with no value is necesssary for proper sorting later. It is deleted afterwards.
        for t in stars:
            if t == h or t == slave:
                pass
            else:
                # Calculates the angle between the line master-slave and master-target
                target_hip = f"{t['hip']}"
                ra3 = m.radians(t['cal_ra'])
                dec3 = m.radians(t['cal_de'])
                h = m.atan2(m.sin(ra3-ra1)*m.cos(dec3), m.cos(dec1)*m.sin(dec3)-m.sin(dec1)*m.cos(dec3)*m.cos(ra3-ra1))
                ang = m.degrees(h1-h)
                if ang < 0:
                    ang += 360
                # print(f"Master: {master_hip}, Slave: {slave_hip}, Target: {target_hip}, Angle: {ang}")
                angles[master_hip][target_hip] = ang

    # Sorts the angle entries not based on their value but based on the distances.
    # I.e. the angle between Star 1 and Star 2 is smaller but gets sorted higher than S1-S3 because the distances S1-S3 is shorter.
    for i in distances:
        temp_dict[i] = {}
        for k in distances[i]:
            temp_dict[i][k] = angles[i][k]
        # x = list(temp_dict[i].keys())[0]
        del temp_dict[i][list(temp_dict[i].keys())[0]]
    angles = temp_dict

    # </cf> Calculates angles between stars

    print(f"Completed {calculations} calculations for {len(stars)} stars in {(time.time() - startTime)} seconds.")

    # <cf> Saving data

    # folder_path = Path.cwd() / f"Map_{latitude}N"
    # save_file = Path.cwd() / f"Map_{latitude}N" / f"Map_{ybp}BP.smp"

    folder_path = Path.cwd() / "Test_Cassiopeia"
    save_file = Path.cwd() / "Test_Cassiopeia" / f"Map_{ybp}BP.smp"

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    else:
        pass

    save_data = shelve.open(str(save_file), "n")
    save_data['mag_limit'] = mag_limit
    save_data['angles'] = angles
    save_data['distances'] = distances
    save_data.close()

    # </cf> Saving data
