#Gotta love the magic numbers!
coords = [ (-15,45),
        (9,63),
        (27,42),
        (5,25),
        (43, 25),
        (61, 3),
        (38, -12),
        (21, 5),
        (10, -35),
        (-8, -52),
        (-25, -34),
        (-5, -16),
        (-43, -14),
        (-61, 5),
        (-39, 23),
        (-22, 4),
        ]
        
self.room1waypoints = room1waypoints = []
for i in range(len(coords)):
    coord = coords[i]
    waypoint = Waypoint(Vec3(coord[0], coord[1], 0.5), i)
    self.room1waypoints.append(waypoint)


self.room1waypoints[0].setNeighbors([self.room1waypoints[1], self.room1waypoints[3], self.room1waypoints[11],
                                self.room1waypoints[14], self.room1waypoints[15]])
self.room1waypoints[1].setNeighbors([self.room1waypoints[0], self.room1waypoints[2]])
self.room1waypoints[2].setNeighbors([self.room1waypoints[1], self.room1waypoints[3], self.room1waypoints[4],
                                self.room1waypoints[7], self.room1waypoints[11]])
self.room1waypoints[3].setNeighbors([self.room1waypoints[0], self.room1waypoints[2], self.room1waypoints[4],
                                self.room1waypoints[7], self.room1waypoints[8], self.room1waypoints[10],
                                self.room1waypoints[11], self.room1waypoints[14], self.room1waypoints[15]])

self.room1waypoints[4].setNeighbors([self.room1waypoints[2], self.room1waypoints[3], self.room1waypoints[5],
                                self.room1waypoints[7], self.room1waypoints[15]])
self.room1waypoints[5].setNeighbors([self.room1waypoints[4], self.room1waypoints[6]])
self.room1waypoints[6].setNeighbors([self.room1waypoints[5], self.room1waypoints[7], self.room1waypoints[8],
                                self.room1waypoints[11], self.room1waypoints[15]])
self.room1waypoints[7].setNeighbors([self.room1waypoints[2], self.room1waypoints[3], self.room1waypoints[4],
                                self.room1waypoints[6], self.room1waypoints[8], self.room1waypoints[11],
                                self.room1waypoints[12], self.room1waypoints[14], self.room1waypoints[15]])

self.room1waypoints[8].setNeighbors([self.room1waypoints[3], self.room1waypoints[6], self.room1waypoints[7],
                                self.room1waypoints[9], self.room1waypoints[11]])
self.room1waypoints[9].setNeighbors([self.room1waypoints[8], self.room1waypoints[10]])
self.room1waypoints[10].setNeighbors([self.room1waypoints[3], self.room1waypoints[9], self.room1waypoints[11],
                                self.room1waypoints[12], self.room1waypoints[15]])
self.room1waypoints[11].setNeighbors([self.room1waypoints[0], self.room1waypoints[2], self.room1waypoints[3],
                                self.room1waypoints[6], self.room1waypoints[7], self.room1waypoints[8],
                                self.room1waypoints[10], self.room1waypoints[12], self.room1waypoints[15]])

self.room1waypoints[12].setNeighbors([self.room1waypoints[7], self.room1waypoints[10], self.room1waypoints[11],
                                self.room1waypoints[13], self.room1waypoints[15]])
self.room1waypoints[13].setNeighbors([self.room1waypoints[12], self.room1waypoints[14]])
self.room1waypoints[14].setNeighbors([self.room1waypoints[0], self.room1waypoints[3], self.room1waypoints[7],
                                self.room1waypoints[13], self.room1waypoints[15]])
self.room1waypoints[15].setNeighbors([self.room1waypoints[0], self.room1waypoints[3], self.room1waypoints[4],
                                self.room1waypoints[6], self.room1waypoints[7], self.room1waypoints[10],
                                self.room1waypoints[11], self.room1waypoints[12], self.room1waypoints[14]])


