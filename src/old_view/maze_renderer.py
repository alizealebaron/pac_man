# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_renderer.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/28 16:53:13 by rruiz           #+#    #+#               #
#  Updated: 2026/06/01 11:12:29 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade
from PIL import Image

WALL_DIR = 'assets/sprite/wall/'
MAP_NAME = 'tiny_wood.png'
MAP_FILE = f'{WALL_DIR}' + f'{MAP_NAME}'
TILE_SIZE = 64

class MazeRenderer:
    """Gère le rendu du labyrinthe"""

    def __init__(self, maze: list[list[int]], window_width: float, window_height: float, hud_width_left: float = 200, hud_width_right: float = 200):
        self.maze = maze
        self.window_width = window_width
        self.window_height = window_height
        self.hud_width_left = hud_width_left
        self.hud_width_right = hud_width_right

        self.scale = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

        self.sprites = arcade.SpriteList()
        self.sprite_sheet = self._load_sprites(MAP_FILE)
        self._build_maze_sprites()

    def _build_maze_sprites(self):
        nb_columns = len(self.maze[0])
        maze_width_size = nb_columns * TILE_SIZE
        nb_lines = len(self.maze)
        maze_height_size = nb_lines * TILE_SIZE

        available_width = self.window_width - self.hud_width_left - self.hud_width_right

        if available_width / maze_width_size > self.window_height / maze_height_size:
            self.scale = self.window_height / maze_height_size * 0.95
        else:
            self.scale = available_width / maze_width_size * 0.95

        self.offset_x = self.hud_width_left + (available_width - maze_width_size * self.scale) / 2
        self.offset_y = ((self.window_height) - maze_height_size * self.scale) / 2

        for y in range(1, nb_lines + 1):
            for x in range(1, nb_columns + 1):
                wall_value = self.maze[y - 1][x - 1]
                wall = self.sprite_sheet[wall_value]
                wall_texture = arcade.Texture(wall)

                center_x = (x - 0.5) * TILE_SIZE * self.scale + self.offset_x
                center_y = (y - 0.5) * TILE_SIZE * self.scale + self.offset_y

                sprite = arcade.Sprite(wall_texture, center_x=center_x, center_y=center_y, scale=self.scale)
                self.sprites.append(sprite)

    def _load_sprites(self, path: str) -> list:
        img = Image.open(path)
        frames = []

        for x in range(0, img.width, TILE_SIZE):
            frame = img.crop((x, 0, x + TILE_SIZE, TILE_SIZE))
            frames.append(frame)

        return frames

    def draw(self):
        """ Draw everything """
        self.sprites.draw()
