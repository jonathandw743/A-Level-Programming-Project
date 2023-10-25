from geometry.rectangle import Rectangle
from geometry.vector import Vector

"""
update flow should be:
- set acceleration to 0
- apply accelerations/force eg move, gravity, jump
- update velocity and displacement
- collide
- update position
"""


class Player:
    def __init__(self, x, y, hw, hh, vel_x=0, vel_y=0):
        self.rect = Rectangle(x, y, hw, hh)
        self.vel = Vector(vel_x, vel_y)
        self.acc = Vector(0, 0)
        self.dis = Vector(0, 0)
        self.grounded = False

    def reset_grounded(self):
        self.grounded = False

    def set_grounded(self):
        self.grounded = True

    def jump(self, jump_input, power, dt, play_jump_sound=None):
        if jump_input and self.grounded:
            self.apply_acc(Vector(0, -power / dt))
            # play the jump sound
            if play_jump_sound:
                play_jump_sound()

    def air_resistance(self, power):
        self.apply_acc(self.vel.flip() * power)

    def ground_friction(self, power):
        # square of speed?
        if self.grounded:
            self.apply_acc(Vector(-self.vel.x * power, 0))

    def gravity(self, g):
        self.apply_acc(Vector(0, g))

    def move_horizontal(
        self, left_input, right_input, grounded_speed, ungrounded_speed
    ):
        self.apply_acc(
            Vector(
                (right_input - left_input)
                * (grounded_speed if self.grounded else ungrounded_speed),
                0,
            )
        )

    def apply_acc(self, acc):
        self.acc = self.acc + acc

    def reset_acc(self):
        self.acc = Vector(0, 0)

    def update_displacement_and_velocity(self, dt):
        # s = ut + 0.5at2
        self.dis = self.vel * dt + self.acc * (0.5 * dt * dt)
        # v = u + at
        self.vel = self.vel + self.acc * dt

    def update_position(self):
        self.rect.pos = self.rect.pos + self.dis

    def is_in_bounds(self, bounds: Rectangle):
        if self.rect.pos.x > bounds.right_pos():
            return False
        if self.rect.pos.y > bounds.bottom_pos():
            return False
        if self.rect.pos.x < bounds.left_pos():
            return False
        if self.rect.pos.y < bounds.top_pos():
            return False
        return True

    # # for collisions with the centre of the rectangle
    # def collision_x(self, x, bounce_factor):
    #     y_change_sf = (x - self.rect.pos.x) / self.dis.x
    #     self.rect.pos.y += self.dis.y * y_change_sf
    #     self.rect.pos.x = x
    #     self.vel.x = -self.vel.x * bounce_factor
    #     self.dis = Vector (
    #         (x - (self.rect.pos.x + self.dis.x)) * bounce_factor,
    #         self.dis.y * (1.0 - y_change_sf),
    #     )

    # # for collisions with the centre of ther rectangle
    # def collision_y(self, y, bounce_factor):
    #     x_change_sf = (y - self.rect.pos.y) / self.dis.y
    #     self.rect.pos.x += self.dis.x * x_change_sf
    #     self.rect.pos.y = y
    #     self.vel.y = -self.vel.y * bounce_factor
    #     self.dis = Vector (
    #         (self.dis.x * (1.0 - x_change_sf)) * bounce_factor,
    #         y - (self.rect.pos.y + self.dis.y),
    #     )

    # for collisions with the centre of the rectangle
    def no_bounce_collision_x(self, x):
        self.vel.x = 0
        self.dis = Vector(
            x - self.rect.pos.x,
            self.dis.y,
        )

    # for collisions with the centre of the rectangle
    def no_bounce_collision_y(self, y):
        self.vel.y = 0
        self.dis = Vector(
            self.dis.x,
            y - self.rect.pos.y,
        )

    def collide_with_rectangle_discrete(self, rect):
        """
        two rectangles colliding can be simplified to a rectangle and point colliding
        """
        # combined rectangle
        r = rect.combine_rectangle(self.rect)
        # point
        p = self.rect.pos

        # positions of the sides of the rectangle
        right = r.right_pos()
        bottom = r.bottom_pos()
        left = r.left_pos()
        top = r.top_pos()

        # early return if point is outside the rectangle
        if (p.x >= right) or (p.y >= bottom) or (p.x <= left) or (p.y <= top):
            return

        # find the closest wall
        right_dist = right - p.x
        bottom_dist = bottom - p.y
        left_dist = p.x - left
        top_dist = p.y - top

        min_dist = min(right_dist, bottom_dist, left_dist, top_dist)

        if min_dist == right_dist:
            # collision with right wall of rectangle
            p.x = right
            self.vel.x = 0
        elif min_dist == bottom_dist:
            # collision with bottom wall of rectangle
            p.y = bottom
            self.vel.y = 0
        elif min_dist == left_dist:
            # collision with left wall of rectangle
            p.x = left
            self.vel.x = 0
        else:
            # collision with top wall of rectangle
            p.y = top
            self.vel.y = 0

    def rectangle_collision_detection(self, rect):
        """
        two rectangles colliding can be simplified to a rectangle and point colliding
        """
        # combined rectangle
        r = rect.combine_rectangle(self.rect)
        # point
        p = self.rect.pos
        # vector
        v = self.dis
        # end point
        e = p + v

        # positions of the sides of the rectangle
        right = r.right_pos()
        bottom = r.bottom_pos()
        left = r.left_pos()
        top = r.top_pos()

        if (
            (p.x >= right and e.x >= right)
            or (p.y >= bottom and e.y >= bottom)
            or (p.x <= left and e.x <= left)
            or (p.y <= top and e.y <= top)
        ):
            return False

        # vectors from p to each corner of r
        br_cv = r.bottom_right_pos() - p
        bl_cv = r.bottom_left_pos() - p
        tr_cv = r.top_right_pos() - p
        tl_cv = r.top_left_pos() - p

        # sign (+/-) of dot product of corner vector with v
        dp_br_sign = Vector.dot(v, br_cv) > 0.0
        dp_bl_sign = Vector.dot(v, bl_cv) > 0.0
        dp_tl_sign = Vector.dot(v, tl_cv) > 0.0
        dp_tr_sign = Vector.dot(v, tr_cv) > 0.0

        # this may be covered by the first return case
        if (
            (not dp_br_sign)
            and (not dp_bl_sign)
            and (not dp_tl_sign)
            and (not dp_tr_sign)
        ):
            return False

        # v rotated 90 degrees
        perp_v = v.rotate90()

        # sign (+/-) of dot product of corner vector with v rotated 90 degrees
        perp_dp_br_sign = Vector.dot(perp_v, br_cv) > 0.0
        perp_dp_bl_sign = Vector.dot(perp_v, bl_cv) > 0.0
        perp_dp_tl_sign = Vector.dot(perp_v, tl_cv) > 0.0
        perp_dp_tr_sign = Vector.dot(perp_v, tr_cv) > 0.0

        if (
            perp_dp_br_sign and perp_dp_bl_sign and perp_dp_tl_sign and perp_dp_tr_sign
        ) or (
            (not perp_dp_br_sign)
            and (not perp_dp_bl_sign)
            and (not perp_dp_tl_sign)
            and (not perp_dp_tr_sign)
        ):
            return False

        return {
            "v": v,
            "right": right,
            "bottom": bottom,
            "left": left,
            "top": top,
            "perp_dp_br_sign": perp_dp_br_sign,
            "perp_dp_bl_sign": perp_dp_bl_sign,
            "perp_dp_tl_sign": perp_dp_tl_sign,
            "perp_dp_tr_sign": perp_dp_tr_sign,
        }

    def rectangle_collision_response(self, collision):
        if not collision:
            return
        v = collision["v"]
        right = collision["right"]
        bottom = collision["bottom"]
        left = collision["left"]
        top = collision["top"]
        perp_dp_br_sign = collision["perp_dp_br_sign"]
        perp_dp_bl_sign = collision["perp_dp_bl_sign"]
        perp_dp_tl_sign = collision["perp_dp_tl_sign"]
        perp_dp_tr_sign = collision["perp_dp_tr_sign"]
        if v.x > 0.0:
            if v.y > 0.0:
                if perp_dp_tl_sign:
                    # top
                    self.no_bounce_collision_y(top)
                    self.set_grounded()
                else:
                    # left
                    self.no_bounce_collision_x(left)
            else:
                if perp_dp_bl_sign:
                    # left
                    self.no_bounce_collision_x(left)
                else:
                    # bottom
                    self.no_bounce_collision_y(bottom)
        else:
            if v.y > 0.0:
                if perp_dp_tr_sign:
                    # right
                    self.no_bounce_collision_x(right)
                else:
                    # top
                    self.no_bounce_collision_y(top)
                    self.set_grounded()
            else:
                if perp_dp_br_sign:
                    # bottom
                    self.no_bounce_collision_y(bottom)
                else:
                    # right
                    self.no_bounce_collision_x(right)

    # continuous collision detection
    def collide_with_rectangle(self, rect):
        collision = self.rectangle_collision_detection(rect)
        self.rectangle_collision_response(collision)