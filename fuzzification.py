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
