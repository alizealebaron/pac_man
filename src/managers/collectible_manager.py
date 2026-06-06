# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : collectible_manager.py                                           #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : Invalid date        by -----------                             #
# @update   : 2026/06/02 15:08:59 by alebaron                                #
# ************************************************************************** #


import arcade
from src.models.configmodel import ConfigModel

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
    """Gère le placement et l'affichage des pacgums"""

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, maze: list[list[int]], scale: float = 1.0,
                 offset_x: float = 0.0, offset_y: float = 0.0):
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

        nb_columns = len(self.maze[0])
        nb_lines = len(self.maze)

        # Super pacgums dans les coins
        super_pacgum_coords = [(1, 1), (1, nb_lines), (nb_columns, 1),
                               (nb_columns, nb_lines)]

        # Pas de pacgum au centre du maze
        x_center = (nb_columns) // 2 if nb_columns % 2 == 0 else (nb_columns + 1) // 2
        y_center = (nb_lines) // 2 + 1 if nb_lines % 2 == 0 else (nb_lines + 1) // 2
        center = (x_center, y_center)

        for y in range(1, nb_lines + 1):
            for x in range(1, nb_columns + 1):
                curr_coord = (x, y)
                if self.maze[y - 1][x - 1] == 15 or curr_coord == center:
                    continue
                center_x = (x - 0.5) * TILE_SIZE * self.scale + self.offset_x
                center_y = (y - 0.5) * TILE_SIZE * self.scale + self.offset_y

                if curr_coord in super_pacgum_coords:
                    sprite = arcade.Sprite(SUPER_PACGUM_PATH, center_x=center_x, center_y=center_y, scale=self.scale)
                    self.spg_sprites.append(sprite)
                else:
                    sprite = arcade.Sprite(PACGUM_PATH, center_x=center_x, center_y=center_y, scale=self.scale)
                    self.pg_sprites.append(sprite)

    # +---------------------------------------------------------------------+
    # |                           Get collectibles                          |
    # +---------------------------------------------------------------------+

    def remove_pacgum(self,
                      player_list: arcade.SpriteList,
                      config: ConfigModel,
                      x: int,
                      y: int) -> int:
        total_points = 0

        # Checking de collision

        for player in player_list:
            lst_pg = arcade.check_for_collision_with_list(player,
                                                          self.pg_sprites)
            lst_spg = arcade.check_for_collision_with_list(player,
                                                           self.spg_sprites)

        for collectible in lst_pg:
            self.pg_sprites.remove(collectible)
            total_points += config.points_per_pacgum

        for collectible in lst_spg:
            self.spg_sprites.remove(collectible)
            total_points += config.points_per_super_pacgum

        is_all_collected = (len(self.spg_sprites) == 0 and
                            len(self.pg_sprites) == 0)

        return (total_points, is_all_collected)

    # +---------------------------------------------------------------------+
    # |                                 Draw                                |
    # +---------------------------------------------------------------------+

    def draw(self):
        """ Draw everything """
        self.spg_sprites.draw()
        self.pg_sprites.draw()
