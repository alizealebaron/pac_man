# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  enemy_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 09:41:40 by rruiz           #+#    #+#               #
#  Updated: 2026/06/09 09:31:25 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+

import arcade
from src.models.configmodel import ConfigModel
from src.models.enemymodel import EnemyModel
from src.models.levelModel import Level
from src.models.playerModel import PlayerModel

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

    def __init__(self, config: ConfigModel, curr_level: Level, player: PlayerModel):
        self.config = config
        self.level = curr_level
        self.player = player
        self.enemies: list[EnemyModel] = self._create_enemies()

        self.enemies_sprite = arcade.SpriteList()
        for enemy in self.enemies:
            self.enemies_sprite.append(enemy.sprite)

    # +---------------------------------------------------------------------+
    # |                            Init Method                              |
    # +---------------------------------------------------------------------+

    def _create_enemies(self) -> list[EnemyModel]:

        enemies = []
        enemies_infos = [blinky, clyde]

        for info in enemies_infos:
            mon = info
            enemy = EnemyModel(mon, self.level.maze.maze, self.player)
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
