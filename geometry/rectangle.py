from .vector import Vector


class Rectangle:
    def __init__(self, x, y, hw, hh):
        self.pos = Vector(x, y)
        self.size = Vector(hw, hh)

    def __str__(self):
        return f"Rectangle: (pos: {self.pos} dim: {self.size})"

    def unwrap(self):
        return self.pos.unwrap(), self.size.unwrap()

    def corner_rect_tuple(self):
        return (self.left_pos(), self.top_pos(), self.size.x * 2, self.size.y * 2)

    def combine_rectangle(self, other):
        return Rectangle(
            self.pos.x,
            self.pos.y,
            self.size.x + other.size.x,
            self.size.y + other.size.y,
        )

    def contains_point(self, p):
        return not (
            p.x < self.pos.x - self.size.x
            or p.y < self.pos.y - self.size.y
            or p.x > self.pos.x + self.size.x
            or p.y > self.pos.y + self.size.y
        )

    def right_pos(self):
        return self.pos.x + self.size.x

    def bottom_pos(self):
        return self.pos.y + self.size.y

    def left_pos(self):
        return self.pos.x - self.size.x

    def top_pos(self):
        return self.pos.y - self.size.y

    def bottom_right_pos(self):
        return self.pos + self.size

    def bottom_left_pos(self):
        return self.pos + self.size.reflect_x()

    def top_left_pos(self):
        return self.pos + self.size.flip()

    def top_right_pos(self):
        return self.pos + self.size.reflect_y()


if __name__ == "__main__":
    r = Rectangle(0, 0, 20, 10)
    print(r.bottom_left_pos())

    print(str(r))


# class DynamicRectangle(Rectangle):

#     def __init__(self, x, y, hw, hh, vel_x=0, vel_y=0):
#         super().__init__(x, y, hw, hh)
#         self.vel = Vector(vel_x, vel_y)

#     def __str__(self):
#         return f'DynamicRectangle: (pos: {self.pos} dim: {self.size} vel: {self.vel})'

#     def move(self):
#         self.pos += self.vel

#     def collide_with(self, other):
#         combined_rectangle = other.combine_rectangle(self)

#         if not combined_rectangle.contains_point(self.pos):
#             return

#         exit_direction = self.vel * -1

#         if exit_direction.x > 0:
#             if exit_direction.y > 0:
#                 corner_number = 0
#             else:
#                 corner_number = 3
#         else:
#             if exit_direction.y > 0:
#                 corner_number = 1
#             else:
#                 corner_number = 2

#         corner_vector = combined_rectangle.corner_vector(corner_number)

#         perp_exit_vector = exit_direction.rotate90()
#         if Vector.dot(corner_vector, perp_exit_vector) > 0:
#             edge_number = corner_number - 1
#         else:
#             edge_number = corner_number

#         # print(edge_number)

#         if edge_number == 0 or edge_number == 2:
#             edge_position = combined_rectangle.corner_pos(edge_number).y
#             self.pos.y += (edge_position - self.pos.y) * 2
#             self.vel.y *= -1
#         elif edge_number == 1 or edge_number == 3:
#             edge_position = combined_rectangle.corner_pos(edge_number).x
#             self.pos.x += (edge_position - self.pos.x) * 2
#             self.vel.x *= -1
