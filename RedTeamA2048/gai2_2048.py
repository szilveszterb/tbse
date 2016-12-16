import math
import numpy
import time

from pybrain.tools.shortcuts import buildNetwork
from pyevolve import G1DList
from pyevolve import GSimpleGA, Mutators
from pyevolve import Selectors

from g2048 import logic

DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_RIGHT = (1, 0)
DIR_LEFT = (-1, 0)

myId = "admin"

kmap = {"UP": 38, "DOWN": 40, "LEFT": 37, "RIGHT": 39}
lkmap = {"UP": DIR_UP, "DOWN": DIR_DOWN, "LEFT": DIR_RIGHT, "RIGHT": DIR_LEFT}

STEPS = ["UP", "DOWN", "RIGHT", "LEFT"]


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
    new_params = numpy.array(genome)
    net._setParameters(new_params)

    game = logic.Game()
    game.new_game()
    steps = 0

    while(not game.board.game_over()):
        new_game_state = []
        old_game_state = []
        steps += 1
        for row in game.board._board:
            old_game_state = old_game_state + list(row)

        result = net.activate(old_game_state)
        ma = max(result)

        direction = [i for i, j in enumerate(result) if j == ma]

        game.shift(lkmap[STEPS[direction[0]]])
        biggest_field = 0
        for row in game.board._board:
            new_game_state = new_game_state + list(row)
            for field in row:
                if field > biggest_field:
                    biggest_field = field

        if new_game_state == old_game_state:
            break

    with open(statistic_file_name, 'a') as f:
        f.write('{};{};{}\n'.format(game.score, steps, int(math.pow(2, biggest_field))))

    return game.score


def G1DListTSPInitializator(genome, **args):
    """ The initializator for the TSP """

    gen = net.params
    genome.setInternalList(gen)


def run_main():

    global net
    net = buildNetwork(16, 500, 4)

    global statistic_file_name
    statistic_file_name = "gai_statistic_{}.csv".format(int(time.time()))
    with open(statistic_file_name, 'a') as f:
        f.write('score;steps;biggest_field\n')

    # par = net.params
    # new_params = numpy.array([1.1 for i in range(0,37)])

    # Genome instance
    genome = G1DList.G1DList(len(net.params))
    genome.setParams(rangemin=-10, rangemax=10)
    # genome.setParams(allele=setOfAlleles)

    # The evaluator function (objective function)
    genome.evaluator.set(eval_func)
    genome.initializator.set(G1DListTSPInitializator)
    # This mutator and initializator will take care of
    # initializing valid individuals based on the allele set
    # that we have defined before
    genome.mutator.set(Mutators.G1DListMutatorRealRange)
    # genome.initializator.set(Initializators.G1DListInitializatorAllele)
    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)
    ga.selector.set(Selectors.GRouletteWheel)
    ga.setGenerations(20000)
    ga.setPopulationSize(20000)
    ga.stepCallback.set(evolve_callback)

    # Do the evolution
    ga.evolve(freq_stats=100)

    # Best individual
    print ga.bestIndividual()

if __name__ == "__main__":
    run_main()
