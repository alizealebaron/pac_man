# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_renderer.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/28 16:53:13 by rruiz           #+#    #+#               #
#  Updated: 2026/06/13 12:19:45 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade
from PIL import Image
import random

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


WALL_DIR = 'assets/sprite/wall/'
MAP_NAME = ['electric_maze.png', 'joyous_tower.png', 'mount_faraway.png',
            'purity_forest.png']
MAP_FILE = f'{WALL_DIR}' + f'{random.choice(MAP_NAME)}'
TILE_SIZE = 64


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class MazeRenderer:

    """Classe responsable du rendu du labyrinthe à partir d'une matrice de
    valeurs entières représentant les différents types de murs et de chemins.

    Attributs:
        maze (list[list[int]]): La matrice représentant le labyrinthe.
        window_width (float): La largeur de la fenêtre de jeu.
        window_height (float): La hauteur de la fenêtre de jeu.
        hud_width_left (float): La largeur de l'interface utilisateur à
            gauche du labyrinthe.
        hud_width_right (float): La largeur de l'interface utilisateur à
            droite du labyrinthe.
        scale (float): Le facteur de mise à l'échelle pour ajuster le
            labyrinthe à la taille de la fenêtre.
        offset_x (float): Le décalage horizontal pour centrer le labyrinthe
            dans la fenêtre.
        offset_y (float): Le décalage vertical pour centrer le labyrinthe
            dans la fenêtre.
        sprites (arcade.SpriteList): La liste des sprites représentant les murs
            et les chemins du labyrinthe.
        sprite_sheet (list): La liste des textures extraites de la feuille de
            sprites pour les différents types de murs et de chemins.
        """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, maze: list[list[int]], window_width: float,
                 window_height: float, hud_width_left: float = 200,
                 hud_width_right: float = 200) -> None:

        """
        Initialise le MazeRenderer avec les paramètres nécessaires pour le
        rendu du labyrinthe.

        Args:
            maze (list[list[int]]): La matrice représentant le labyrinthe.
            window_width (float): La largeur de la fenêtre de jeu.
            window_height (float): La hauteur de la fenêtre de jeu.
            hud_width_left (float, optional): La largeur de l'interface
                utilisateur à gauche du labyrinthe. Par défaut à 200.
            hud_width_right (float, optional): La largeur de l'interface
                utilisateur à droite du labyrinthe. Par défaut à 200.
        """

        self.maze = maze
        self.window_width = window_width
        self.window_height = window_height
        self.hud_width_left = hud_width_left
        self.hud_width_right = hud_width_right

        self.scale = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

        self.sprites: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.sprite_sheet = self._load_sprites(MAP_FILE)
        self._build_maze_sprites()

    # +---------------------------------------------------------------------+
    # |                               Methods                               |
    # +---------------------------------------------------------------------+

    def _build_maze_sprites(self) -> None:

        """
        Construit les sprites du labyrinthe à partir de la matrice de valeurs
        et de la feuille de sprites. Calcule également les facteurs de
        mise à l'échelle et les décalages pour centrer le labyrinthe dans la
        fenêtre.
        """

        nb_columns = len(self.maze[0])
        maze_width_size = nb_columns * TILE_SIZE
        nb_lines = len(self.maze)
        maze_height_size = nb_lines * TILE_SIZE

        available_width = (self.window_width - self.hud_width_left -
                           self.hud_width_right)

        if (available_width / maze_width_size >
           self.window_height / maze_height_size):

            self.scale = self.window_height / maze_height_size * 0.95
        else:
            self.scale = available_width / maze_width_size * 0.95

        self.offset_x = (self.hud_width_left +
                         (available_width - maze_width_size * self.scale) / 2)

        self.offset_y = (((self.window_height) -
                          maze_height_size * self.scale) / 2)

        for y in range(1, nb_lines + 1):
            for x in range(1, nb_columns + 1):
                wall_value = self.maze[y - 1][x - 1]
                wall = self.sprite_sheet[wall_value]
                wall_texture = arcade.Texture(wall)

                center_x = (x - 0.5) * TILE_SIZE * self.scale + self.offset_x
                center_y = (y - 0.5) * TILE_SIZE * self.scale + self.offset_y

                sprite = arcade.Sprite(wall_texture, center_x=center_x,
                                       center_y=center_y, scale=self.scale)
                self.sprites.append(sprite)

    def _load_sprites(self, path: str) -> list[Image.Image]:

        """
        Charge les textures des murs et des chemins à partir d'une feuille de
        sprites.

        Args:
            path (str): Le chemin vers la feuille de sprites.

        Returns:
            list: Une liste de textures extraites de la feuille de sprites.
        """

        img = Image.open(path)
        frames = []

        for x in range(0, img.width, TILE_SIZE):
            frame = img.crop((x, 0, x + TILE_SIZE, TILE_SIZE))
            frames.append(frame)

        return frames

    def draw(self) -> None:

        """
        Méthode appelée pour dessiner les sprites.
        """

        self.sprites.draw()
