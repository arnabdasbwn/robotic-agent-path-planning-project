coords = [ (143, 72),
		 (144, 47),
		 (153, -75),
		 (136, -58),
		 (163, 43),
		 (266, 15),
		 (258, -5),
		 (243, -73)
        ]
        
self.room3waypoints = room3waypoints = []
for i in range(len(coords)):
    coord = coords[i]
    room3waypoint = Waypoint(Vec3(coord[0], coord[1], 0.5), i)
    self.room3waypoints.append(room3waypoint)


self.room3waypoints[0].setNeighbors([self.room3waypoints[1], self.room3waypoints[4], self.room3waypoints[5]])
self.room3waypoints[1].setNeighbors([self.room3waypoints[0], self.room3waypoints[3], self.room3waypoints[4]])
self.room3waypoints[2].setNeighbors([self.room3waypoints[3]])
self.room3waypoints[3].setNeighbors([self.room3waypoints[1], self.room3waypoints[2], self.room3waypoints[4]])
self.room3waypoints[4].setNeighbors([self.room3waypoints[0], self.room3waypoints[1], self.room3waypoints[3], self.room3waypoints[5]])
self.room3waypoints[5].setNeighbors([self.room3waypoints[0], self.room3waypoints[4], self.room3waypoints[6]])
self.room3waypoints[6].setNeighbors([self.room3waypoints[5], self.room3waypoints[7]])
self.room3waypoints[7].setNeighbors([self.room3waypoints[6]])
