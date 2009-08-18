#Client code sxrclient.py
import xmlrpclib
import orbitSystem
#import planetarium
import Eval
import cPickle
#from planetarium import Universe
from orbitSystem import Body
from orbitSystem import System
from orbitSystem import Galaxy
#import psyco
#psyco.full()
from Eval import Eval

class solarClient(object):
    def __init__(self, xString='http://bamdastard.kicks-ass.net:8000', scoreThresh=1, sysName="none"):
        self.connected=False
        if sysName != "none":
            self.xString = xString
            self.sysName = sysName
            self.retrieveSystem()
        if xString == "runSol":
            self.runSol()
        if xString == "standalone":
            print "launching disconnected viewer"
            self.runLocal()
        try:
            print "connecting to server "+xString
            self.server = xmlrpclib.Server(xString)
            print "connection acquired"
            self.scoreThreshold =scoreThresh;
            self.score = 1000
##            while self.score > self.scoreThreshold:
##                print "retrieving a system"
##                self.xfile = self.server.getSystem()
##                print "converting xfile"
##                self.mySystem = cPickle.loads(self.xfile)
##                print "launching evaluator"
##                self.Evaluator = Eval(self.mySystem, 1000)
##                print "calculating score"
##                self.score = self.Evaluator.evaluate()
##                print "system stability score = "
##                print self.score
##            print "found acceptable system, recording system as: "
            self.retrieveGalaxy()
            self.generateSystem()
            self.insertSystem()
            self.launchSystem()
            
            #print self.xfile
#            print "launching planetarium.. .  .    .        ."
#            import planetarium
#            self.planetWindow = planetarium.Universe(self.Evaluator)
#            run()
        except:
            print "oops, there was an error"
            self.runLocal()
    def insertSystem(self):
        self.xfile=cPickle.dumps(self.mySystem)
        self.connectToServer()
        sysName = self.server.insertSystem(self.xfile)
        print sysName
        
    def getAllStars(self):
        print "getting all star names"
        allStars = self.server.getAllStars()
        for star in allStars:
            print star
        return

    def connectToServer(self):
        print "connecting to server "
        print self.xString
        self.server = xmlrpclib.Server(self.xString)
        self.connected=True
        
    def retrieveGalaxy(self):
        self.connectToServer(self)
        print "retrieving galaxy"
        xfile = self.server.getGalaxy()
        print "loading galaxy"
        self.galaxy=cPickle.loads(xfile)
        

    def retrieveSystem(self):
        self.connectToServer(self)        
        self.getAllStars()
        print "attempting to retrieve and launch system: "
        print self.sysName
        self.xfile = self.server.retrieveSystem(self.sysName)
        print "unpacking system"
        self.mySystem = cPickle.loads(self.xfile)
        print "launching evaluator"
        self.Evaluator = Eval(self.mySystem, 1000)
        print "calculating score"
        self.score = self.Evaluator.evaluate()
        print "system stability score = "
        print self.score
        print "launching planetarium.. .  .    .        ."
        import planetarium
        self.planetWindow = planetarium.Universe(self.Evaluator)
        run()
        
    def runSol(self):
        print "earthSun"
        sysCount = 0
        self.mySystem = System(sysCount)
        self.Evaluator = Eval(self.mySystem, 1000)
        print "number of bodies:"
        print len(self.mySystem.bodies)
        print "launching planetarium.. .  .    .        ."
        import planetarium
        self.planetWindow = planetarium.Universe(self.Evaluator)
        run()

    def generateSystem(self):
        sysCount = 1
        self.mySystem = System(sysCount)
        self.Evaluator = Eval(self.mySystem, 1000)
        self.scoreThreshold =1;
        self.score = 1000
        starcount=1
        bodycount=2
        bodyDistance=3
        bodySpeed=0.05
        while self.score > self.scoreThreshold:
            self.mySystem = System(sysCount, starcount, bodycount, bodyDistance, bodySpeed)
            self.Evaluator = Eval(self.mySystem, 1000)
            self.score = self.Evaluator.evaluate()
            print "system stability score = "
            print self.score
            sysCount+=1
        print "adding planets"
        planetCount = 3
        while len(self.mySystem.bodies)< planetCount:
            self.mySystem.addSinglePlanet()
        print "number of bodies:"
        print len(self.mySystem.bodies)
        
        
    def launchSystem(self):
        print "launching planetarium.. .  .    .        ."
        import planetarium
        self.planetWindow = planetarium.Universe(self.Evaluator,.02, self.galaxy.stars)
        run()
        
    def runLocal(self):
        print "generating system locally"
        self.galaxy = Galaxy()
        print "galaxy completed"
        self.generateSystem()
        self.launchSystem()        

#Uncomment the following line to retrieve "system6" from the server
#defaultClient = solarClient('http://bamdastard.kicks-ass.net:8000', 1, "system20.sys")
#Uncomment the following line if you want the client to run offline
#defaultClient = solarClient("standalone")
#defaultClient = solarClient("runSol")
#This is the default configuration which attempts to retrieve a system from
#the server. Failure will cause the client to launch locally in disconnected mode
defaultClient = solarClient('http://bamdastard.kicks-ass.net:8000', 1, "none")
