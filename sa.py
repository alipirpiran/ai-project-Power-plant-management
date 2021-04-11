import input
import random
import numpy as np
import numpy.random as rn
import matplotlib.pyplot as plt
# from index import Annealing
from models import ChartData


class Annealing:
    def __init__(self, range, max_temp, value_function, neighbour_function, get_max=False, data=None):
        self.range = range
        self.max_temp = max_temp

        self.get_max = get_max

        self.value_function = value_function
        self.neighbour_function = neighbour_function

        self.data = data

    def start_annealing(self):
        best_input = self.random_start()
        best_value = self.get_value(best_input)

        self.neighbours = []
        temp = self.max_temp
        colling_factor = 0.9995
        step = 0
        current = best_input
        current_value = self.get_value(current)

        chart_data = ChartData(self.data.intervals, self.data.units)

        while temp > 1:
            temp = temp * colling_factor
            step += 1
            new_input = self.random_neighbour(current, temp, self.max_temp)
            new_value = self.get_value(new_input)

            if self.acceptance_probability(best_value, new_value, temp) > rn.random():
                current = new_input
                current_value = self.get_value(current)

            chart_data.add_result(best_value)

            if (self.get_max and current_value > best_value) or (
                    not self.get_max and current_value < best_value):
                chart_data.load_units_from_array(best_input)
                best_input = current
                best_value = self.get_value(best_input)
            self.neighbours.append(new_input)

        return best_input, best_value, chart_data

    def random_start(self):
        return self.neighbour_function(None, None, None)

    def get_value(self, input):
        return self.value_function(input)

    def random_neighbour(self, input, temp, max_temp):
        return self.neighbour_function(input, temp, max_temp)

    def acceptance_probability(self, cost, new_cost, temperature):
        if (self.get_max and new_cost > cost) or (not self.get_max and new_cost < cost):
            return 1
        else:
            p = np.exp(- (new_cost - cost) / temperature)
            return p

    def get_temp(self, fraction):
        return self.max_temp - self.max_temp * fraction

    def clip(self, x):
        a, b = self.range
        return max(min(x, b), a)


class Data:
    def __init__(self):
        self.intervals = input.get_intervals()
        self.units = input.get_units(self.intervals)

    def neighbour(self, input, temp, max_temp):
        if temp is None:
            for unit in self.units:
                unit.get_random_layout()
            return self.units
        nesbat = temp / max_temp
        count = len(self.units) * nesbat
        count = int(count)

        for i in range(count):
            unit = random.choice(self.units)
            unit.get_random_layout()
        return self.units

    def fitness(self, units):
        for i in range(len(self.intervals)):
            interval = self.intervals[i]
            total_load = 0
            for unit in units:
                total_load += unit.capacity if unit.layout[i] == 0 else 0
            interval.total_load = total_load

        min_load = self.intervals[0].total_load - self.intervals[0].min_load
        for interval in self.intervals:
            _min_load = interval.total_load - interval.min_load
            if _min_load < min_load:
                min_load = _min_load
        return min_load


data = Data()
an = Annealing(None, 50, data.fitness, data.neighbour, get_max=True, data=data)
best_input, best_value, chartData = an.start_annealing()

chartData.refresh_interval_values()

print('\n***** Units *****')
for unit in data.units:
    print(unit)
print('\n***** Intervals *****')
for interval in data.intervals:
    print(interval)

chartData.show()
