from agent import Agent
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import Vec3
from pandac.PandaModules import Vec2
from pandac.PandaModules import BitMask32
from pandac.PandaModules import LineSegs
from pandac.PandaModules import NodePath
from pandac.PandaModules import TextNode
from pandac.PandaModules import TextureStage
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
import random
import math
from math import sqrt
from waypoint import Waypoint
from pathFinder import PathFinder
from tasktimer import taskTimer
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import CollisionHandlerEvent
        
class NPC(Agent, DirectObject):
    collisionCount = 0
    npcState = None
    def __init__(self, 
                modelStanding, 
                modelAnimationDict, 
                turnRate, 
                speed, 
                agentList, 
                name = "",
                rangeFinderCount = 13,
                collisionMask=BitMask32.allOff(),
                adjacencySensorThreshold = 0,
                radarSlices = 0,
                radarLength = 0.0,
                scale = 1.0,
                brain = None,
                massKg = 0.1,
                collisionHandler = None,
                collisionTraverser = None,
                waypoints = None):
        Agent.__init__(self, modelStanding, modelAnimationDict, turnRate, speed, agentList, massKg, collisionMask, name, collisionHandler, collisionTraverser)
        self.collisionMask = collisionMask
        self.adjacencySensorThreshold = adjacencySensorThreshold
        self.radarSlices = radarSlices
        self.radarLength = radarLength
        self.scale = scale
        self.brain = brain
        self.npcState = "retriveKey"
        self.waypoints = waypoints
	self.targetReached = False
        self.setScale(self.scale)
        self.currentTarget = None
        self.player = None
        self.bestPath = None
        self.key = None
        self.keyInHand = False
        self.hasFallen = False
        self.pathSmoothening = True

            
    def togglePathSmoothening(self, value = None):
        if(value == True):
            self.pathSmoothening = value
        elif(value == False):
            self.pathSmoothening = value
        else:#Welcome to Quantum Computing!! LOL!
            self.pathSmoothening = not self.pathSmoothening
            
    isMoving = False
    def act(self, task):
        if(not self.hasFallen):
            if(self.getZ() < -100):
                print(self.name + "Says: Aieee! I've fallen through the floor!! I'm at " + str(self.getPos()))
                self.hasFallen = True
        #HACK!
        if(self.getZ(render) < -0.5):
            self.setZ(render, 0.1)
        pushAmount = 0.4
        pushArea = 88 #Distance from center of room to begin pushing
        if(self.name == "target"):
            if self.getX(render) > pushArea:
                self.setX(render, pushArea)
            if self.getX(render) < -pushArea:
                self.setX(render, -pushArea)
            if self.getY(render) > pushArea:
                self.setY(render, pushArea)
            if self.getY(render) < -pushArea:
                self.setY(render, -pushArea)
            
        if self.bestPath:
            self.followBestPath()
        if self.npcState == "seek":
            if self.currentTarget:
                self.seek(self.currentTarget.getPos(render))
        elif self.npcState == "retriveKey":
            if self.currentTarget:
                self.seek(self.currentTarget.getPos(render))
            if self.distanceToPlayer() < 5:#If collided with Player
                self.targetReached = True
        return Task.cont

    def setTarget(self, mainTarget):
        self.mainTarget = mainTarget
        
    def start(self):
	self.bestPath = PathFinder.AStar(self, self.mainTarget, self.waypoints)
                
    def drawBestPath(self):
        if self.bestPath != None:
            ls = LineSegs()
            ls.setThickness(10.0)
            for i in range(len(self.bestPath) - 1):
                ls.setColor(0,0,1,1)
                ls.moveTo(self.bestPath[i].getPos())
                ls.drawTo(self.bestPath[i+1].getPos())
                np = NodePath(ls.create("aoeu"))
                np.reparentTo(render)
                
    def distanceToPlayer(self):
        return self.getDistance(self.mainTarget)
    
    def followBestPath(self):
        """ 
        This function tells the NPC to continue following the best path 
        
        Basically, it checks the currentTarget to determine if we're already seeking to the correct waypoint.
        When we finally reach the currentTarget, we pop it off the bestPath list and set the currentTarget
        to the next waypoint in bestPath.
        
        At this point, we also need to re-run AStar from our new currentTarget to the destination, which is
        bestPath[-1]. We store as our new bestPath and continue from there.
        """

        assert self.bestPath, "self.bestPath must be valid before calling followBestPath"
        
        if self.currentTarget is not self.bestPath[0]:
            self.currentTarget = self.bestPath[0]
        
        #Comment out next two lines to disable path smoothening.
        if(self.pathSmoothening):
            #attempting to smoothen path
            #print("Checking if there is a clear path to next target")
            while(len(self.bestPath) > 1 and PathFinder.waypointIsReachable(self, self.bestPath[1])):
                #print("Next waypoint is reachable, skipping to next")
                self.bestPath.pop(0)
                self.currentTarget = self.bestPath[0]
        # have we reached our currentTarget?
        if PathFinder.distance(self, self.currentTarget) < 2: #This number must be greater than distance in seek()
            assert self.currentTarget == self.bestPath.pop(0), "We've reached our currentTarget, but it's not in our bestPath"
            # Are there any waypoints left to follow?
            if self.bestPath:
                self.currentTarget = self.bestPath[0]
            if len(self.bestPath) > 1:
                self.bestPath = PathFinder.AStar(self.bestPath[0], self.bestPath[-1], self.waypoints)


    def seek(self, position):
        worldPosition = self.getPos(render)
        worldTargetPosition = position
        worldHeading = self.getH(render)
        worldHeading = worldHeading % 360
        worldYDirection = worldTargetPosition.getY() - worldPosition.getY()
        worldXDirection = worldTargetPosition.getX() - worldPosition.getX()
        worldDirectionToTarget = math.degrees(math.atan2(worldYDirection, worldXDirection))
        distanceToTarget = math.hypot(worldYDirection, worldXDirection)
        angleToTarget = worldDirectionToTarget - worldHeading + 180
        angleToTarget = angleToTarget % 360
        turnAngle = self.turnRate * taskTimer.elapsedTime
        distance = self.speed * taskTimer.elapsedTime
        
        if(not self.targetReached):
            if not self.isMoving:
                self.loop("run")
                self.isMoving = True
            if(60 <= angleToTarget <= 150):
                self.moveForward(distance)
            if(0 <= angleToTarget < 90):
                self.turnRight(turnAngle)
            elif(90 <= angleToTarget < 180):
                self.turnLeft(turnAngle)
            elif(180 <= angleToTarget < 270):
                self.turnLeft(turnAngle)
            elif(270 <= angleToTarget < 360):
                self.turnRight(turnAngle)
            #else:
            #    print("You can start crying now.")
        else:
            if self.isMoving:
                self.stop()
                self.pose("walk", 5)
                self.isMoving = False
        return

if __name__ == "__main__":
    N = NPC("models/ralph",
            {"run":"models/ralph-run"},
            turnRate = 5,
            speed = 100,
            agentList = [])
    print ("compiled good")
    
