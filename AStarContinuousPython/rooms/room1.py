coords = [ (-75,65),
         (-55,65),
         (-5, 55),
         (45, 55),
         (45, 35),
         (55, 65),
         (75, 65),
         (75, -75),
         (55, -75),
         (5,  -65),
         (-15,-65),
         (-75,  0),
        ]
        
self.room1waypoints = room1waypoints = []
for i in range(len(coords)):
    coord = coords[i]
    room1waypoint = Waypoint(Vec3(coord[0], coord[1], 0.5), i)
    self.room1waypoints.append(room1waypoint)


self.room1waypoints[0].setNeighbors([self.room1waypoints[11], self.room1waypoints[1]])
self.room1waypoints[1].setNeighbors([self.room1waypoints[0], self.room1waypoints[2]])
self.room1waypoints[2].setNeighbors([self.room1waypoints[1], self.room1waypoints[3]])
self.room1waypoints[3].setNeighbors([self.room1waypoints[2], self.room1waypoints[4], self.room1waypoints[5]])
self.room1waypoints[4].setNeighbors([self.room1waypoints[3], self.room1waypoints[5]])
self.room1waypoints[5].setNeighbors([self.room1waypoints[3], self.room1waypoints[4], self.room1waypoints[6]])
self.room1waypoints[6].setNeighbors([self.room1waypoints[5], self.room1waypoints[7]])
self.room1waypoints[7].setNeighbors([self.room1waypoints[6], self.room1waypoints[8]])
self.room1waypoints[8].setNeighbors([self.room1waypoints[7], self.room1waypoints[9]])
self.room1waypoints[9].setNeighbors([self.room1waypoints[8], self.room1waypoints[10]])
self.room1waypoints[10].setNeighbors([self.room1waypoints[9], self.room1waypoints[11]])
self.room1waypoints[11].setNeighbors([self.room1waypoints[10], self.room1waypoints[0]])

