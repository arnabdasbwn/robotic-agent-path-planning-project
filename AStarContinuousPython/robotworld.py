# from the file character.py, import the class character
#include character.py
#from pandac.PandaModules import loadPrcFileData
#loadPrcFileData("", "fullscreen 1")
#loadPrcFileData("", "win-size 1024 768")
import direct.directbase.DirectStart
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import BitMask32
from pandac.PandaModules import CardMaker
from pandac.PandaModules import CollisionHandlerEvent
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionPolygon
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import ForceNode
from pandac.PandaModules import LinearVectorForce
from pandac.PandaModules import LineSegs
from pandac.PandaModules import NodePath
from pandac.PandaModules import PhysicsCollisionHandler
from pandac.PandaModules import Point3
from pandac.PandaModules import TexGenAttrib
from pandac.PandaModules import TextNode
from pandac.PandaModules import Texture
from pandac.PandaModules import TextureStage
from pandac.PandaModules import TransparencyAttrib
from pandac.PandaModules import Vec3
from npc import NPC
import sys
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
##from neural_network import NeuralNetwork
from waypoint import Waypoint
from pathFinder import PathFinder
from tasktimer import taskTimer
from direct.gui.DirectEntry import DirectEntry
import random

class World(DirectObject):     
    def __init__(self):
        DirectObject.__init__(self)
        
        self.pathSmoothening = False
        self.showWaypoints = True
        self.showCollisions = False
        
        self.accept("escape", sys.exit)
        
        self.__setupEnvironment()
        self.__setupCollisions()
        self.__setupGravity()
        self.__setupLevel()
        self.__setupTarget()
        self.__setupNPC()
        self.__setupCamera()
        self.__setupTasks()
        
        self.setKeymap()
        self.__NPC.pathSmoothening = self.pathSmoothening

        if(self.showWaypoints):
            print("Showing waypoints")
            for w in self.roomWaypoints:
                w.draw()
        

    def __setupCollisions(self):
        self.cTrav = CollisionTraverser("traverser")
        base.cTrav = self.cTrav
        
        self.physicsCollisionHandler = PhysicsCollisionHandler()
        self.physicsCollisionHandler.setDynamicFrictionCoef(0.5)
        self.physicsCollisionHandler.setStaticFrictionCoef(0.7)

    def __setupGravity(self):
        base.particlesEnabled = True
        base.enableParticles()
        
        gravityFN=ForceNode('world-forces')
        gravityFNP=render.attachNewNode(gravityFN)
        gravityForce=LinearVectorForce(0,0,-6) #gravity acceleration ft/s^2
        gravityFN.addForce(gravityForce)

        base.physicsMgr.addLinearForce(gravityForce)

    def __setupEnvironment(self):
        cm = CardMaker("ground")
	size = 100
        cm.setFrame(-size, size, -size, size)
        environment = render.attachNewNode(cm.generate())
        environment.lookAt(0, 0, -1)
        environment.setPos(0, 0, 0)
        environment.setCollideMask(BitMask32.allOn())
        environment.reparentTo(render)
        
        texture = loader.loadTexture("textures/ground.png")
        
        # This is so the textures can look better from a distance
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        
        environment.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition) 
        environment.setTexScale(TextureStage.getDefault(), 0.02, 0.02)
        environment.setTexture(texture, 1)

            
    def __setupLevel(self):
        """
        Originally planned to have multiple levels, that never happened.
        """
        level1 = render.attachNewNode("level 1 node path")
        
        execfile("rooms/room.py")

        self.room = loader.loadModel("rooms/room")
        self.room.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        self.room.setScale(10)
        self.room.setTexScale(TextureStage.getDefault(), 10)
        self.room.reparentTo(render)
        self.room.find("**/Cube;+h").setTag("Room", "1")
        
        gate = loader.loadModel("models/box")
        
        gateTo2 = self.room.attachNewNode("gateTo2")
        gate.instanceTo(gateTo2)
        gateTo2.setPos(8, -10, 0)
        gateTo2.hide()
        
        self.physicsCollisionHandler.addInPattern("%fn-into-%in")
        self.physicsCollisionHandler.addOutPattern("%fn-out-%in")

        #messenger.toggleVerbose()
        self.gate = gate
        

    __globalAgentList = []
    __mainTarget = None
    def __setupTarget(self):
        modelStanding = "models/ralph"
        modelRunning = "models/ralph-run"
        modelWalking = "models/ralph-walk"
        self.__mainTarget = NPC(modelStanding, 
                            {"run":modelRunning, "walk":modelWalking},
                            turnRate = 150, 
                            speed = 0,
                            agentList = self.__globalAgentList,
                            collisionMask = BitMask32.bit(1),
                            name="target",
                            massKg = 35.0,
                            collisionHandler = self.physicsCollisionHandler,
                            collisionTraverser = self.cTrav)
        # Make it visible
        self.__mainTarget.reparentTo(render)
        self.__mainTarget.setPos(-20, -10, 0)#-210
        self.gate.find("**/Cube;+h").setCollideMask(~self.__mainTarget.collisionMask)
        
    __targetCount = 0
    __targets = []
    __agentToTargetMap = {}
    def __setupNPC(self):
        # This is to support the collisions for each node. See the paragraph comment
        # above where we modify the npc's collision node
