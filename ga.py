import random as pyrnd
from numpy import random
from models import ChartData, Genome
import input as file_input

random.seed(1)


class Genetic:
    def __init__(self, pc, pm, units, intervals, N):
        self.pc = pc
        self.pm = pm
        self.units = units
        self.intervals = intervals
        self.N = N

    def crossover(self, g1: Genome, g2: Genome):
        if random.random() > self.pc:
            return g1, g2

        g1, g2 = g1.crossover(g2)
        return g1, g2

    def run(self):
        population = []
        results = []

        chart_data = ChartData(self.intervals, self.units)

        for i in range(self.N):
            genome = Genome(units=self.units, intervals=self.intervals)
            population.append(genome)

        for _ in range(100):

            population = sorted(population, key=lambda genome: genome.fitness(), reverse=True)

            results.append(population[0].fitness())
            chart_data.add_result(population[0].fitness())

            next_generation = population[:2]

            for i in range(int(len(population) / 2) - 1):
                weights = []
                for genome in population:
                    weights += [genome.fitness()] if genome.fitness() > 0 else [1]
                parents = pyrnd.choices(population=population, weights=weights,
                                        k=2)
                child_1, child_2 = self.crossover(parents[0], parents[1])

                child_1 = child_1.mutate(self.pm)
                child_2 = child_2.mutate(self.pm)

                next_generation += [child_1, child_2]
            population = next_generation
        return population, chart_data


intervals = file_input.get_intervals()
units = file_input.get_units(intervals)

g = Genetic(pc=7, pm=0.0001, units=units, intervals=intervals, N=100)

population, chart_data = g.run()

chart_data.load_units_from_genome(population[0])
chart_data.show()
