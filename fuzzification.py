from typing import List
import matplotlib.pyplot as plt
import numpy as np
import csv


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
    def __init__(self, fuzzySets, currentTable, target, then):
        self.fuzzySets = fuzzySets
        self.currentTable = currentTable
        self.target = target
        self.then = then

    def __call__(self, currentTemp, targetTemp):
        currentTempsMemberships = []
        for fSet in self.currentTable:
            foundSet = next((x for x in self.fuzzySets if x.name == fSet), None)
            currentTempsMemberships.append(foundSet(currentTemp)['value'])

        foundSet = next((x for x in self.fuzzySets if x.name == self.target), None)
        targetMembership = foundSet(targetTemp)['value']

        result = min(max(currentTempsMemberships), targetMembership)
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


def loadRules(filename, fuzzySets):
    rules = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            currentTempslist = list(row[0].split(";"))
            rules.append(Rule(fuzzySets, currentTempslist, row[1], row[2]))
        return rules


def rulesAggregation(rules, outputFuzzySets):
    result = [0] * 200
    for set in outputFuzzySets:
        for i in range(200):
            if set(i)['value'] > 0:
                matches = [x['membership'] for x in rules if x['action'] == set.name and x['membership'] > 0]
                if len(matches) > 0:
                    tmp = set(i)['value']
                    if result[i] < min(max(matches), tmp):
                     result[i] = min(max(matches), tmp)
    return result

#defuzzification methods
def calulcateCentroid(plot):
    n = len(plot)
    x = list(range(n))
    num = 0
    denum = 0
    for i in range(n):
        num += x[i] * plot[i]
        denum += plot[i]
    return {'name': 'Centroid', 'value': num / denum}



def maxMembershipPrinciple(plot):
    n = len(plot)
    maxMem = 0
    x = list(range(n))
    for i in range(n):
        if plot[i] > maxMem:
            maxMem = plot[i]
            result = x[i]
    return {'name': 'Max Membership Principle', 'value': result}



def drawFinalPlot(outputFuzzySets, aggregatedRules, points):

    plt.figure(figsize=(12,6))
    plt.ylim(0, 1)
    for x in outputFuzzySets:
        plt.plot(np.linspace(0, 200, 200), [x(i)['value'] for i in range(0, 200)], '--', label=x.name, linewidth='0.5')

    plt.fill_between(np.linspace(0, 200, 200), aggregatedRules)
    plt.plot(np.linspace(0, 200, 200), aggregatedRules, label="Output membership", fillstyle='full')
    for point in points:
        plt.axvline(x=point['value'], label=f'{point["name"]}: {point["value"]}', color='black')

    plt.ylabel('memberships')
    plt.legend()
    plt.show()


def test_functions():
#fuzzy sets for input
    very_cold = Trapezoid("VERY COLD", -20, -20, 5, 10)
    cold = Triangle("COLD", 5, 10, 15)
    warm = Gaussian("WARM", 18, 3)
    hot = Gaussian("HOT", 22, 5)
    very_hot = Trapezoid("VERY HOT", 25, 30, 50, 50)
    classesB = [very_cold, cold, warm, hot, very_hot]
    classes = import_sets_from_csv("inputSets.csv")

#fuzzy sets for output
    cool = Triangle("COOL", 0, 50, 100)
    no_change = Triangle("NO CHANGE", 50, 100, 150)
    heat = Triangle("HEAT", 100, 150, 200)
    outputFuzzySetsB = [cool, no_change, heat]
    outputFuzzySets = import_sets_from_csv("outputSets.csv")

    rules = loadRules("rules.csv", classes)

    for x in rules:
        print(x)

    temp1 = 18
    temp2 = 22

    current = [x(temp1) for x in classes]
    target = [x(temp2) for x in classes]

    print(current)
    print(target)

    evaluatedRules = [x(temp1, temp2) for x in rules]


    aggregatedRules = rulesAggregation(evaluatedRules, outputFuzzySets)
    centroid = calulcateCentroid(aggregatedRules)
    maxMembershipPrincipleResult = maxMembershipPrinciple(aggregatedRules)

    drawFinalPlot(outputFuzzySets, aggregatedRules, [centroid, maxMembershipPrincipleResult])


test_functions()
