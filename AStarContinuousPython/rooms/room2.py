coords = [ (-75,-135),
         (-55,-135),
         (-5,-145),
         (45,-145),
         (45,-165),
         (55,-135),
         (75,-135),
         (75,-275),
         (55,-275),
         (5,-265),
         (-15,-265),
         (-75,-200),
        ]
        
self.room2waypoints = room2waypoints = []
for i in range(len(coords)):
    coord = coords[i]
    room2waypoint = Waypoint(Vec3(coord[0], coord[1], 0.5), i)
    self.room2waypoints.append(room2waypoint)


self.room2waypoints[0].setNeighbors([self.room2waypoints[11], self.room2waypoints[1]])
self.room2waypoints[1].setNeighbors([self.room2waypoints[0], self.room2waypoints[2]])
self.room2waypoints[2].setNeighbors([self.room2waypoints[1], self.room2waypoints[3]])
self.room2waypoints[3].setNeighbors([self.room2waypoints[2], self.room2waypoints[4], self.room2waypoints[5]])
self.room2waypoints[4].setNeighbors([self.room2waypoints[3], self.room2waypoints[5]])
self.room2waypoints[5].setNeighbors([self.room2waypoints[3], self.room2waypoints[4], self.room2waypoints[6]])
self.room2waypoints[6].setNeighbors([self.room2waypoints[5], self.room2waypoints[7]])
self.room2waypoints[7].setNeighbors([self.room2waypoints[6], self.room2waypoints[8]])
self.room2waypoints[8].setNeighbors([self.room2waypoints[7], self.room2waypoints[9]])
self.room2waypoints[9].setNeighbors([self.room2waypoints[8], self.room2waypoints[10]])
self.room2waypoints[10].setNeighbors([self.room2waypoints[9], self.room2waypoints[11]])
self.room2waypoints[11].setNeighbors([self.room2waypoints[10], self.room2waypoints[0]])

