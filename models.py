from typing import List
import random

import numpy as np
import matplotlib.pyplot as plt


class Unit:
    def __init__(self, number, capacity, maintenance_count, intervals_count):
        self.number = int(number)
        self.capacity = int(capacity)
        self.maintenance_count = int(maintenance_count)
        self.intervals_count = intervals_count

        self.layout = []
        return

    # def assign_interval(self, interval):
    #     if len(self.assigned_intervals) < self.maintenance_count:

    def get_random_layout(self):
        start_maintenance_index = random.randint(0, self.intervals_count - 1)
        layout = [0 for i in range(self.intervals_count)]

        for i in range(start_maintenance_index, start_maintenance_index + self.maintenance_count):
            i = i % self.intervals_count
            layout[i] = 1

        self.layout = layout
        return layout

    # def get_random_layout(self, layout):

    def __str__(self):
        str_layout = [str(index) for index in self.layout]
        return '{number}\t capacity: {capacity}\t maintenance count: {intervals}\tlayout: {layout}'.format(
            number=self.number,
            capacity=self.capacity,
            intervals=self.maintenance_count,
            layout=str.join(' ', str_layout))


class Interval:
    def __init__(self, number, load):
        self.number = int(number)
        self.min_load = int(load)
        self.units: List[Unit] = []
        self.total_load = 0
        pass

    def get_load(self):
        load = 0
        for unit in self.units:
            load += unit.capacity
        return load

    def get_active_units(self, units: List[List[int]]):
        active_units = []
        for unit in units:
            if unit[self.number - 1] == 0:
                active_units.append(unit)
        return active_units

    def get_deactive_units(self, units):
        deactive_units = []
        for unit in units:
            if unit[self.number - 1] == 1:
                deactive_units.append(unit)
        return deactive_units

    def __str__(self):
        return '{number}\t min_load: {load}\tcurrent load: {total_load}'.format(number=self.number, load=self.min_load,
                                                                                total_load=self.total_load)


class Genome:
    def __init__(self, units: List[Unit], intervals: List[Interval]):
        self.original_units = units
        self.units: List[List[int]] = []

        for unit in units:
            self.units.append(unit.get_random_layout())

        self.intervals = intervals

    def get_binary(self):
        return

    def crossover(self, other_genome: 'Genome'):
        unit_count = len(self.units)
        point_1 = random.randint(0, int(unit_count / 2))
        point_2 = random.randint(int(unit_count / 2), unit_count)
        slice_1 = self.units[:point_1] + other_genome.units[point_1:point_2] + self.units[point_2:]
        slice_2 = other_genome.units[:point_1] + self.units[point_1:point_2] + other_genome.units[point_2:]

        self.units = slice_1
        other_genome.units = slice_2

        return self, other_genome

    def mutate(self, probability) -> 'Genome':
        if random.random() > probability:
            return self

        index = random.randint(0, len(self.units) - 1)
        self.units[index] = self.original_units[index].get_random_layout()
        return self

    def fitness(self):
        interval_count = self.original_units[0].intervals_count

        for i in range(interval_count):
            total_load = 0
            for unit_index in range(len(self.units)):
                unit = self.units[unit_index]
                if unit[i] == 1:
                    continue
                total_load += self.original_units[unit_index].capacity
            self.intervals[i].total_load = total_load

        min_load = self.intervals[0].total_load - self.intervals[0].min_load
        for interval in self.intervals:
            _min_load = interval.total_load - interval.min_load
            if _min_load < min_load:
                min_load = _min_load

        # if min_load < 0:
        #     min_load = 0

        return min_load

    def __str__(self):
        s = ''
        for unit in self.units:
            s += ''.join(str(unit))
        s += '\nfitness = {fitness}'.format(fitness=self.fitness())
        return s


class ChartData:
    def __init__(self, intervals: List[Interval], units: List[Unit]):
        self.intervals = intervals
        self.units = units
        self.units_values = []

        self.results = []

    def add_result(self, value):
        self.results.append(value)

    def get_chart_data(self):
        data = {}

        for interval in self.intervals:
            name = f'Interval {interval.number}'
            extra_load = interval.total_load - interval.min_load
            data[name] = [interval.min_load, extra_load, ]

            active_units = interval.get_active_units(self.units_values)
            for i, unit in enumerate(self.units_values):
                if unit in active_units: continue
                data[name] += [self.units[i].capacity]
        return data

    def get_max_deative_units_count(self):
        max_deactive_units_count = 0
        for interval in self.intervals:
            active_units_count = len(interval.get_active_units(self.units_values))
            deative_units_count = len(self.units) - active_units_count
            if deative_units_count > max_deactive_units_count:
                max_deactive_units_count = deative_units_count
        return max_deactive_units_count

    def load_units_from_genome(self, genome: Genome):
        self.units_values = []
        for i, unit in enumerate(genome.units):
            self.units_values.append(unit.copy())

    def load_units_from_array(self, units: List[Unit]):
        self.units_values = []
        for i, unit in enumerate(units):
            self.units_values.append(unit.layout.copy())

    def refresh_interval_values(self):
        for i, unit in enumerate(self.units_values):
            self.units[i].layout = unit

        for i in range(len(self.intervals)):
            interval = self.intervals[i]
            total_load = 0
            for j, unit in enumerate(self.units_values):
                total_load += self.units[j].capacity if unit[i] == 0 else 0
            interval.total_load = total_load

        min_load = self.intervals[0].total_load - self.intervals[0].min_load
        for interval in self.intervals:
            _min_load = interval.total_load - interval.min_load
            if _min_load < min_load:
                min_load = _min_load
        return

    def show(self):
        self.refresh_interval_values()
        data = self.get_chart_data()
        max_deative_units_count = self.get_max_deative_units_count()

        labels = ['min', 'extra', 'unit']
        intervals_count = len(self.intervals)
        Pos = range(intervals_count)
        vertical_parts_count = 2 + max_deative_units_count
        values = list(data.values())

        fig, axs = plt.subplots(2)
        top_ax = axs[0]
        bottom_ax = axs[1]

        top_ax.plot(self.results)

        latest_values = np.arange(intervals_count)
        for i in range(vertical_parts_count):
            value = []
            for item in values:
                if i >= len(item):
                    value += [0]
                    continue
                value += [item[i]]

            label = labels[i] if i < len(labels) else labels[-1]
            rects = bottom_ax.bar(Pos, np.array(value), label=label, bottom=latest_values)

            deactive_index = 0
            for val, h in enumerate(value):
                interval = self.intervals[val]
                if h == 0:
                    continue
                x = rects[val].get_x()
                y = rects[val].get_y()
                height = rects[val].get_height()
                width = rects[val].get_width()

                if i == 0:
                    rect_label = 'Min'
                elif i == 1:
                    rect_label = 'Extra'
                else:
                    if (i - 2) <= len(interval.get_deactive_units(self.units_values)):
                        u = interval.get_deactive_units(self.units_values)[i - 2]
                        index = self.units_values.index(u)
                        rect_label = 'Unit' + str(self.units[index].number)
                    deactive_index += 1

                bottom_ax.text(x + width / 2., y + height / 2., rect_label, ha='center', va='center', color='white')
            latest_values += value

        plt.xticks(Pos, data.keys())
        # plt.legend()

        plt.show()
