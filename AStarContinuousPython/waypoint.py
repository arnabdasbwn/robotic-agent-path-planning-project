from pandac.PandaModules import NodePath
from pandac.PandaModules import Texture
from pandac.PandaModules import LineSegs

class Waypoint(NodePath):
    
    def __init__(self, position, ID = -1):
        NodePath.__init__(self, "Waypoint " + str(ID))
        self.setPos(render, position)
        self.texture = loader.loadTexture("textures/blue.jpg")
        self.costToThisNode = 0
        self.visited = False
        self.neighbors = []
        self.ID = ID
        self.previousWaypoint = None
        torusModel = "models/Torus/Torus.egg"
        self.torus = loader.loadModel(torusModel)

    def getNodeID(self):
        return self.ID
    
    def setPreviousWaypoint(self, previousWaypoint):
        self.previousWaypoint = previousWaypoint

    def getPreviousWaypoint(self):
        return self.previousWaypoint
    
    def visit(self):
        self.visited = True

    def wasVisited(self):
        return self.visited
        
    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
        
    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)
        
    def getNeighbors(self):
        return self.neighbors
    
    def setCostToNode(self, cost):
        self.costToThisNode = cost
        
    def getCostToNode(self):
        return self.costToThisNode
    
    def changeToGreen(self):
        self.texture = loader.loadTexture("textures/green.jpg")
        self.torus.setTexture(self.texture, 1)

    def changeToYellow(self):
        self.texture = loader.loadTexture("textures/yellow.jpg")
        self.torus.setTexture(self.texture, 1)
        
    def changeToBlue(self):
        self.texture = loader.loadTexture("textures/blue.jpg")
        self.torus.setTexture(self.texture, 1)
        
    def changeToSnowish(self):
        self.texture = loader.loadTexture("textures/snowish.jpg")
        self.texture.setMinfilter(Texture.FTLinearMipmapLinear)
        self.torus.setTexture(self.texture, 1)

    def draw(self):  
        torus = self.torus
        torus.setScale(5, 5, 5)
        torus.setTexture(self.texture, 1)
        torus.reparentTo(render)
        torus.setPos(render, self.getPos())
        torus.show()
        self.drawLineToNeighbors()
        
    def drawLineToNeighbors(self):
        ls = LineSegs()
        ls.setThickness(1.0)
        for neighbor in self.neighbors:
            ls.setColor(1,1,1,1)
            ls.moveTo(self.getPos(render))
            ls.drawTo(neighbor.getPos(render))
        self.np = NodePath(ls.create("Neighbor Line Segment"))
        self.np.reparentTo(render)
            
    def erase(self):
        self.torus.hide()
        self.np.hide()
        
    #def hideLineToNeighbors(self):
        
        
