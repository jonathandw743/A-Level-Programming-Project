from geometry.vector import Vector


class Camera:
    def __init__(
        self,
        x,
        y,
        screen_width_pix,
        screen_height_pix,
        game_space_visible_width=0,
        game_space_visible_height=0,
    ):
        self.screen_width_pix = screen_width_pix
        self.screen_height_pix = screen_height_pix
        self.pos = Vector(x, y)
        # If the visible height of the screen is given, use that to calculate the zoom
        if game_space_visible_width != 0:
            self.zoom = self.screen_width_pix / game_space_visible_width
        # same for the width
        elif game_space_visible_height != 0:
            self.zoom = self.screen_height_pix / game_space_visible_height
        else:
            print("Camera zoom cannot be calculated.")
            self.zoom = 1

    def game_space_to_screen_space_x_pos(self, x):
        return (x - self.pos.x) * self.zoom + self.screen_width_pix / 2

    def game_space_to_screen_space_y_pos(self, y):
        return (y - self.pos.y) * self.zoom + self.screen_height_pix / 2

    def game_space_to_screen_space_x_dim(self, x):
        return x * self.zoom

    def game_space_to_screen_space_y_dim(self, y):
        return y * self.zoom

    def game_space_to_screen_space_pos(self, pos):
        return Vector(
            self.game_space_to_screen_space_x_pos(pos.x),
            self.game_space_to_screen_space_y_pos(pos.y),
        )

    def game_space_to_screen_space_dim(self, dim):
        return Vector(
            self.game_space_to_screen_space_x_dim(dim.x),
            self.game_space_to_screen_space_y_dim(dim.y),
        )

    def game_space_to_screen_space_corner_rect_tuple(self, rect_tuple):
        return (
            self.game_space_to_screen_space_x_pos(rect_tuple[0]),
            self.game_space_to_screen_space_y_pos(rect_tuple[1]),
            self.game_space_to_screen_space_x_dim(rect_tuple[2]),
            self.game_space_to_screen_space_y_dim(rect_tuple[3]),
        )
