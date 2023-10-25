from math import atan2


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        return Vector(self.x * k, self.y * k)

    def __truediv__(self, k):
        return self * (1 / k)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __iter__(self):
        return iter([self.x, self.y])

    def unwrap(self):
        return self.x, self.y

    def copy(self):
        return Vector(self.x, self.y)

    def angle(self):
        return atan2(self.y, self.x)

    @staticmethod
    def dot(v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    def rotate90(self):
        return Vector(-self.y, self.x)

    def reflect_x(self):
        return Vector(-self.x, self.y)

    def reflect_y(self):
        return Vector(self.x, -self.y)

    def flip(self):
        return Vector(-self.x, -self.y)

    @staticmethod
    def from_tuple(vector_tuple):
        return Vector(vector_tuple[0], vector_tuple[1])

    def to_tuple(self):
        return (self.x, self.y)


if __name__ == "__main__":
    a = Vector(2, 4)
    b = Vector(3, 5)

    print(a + b)

    a = Vector(2, 4)
    b = Vector(-2, -4)

    print(a.angle(), b.angle())