#        playerCollisionNP = self.__mainTarget.find("* collision node")

        modelStanding = "models/ralph"
        modelRunning = "models/ralph-run"
        modelWalking = "models/ralph-walk"
        self.__NPC = NPC(modelStanding, 
                                {"run":modelRunning, "walk":modelWalking},
                                turnRate = 150, 
                                speed = 15,
                                agentList = self.__globalAgentList,
                                name = "Ralph",
                                collisionMask = BitMask32.bit(3),
                                rangeFinderCount = 13,
                                adjacencySensorThreshold = 5,
                                radarSlices = 5,
                                radarLength = 0,
                                scale = 1.0,
                                massKg = 35.0,
                                collisionHandler = self.physicsCollisionHandler,
                                collisionTraverser = self.cTrav,
                                waypoints = self.roomWaypoints)
        self.__NPC.setFluidPos(render, 20, 10, 0)#-190
        self.__NPC.setScale(render, 1)
        self.__NPC.setTarget(self.__mainTarget)

        self.__NPC.reparentTo(render)
	self.__NPC.start()
    
    def __setupTasks(self):
        """
        This function sets up all the tasks used in the world
        """
        taskMgr.add(taskTimer, "taskTimer")
        taskMgr.add(self.__NPC.act, "actTask")

    def __setupCamera(self):
        #This camera position shows the whole level
        base.camera.setPos(100,-100, 795) #This is debug camera position.
        base.camera.lookAt(100,-100,0)
        base.disableMouse()
        base.camera.reparentTo(self.__NPC.actor)
        base.camera.setPos(0, 60, 200)
        base.camera.lookAt(self.__NPC)
        base.camera.setP(base.camera.getP() + 10)
    
    def cameraViewRoomPos(self):
        base.camera.reparentTo(render)
        #This camera position shows entire room at once
        base.camera.setPos(0,0, 300) #This is debug camera position.
        base.camera.lookAt(0,0,0)        

    def cameraRegularPos(self):        
        base.camera.reparentTo(self.__NPC.actor)
        base.camera.setPos(0, 60, 200)
        base.camera.lookAt(self.__NPC)
        base.camera.setP(base.camera.getP() + 10)
        
    positionHeadingText = OnscreenText(text="", style=1, fg=(1,1,1,1),
                   pos=(-1.3,-0.95), align=TextNode.ALeft, scale = .05, mayChange = True)
                
    __keyMap = {"enablePathSmoothening":False,
        "showWaypoints":False}

    def setKeymap(self):
        def toggleWaypoints(key):
            self.showWaypoints = not self.showWaypoints
            if(self.showWaypoints):
                print("Showing waypoints")
                for w in self.roomWaypoints:
                    w.draw()
            else:
                print("Hiding waypoints")
                for w in self.roomWaypoints:
                    w.erase()
        
        def togglePathSmoothening(key):
            self.__NPC.togglePathSmoothening()
            
        def toggleCollisions(key):
            if(self.showCollisions):
                base.cTrav.showCollisions(render)
            else:
                base.cTrav.hideCollisions()

            self.showCollisions = not self.showCollisions
            print("showCollisions = " + str(self.showCollisions))
            
        self.accept("p",              togglePathSmoothening, ["togglePathSmoothening"])
        self.accept("w",              toggleWaypoints, ["toggleWaypoints"])
        self.accept("c",              toggleCollisions, ["toggleCollisions"])
        self.accept("1", self.cameraRegularPos)
        self.accept("2", self.cameraViewRoomPos)
        
    
if __name__ == "__main__":
    w = World()
    
    run()
    print("World compiled correctly")
