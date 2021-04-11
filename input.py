from models import Unit, Interval

units_dir = './inputs/units.txt'
intervals_dir = './inputs/intervals.txt'


def get_units(total_intervals):
    f = open(units_dir)

    units_count = int(f.readline())
    units = []

    for index in range(units_count):
        unit_number = f.readline()
        unit_capacity = f.readline()
        unit_maintenance_count = f.readline()
        unit = Unit(unit_number, unit_capacity, unit_maintenance_count, len(total_intervals))
        units.append(unit)

    return units


def get_intervals():
    f = open(intervals_dir)

    intervals_count = int(f.readline())
    intervals = []

    for i in range(intervals_count):
        interval_number = f.readline()
        interval_load = f.readline()
        interval = Interval(interval_number, interval_load)
        intervals.append(interval)

    return intervals

#
# for item in get_intervals():
#     print(item)
