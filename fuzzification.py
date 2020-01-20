import csv

import matplotlib.pyplot as plt
import numpy as np


class Triangle:
    def __init__(self, name, start, peak, end, none=0):
        self.name = name
        self.a = start
        self.b = peak
        self.c = end

    def __str__(self):
        return ' ' + self.name + str(self.a) + str(self.b) + str(self.c)

    def __call__(self, x):
        if x < self.a or x > self.c:
            return {'set': self.name, 'value': 0}
        elif x == self.b:
            return {'set': self.name, 'value': 1}
        elif x < self.b:
            return {'set': self.name, 'value': (x - self.a) / (self.b - self.a)}
        elif x > self.b:
            return {'set': self.name, 'value': 1 - ((x - self.b) / (self.c - self.b))}


class Trapezoid:
    def __init__(self, name, start, peak_first, peak_second, end):
        self.name = name
        self.a = start
        self.b = peak_first
        self.c = peak_second
        self.d = end

    def __call__(self, x):
        if x < self.a or x > self.d:
            return {'set': self.name, 'value': 0}
        elif self.b <= x <= self.c:
            return {'set': self.name, 'value': 1}
        elif x < self.b:
            return {'set': self.name, 'value': (x - self.a) / (self.b - self.a)}
        elif x > self.c:
            return {'set': self.name, 'value': 1 - ((x - self.c) / (self.d - self.c))}


class Gaussian:
    def __init__(self, name, expected_value, sigma, none_1=0, none_2=0):
        self.name = name
        self.mu = expected_value
        self.sigma = sigma

    def __call__(self, x):
        return {'set': self.name, 'value': np.exp(-np.power(x - self.mu, 2.) / (2 * np.power(self.sigma, 2.)))}


# you can create rules by giving parameters:
# 1 - list of fuzze sets objects
# 2 - list of temperatures in rule
# 3 - what is target temperature (after 'AND')
# 4 - what is the actions (after 'THEN')
class Rule:
    def __init__(self, fuzzy_sets, current_table, target, then):
        self.fuzzySets = fuzzy_sets
        self.currentTable = current_table
        self.target = target
        self.then = then

    def __call__(self, current_temp, target_temp):
        current_temps_memberships = []
        for fSet in self.currentTable:
            found_set = next((x for x in self.fuzzySets if x.name == fSet), None)
            current_temps_memberships.append(found_set(current_temp)['value'])

        found_set = next((x for x in self.fuzzySets if x.name == self.target), None)
        target_membership = found_set(target_temp)['value']

        result = min(max(current_temps_memberships), target_membership)
        return {'action': self.then, 'membership': result}

    def __str__(self):
        current_string = ' or '.join(self.currentTable)
        return f"If it's {current_string} and target is {self.target} then {self.then}."


def import_sets_from_csv(filename):
    sets = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp = [x.replace("\"", "") for x in row]
            if tmp[1] == "Triangle":
                sets.append(Triangle(tmp[0], int(tmp[2]), int(tmp[3]), int(tmp[4])))
            elif tmp[1] == "Trapeze":
                sets.append(Trapezoid(tmp[0], int(tmp[2]), int(tmp[3]), int(tmp[4]), int(tmp[5])))
            elif tmp[1] == "Gaussian":
                sets.append(Gaussian(tmp[0], int(tmp[2]), int(tmp[3])))
    return sets


def load_rules(filename, fuzzy_sets):
    rules = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            current_tempslist = list(row[0].split(";"))
            rules.append(Rule(fuzzy_sets, current_tempslist, row[1], row[2]))
        return rules


def rules_aggregation(rules, output_fuzzy_sets):
    result = [0] * 200
    for out_set in output_fuzzy_sets:
        for i in range(200):
            if out_set(i)['value'] > 0:
                matches = [x['membership'] for x in rules if x['action'] == out_set.name and x['membership'] > 0]
                if len(matches) > 0:
                    tmp = out_set(i)['value']
                    if result[i] < min(max(matches), tmp):
                        result[i] = min(max(matches), tmp)
    return result


# defuzzification methods
def calulcate_centroid(plot):
    n = len(plot)
    x = list(range(n))
    num = 0
    denum = 0
    for i in range(n):
        num += x[i] * plot[i]
        denum += plot[i]
    return {'name': 'Centroid', 'value': num / denum}


def max_membership_principle(plot):
    n = len(plot)
    max_mem = 0
    x = list(range(n))
    result = 0
    for i in range(n):
        if plot[i] > max_mem:
            max_mem = plot[i]
            result = x[i]
    return {'name': 'Max Membership Principle', 'value': result}


def draw_final_plot(output_fuzzy_sets, aggregated_rules, points):
    plt.figure(figsize=(12, 6))
    plt.ylim(0, 1)
    for x in output_fuzzy_sets:
        plt.plot(np.linspace(0, 200, 200), [x(i)['value'] for i in range(0, 200)], '--', label=x.name, linewidth='0.5')

    plt.fill_between(np.linspace(0, 200, 200), aggregated_rules)
    plt.plot(np.linspace(0, 200, 200), aggregated_rules, label="Output membership", fillstyle='full')
    for point in points:
        plt.axvline(x=point['value'], label=f'{point["name"]}: {point["value"]}', color='black')

    plt.ylabel('memberships')
    plt.legend()
    plt.show()


def test_functions():
    # fuzzy sets for input
    very_cold = Trapezoid("VERY COLD", -20, -20, 5, 10)
    cold = Triangle("COLD", 5, 10, 15)
    warm = Gaussian("WARM", 18, 3)
    hot = Gaussian("HOT", 22, 5)
    very_hot = Trapezoid("VERY HOT", 25, 30, 50, 50)
    classes_b = [very_cold, cold, warm, hot, very_hot]
    classes = import_sets_from_csv("inputSetsAdjusted.csv")

    # fuzzy sets for output
    cool = Triangle("COOL", 0, 50, 100)
    no_change = Triangle("NO CHANGE", 50, 100, 150)
    heat = Triangle("HEAT", 100, 150, 200)
    output_fuzzy_sets_b = [cool, no_change, heat]
    output_fuzzy_sets = import_sets_from_csv("outputSets.csv")

    rules = load_rules("rules.csv", classes)

    # for x in rules:
    #    print(x)

    temp = 32.0
    temp_target = 2.0

    current = [x(temp) for x in classes]
    target = [x(temp_target) for x in classes]

    print(current)
    print(target)

    evaluated_rules = [x(temp, temp_target) for x in rules]

    aggregated_rules = rules_aggregation(evaluated_rules, output_fuzzy_sets)
    centroid = calulcate_centroid(aggregated_rules)
    max_membership_principle_result = max_membership_principle(aggregated_rules)

    draw_final_plot(output_fuzzy_sets, aggregated_rules, [centroid, max_membership_principle_result])


def temperature_simulation(start, target, timesteps, input_sets, output_sets, rules_set, method):
    input_sets = import_sets_from_csv(input_sets)

    output_sets = import_sets_from_csv(output_sets)

    rules = load_rules(rules_set, input_sets)

    for _ in range(0, timesteps):
        target = [x(target) for x in input_sets]

        evaluated_rules = [x(start, target) for x in rules]

        output = _

        aggregated_rules = rules_aggregation(evaluated_rules, output_sets)
        if method is "centroid":
            output = calulcate_centroid(aggregated_rules)
        if method is "mmp":
            output = max_membership_principle(aggregated_rules)

        start += ((output['value'] - 100) * 2) / 1000

        print(round(start, 2))


test_functions()
