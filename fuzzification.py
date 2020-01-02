import numpy as np


class Triangle:
    def __init__(self, start, peak, end, none=0):
        self.a = start
        self.b = peak
        self.c = end

    def __call__(self, x):
        if x < self.a or x > self.c:
            return 0
        elif x == self.b:
            return 1
        elif x < self.b:
            return (x - self.a) / (self.b - self.a)
        elif x > self.b:
            return 1 - ((x - self.b) / (self.c - self.b))


class Trapezoid:
    def __init__(self, start, peak_first, peak_second, end):
        self.a = start
        self.b = peak_first
        self.c = peak_second
        self.d = end

    def __call__(self, x):
        if x < self.a or x > self.d:
            return 0
        elif self.b <= x <= self.c:
            return 1
        elif x < self.b:
            return (x - self.a) / (self.b - self.a)
        elif x > self.c:
            return 1 - ((x - self.c) / (self.d - self.c))


class Gaussian:
    def __init__(self, expected_value, sigma, none_1=0, none_2=0):
        self.mu = expected_value
        self.sigma = sigma

    def __call__(self, x):
        return np.exp(-np.power(x - self.mu, 2.) / (2 * np.power(self.sigma, 2.)))

# you can create rules by giving parameters:
# 1 - table with values which temperatures are after IF
# 2 - what is target temperature (after 'AND')
# 3 - what is the actions (after 'THEN')
class Rule:
    def __init__(self, currentTable, target, then):
        self.indexes = [0, 0, 0, 0, 0]
        if "VERY COLD" in currentTable: self.indexes[0] = 1
        if "COLD" in currentTable: self.indexes[1] = 1
        if "WARM" in currentTable: self.indexes[2] = 1
        if "HOT" in currentTable: self.indexes[3] = 1
        if "VERY HOT" in currentTable: self.indexes[4] = 1
        self.target = target
        self.then = then

#to evaluate the rule you need to give parameters:
# 1 - table with memberships for every function
# 2 - target temperature memberships for every function
# rule evaluation returns list with values for [Cool, No_Change, Heat]
    def __call__(self, currentTempMemberships, targetMemberships):
        firedMemberships = []
        for idx, val in enumerate(self.indexes):
            if val == 1: firedMemberships.append(currentTempMemberships[idx])

        if self.target == "VERY COLD": targetMemValue = targetMemberships[0]
        if self.target == "COLD": targetMemValue = targetMemberships[1]
        if self.target == "WARM": targetMemValue = targetMemberships[2]
        if self.target == "HOT": targetMemValue = targetMemberships[3]
        if self.target == "VERY HOT": targetMemValue = targetMemberships[4]

        value = min(max(firedMemberships), targetMemValue)
        if self.then == "COOL":
            return [value, 0, 0]
        elif self.then == "NO CHANGE":
            return [0, value, 0]
        elif self.then == "HEAT":
            return [0, 0, value]


# Every rule evaluation returns list with values for [Cool, No_Change, Heat]

def evaluateRule1(currentTempMemberships, targetMemberships):
    return [0, min(currentTempMemberships[0], targetMemberships[0]), 0]

def evaluateRule2(currentTempMemberships, targetMemberships):
    return [min(max(currentTempMemberships[1], currentTempMemberships[2], currentTempMemberships[3], currentTempMemberships[4]), targetMemberships[0]), 0, 0]

def evaluateRule3(currentTempMemberships, targetMemberships):
    return [0, 0, min(currentTempMemberships[0], targetMemberships[1])]

def evaluateRule4(currentTempMemberships, targetMemberships):
    return [0,  min(currentTempMemberships[1], targetMemberships[1]), 0]

def evaluateRule5(currentTempMemberships, targetMemberships):
    return [min(max(currentTempMemberships[2], currentTempMemberships[3], currentTempMemberships[4]), targetMemberships[1]), 0, 0]

def evaluateRule6(currentTempMemberships, targetMemberships):
    return [0,  0, min(max(currentTempMemberships[0], currentTempMemberships[1]), targetMemberships[2])]

def evaluateRule7(currentTempMemberships, targetMemberships):
    return [0, min(currentTempMemberships[2], targetMemberships[2]), 0]

def evaluateRule8(currentTempMemberships, targetMemberships):
    return [min(max(currentTempMemberships[3], currentTempMemberships[4]), targetMemberships[2]), 0, 0]

def evaluateRule9(currentTempMemberships, targetMemberships):
    return [0, 0, min(max(currentTempMemberships[0], currentTempMemberships[1], currentTempMemberships[2]), targetMemberships[3])]

def evaluateRule10(currentTempMemberships, targetMemberships):
    return [0,  min(currentTempMemberships[3], targetMemberships[3]), 0]

def evaluateRule11(currentTempMemberships, targetMemberships):
    return [min(currentTempMemberships[4], targetMemberships[3]), 0, 0]

def evaluateRule12(currentTempMemberships, targetMemberships):
    return [0, 0, min(max(currentTempMemberships[0], currentTempMemberships[1], currentTempMemberships[2], currentTempMemberships[3]), targetMemberships[4])]

def evaluateRule13(currentTempMemberships, targetMemberships):
    return [0,  min(currentTempMemberships[4], targetMemberships[4]), 0]

def evaluateRules(currentTempMemberships, targetMemberships):
    result=[]
    result.append(evaluateRule1(currentTempMemberships, targetMemberships))
    result.append(evaluateRule2(currentTempMemberships, targetMemberships))
    result.append(evaluateRule3(currentTempMemberships, targetMemberships))
    result.append(evaluateRule4(currentTempMemberships, targetMemberships))
    result.append(evaluateRule5(currentTempMemberships, targetMemberships))
    result.append(evaluateRule6(currentTempMemberships, targetMemberships))
    result.append(evaluateRule7(currentTempMemberships, targetMemberships))
    result.append(evaluateRule8(currentTempMemberships, targetMemberships))
    result.append(evaluateRule9(currentTempMemberships, targetMemberships))
    result.append(evaluateRule10(currentTempMemberships, targetMemberships))
    result.append(evaluateRule11(currentTempMemberships, targetMemberships))
    result.append(evaluateRule12(currentTempMemberships, targetMemberships))
    result.append(evaluateRule13(currentTempMemberships, targetMemberships))
    return result


def test_functions():
    very_cold = Trapezoid(-20, -20, 10, 15)
    cold = Triangle(5, 10, 15)
    warm = Gaussian(18, 3)
    hot = Gaussian(22, 5)
    very_hot = Trapezoid(25, 30, 50, 50)

    classes = [very_cold, cold, warm, hot, very_hot]

    temp1 = 22
    temp2 = 29
    temp3 = 8

    current = [x(temp1) for x in classes]
    target = [x(temp2) for x in classes]
    memberships3 = [x(temp3) for x in classes]

    rule1 = Rule(["VERY COLD"], "VERY COLD", "NO CHANGE")
    rule12 = Rule(["VERY COLD", "COLD", "WARM", "HOT"], "VERY HOT", "HEAT")

    print(current)
    print(target)
    print(memberships3)
    print(evaluateRules(current, target))
    print(rule1(current, target))

    print(rule12(current, target))


test_functions()


