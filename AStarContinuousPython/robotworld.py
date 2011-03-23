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
from player import Player
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
        self.__setupMainAgent()
        self.__setupNPC()
        self.__setupCamera()
        #Many things within the NPC are dependant on the level it is in.
#        self.__NPC.setKeyAndNestReference(self.keyNest1, self.room1Key)
#        self.__room2NPC.setKeyAndNestReference(self.keyNest2, self.room2Key)
        #self.__room2NPC.handleTransition("playerLeftRoom")
#        self.__room3NPC.setKeyAndNestReference(self.keyNest3, self.room3Key)
        #self.__room3NPC.handleTransition("playerLeftRoom")
        self.__setupTasks()
        
        self.setKeymap()
        self.room1Key = "models/blueKeyHUD.png"
        self.__mainAgent.setCurrentKey(self.room1Key)
        self.__NPC.pathSmoothening = self.pathSmoothening

        if(self.showWaypoints):
            print("Showing waypoints")
            for w in self.room1waypoints:
                w.draw()
            for w in self.room2waypoints:
                w.draw()
            for w in self.room3waypoints:
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
        size = 200
        cm.setFrame(-size, size, -size, size)
        environment = render.attachNewNode(cm.generate())
        environment.lookAt(0, 0, -1)
        environment.setPos(100, -100, 0)
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
        Some notes and caveats: Each time you add a room, make sure that you tag it with key "Room" and value "<room number>".
        This is so our A* algorithm can do clear path detection on only the rooms, not anything else.
        """
        level1 = render.attachNewNode("level 1 node path")
        
        execfile("rooms/room1.py")

        self.room1 = loader.loadModel("rooms/room1")
        self.room1.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        self.room1.setScale(10)
        self.room1.setTexScale(TextureStage.getDefault(), 10)
        self.room1.reparentTo(render)
        self.room1.find("**/Cube*;+h").setTag("Room", "1")

        keyNest = loader.loadModel("models/nest")
        keyNest.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        keyNest.setScale(0.5)
        keyNest.setTexScale(TextureStage.getDefault(), 0.1)
        
        #self.setWaypoints("room2")
        self.room2waypoints = None
        execfile("rooms/room2.py")

        self.room2 = loader.loadModel("rooms/room2")
        self.room2.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        self.room2.setScale(10)
        self.room2.setTexScale(TextureStage.getDefault(), 10)
        self.room2.reparentTo(level1)
        self.room2.setY(self.room1, -20)
        self.room2.find("**/Cube*;+h").setTag("Room", "2")
                
        execfile("rooms/room3.py")
        
        room3Model = loader.loadModel("rooms/room3")
        room3Model.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        room3Model.setH(90)
        room3Model.setP(180)
        room3Model.setZ(2)
        self.room3 = level1.attachNewNode("room 3")
        room3Model.reparentTo(self.room3)
        self.room3.setScale(10)
        self.room3.setTexScale(TextureStage.getDefault(), 10)
        self.room3.reparentTo(level1)
        self.room3.setX(self.room1, 20)
        self.room3.find("**/Cube*;+h").setTag("Room", "3")
                                                
        room2Floor = self.room2.attachNewNode(CollisionNode("room2Floor"))
        room2Floor.node().addSolid(CollisionPolygon(Point3(9,-9,0), Point3(9,9,0),
                                                Point3(-9,9,0), Point3(-9,-9,0)))

                                                

        
        gate = loader.loadModel("models/box")
        
        gateTo2 = self.room1.attachNewNode("gateTo2")
        gate.instanceTo(gateTo2)
        gateTo2.setPos(8, -10, 0)
        gateTo2.hide()
        
        gateTo3 = self.room1.attachNewNode("gateTo3")
        gate.instanceTo(gateTo3)
        gateTo3.setPos(10, 8, 0)
        gateTo3.hide()
        
        self.physicsCollisionHandler.addInPattern("%fn-into-%in")
        self.physicsCollisionHandler.addOutPattern("%fn-out-%in")
        
    
        
        def orderNPC(parameters, entry):
            self.__NPC.start()#self.__NPC.handleTransition("start")
        
        self.accept("target collision node-into-room1Floor", orderNPC, ["target has entered room 1"])
        self.accept("target collision node-into-room2Floor", orderNPC, ["target has entered room 2"])
        self.accept("target collision node-into-room3Floor", orderNPC, ["target has entered room 3"])
#        self.accept("ralph collision node-out-room3Floor", orderNPC, ["ralph has left room 3"])
#        self.accept("Eve 1 collision node-into-Cube1", orderNPC, ["NPC1 bumped into wall"])
#        self.accept("Eve 2 collision node-into-Cube2", orderNPC, ["NPC2 bumped into wall"])
#        self.accept("Eve 3 collision node-into-Cube3", orderNPC, ["NPC3 bumped into wall"])
        

        #messenger.toggleVerbose()
        self.gate = gate
        

    __globalAgentList = []
    __mainAgent = None
    def __setupMainAgent(self):
        modelStanding = "models/ralph"
        modelRunning = "models/ralph-run"
        modelWalking = "models/ralph-walk"
        self.__mainAgent = Player(modelStanding, 
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
        self.__mainAgent.reparentTo(render)
        self.__mainAgent.setPos(-20, -210, 0)
        self.gate.find("**/Cube;+h").setCollideMask(~self.__mainAgent.collisionMask)
        
    __targetCount = 0
    __targets = []
    __agentToTargetMap = {}
    def __setupNPC(self):
        # This is to support the collisions for each node. See the paragraph comment
        # above where we modify the npc's collision node
#        playerCollisionNP = self.__mainAgent.find("* collision node")

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
                                waypoints = self.room2waypoints)
        self.__NPC.setFluidPos(render, 20, -190, 0)
        self.__NPC.setScale(render, 1)
        self.__NPC.setMainTarget(self.__mainAgent)

        self.__NPC.reparentTo(render)
    
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
    
    def cameraRoom1Pos(self):
        base.camera.reparentTo(render)
        #This camera position shows room1
        base.camera.setPos(0,0, 350) #This is debug camera position.
        base.camera.lookAt(0,0,0)        
        
    def cameraRoom2Pos(self):
        base.camera.reparentTo(render)
        #This camera position shows room2
        base.camera.setPos(0,-200, 350) #This is debug camera position.
        base.camera.lookAt(0,-200,0)    
        
    def cameraRoom3Pos(self):
        base.camera.reparentTo(render)
        #This camera position shows room3
        base.camera.setPos(200,0, 350) #This is debug camera position.
        base.camera.lookAt(200,0,0)
        
    def cameraRegularPos(self):        
        base.camera.reparentTo(self.__NPC.actor)
        base.camera.setPos(0, 60, 60)
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
                for w in self.room1waypoints:
                    w.draw()
                for w in self.room2waypoints:
                    w.draw()
                for w in self.room3waypoints:
                    w.draw()
            else:
                print("Hiding waypoints")
                for w in self.room1waypoints:
                    w.erase()
                for w in self.room2waypoints:
                    w.erase()
                for w in self.room3waypoints:
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
        self.accept("1", self.cameraRoom1Pos)
        self.accept("2", self.cameraRoom2Pos)
        self.accept("3", self.cameraRoom3Pos)
        self.accept("4", self.cameraRegularPos)
        
    
if __name__ == "__main__":
    w = World()
    
    run()
    print("World compiled correctly")
