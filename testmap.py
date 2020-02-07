# Florian Fruehwirth
# Testmap: Functionally the same as starmap but creates simpler output files for testing purposes
# Last change: 29.01.20

# Polaris 11767
# Sirius 32349
# Vega 91262
# γ Lyr 93194
# Deneb 102098
# γ Cyg 100453

import math as m
import time
import pickle

hip = open('test_stars.txt')
lines = hip.readlines()  # Puts every line of the catalog in an list item
stars = []  # Empty list of stars
ngstars = []  # List of stars with missing valeus
latitude = 47  # Latitde of the observer
ybp = 30000  # Years before present
deg_per_mas = 0.000000278  # conversion factor from miliarcseconds to degrees
dec_limit = -(90 - latitude)  # Declination limit based on observer latitude
mag_limit = 20
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


# Function to calculate angular distance between stars
def calculate_angular_distance(active_star, target_star):  # Takes HIP IDs as input
    active_entry = next(item for item in stars if item['hip'] == active_star)  # Finds item in hip list based on ID
    target_entry = next(item for item in stars if item['hip'] == target_star)
    ra1 = active_entry['ra']
    dec1 = active_entry['de']
    ra2 = target_entry['ra']
    dec2 = target_entry['de']

    ra1 = m.radians(ra1)
    dec1 = m.radians(dec1)

    ra2 = m.radians(ra2)
    dec2 = m.radians(dec2)

    ang = m.degrees(m.acos((m.sin(dec1) * m.sin(dec2)) + (m.cos(dec1) * m.cos(dec2) * m.cos(ra1 - ra2))))
    active_entry[f'dis_{target_star}'] = ang  # Adds the angular distance to the target star to the item list of the active star
    target_entry[f'dis_{active_star}'] = ang  # Adds the angular distance to the active star to the item list of the target star





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

startTime = time.time()
for i in stars:
    for k in stars:
        if (f"dis_{i['hip']}" in k):  # Checks if the calculation has already been done in reverse
            pass
        elif (i != k):  # Avoids calculating distances of 0
            calculate_angular_distance(i['hip'], k['hip'])
            calculations += 1
            print(f"{calculations}/{todo}")  # Shows how many calculations have been done already vs how many are necessary

print(f"Completed {calculations} calculations for {len(stars)} stars in {(time.time() - startTime)} seconds.")

print(stars)

# save_file = open("save.dat", "w+b")
# pickle.dump(stars, save_file)
# save_file.close()
