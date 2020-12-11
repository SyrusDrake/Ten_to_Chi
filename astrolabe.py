import math as m

class Astrobale:

    def __init__(self, user_map, starmap):
        self.matches = {}
        self.norma_markers = {}
        # debug = open("debug.txt", "w+")
        self.star_distances = starmap.distances
        self.star_angles = starmap.angles
        self.normd_star = starmap.norm_dist
        self.norma_star = starmap.norm_ang
        self.markers = user_map

    def calculate_marker_distances(self):
        marker_distances = {}
        x1 = self.markers[list(self.markers.keys())[0]]['x']
        y1 = self.markers[list(self.markers.keys())[0]]['y']
        for point in self.markers:  # Goes through all markers except the first
            x2 = self.markers[point]['x']
            y2 = self.markers[point]['y']
            ID = point
            dis = m.sqrt((x2-x1)**2+(y2-y1)**2)  # calculates the distances
            if dis == 0:
                pass
            else:
                marker_distances[ID] = dis
        marker_distances = {k: v for k, v in sorted(marker_distances.items(), key=lambda item: item[1])}  # sorts the dictionary entries by value

        self.normd_markers = {}
        ref_values = list(marker_distances.values())[0]  # Takes the first entry in the list of values
        for i in marker_distances:  # Iterates through the entire list and divides all values by the chosen reference values.
            self.normd_markers[i] = (marker_distances[i]/ref_values)

    def calculate_marker_bearings(self):
        bearings = {}
        x1 = self.markers['1']['x']
        y1 = self.markers['1']['y']

        for i in range(2, len(self.markers)+1):
            x2 = self.markers[str(i)]['x']
            y2 = self.markers[str(i)]['y']
            ang = 180-m.degrees(m.atan2(x2-x1, y2-y1))
            bearings[str(i)] = ang

        temp_dict = {}
        b1 = bearings[list(self.normd_markers)[0]]  # uses nearest neighbour as "normalizer" for bearings
        temp_dict[list(self.normd_markers)[0]] = 0.0
        del bearings[list(self.normd_markers)[0]]  # removes "normalizer" from bearings list so it isn't used again

        # Calculates angles between markers based on their bearings
        for i in bearings:
            b2 = bearings[i]
            ang = b1 - b2
            if ang > 180:
                ang = ang-360
            elif ang < -180:
                ang += 360
            temp_dict[i] = ang

        # Sorts the normalized angles not on their values but on the values of the distances
        for k in list(self.normd_markers.keys()):
            self.norma_markers[k] = temp_dict[k]

    def calculate(self):

        for a in self.normd_star:
            for n in self.normd_star[a]:
                mid = f'{a}-{n}'
                self.matches[mid] = {}
                self.matches[mid]['Matches'] = 0
                self.matches[mid]['Diff_d'] = 0
                self.matches[mid]['Diff_a'] = 0
                for t in self.normd_star[a][n]:
                    compd_star = self.normd_star[a][n][t]
                    compa_star = self.norma_star[a][n][t]
                    for i in list(self.normd_markers.keys())[1:]:
                        compd_markers = self.normd_markers[i]
                        compa_markers = self.norma_markers[i]
                        diff_d = compd_star-compd_markers
                        diff_a = compa_star-compa_markers

                        if abs(diff_d) < 0.40 and abs(diff_a) < 3:
                            if self.matches[mid]['Matches'] == 0:
                                # self.debug.write(f'Master: {a}, Normalizer: {n}, Target: {t}, Difference distance: {diff_d}, Difference angle: {diff_a}, Marker: {i}\r\n')
                                self.matches[mid]['Matches'] += 1
                                self.matches[mid]['Diff_d'] += abs(diff_d)
                                self.matches[mid]['Diff_a'] += abs(diff_a)
                                self.matches[mid]['Marker 1'] = a
                                self.matches[mid][f'Marker {list(self.normd_markers.keys())[0]}'] = n
                                self.matches[mid][f'Marker {i}'] = t
                            elif f'Marker {i}' not in list(self.matches[mid].keys()):
                                # debug.write(f'Master: {a}, Normalizer: {n}, Target: {t}, Difference distance: {diff_d}, Difference angle: {diff_a}, Marker: {i}\r\n')
                                self.matches[mid]['Matches'] += 1
                                self.matches[mid]['Diff_d'] += abs(diff_d)
                                self.matches[mid]['Diff_a'] += abs(diff_a)
                                self.matches[mid][f'Marker {i}'] = t

        for k, v in list(self.matches.items()):
            if v['Matches'] < len(list(self.normd_markers))-1:
                del self.matches[k]

        self.sort_dist = {k: v for k, v in sorted(self.matches.items(), key=lambda item: item[1]['Diff_d'])}
        self.sort_ang = {k: v for k, v in sorted(self.matches.items(), key=lambda item: item[1]['Diff_a'])}

        del_list = list(self.sort_dist.keys())[30:]

        for i in del_list:
            del self.sort_dist[i]

        del_list = list(self.sort_ang.keys())[30:]

        for i in del_list:
            del self.sort_ang[i]

        print("Sorted by distance-deviation--------------")
        for i in self.sort_dist:
            print(self.sort_dist[i])

        print("Sorted by angle-deviation--------------")
        for i in self.sort_ang:
            print(self.sort_ang[i])

        print("In both--------------")
        for i in self.sort_dist:
            if i in self.sort_ang:
                print(self.sort_dist[i])
