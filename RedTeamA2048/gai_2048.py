from pyevolve import G1DList
from pyevolve import GSimpleGA, Mutators, Initializators
from pyevolve import Selectors, GAllele
from socketIO_client import SocketIO, LoggingNamespace
import sys
import time

myId = "Red Team"

kmap = {"UP": 38, "DOWN": 40, "LEFT": 37, "RIGHT": 39}

# The step callback function, this function
# will be called every step (generation) of the GA evolution
def evolve_callback(ga_engine):
   generation = ga_engine.getCurrentGeneration()
   if generation % 100 == 0:
      print "Current generation: %d" % (generation,)
      print ga_engine.getStatistics()
   return False

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(genome):
    global score
    score = 0
    global geno
    geno = genome
    def algorithm(data):
        data = data.split(" ")
        global score
        global geno
        score = int(data[0])

        if len(geno) > 0:
            socketIO.emit("aiwrite", kmap[geno[0]])
            geno = geno[1:len(geno)-1]
        else:
            socketIO.disconnect()

    def error(msg):
        print(msg)
        socketIO.disconnect()
        pass

    socketIO = SocketIO('diosd', 5000, LoggingNamespace)

    socketIO.on("airead", algorithm)
    socketIO.on("error", error)
    socketIO.on("disconnected", error)
    #socketIO.emit("login", myId, "admin")
    socketIO.emit("connect")
    socketIO.emit("aictl", myId)
    try:
        socketIO.wait()
    except:
        pass

    print("Score:" + str(score))
    return score

def run_main():
   # Genome instance
   setOfAlleles = GAllele.GAlleles()

   for i in xrange(1000):
      # You can even add objects instead of strings or
      # primitive values
      a = GAllele.GAlleleList(['UP','DOWN', 'LEFT', 'RIGHT'])
      setOfAlleles.add(a)

   # Genome instance
   genome = G1DList.G1DList(300)
   #genome.setParams(rangemin=0, rangemax=10)
   genome.setParams(allele=setOfAlleles)

   # The evaluator function (objective function)
   genome.evaluator.set(eval_func)
   # This mutator and initializator will take care of
   # initializing valid individuals based on the allele set
   # that we have defined before
   genome.mutator.set(Mutators.G1DListMutatorAllele)
   genome.initializator.set(Initializators.G1DListInitializatorAllele)
   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.selector.set(Selectors.GRouletteWheel)
   ga.setGenerations(800)
   ga.stepCallback.set(evolve_callback)

   # Do the evolution
   ga.evolve()

   # Best individual
   print ga.bestIndividual()

if __name__ == "__main__":
   run_main()
