#!/usr/bin/python

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
        
        
self.roomWaypoints = roomWaypoints = []
for i in range(len(coords)):
    coord = coords[i]
    room1waypoint = Waypoint(Vec3(coord[0], coord[1], 0.5), i)
    self.roomWaypoints.append(room1waypoint)


self.roomWaypoints[0].setNeighbors([self.roomWaypoints[11], self.roomWaypoints[1]])
self.roomWaypoints[1].setNeighbors([self.roomWaypoints[0], self.roomWaypoints[2]])
self.roomWaypoints[2].setNeighbors([self.roomWaypoints[1], self.roomWaypoints[3]])
self.roomWaypoints[3].setNeighbors([self.roomWaypoints[2], self.roomWaypoints[4], self.roomWaypoints[5]])
self.roomWaypoints[4].setNeighbors([self.roomWaypoints[3], self.roomWaypoints[5]])
self.roomWaypoints[5].setNeighbors([self.roomWaypoints[3], self.roomWaypoints[4], self.roomWaypoints[6]])
self.roomWaypoints[6].setNeighbors([self.roomWaypoints[5], self.roomWaypoints[7]])
self.roomWaypoints[7].setNeighbors([self.roomWaypoints[6], self.roomWaypoints[8]])
self.roomWaypoints[8].setNeighbors([self.roomWaypoints[7], self.roomWaypoints[9]])
self.roomWaypoints[9].setNeighbors([self.roomWaypoints[8], self.roomWaypoints[10]])
self.roomWaypoints[10].setNeighbors([self.roomWaypoints[9], self.roomWaypoints[11]])
self.roomWaypoints[11].setNeighbors([self.roomWaypoints[10], self.roomWaypoints[0]])

