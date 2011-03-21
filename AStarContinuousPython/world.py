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
        
        self.pathSmoothening = True
        self.showWaypoints = False
        self.showCollisions = False
        
        self.accept("escape", sys.exit)
        
        self.__setupEnvironment()
        self.__setupCollisions()
        self.__setupGravity()
        self.__setupLevel()
        self.__setupMainAgent()
#        self.__setupOtherAgents()
        self.__setupNPCs()
        self.__setupCamera()
        self.__setupRandomClutter()
        #Many things within the NPC are dependant on the level it is in.
        self.__room1NPC.setKeyAndNestReference(self.keyNest1, self.room1Key)
        self.__room2NPC.setKeyAndNestReference(self.keyNest2, self.room2Key)
        #self.__room2NPC.handleTransition("playerLeftRoom")
        self.__room3NPC.setKeyAndNestReference(self.keyNest3, self.room3Key)
        #self.__room3NPC.handleTransition("playerLeftRoom")
        self.__setupTasks()
        
        self.setKeymap()

        # This is for the HUD
        self.keyImages = {
              self.room1Key:"models/redKeyHUD.png",
              self.room2Key:"models/blueKeyHUD.png",
              self.room3Key:"models/greenKeyHUD.png" }
        self.room1KeyInHUD = False
        self.room2KeyInHUD = False
        self.room3KeyInHUD = False
        self.redKeyImage = OnscreenImage(image = self.keyImages[self.room1Key], pos = (0.9, 0, 0.9), scale = (0.0451, 0, 0.1))
        self.redKeyImage.setTransparency(TransparencyAttrib.MAlpha)
        self.redKeyImage.hide()
        self.blueKeyImage = OnscreenImage(image = self.keyImages[self.room2Key], pos = (0.7, 0, 0.9), scale = (0.0451, 0, 0.1))
        self.blueKeyImage.setTransparency(TransparencyAttrib.MAlpha)
        self.blueKeyImage.hide()
        self.greenKeyImage = OnscreenImage(image = self.keyImages[self.room3Key], pos = (0.5, 0, 0.9), scale = (0.0451, 0, 0.1))
        self.greenKeyImage.setTransparency(TransparencyAttrib.MAlpha)
        self.greenKeyImage.hide()

        

    def reComputeHUD(self, room):
       """
       reComputeHUD is called when the player leaves a room and enters another room.
       The HUD shows the images of the keys that the player has in his backpack,
       but not the key to the current room.
       """
##       assert False, "add the hack to make sure she doesn't fall through the ground"
       if self.__mainAgent.hasKey(self.room1Key) and room is not self.room1:
          #self.redKeyImage.show()
          self.room1Key.reparentTo(base.cam)
          self.room1Key.setScale(render, 1.25)
          self.room1Key.setP(base.cam, 0)
          self.room1Key.setPos(base.cam.getX(base.cam) + 2.1, base.cam.getY(base.cam) + 10, base.cam.getZ(base.cam) + 2.1)
          self.room1KeyInHUD = True
       elif self.__mainAgent.hasKey(self.room1Key) and room is self.room1:
          rightHand = self.__mainAgent.actor.exposeJoint(None, 'modelRoot', 'RightHand')
          self.room1Key.reparentTo(rightHand)
          self.room1Key.setPosHpr(.11,-1.99,.06, 0,-90,0)
          self.room1Key.setScale(render, 10)
          self.room1Key.setTexScale(TextureStage.getDefault(), 1)
          self.room1KeyInHUD = False
          self.redKeyImage.hide()
       else:
          self.redKeyImage.hide()
          self.room1KeyInHUD = False

       if self.__mainAgent.hasKey(self.room2Key) and room is not self.room2:
          #self.blueKeyImage.show()
          self.room2Key.reparentTo(base.cam)
          self.room2Key.setScale(render, 1.25)
          self.room2Key.setP(base.cam, 0)
          self.room2Key.setPos(base.cam.getX(base.cam) + 2.5, base.cam.getY(base.cam) + 10, base.cam.getZ(base.cam) + 2.1)
          self.room2KeyInHUD = True
       elif self.__mainAgent.hasKey(self.room2Key) and room is self.room2:
          rightHand = self.__mainAgent.actor.exposeJoint(None, 'modelRoot', 'RightHand')
          self.room2Key.reparentTo(rightHand)
          self.room2Key.setPosHpr(.11,-1.99,.06, 0,-90,0)
          self.room2Key.setScale(render, 10)
          self.room2Key.setTexScale(TextureStage.getDefault(), 1)
          self.room2KeyInHUD = False
          self.blueKeyImage.hide()
       elif (self.blueKeyImage != None):
          self.blueKeyImage.hide()
          self.room2KeyInHUD = False

       if self.__mainAgent.hasKey(self.room3Key) and room is not self.room3:
          #self.greenKeyImage.show()
          self.room3Key.reparentTo(base.cam)
          self.room3Key.setScale(render, 1.25)
          self.room3Key.setP(base.cam, 0)
          self.room3Key.setPos(base.cam.getX(base.cam) + 3.0, base.cam.getY(base.cam) + 10, base.cam.getZ(base.cam) + 2.1)
          self.room3KeyInHUD = True
       elif self.__mainAgent.hasKey(self.room3Key) and room is self.room3:
          rightHand = self.__mainAgent.actor.exposeJoint(None, 'modelRoot', 'RightHand')
          self.room3Key.reparentTo(rightHand)
          self.room3Key.setPosHpr(.11,-1.99,.06, 0,-90,0)
          self.room3Key.setScale(render, 10)
          self.room3Key.setTexScale(TextureStage.getDefault(), 1)
          self.room3KeyInHUD = False
          self.greenKeyImage.hide()
       elif (self.greenKeyImage != None):
          self.greenKeyImage.hide()

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

