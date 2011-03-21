from direct.fsm import FSM

class npcFSM(FSM.FSM):
    def __init__(self):
        FSM.FSM.__init__(self, "npcFSM")
        self.defaultTransitions = {
            'wander' : [ 'retriveKey', 'seek' ],
            'retriveKey' : [ 'wander', 'returnKey' ],
            'seek' : [ 'wander' ],
            'returnKey' : [ 'wander' ]
            }

##    def wander(self, npc)
##        npc.


    def enterRetriveKey(self, player, npc, pathfinder, waypoints):
        #makeSureAStarIsCalled()
        pass
        
    def exitRetriveKey(self):
        pass
        
    nextState = {
        ('wander', 'keyTaken') : 'retriveKey',
        ('wander', 'withinRange') : 'seek',
        ('retrieveKey', 'leftRoom') : 'wander',
        ('retrieveKey', 'gotKey') : 'returnKey',
        ('seek', 'outOfRange') : 'wander',
        ('seek', 'leftRoom') : 'wander',
        ('returnKey', 'keyReturned') : 'wander',
        }

    def defaultFilter(self, request, args):
        key = (self.state, request)
        return self.nextState.get(key)
    
    
if __name__ == "__main__":
    myfsm = npcFSM()
    print("compiled")



#### DELETE EVERYTHING BELOW HERE
##    def changeState(transition):
##        if(npcState == "wander"):
##            if(transition == "keyTaken"):
##                self.npcState = "retriveKey"
##            elif(transition == "withinRange"):
##                self.npcState = "seek"
##        elif(npcState == "retriveKey"):
##            if(transition == "leftRoom"):
##                self.npcState = "wander"
##            elif(transition == "gotKey"):
##                self.npcState = "returnKey"
##        elif(npcState == "seek"):
##            if(transition == "outOfRange"):
##                self.npcState = "wander"
##            elif(transitin == "leftRoom"):
##                self.npcState = "wander"
##        elif(npcState == "returnKey"):
##            if(transition == "keyReturn"):
##                self.npcState = "wander"
##                
##    def manageState():
##        if(npcState == "wander"):
##            self.wander()
##            if(distanceToPlayer() < radarLength):
##                changeState("withinRange")
##            elif(ralphTookKey):
##                changeState("keyTaken")

