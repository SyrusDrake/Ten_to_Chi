import math as m
import pickle
from pathlib import Path
import os
import tkinter.filedialog


class Atlas:

    def __init__(self, latitude, ybp_min, step_size, ybp_max, mag_limit, neighbours):
        self.latitude = latitude  # Latitude of the observer
        self.step_size = step_size
        self.ybp_min = ybp_min
        self.ybp_max = ybp_max
        self.mag_limit = mag_limit
        self.neighbours = neighbours
        self.dec_limit = -(90 - self.latitude)  # Declination limit based on observer latitude
        self.DEG_PER_MAS = 0.000000278  # conversion factor from miliarcseconds to degrees
        self.atlas = {}

    def createAtlas(self):
        if (self.step_size == 0):
            # Only creates one map if only one date is selected
            self.atlas[f"map_{self.ybp_min}BP"] = Map(self.ybp_min, self)
            self.atlas[f"map_{self.ybp_min}BP"].createMap()

        else:
            for x in range(self.ybp_min, self.ybp_max + 1, self.step_size):
                self.atlas[f"map_{x}BP"] = Map(x, self)
                self.atlas[f"map_{x}BP"].createMap()

        self.save()

    def save(self):
        min = int(self.ybp_min / 1000)
        max = int(self.ybp_max / 1000)
        default = Path.cwd() / "Atlases" / f"Atlas_{self.latitude}N_{min}k-{max}k"

        if not os.path.exists(default):
            os.mkdir(default)

        path = tkinter.filedialog.askdirectory(initialdir=default, title="Please select a directory")

        if os.path.normpath(path) != os.path.normpath(default):
            os.rmdir(default)

        for map in self.atlas:
            filename = os.path.join(path, f"Map_{int(self.atlas[map].ybp/1000)}k BP.map")
            file = open(filename, 'wb')
            pickle.dump(self.atlas[map], file)
            file.close()


class Map(Atlas):

    def __init__(self, ybp, parent):
        super().__init__(parent.latitude, parent.ybp_min, parent.step_size, parent.ybp_max, parent.mag_limit, parent.neighbours)
        self.ybp = ybp
        self.stars = []  # Empty list of stars
        self.distances = {}  # Distances from each star to its neighbours
        self.angles = {}  # Bearings between each star and its neighbours
        self.norm_dist = {}
        self.norm_ang = {}

    def calculate_new_coordinates(self, ra, de, pm_ra, pm_de, ybp):
        # Calculates new positions of stars from their proper motions
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

    # get all stars
    def chop(self, line):
        choppedline = []
        list_with_space = line.rsplit('|')
        for item in list_with_space:
            choppedline.append(item.strip())    # Removes whitepsaces (?)
        return choppedline

    # Function to calculate angular distance between stars
    def calculate_angular_distance(self, active_entry, target_entry):  # Takes HIP IDs as input

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

    def createMap(self):
        self.hip = open('hip_main.dat')  # The HIP catalogue
        # self.hip = open('hip_test.dat')
        lines = self.hip.readlines()  # Puts every line of the catalog in an list item

        for line in lines:
            # div by '|'
            chopdline = self.chop(line)
            try:
                newstar = {}
                newstar['hip'] = int(chopdline[1])
                newstar['mag'] = float(chopdline[5])
                newstar['ra'] = float(chopdline[8])
                newstar['de'] = float(chopdline[9])
                newstar['pm_ra'] = float(chopdline[12]) * self.DEG_PER_MAS
                newstar['pm_de'] = float(chopdline[13]) * self.DEG_PER_MAS
                newstar['cal_ra'], newstar['cal_de'] = self.calculate_new_coordinates(newstar['ra'], newstar['de'], newstar['pm_ra'],
                                                                                      newstar['pm_de'], self.ybp)

                # Checks if star is visible at position and due to brightness. Otherwise skips it.
                if newstar['cal_de'] > self.dec_limit and newstar['mag'] <= self.mag_limit:
                    # Adds dictionary items
                    self.stars.append(newstar)

            except ValueError:
                # data missing
                pass

        self.hip = None

        # Creates an empty dictionary of dictionaries since creating nested entries from scratch seems to be impossible.
        for i in self.stars:
            self.distances[f"{i['hip']}"] = {}
            self.angles[f"{i['hip']}"] = {}

        for a in self.stars:
            active_hip = f"{a['hip']}"
            for t in self.stars:
                target_hip = f"{t['hip']}"
                # Checks if the calculation has already been done in reverse
                if target_hip in self.distances and active_hip in self.distances[target_hip]:
                    pass
                elif (a != t):  # Avoids calculating distances of 0
                    ang = self.calculate_angular_distance(a, t)
                    self.distances[active_hip][target_hip] = self.distances[target_hip][active_hip] = ang

        # Sorts the distances and removes all but the closest (number defined above as "neighbours")
        for a in self.distances:
            self.distances[a] = {k: v for k, v in sorted(self.distances[a].items(), key=lambda item: item[1])}
            del_list = list(self.distances[a].keys())[self.neighbours:]
            for i in del_list:
                del self.distances[a][i]

        # Normalizes all distances by setting the closest one as 1 and dividing the others by its value
        for i in self.distances:
            self.norm_dist[i] = {}
            for d in self.distances[i]:
                self.norm_dist[i][d] = {}
                divisor = self.distances[i][d]
                for x in self.distances[i]:
                    normalized = self.distances[i][x] / divisor
                    self.norm_dist[i][d][x] = normalized

        # Calculates bearings between stars
        for master in self.stars:
            active_hip = f"{master['hip']}"
            for t in self.distances[active_hip]:
                target = next(item for item in self.stars if item["hip"] == int(t))
                m_ra = m.radians(master['cal_ra'])
                m_dec = m.radians(master['cal_de'])
                t_ra = m.radians(target['cal_ra'])
                t_dec = m.radians(target['cal_de'])
                x = m.cos(t_dec) * m.sin(t_ra - m_ra)
                y = m.cos(m_dec) * m.sin(t_dec) - m.sin(m_dec) * m.cos(t_dec) * m.cos(t_ra - m_ra)
                ang = m.degrees(m.atan2(x, y))
                self.angles[active_hip][t] = -ang

        # Calculates angle between a star, its closest neighbour and every other star, based on their bearings
        for i in self.angles:
            self.norm_ang[i] = {}
            for s in self.angles[i]:
                self.norm_ang[i][s] = {}
                secondary = self.angles[i][s]
                for x in self.angles[i]:
                    normalized = secondary - self.angles[i][x]
                    if normalized > 180:
                        normalized = normalized - 360
                    elif normalized < -180:
                        normalized += 360
                    self.norm_ang[i][s][x] = normalized
