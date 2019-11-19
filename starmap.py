hip = open('hip_main.dat')
lines = hip.readlines()  # Puts every line of the catalog in an list item
stars = []  # Empty list of stars
ngstars = []
ybp = 2  # Years before present
latitude = 47
deg_per_mas = 0.000000278  # conversion factor from miliarcseconds to degrees
dec_limit = -(90 - latitude)


# get all star
def chop(line):
    choppedline = []
    list_with_space = line.rsplit('|')
    for item in list_with_space:
        choppedline.append(item.strip())    # Removes whitepsaces (?)
    return choppedline


def calculate_new_coordinates(ra, de, pm_ra, pm_de, ybp):
    new_ra = ra + ((pm_ra * ybp) % 360)
    new_de = de + ((pm_de * ybp) % 360)

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


newstar = {}
newstar['hip'] = int(000)
newstar['mag'] = float(1.0)
newstar['ra'] = float(10.0)
newstar['de'] = float(45.0)
newstar['pm_ra'] = 1.0
newstar['pm_de'] = 2.0
newstar['cal_ra'], newstar['cal_de'] = calculate_new_coordinates(newstar['ra'], newstar['de'], newstar['pm_ra'], newstar['pm_de'], ybp)
stars.append(newstar)


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

        if newstar['cal_de'] > dec_limit and newstar['mag'] <= 6.5:
            # Adds dictionary items
            stars.append(newstar)

    except ValueError:
        # data missing
        ngstars.append(newstar)

print(next(item for item in stars if item['hip'] == 63))
