"""Module contains figures, classes, attributes and methods for calculation."""

import math


class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def square(self):
        return 0


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def square(self):
        return math.pi * self.radius ** 2

    def contains(self, point):
        dist = math.hypot(point.x - self.x, point.y - self.y)
        return dist <= self.radius


class Rectangle(Shape):
    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

    def square(self):
        return self.width * self.height


class Parallelogram(Rectangle):
    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width)
        self.angle = angle

    def square(self):
        angle_radians = math.radians(self.angle)
        return self.width * self.height * math.sin(angle_radians)

    def print_angle(self):
        print(self.angle)

    def __str__(self):
        result = super().__str__()
        return result + (f'\nParallelogram: {self.width},'
                         f'{self.height}, {self.angle}')

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Triangle(Shape):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        super().__init__(x1, y1)
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.x3, self.y3 = x3, y3

    def square(self):
        area = abs(self.x1*(self.y2 - self.y3) +
                   self.x2*(self.y3 - self.y1) +
                   self.x3*(self.y1 - self.y2)) / 2
        return area


class Scene:
    def __init__(self):
        self._figures = []

    def add_figure(self, figure):
        self._figures.append(figure)

    def total_square(self):
        return sum(f.square() for f in self._figures)

    def __str__(self):
        desc = 'Scene containing:\n'
        for fig in self._figures:
            desc += f'{fig.__class__.__name__} with area {fig.square()}\n'
        return desc


r = Rectangle(0, 0, 10, 20)
r1 = Rectangle(10, 0, -10, 20)
r2 = Rectangle(0, 20, 100, 20)

c = Circle(10, 0, 10)
c1 = Circle(100, 100, 5)
pt_inside = Point(15, 0)
pt_outside = Point(25, 0)

print('Point', (pt_inside.x, pt_inside.y),
      'inside circle:', c.contains(pt_inside))
print('Point', (pt_outside.x, pt_outside.y),
      'inside circle:', c.contains(pt_outside))

p = Parallelogram(1, 2, 20, 30, 45)
print('Parallelogram area:', p.square())

t = Triangle(0, 0, 4, 0, 0, 3)
print('Triangle area:', t.square())

scene = Scene()
scene.add_figure(r)
scene.add_figure(r1)
scene.add_figure(r2)
scene.add_figure(c)
scene.add_figure(c1)
scene.add_figure(p)
scene.add_figure(t)

print('Total area of all figures in the scene:', scene.total_square())
print(scene)