#        skyBox = loader.loadModel("models/SunnySky/sunny")
#        skyBox.setScale(10)
#        skyBox.reparentTo(render)
        
    def animateItems(self, task):
        if(not (self.__mainAgent.hasKey(self.room1Key) or self.__room1NPC.hasKey()) or self.room1KeyInHUD):
            self.rotate(self.room1Key)
        if(not self.__mainAgent.hasKey(self.room2Key) and not self.__room2NPC.hasKey() or self.room2KeyInHUD):
            self.rotate(self.room2Key)
        if(not self.__mainAgent.hasKey(self.room3Key) and not self.__room3NPC.hasKey() or self.room3KeyInHUD):
            self.rotate(self.room3Key)
        return Task.cont

    hasAllKeys = False
    playerWasKilledByNPC1 = False
    playerWasKilledByNPC2 = False
    playerWasKilledByNPC3 = False
    #gameOver = False
    fadeCounter = 200
    def checkGameState(self, task, message = None):
        goodEndingText = OnscreenText(text="", style=1, fg=(0,0,1,0.01),
                            pos=(0,.4), align=TextNode.ACenter, scale = .25, mayChange = True)
        BaadEndingText = OnscreenText(text="", style=1, fg=(1,0,0,0.01),
                            pos=(0,.4), align=TextNode.ACenter, scale = .25, mayChange = True)
        if(self.fadeCounter > 0):
            if(self.__mainAgent.hasKey(self.room1Key) and self.__mainAgent.hasKey(self.room2Key) and self.__mainAgent.hasKey(self.room3Key)):
                self.hasAllKeys = True
                #goodEndingText.setText("You have all 3 keys!")
            if(self.hasAllKeys):
                goodEndingText.setText("You have all 3 keys!")
            if(PathFinder.distance(self.__mainAgent, self.__room1NPC) < 5 and self.__room1NPC.getState() != "returnKey"):
                if(not self.__mainAgent.hasKey(self.room1Key)):
                    self.playerWasKilledByNPC1 = True
            if(self.playerWasKilledByNPC1):
                self.fadeCounter = self.fadeCounter - 1
                BaadEndingText.setText("Killed by Eve clone Alpha")
            if(PathFinder.distance(self.__mainAgent, self.__room2NPC) < 5 and self.__room2NPC.getState() != "returnKey"):
                if(not self.__mainAgent.hasKey(self.room2Key)):
                    self.playerWasKilledByNPC2 = True
            if(self.playerWasKilledByNPC2):
                self.fadeCounter = self.fadeCounter - 1
                BaadEndingText.setText("Killed by Eve clone Beta")
            if(PathFinder.distance(self.__mainAgent, self.__room3NPC) < 5 and self.__room3NPC.getState() != "returnKey"):
                if(not self.__mainAgent.hasKey(self.room3Key)):
                    self.playerWasKilledByNPC3 = True
            if(self.playerWasKilledByNPC3):
                self.fadeCounter = self.fadeCounter - 1
                BaadEndingText.setText("Killed by Eve clone Gamma")
        return Task.cont
    
    currentAngle = 0
    def rotate(self, someItem):
        if someItem != None:
            self.currentAngle = self.currentAngle + 250 * taskTimer.elapsedTime
            self.currentAngle %= 360
            someItem.setH(self.currentAngle)
            
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

        #place keyNest (Like a birds nest, but for keys!)
        self.keyNest1 = self.room1.attachNewNode("key nest 1")
        keyNest.instanceTo(self.keyNest1)
        self.keyNest1.setPos(0, 0, 0.05)

        self.room1Key = loader.loadModel("models/redKey")
        self.room1Key.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        self.room1Key.reparentTo(self.keyNest1)
        self.room1Key.setScale(render, 10)
        self.room1Key.setTexScale(TextureStage.getDefault(), 0.1)
        
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
        
        self.keyNest2 = self.room2.attachNewNode("key nest 2")
        keyNest.instanceTo(self.keyNest2)
        self.keyNest2.setPos(-2.5, -2.5, 0.05)
        
        self.room2Key = loader.loadModel("models/blueKey")
        self.room2Key.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        self.room2Key.reparentTo(self.keyNest2)
        self.room2Key.setScale(render, 10)
        self.room2Key.setTexScale(TextureStage.getDefault(), 0.1)
        
        # Jim thinks there should be a comment here
        # he also thinks that the above comment is very useful
        # TODO: fix this hack by re-creating room3 in blender
        
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
        
        
        self.keyNest3 = self.room3.attachNewNode("room 3 keynest") 
        keyNest.instanceTo(self.keyNest3)
        self.keyNest3.setPos(0, 0, 0.05)
        
        
        self.room3Key = loader.loadModel("models/greenKey")
        self.room3Key.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        self.room3Key.reparentTo(self.keyNest3)
        self.room3Key.setScale(render, 10)
        self.room3Key.setTexScale(TextureStage.getDefault(), 0.1)
        
        
        room3SphereOfDoom = self.room3.attachNewNode(CollisionNode("Jim's Hair"))
        room3SphereOfDoom.node().addSolid(CollisionSphere(3, -9, 0.5, 1.0))
        
        room1Floor = self.room1.attachNewNode(CollisionNode("room1Floor"))
        room1Floor.node().addSolid(CollisionPolygon(Point3(9,-9,0), Point3(9,9,0),
                                                Point3(-9,9,0), Point3(-9,-9,0)))
                                                
        room2Floor = self.room2.attachNewNode(CollisionNode("room2Floor"))
        room2Floor.node().addSolid(CollisionPolygon(Point3(9,-9,0), Point3(9,9,0),
                                                Point3(-9,9,0), Point3(-9,-9,0)))

        room3Floor = self.room3.attachNewNode(CollisionNode("room3Floor"))
        room3Floor.node().addSolid(CollisionPolygon(Point3(9,-9,0), Point3(9,9,0),
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
            
            if(parameters == "ralph has entered room 1"):
                self.__room1NPC.handleTransition("playerEnteredRoom")
                self.reComputeHUD(self.room1)
                if self.__mainAgent.hasKey(self.room1Key):
                    self.__mainAgent.setCurrentKey(self.room1Key)
            elif(parameters == "ralph has left room 1"):
                self.__room1NPC.handleTransition("playerLeftRoom")
                if self.__mainAgent.hasKey(self.room1Key):
                    self.__mainAgent.setCurrentKey(None)
            elif(parameters == "ralph has entered room 2"):
                self.__room2NPC.handleTransition("playerEnteredRoom")
                self.reComputeHUD(self.room2)
                if self.__mainAgent.hasKey(self.room2Key):
                    self.__mainAgent.setCurrentKey(self.room2Key)
            elif(parameters == "ralph has left room 2"):
                self.__room2NPC.handleTransition("playerLeftRoom")
                if self.__mainAgent.hasKey(self.room2Key):
                    self.__mainAgent.setCurrentKey(None)
            elif(parameters == "ralph has entered room 3"):
                self.__room3NPC.handleTransition("playerEnteredRoom")
                if self.__mainAgent.hasKey(self.room3Key):
                    self.__mainAgent.setCurrentKey(self.room3Key)
                self.reComputeHUD(self.room3)
            elif(parameters == "ralph has left room 3"):
                self.__room3NPC.handleTransition("playerLeftRoom")
                if self.__mainAgent.hasKey(self.room3Key):
                    self.__mainAgent.setCurrentKey(None)
            elif(parameters == "NPC1 bumped into wall"):
                self.__room1NPC.handleTransition("bumpedIntoWall")
            elif(parameters == "NPC2 bumped into wall"):
                self.__room2NPC.handleTransition("bumpedIntoWall")
            elif(parameters == "NPC3 bumped into wall"):
                self.__room3NPC.handleTransition("bumpedIntoWall")
                
        
        self.accept("ralph collision node-into-room1Floor", orderNPC, ["ralph has entered room 1"])
        self.accept("ralph collision node-out-room1Floor", orderNPC, ["ralph has left room 1"])
        self.accept("ralph collision node-into-room2Floor", orderNPC, ["ralph has entered room 2"])
        self.accept("ralph collision node-out-room2Floor", orderNPC, ["ralph has left room 2"])
        self.accept("ralph collision node-into-room3Floor", orderNPC, ["ralph has entered room 3"])
        self.accept("ralph collision node-out-room3Floor", orderNPC, ["ralph has left room 3"])
        self.accept("Eve 1 collision node-into-Cube1", orderNPC, ["NPC1 bumped into wall"])
        self.accept("Eve 2 collision node-into-Cube2", orderNPC, ["NPC2 bumped into wall"])
        self.accept("Eve 3 collision node-into-Cube3", orderNPC, ["NPC3 bumped into wall"])
        

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
                            speed = 25,
                            agentList = self.__globalAgentList,
                            collisionMask = BitMask32.bit(1),
                            name="ralph",
                            massKg = 35.0,
                            collisionHandler = self.physicsCollisionHandler,
                            collisionTraverser = self.cTrav)
        # Make it visible
        self.__mainAgent.reparentTo(render)
        self.__mainAgent.setPos(31, 35, 50)
        self.gate.find("**/Cube;+h").setCollideMask(~self.__mainAgent.collisionMask)
        
    __targetCount = 0
    __targets = []
    __agentToTargetMap = {}
    def __setupNPCs(self):
        # This is to support the collisions for each node. See the paragraph comment
        # above where we modify the npc's collision node
        playerCollisionNP = self.__mainAgent.find("* collision node")

        modelStanding = "models/eve"
        modelRunning = "models/eve-run"
        modelWalking = "models/eve-walk"
        self.__room1NPC = NPC(modelStanding, 
                                {"run":modelRunning, "walk":modelWalking},
                                turnRate = 150, 
                                speed = 15,
                                agentList = self.__globalAgentList,
                                name = "Eve 1",
                                collisionMask = BitMask32.bit(3),
                                rangeFinderCount = 13,
                                adjacencySensorThreshold = 5,
                                radarSlices = 5,
                                radarLength = 40,
                                scale = 1.0,
                                massKg = 35.0,
                                collisionHandler = self.physicsCollisionHandler,
                                collisionTraverser = self.cTrav,
                                waypoints = self.room1waypoints)
        self.__room1NPC.setFluidPos(render, 0, 0, 10)
        self.__room1NPC.setScale(render, 1)
        self.__room1NPC.setPlayer(self.__mainAgent)
        self.__room1NPC.reparentTo(render)


        # So here's what I'm thinking. Currently, two collisions are happening when
        # we collide with an NPC. Those are Player-->NPC and NPC-->Player. This is
        # causing some jumpiness, which in tern causes some collisions to fail (e.g.,
        # falling through the floor). In order to fix this, we need to ignore one of
        # these collisions. Since the NPC should react to the Player, and not vice-versa,
        # I'll ignore the Player-->NPC collision. To do this, we need to set Player's into
        # collide mask to exclude NPC's from collide mask. Let's hope this doesn't break
        # anything.
        npcCollisionNP = self.__room1NPC.find("* collision node")
        npcCollisionNP.node().setIntoCollideMask(npcCollisionNP.node().getIntoCollideMask() & 
                                                ~playerCollisionNP.node().getIntoCollideMask())
        
##        modelStanding = "models/bunny/bunny"
##        modelRunning = "models/bunny/bunny"
##        modelWalking = "models/bunny/bunny"
        self.__room2NPC = NPC(modelStanding,
                                {"run":modelRunning, "walk":modelWalking},
                                turnRate = 150, 
                                speed = 15,
                                agentList = self.__globalAgentList,
                                name = "Eve 2",#"das Osterhase",
                                collisionMask = BitMask32.bit(4),
                                rangeFinderCount = 13,
                                adjacencySensorThreshold = 5,
                                radarSlices = 5,
                                radarLength = 40,
                                scale = 1.0,
                                massKg = 35.0,
                                collisionHandler = self.physicsCollisionHandler,
                                collisionTraverser = self.cTrav,
                                waypoints = self.room2waypoints)
        self.__room2NPC.setPos(-20, -210, 10)
        self.__room2NPC.setPlayer(self.__mainAgent)
        self.__room2NPC.reparentTo(render)
        npcCollisionNP = self.__room2NPC.find("* collision node")
        npcCollisionNP.node().setIntoCollideMask(npcCollisionNP.node().getIntoCollideMask() & 
                                                ~playerCollisionNP.node().getIntoCollideMask())

        self.__room3NPC = NPC(modelStanding, 
                                {"run":modelRunning, "walk":modelWalking},
                                turnRate = 150, 
                                speed = 15,
                                agentList = self.__globalAgentList,
                                name = "Eve 3",#"der Hoppelhaschen",
                                collisionMask = BitMask32.bit(5),
                                rangeFinderCount = 13,
                                adjacencySensorThreshold = 5,
                                radarSlices = 5,
                                radarLength = 40,
                                scale = 1.0,
                                massKg = 35.0,
                                collisionHandler = self.physicsCollisionHandler,
                                collisionTraverser = self.cTrav,
                                waypoints = self.room3waypoints)
        self.__room3NPC.setPos(210, 0, 10)
        self.__room3NPC.setPlayer(self.__mainAgent)
        self.__room3NPC.reparentTo(render)
        npcCollisionNP = self.__room3NPC.find("* collision node")
        npcCollisionNP.node().setIntoCollideMask(npcCollisionNP.node().getIntoCollideMask() & 
                                                ~playerCollisionNP.node().getIntoCollideMask())
        
    def __setupRandomClutter(self):
##        self.ball1 = loader.loadModel("models/ball")
##        #self.ball1.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
##        self.ball1.findTexture("hedge.jpg")
##        self.ball1.setTexScale(TextureStage.getDefault(), 0.1)
##        self.ball1.setPos(0,0,0)
##        self.ball1.reparentTo(render)
        pass
        

    
    def __setupTasks(self):
        """
        This function sets up all the tasks used in the world
        """
        taskMgr.add(taskTimer, "taskTimer")
        
        #for index, ralph in enumerate(self.__otherRalphs):


##            taskMgr.add(ralph.sense, "sense" + str(index))
##            taskMgr.add(ralph.think, "think" + str(index))
##            taskMgr.add(ralph.act,   "act"   + str(index))
            #taskMgr.add(ralph.wanderTask, "wander" + str(index))
##            taskMgr.add(ralph.seekTask, "seekTask" + str(index), extraArgs = [self.__agentToTargetMap[ralph]], appendTask = True)
            
        taskMgr.add(self.__printPositionAndHeading, "__printPositionAndHeading")
        
##        listOfTargets = [(target.getX(), target.getY()) for target in self.__targets]
##        agentList = [(ralph.getX(), ralph.getY()) for ralph in self.__otherRalphs]
##        taskMgr.add(self.neatEvaluateTask, "self.neatEvaluateTask", extraArgs = [listOfTargets, self.__otherRalphs], appendTask = True)
        
        self.__mainAgent.setKeymap()
        taskMgr.add(self.__mainAgent.processKey, "processKeyTask")

          #  taskMgr.add(self.__mainAgent.handleCollisionTask, "handleCollisionTask")
##        taskMgr.add(self.ralph.wanderTask, "wander")
        
        taskMgr.add(self.__room1NPC.sense, "senseTask")
        taskMgr.add(self.__room2NPC.sense, "senseTask")
        taskMgr.add(self.__room3NPC.sense, "senseTask")
##        taskMgr.add(self.ralph.think, "thinkTask")
        taskMgr.add(self.__room1NPC.act, "actTask")
        taskMgr.add(self.__room2NPC.act, "actTask")
        taskMgr.add(self.__room3NPC.act, "actTask")
        taskMgr.add(self.checkGameState, "gameStateTask")
        taskMgr.add(self.animateItems, "animateItemsTask")
        #taskMgr.add(self.processKey, "processKeyTask")

        # This is for path finding
        #taskMgr.add(self.__room1NPC.followPath, "followPathTask", extraArgs = [self.bestPath], appendTask = True)

    def __setupCamera(self):
        #This camera position shows the whole level
        base.camera.setPos(100,-100, 795) #This is debug camera position.
        base.camera.lookAt(100,-100,0)
        #This camera position shows room1
        #base.camera.setPos(0,0, 375) #This is debug camera position.
        #base.camera.lookAt(0,0,0)
        #This camera position shows room2
        #base.camera.setPos(0,-200, 375) #This is debug camera position.
        #base.camera.lookAt(0,-200,0)    
        #This camera position shows room3
        #base.camera.setPos(200,0, 375) #This is debug camera position.
        #base.camera.lookAt(200,0,0)    
        #base.oobeCull()
        #base.oobe()
        base.disableMouse()
        base.camera.reparentTo(self.__mainAgent.actor)
        base.camera.setPos(0, 60, 60)
        base.camera.lookAt(self.__mainAgent)
        base.camera.setP(base.camera.getP() + 10)
    
    def cameraRoom1Pos(self):
        base.camera.reparentTo(render)
        #This camera position shows room1
        base.camera.setPos(0,0, 375) #This is debug camera position.
        base.camera.lookAt(0,0,0)        
        
    def cameraRoom2Pos(self):
        base.camera.reparentTo(render)
        #This camera position shows room2
        base.camera.setPos(0,-200, 375) #This is debug camera position.
        base.camera.lookAt(0,-200,0)    
        
    def cameraRoom3Pos(self):
        base.camera.reparentTo(render)
        #This camera position shows room3
        base.camera.setPos(200,0, 375) #This is debug camera position.
        base.camera.lookAt(200,0,0)
        
    def cameraRegularPos(self):        
        base.camera.reparentTo(self.__mainAgent.actor)
        base.camera.setPos(0, 60, 60)
        base.camera.lookAt(self.__mainAgent)
        base.camera.setP(base.camera.getP() + 10)
        
    positionHeadingText = OnscreenText(text="", style=1, fg=(1,1,1,1),
                   pos=(-1.3,-0.95), align=TextNode.ALeft, scale = .05, mayChange = True)
                

    def __printPositionAndHeading(self, task):
        heading = self.__mainAgent.getH()
        heading %= 360.0
            
##        self.positionHeadingText.setText("Position: (" + 
##            str(self.__mainAgent.getX()) + ", " + 
##            str(self.__mainAgent.getY()) + ", " +
##            str(self.__mainAgent.getZ()) + ") at heading " + 
##            str(heading))
##        return Task.cont

    # Every generation, throw out the old brains and put in the new ones. At
    # this point we can start all over with new nodes.
    generationCount = 0
    generationLifetimeTicks = 500
    neatEvaluateTaskCallCount = 0
##    neuralNetwork = NeuralNetwork()
    def neatEvaluateTask(self, listOfTargets, agentList, task):
        self.neatEvaluateTaskCallCount += 1
        if self.generationLifetimeTicks == self.neatEvaluateTaskCallCount:
            self.neatEvaluateTaskCallCount = 0
            oldBrains = [agent.brain for agent in agentList]
            self.generationCount += 1
            listOfPositions = [(agent.getX(), agent.getY()) for agent in agentList]
            newBrains = self.neuralNetwork.nextGeneration(oldBrains, listOfTargets, listOfPositions)
            
            for agent, brain in zip(agentList, newBrains):
                agent.brain = brain
                agent.setPos(self.startingPositions[agent])

        return Task.cont
    
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
            self.__room1NPC.togglePathSmoothening()
            self.__room2NPC.togglePathSmoothening()
            self.__room3NPC.togglePathSmoothening()
            
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
