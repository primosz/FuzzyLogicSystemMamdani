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


def test_functions():
    just_right = Triangle(15, 20, 25)
    cold = Trapezoid(-20, -20, 10, 15)
    mild = Gaussian(12, 3)
    warm = Gaussian(20, 5)
    hot = Trapezoid(25, 30, 50, 50)

    classes = [just_right, cold, mild, warm, hot]

    temp1 = 18
    temp2 = 23
    temp3 = 8

    memberships1 = [x(temp1) for x in classes]
    memberships2 = [x(temp2) for x in classes]
    memberships3 = [x(temp3) for x in classes]

    print(memberships1)
    print(memberships2)
    print(memberships3)


test_functions()
