# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  collectible_manager.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/09 08:30:01 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 15:11:43 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+

import arcade
from src.models.configmodel import ConfigModel
from src.models.playerModel import PlayerModel
from typing import Tuple

# +-------------------------------------------------------------------------+
# |                                  CONST                                  |
# +-------------------------------------------------------------------------+


PACGUM_PATH = 'assets/sprite/collectible/pacgum.png'
SUPER_PACGUM_PATH = 'assets/sprite/collectible/super_pacgum.png'
TILE_SIZE = 64


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class CollectibleManager:
    """
    Manager pour les pacgums et super pacgums.

    Attributes:
        maze (list[list[int]]): Le labyrinthe du niveau.
        scale (float): Le facteur de mise à l'échelle pour les sprites.
        offset_x (float): Décalage horizontal pour le positionnement des
            sprites.
        offset_y (float): Décalage vertical pour le positionnement des
            sprites.
        pg_sprites (arcade.SpriteList): Liste de sprites pour les pacgums.
        spg_sprites (arcade.SpriteList): Liste de sprites pour les super
            pacgums.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, maze: list[list[int]], scale: float = 1.0,
                 offset_x: float = 0.0, offset_y: float = 0.0):

        """
        Initialise le manager de collectibles.

        Args:
            maze (list[list[int]]): Le labyrinthe du niveau.
            scale (float, optional): Le facteur de mise à l'échelle pour les
                sprites. Par défaut à 1.0.
            offset_x (float, optional): Décalage horizontal pour le
                positionnement des sprites. Par défaut à 0.0.
            offset_y (float, optional): Décalage vertical pour le
                positionnement des sprites. Par défaut à 0.0.
        """

        self.maze = maze
        self.scale = scale
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.pg_sprites = arcade.SpriteList()
        self.spg_sprites = arcade.SpriteList()

        # Initialiser les pacgums
        self._place_collectibles()

    # +---------------------------------------------------------------------+
    # |                               Methods                               |
    # +---------------------------------------------------------------------+

    def _place_collectibles(self):
        """
        Place les pacgums et super pacgums sur le labyrinthe en fonction
        de la configuration du maze.
        """

        nb_columns = len(self.maze[0])
        nb_lines = len(self.maze)

        # Super pacgums dans les coins
        super_pacgum_coords = [(1, 1), (1, nb_lines), (nb_columns, 1),
                               (nb_columns, nb_lines)]

        # Pas de pacgum au centre du maze
        x_center = ((nb_columns) // 2 if nb_columns % 2 == 0 else
                    (nb_columns + 1) // 2)
        y_center = ((nb_lines) // 2 + 1 if nb_lines % 2 == 0 else
                    (nb_lines + 1) // 2)
        center = (x_center, y_center)

        for y in range(1, nb_lines + 1):
            for x in range(1, nb_columns + 1):
                curr_coord = (x, y)
                if self.maze[y - 1][x - 1] == 15 or curr_coord == center:
                    continue
                center_x = (x - 0.5) * TILE_SIZE * self.scale + self.offset_x
                center_y = (y - 0.5) * TILE_SIZE * self.scale + self.offset_y

                if curr_coord in super_pacgum_coords:
                    sprite = arcade.Sprite(SUPER_PACGUM_PATH,
                                           center_x=center_x,
                                           center_y=center_y,
                                           scale=self.scale)
                    self.spg_sprites.append(sprite)
                else:
                    sprite = arcade.Sprite(PACGUM_PATH,
                                           center_x=center_x,
                                           center_y=center_y,
                                           scale=self.scale)
                    self.pg_sprites.append(sprite)

    # +---------------------------------------------------------------------+
    # |                           Get collectibles                          |
    # +---------------------------------------------------------------------+

    def remove_pacgum(self,
                      player_list: arcade.SpriteList,
                      config: ConfigModel,
                      player: PlayerModel) -> Tuple[int, bool]:

        """
        Vérifie les collisions entre le joueur et les collectibles,
        les supprime si nécessaire, et retourne les points gagnés
        et si tous les collectibles ont été collectés.

        Args:
            player_list (arcade.SpriteList): La liste de sprites du joueur.
            config (ConfigModel): La configuration du jeu, utilisée pour
                déterminer les points à attribuer.

        Returns:
            Tuple[int, bool]: Un tuple contenant les points gagnés et un
            booléen indiquant si tous les collectibles ont été collectés.
        """

        total_points = 0

        # Checking de collision

        for player_sprite in player_list:
            lst_pg = arcade.check_for_collision_with_list(player_sprite,
                                                          self.pg_sprites)
            lst_spg = arcade.check_for_collision_with_list(player_sprite,
                                                           self.spg_sprites)

        for collectible in lst_pg:
            self.pg_sprites.remove(collectible)
            total_points += config.points_per_pacgum

        for collectible in lst_spg:
            self.spg_sprites.remove(collectible)
            total_points += config.points_per_super_pacgum
            player.is_super = True
            player.super_timer = 0.0

        is_all_collected = (len(self.spg_sprites) == 0 and
                            len(self.pg_sprites) == 0)

        return (total_points, is_all_collected)

    # +---------------------------------------------------------------------+
    # |                                 Draw                                |
    # +---------------------------------------------------------------------+

    def draw(self):
        """Dessine les sprites des pacgums et super pacgums."""
        self.spg_sprites.draw()
        self.pg_sprites.draw()
