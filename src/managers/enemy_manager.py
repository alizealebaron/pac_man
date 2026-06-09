# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  enemy_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 09:41:40 by rruiz           #+#    #+#               #
#  Updated: 2026/06/09 08:41:06 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+

import arcade
from src.models.configmodel import ConfigModel
from src.models.enemymodel import EnemyModel
from src.models.levelModel import Level

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


blinky = 'Drifloon'
clyde = 'Duskull'
inky = 'Haunter'
pinky = 'Misdreavus'
TILE_SIZE = 64


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class EnemyManager:

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, config: ConfigModel, curr_level: Level):
        self.config = config
        self.level = curr_level
        self.enemies: list[EnemyModel] = self._create_enemies()

        self.enemies_sprite = arcade.SpriteList()
        for enemy in self.enemies:
            self.enemies_sprite.append(enemy.sprite)

    # +---------------------------------------------------------------------+
    # |                            Init Method                              |
    # +---------------------------------------------------------------------+

    def _create_enemies(self) -> list[EnemyModel]:

        enemies = []
        # width = self.level.maze._width
        # height = self.level.maze._height
        # enemies_infos = [(blinky, 0, 0), (clyde, 0, height - 1), (inky, width - 1, 0), (pinky, width - 1, height - 1)]
        enemies_infos = [(blinky, 0, 0)]

        for info in enemies_infos:
            mon, x, y = info
            enemy = EnemyModel(mon, x, y, self.level.maze.maze)
            enemies.append(enemy)
        return enemies

    # +---------------------------------------------------------------------+
    # |                               Setter                                |
    # +---------------------------------------------------------------------+

    def set_current_level(self, current_level: Level):

        self.level = current_level
        for enemy in self.enemies:
            enemy.reset_pos_and_maze(self.level.maze.maze)

    # +---------------------------------------------------------------------+
    # |                            View Method                              |
    # +---------------------------------------------------------------------+

    def on_update(self, delta_time):
        for enemy in self.enemies:
            enemy.on_update(delta_time)

    def draw(self):
        self.enemies_sprite.draw()
