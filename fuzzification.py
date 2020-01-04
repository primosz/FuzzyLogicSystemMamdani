import numpy as np
import csv

rules = []

class Triangle:
    def __init__(self, name, start, peak, end, none=0):
        self.name=name
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
        return {'set': self.name, 'value':  np.exp(-np.power(x - self.mu, 2.) / (2 * np.power(self.sigma, 2.)))}


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

        currentTempsMemberships=[]
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



def loadRules(filename, fuzzySets):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            currentTempslist = list(row[0].split(";"))
            rules.append(Rule(fuzzySets, currentTempslist, row[1], row[2]))

def test_functions():
    very_cold = Trapezoid("VERY COLD", -20, -20, 5, 10)
    cold = Triangle("COLD", 5, 10, 15)
    warm = Gaussian("WARM", 18, 3)
    hot = Gaussian("HOT", 22, 5)
    very_hot = Trapezoid("VERY HOT", 25, 30, 50, 50)
    classes = [very_cold, cold, warm, hot, very_hot]

    loadRules("rules.csv", classes)


    for x in rules:
        print(x)



    temp1 = 1
    temp2 = 26
    temp3 = 30

    current = [x(temp1) for x in classes]
    target = [x(temp2) for x in classes]
    memberships3 = [x(temp3) for x in classes]



    print(current)
    print(target)
    print(memberships3)

    rule1 = Rule(classes, ["VERY COLD"], "VERY COLD", "NO CHANGE")
#          IF temperature=(Cold OR Warm OR Hot OR Very_Hot) AND target=Very_Cold THEN	Cool
    rule2 = Rule(classes, ["COLD", "WARM", "HOT", "VERY HOT"],        "VERY COLD",      "COOL")
    rule3 = Rule(classes, ["VERY COLD"], "COLD", "HEAT")
    rule4 = Rule(classes, ["COLD"], "COLD", "NO CHANGE")
    rule5 = Rule(classes, ["WARM", "HOT", "VERY HOT"], "COLD", "COOL")
    rule6 = Rule(classes, ["COLD", "VERY COLD"], "WARM", "HEAT")
    rule7 = Rule(classes, ["WARM"], "WARM", "NO CHANGE")
    rule8 = Rule(classes, ["HOT", "VERY HOT"], "WARM", "COOL")
    rule9 = Rule(classes, ["VERY COLD", "COLD", "WARM"], "HOT", "HEAT")
    rule10 = Rule(classes, ["HOT"], "HOT", "NO CHANGE")
    rule11 = Rule(classes, ["VERY HOT"], "WARM", "COOL")
    rule12 = Rule(classes, ["VERY COLD", "COLD", "WARM", "HOT"], "VERY HOT", "HEAT")
    rule13 = Rule(classes, ["VERY HOT"], "VERY HOT", "NO CHANGE")

    print(rule12)

    print(rule1(temp1, temp2))
    print(rule2(temp1, temp2))
    print(rule3(temp1, temp2))
    print(rule4(temp1, temp2))
    print(rule5(temp1, temp2))
    print(rule6(temp1, temp2))
    print(rule7(temp1, temp2))
    print(rule8(temp1, temp2))
    print(rule9(temp1, temp2))
    print(rule10(temp1, temp2))
    print(rule11(temp1, temp2))
    print(rule12(temp1, temp2))
    print(rule13(temp1, temp2))


test_functions()


