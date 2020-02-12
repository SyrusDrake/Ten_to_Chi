# Florian Fruehwirth
# Starmap Alpha
# Last change: 13.02.2020

import math as m
import time
import shelve

hip = open('hip_main.dat')
lines = hip.readlines()  # Puts every line of the catalog in an list item
stars = []  # Empty list of stars
ngstars = []  # List of stars with missing valeus
distances = {}
latitude = 47  # Latitde of the observer
ybp = 30000  # Years before present
deg_per_mas = 0.000000278  # conversion factor from miliarcseconds to degrees
dec_limit = -(90 - latitude)  # Declination limit based on observer latitude
mag_limit = 4.8
# 6.5 is limit of visibility. 4.8 is 1025 stars


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


# <cf> Function to calculate angular distance between stars

# Function to calculate angular distance between stars
def calculate_angular_distance(active_entry, target_entry):  # Takes HIP IDs as input
    active_hip = active_entry['hip']
    target_hip = target_entry['hip']
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

# </cf>


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
        ngstars.append(newstar)
# </cf>


todo = int(((len(stars) - 1) * len(stars)) / 2)  # How many calculations are necessary. Might be removed later.
calculations = 0

# Creates an empty dictionary of dictionaries since creating nested entries from scratch seems to be impossible.
for i in stars:
    distances[i['hip']] = {}

startTime = time.time()
for i in stars:
    active_hip = i['hip']
    for k in stars:
        target_hip = k['hip']
        if target_hip in distances and active_hip in distances[target_hip]:  # Checks if the calculation has already been done in reverse
            pass
        elif (i != k):  # Avoids calculating distances of 0
            ang = calculate_angular_distance(i, k)
            distances[active_hip][target_hip] = distances[target_hip][active_hip] = ang
            calculations += 1
            print(f"{calculations}/{todo}")  # Shows how many calculations have been done already vs how many are necessary

print(f"Completed {calculations} calculations for {len(stars)} stars in {(time.time() - startTime)} seconds.")

print(distances)

save_file = shelve.open("star_save", "n")
save_file['distances'] = distances
save_file.close()
