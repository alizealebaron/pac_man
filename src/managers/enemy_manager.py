# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  enemy_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 09:41:40 by rruiz           #+#    #+#               #
#  Updated: 2026/06/12 11:08:03 by rruiz           ###   ########.fr        #
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

    """
    Manager pour les ennemis.

    Attributes:
        config (ConfigModel): La configuration du jeu.
        level (Level): Le niveau actuel du jeu.
        player (PlayerModel): Le modèle du joueur.
        enemies (list[EnemyModel]): La liste des ennemis du niveau.
        enemies_sprite (arcade.SpriteList): La liste de sprites des ennemis.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, config: ConfigModel, curr_level: Level,
                 player: PlayerModel):

        """
        Initialise le manager des ennemis.

        Args:
            config (ConfigModel): La configuration du jeu.
            curr_level (Level): Le niveau actuel du jeu.
            player (PlayerModel): Le modèle du joueur.
        """

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
        """
        Crée les ennemis du niveau.

        Returns:
            list[EnemyModel]: La liste des ennemis du niveau.
        """

        enemies = []
        enemies_infos = [blinky, clyde, inky, pinky]
        # enemies_infos = [clyde]

        for info in enemies_infos:
            mon = info
            enemy = EnemyModel(mon, self.level.maze.maze, self.player)
            enemies.append(enemy)
        return enemies

    # +---------------------------------------------------------------------+
    # |                               Setter                                |
    # +---------------------------------------------------------------------+

    def set_current_level(self, current_level: Level) -> None:
        """
        Met à jour le niveau actuel pour les ennemis.

        Args:
            current_level (Level): Le nouveau niveau actuel.

        """

        self.level = current_level
        for enemy in self.enemies:
            enemy.reset_pos_and_maze(self.level.maze.maze)

        self.enemies_sprite.clear()
        for enemy in self.enemies:
            self.enemies_sprite.append(enemy.sprite)

    def reset_enemy(self) -> None:
        """Réinitialise les ennemis."""
        for enemy in self.enemies:
            enemy.sprite.color = arcade.color.WHITE
            enemy.is_fleeing = False
            enemy.already_dead = False
            enemy.reset_pos()

    # +---------------------------------------------------------------------+
    # |                            View Method                              |
    # +---------------------------------------------------------------------+

    def on_update(self, delta_time) -> None:
        """Met à jour les ennemis."""

        for enemy in self.enemies:
            enemy.on_update(delta_time)

    def draw(self) -> None:
        """Dessine les ennemis."""
        self.enemies_sprite.draw()

    def get_respawning_enemies(self):
        respawning = []
        for enemy in self.enemies:
            if enemy.is_dead is True:
                respawning.append(enemy)

        return respawning
