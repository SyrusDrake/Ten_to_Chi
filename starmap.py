import math as m

hip = open('hip_test.dat')
lines = hip.readlines()  # Puts every line of the catalog in an list item
stars = []  # Empty list of stars
ngstars = []  # List of stars with missing valeus
latitude = 47  # Latitde of the observer
ybp = 0  # Years before present
deg_per_mas = 0.000000278  # conversion factor from miliarcseconds to degrees
dec_limit = -(90 - latitude)  # Declination limit based on observer latitude
mag_limit = 6.5


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
def calculate_angular_distance(active_star, target_star):  # Takes HIP IDs as input
    active_entry = next(item for item in stars if item['hip'] == active_star)
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
    active_entry[f'dis_{target_star}'] = ang
    target_entry[f'dis_{active_star}'] = ang

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

        if newstar['cal_de'] > dec_limit and newstar['mag'] <= mag_limit:
            # Adds dictionary items
            stars.append(newstar)

    except ValueError:
        # data missing
        ngstars.append(newstar)
# </cf>

# Polaris 11767
# Sirius 32349
# Vega 91262
x = 0

for i in stars:
    for k in stars:
        if (f"dis_{i['hip']}" in k):
            pass
        elif (i != k):
            calculate_angular_distance(i['hip'], k['hip'])


print(stars)
