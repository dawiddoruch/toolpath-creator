import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 10

    def distance(self, p):
        return math.sqrt(math.pow(p.x - self.x, 2) + math.pow(p.y - self.y, 2))

    def belongs_to(self, p, radius=0.01):
        distance = self.distance(p)
        # print("Point ({0},{1}) distance from ({2},{3}) is {4}".format(self.x, self.y, p.x, p.y, distance))
        if distance <= radius:
            return True
        return False

    def print(self, txt=""):
        print("{2}P({0}, {1})".format(self.x, self.y, txt))
