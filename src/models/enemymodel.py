# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  enemymodel.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 09:21:58 by rruiz           #+#    #+#               #
#  Updated: 2026/06/12 17:20:42 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+

import random
import json
from typing import Tuple, Optional
import arcade
from src.models.animated_sprite import AnimatedSprite
from src.models.enemydatamodel import EnemyDataModel
from src.models.playerModel import PlayerModel

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


SPEED = 1
TRANSITION_DISTANCE = 64
ENEMY_FILE = 'data/enemy_data.json'

OPPOSITES = {
    'up': 'down',
    'right': 'left',
    'down': 'up',
    'left': 'right'
}


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class EnemyModel:
    """
    Modèle pour les ennemis du jeu.

    Attributes:
        mon (str): Le nom de l'ennemi.
        maze (list[list[int]]): Le labyrinthe du niveau.
        start_pos (Tuple[int, int]): La position de départ de l'ennemi.
        x (int): La position x actuelle de l'ennemi.
        y (int): La position y actuelle de l'ennemi.
        player (PlayerModel): Le modèle du joueur.
        scale (float): L'échelle du sprite de l'ennemi.
        sprite (AnimatedSprite): Le sprite animé de l'ennemi.
        algo (str): L'algorithme de déplacement de l'ennemi.
        current_direction (str): La direction actuelle de l'ennemi.
        last_direction (str): La dernière direction de l'ennemi.
        pixel_offset_x (int): Le décalage en pixels sur l'axe x pour
            l'animation de déplacement.
        pixel_offset_y (int): Le décalage en pixels sur l'axe y pour
            l'animation de déplacement.
        offset_y (int): Le décalage vertical pour le positionnement du sprite.
        is_fleeing (bool): Est ce que l'ennemie est en train de fuir le player.
        is_dead (bool): Est ce que l'ennemie est mort.
        respawn_timer (float): Le temps avant le respawn de l'ennemie.
        just_respawned (bool): Est ce que l'ennemie viens de respawn.
        death_timer (int): Le temps de mort de l'ennemie.
        already_dead (bool): Est ce que l'ennemie est deja mort.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, mon: str, maze: list[list[int]], player: PlayerModel):

        """
        Initialise le modèle de l'ennemi.

        Args:
            mon (str): Le nom de l'ennemi.
            maze (list[list[int]]): Le labyrinthe du niveau.
            player (PlayerModel): Le modèle du joueur.
        """

        self.mon = mon
        self.maze = self._rev_maze(maze)
        self.start_pos = self._get_start_pos()
        self.x, self.y = self.start_pos
        self.player = player

        enemy_data = self._get_enemy_data(mon)

        self.scale = enemy_data.scale
        self.sprite = AnimatedSprite(mon, enemy_data.width,
                                     enemy_data.height, enemy_data.nb_anim,
                                     is_enemy=True)
        self.sprite.owner = self
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        self.algo = self._asign_algo()
        self.current_direction: Optional[Tuple[int, int]] = None
        self.last_direction: Optional[str] = None
        self.pixel_offset_x = 0
        self.pixel_offset_y = 0
        self.offset_y = self._get_offset_y()
        self.is_fleeing = False
        self.is_dead = False
        self.respawn_timer = 0.0
        self.just_respawned = False
        self.death_timer = 3
        self.already_dead = False

    # +---------------------------------------------------------------------+
    # |                            Reset Method                             |
    # +---------------------------------------------------------------------+

    def reset_pos_and_maze(self, maze: list[list[int]]) -> None:
        """
        Réinitialise la position de l'ennemi et met à jour le labyrinthe.

        Args:
            maze (list[list[int]]): Le nouveau labyrinthe du niveau.
        """

        self.current_direction = None
        self.last_direction = None
        self.maze = self._rev_maze(maze)
        self.start_pos = self._get_start_pos()
        self.reset_pos()
        self._reset_death()

    def reset_pos(self) -> None:
        """
        Réinitialise la position de l'ennemi à sa position de départ et
        réinitialise les offsets pour l'animation de déplacement.
        """

        x, y = self.start_pos
        self.x = x
        self.y = y
        self.pixel_offset_x = 0
        self.pixel_offset_y = 0

    def _reset_death(self) -> None:
        self.is_fleeing = False
        self.is_dead = False
        self.respawn_timer = 0.0
        self.just_respawned = False

    # +---------------------------------------------------------------------+
    # |                            View Method                              |
    # +---------------------------------------------------------------------+

    def on_update(self, delta_time: float) -> None:

        """
        Met à jour la position de l'ennemi en fonction de son algorithme de
        déplacement et met à jour son sprite.

        Args:
            delta_time (float): Le temps écoulé depuis la dernière mise à jour.
        """

        if self.pixel_offset_x == 0 and self.pixel_offset_y == 0:
            self.current_direction = self._enemy_move()

        vx, vy = self.current_direction if self.current_direction else (0, 0)

        self.pixel_offset_x += vx * SPEED
        self.pixel_offset_y += vy * SPEED

        if self.pixel_offset_x >= TRANSITION_DISTANCE:
            self.x += 1
            self.pixel_offset_x = 0
            self.last_direction = (self._velocity_to_direction(
                self.current_direction))
            self.current_direction = None
        elif self.pixel_offset_x <= -TRANSITION_DISTANCE:
            self.x -= 1
            self.pixel_offset_x = 0
            self.last_direction = (self._velocity_to_direction(
                self.current_direction))
            self.current_direction = None

        if self.pixel_offset_y >= TRANSITION_DISTANCE:
            self.y += 1
            self.pixel_offset_y = 0
            self.last_direction = (self._velocity_to_direction(
                self.current_direction))
        elif self.pixel_offset_y <= -TRANSITION_DISTANCE:
            self.y -= 1
            self.pixel_offset_y = 0
            self.last_direction = (self._velocity_to_direction(
                self.current_direction))
            self.current_direction = None

        if self.is_dead:
            self.respawn_timer += delta_time
            self.reset_pos()
            if self.respawn_timer >= self.death_timer:
                self.is_dead = False
                self.just_respawned = True
                self.respawn_timer = 0.0
                self.is_fleeing = False

        if self.is_fleeing:
            if self.sprite.color != arcade.color.BLEU_DE_FRANCE:
                self.sprite.color = arcade.color.BLEU_DE_FRANCE
        else:
            if self.sprite.color != arcade.color.WHITE:
                self.sprite.color = arcade.color.WHITE

        self.sprite.on_update(delta_time)

    # +---------------------------------------------------------------------+
    # |                                Algo                                 |
    # +---------------------------------------------------------------------+

    def _asign_algo(self) -> str:
        """
        Assigne l'algorithme de déplacement en fonction du type d'ennemi.

        Returns:
            str: Le nom de l'algorithme de déplacement assigné à l'ennemi.
        """

        match self.mon:
            case 'Drifloon':
                return 'random'
            case 'Duskull':
                return 'bfs'
            case 'Haunter':
                return 'behind'
            case 'Misdreavus':
                return 'random'
            case _:
                return 'random'

    def _enemy_move(self) -> Tuple[int, int]:
        """
        Détermine la direction de déplacement de l'ennemi en fonction de son
        algorithme de déplacement.

        Returns:
            Tuple[int, int]: Un tuple représentant la direction de déplacement
            de l'ennemi sous la forme (vx, vy), où vx est la composante
            horizontale et vy est la composante verticale.
        """
        if self.is_fleeing:
            return self._escape_move()
        match self.algo:
            case 'random':
                return self._random_move()
            case 'behind':
                return self._behind_move()
            case 'bfs':
                return self._in_front_move()
            case _:
                return (0, 0)

    def _random_move(self) -> Tuple[int, int]:

        """
        Détermine une direction de déplacement aléatoire pour l'ennemi parmi
        les directions possibles, en évitant de revenir en arrière.

        Returns:
            Tuple[int]: Un tuple représentant la direction de déplacement de
            l'ennemi sous la forme (vx, vy), où vx est la composante
            horizontale et vy est la composante verticale.
        """

        possible_dir = self._get_direction(self.x, self.y)

        if self.last_direction:
            opposite = OPPOSITES.get(self.last_direction)
            filtered_dir = []
            for direction in possible_dir:
                if direction != opposite:
                    filtered_dir.append(direction)

            if filtered_dir:
                possible_dir = filtered_dir

        return self._direction_to_velocity(random.choice(possible_dir))

    def _behind_move(self) -> Tuple[int, int]:
        distance = abs(self.x - self.player.x) + abs(self.y - self.player.y)

        if distance <= 1:
            tx, ty = self.player.x, self.player.y
        else:
            tx, ty = self._get_behind_player()
        parent = self._bfs_algo(tx, ty)

        if parent is None:
            return (0, 0)

        node = (tx, ty)
        while parent[node] != (self.x, self.y):
            node = parent[node]

        if node == (self.x, self.y + 1):
            return self._direction_to_velocity('up')
        if node == (self.x + 1, self.y):
            return self._direction_to_velocity('right')
        if node == (self.x, self.y - 1):
            return self._direction_to_velocity('down')
        if node == (self.x - 1, self.y):
            return self._direction_to_velocity('left')

        return (0, 0)

    def _in_front_move(self) -> Tuple[int, int]:
        """
        Détermine la direction de déplacement de l'ennemi en utilisant un
        algorithme de recherche en largeur (BFS) pour trouver le chemin le plus
        court vers le joueur, puis choisit la direction qui rapproche l'ennemi
        du joueur en suivant ce chemin.

        Returns:
            Tuple[int]: Un tuple représentant la direction de déplacement de
            l'ennemi sous la forme (vx, vy), où vx est la composante
            horizontale et vy est la composante verticale.
        """
        parent = self._bfs_algo(self.player.x, self.player.y)

        if parent is None:
            return (0, 0)

        node = (self.player.x, self.player.y)
        while parent[node] != (self.x, self.y):
            node = parent[node]

        if node == (self.x, self.y + 1):
            return self._direction_to_velocity('up')
        if node == (self.x + 1, self.y):
            return self._direction_to_velocity('right')
        if node == (self.x, self.y - 1):
            return self._direction_to_velocity('down')
        if node == (self.x - 1, self.y):
            return self._direction_to_velocity('left')

        return (0, 0)

    def _bfs_algo(
            self,
            target_x: int,
            target_y: int
            ) -> dict[Tuple[int, int], Tuple[int, int]] | None:
        """
        Implémente un algorithme de recherche en largeur (BFS) pour trouver le
        chemin le plus court entre la position actuelle de l'ennemi et la
        position du joueur dans le labyrinthe, en tenant compte des murs et des
        passages.

        Returns:
            dict: Un dictionnaire où les clés sont les coordonnées des nœuds
            visités et les valeurs sont les coordonnées du nœud parent,
            permettant de reconstruire le chemin de l'ennemi vers le joueur.
        """

        visited = set()
        queue = [(self.x, self.y)]
        parent = {}

        while len(queue) > 0:
            current = queue.pop(0)
            visited.add(current)

            possible_dir = self._get_direction(current[0], current[1])
            neighbor = []
            for dir in possible_dir:
                x, y = current
                match dir:
                    case 'up':
                        neighbor.append((x, y + 1))
                    case 'right':
                        neighbor.append((x + 1, y))
                    case 'down':
                        neighbor.append((x, y - 1))
                    case 'left':
                        neighbor.append((x - 1, y))

            for n in neighbor:
                if n not in visited:
                    visited.add(n)
                    parent[n] = current
                    if n == (target_x, target_y):
                        return parent
                    queue.append(n)

        return None

    def _escape_move(self) -> Tuple[int, int]:
        possible_dir = self._get_direction(self.x, self.y)

        if not possible_dir:
            return (0, 0)

        best_dir = None
        best_distance = -1

        for dir in possible_dir:
            match dir:
                case 'up':
                    x, y = self.x, self.y + 1
                case 'right':
                    x, y = self.x + 1, self.y
                case 'down':
                    x, y = self.x, self.y - 1
                case 'left':
                    x, y = self.x - 1, self.y

            distance = abs(self.player.x - x) + abs(self.player.y - y)

            if distance > best_distance:
                best_dir = dir
                best_distance = distance
            elif distance == best_distance:
                if random.choice([True, False]):
                    best_dir = dir

        return self._direction_to_velocity(best_dir)

    # +---------------------------------------------------------------------+
    # |                                Utils                                |
    # +---------------------------------------------------------------------+

    def _get_behind_player(self) -> Tuple[int, int]:

        """
        Calcule les coordonnées d'une position derrière le joueur par
        rapport à l'ennemi, en fonction de la direction actuelle du joueur.

        Returns:
            Tuple[int, int]: Un tuple représentant les coordonnées de la
            position derrière le joueur sous la forme (x, y).
        """

        match self.player.direction:
            case 'up':
                x, y = self.player.x, self.player.y - 1
            case 'right':
                x, y = self.player.x - 1, self.player.y
            case 'down':
                x, y = self.player.x, self.player.y + 1
            case 'left':
                x, y = self.player.x + 1, self.player.y
            case _:
                return self.player.x, self.player.y

        if 0 <= y < len(self.maze) and 0 <= x < len(self.maze[0]):
            if self._get_direction(x, y):
                return x, y

        return self.player.x, self.player.y

    def _get_direction(self, x: int, y: int) -> list[str]:

        """
        Détermine les directions de déplacement possibles pour l'ennemi à
        partir de sa position actuelle dans le labyrinthe, en vérifiant les
        murs et les passages.

        Args:
            x (int): La position x actuelle de l'ennemi.
            y (int): La position y actuelle de l'ennemi.

        Returns:
            list[str]: Une liste de directions possibles parmi 'up', 'right',
            'down', 'left'.
        """

        possible_dir = []
        if not self.maze[y][x] & 1:
            possible_dir.append('up')
        if not self.maze[y][x] & 2:
            possible_dir.append('right')
        if not self.maze[y][x] & 4:
            possible_dir.append('down')
        if not self.maze[y][x] & 8:
            possible_dir.append('left')
        return possible_dir

    def _direction_to_velocity(self, direction: str | None) -> Tuple[int, int]:

        """
        Convertit une direction de déplacement en une composante de vitesse
        correspondante.

        Args:
            direction (str): La direction de déplacement, parmi 'up', 'right',
            'down', 'left'.

        Returns:
            Tuple[int]: Un tuple représentant la composante de vitesse
            correspondante à la direction donnée, sous la forme (vx, vy), où
            vx est la composante horizontale et vy est la composante verticale.
        """

        match direction:
            case 'up':
                self.sprite.current_direction = 'up'
                return (0, 1)
            case 'right':
                self.sprite.current_direction = 'right'
                return (1, 0)
            case 'down':
                self.sprite.current_direction = 'down'
                return (0, -1)
            case 'left':
                self.sprite.current_direction = 'left'
                return (-1, 0)
            case _:
                return (0, 0)

    def _velocity_to_direction(
            self,
            velocity: Tuple[int, int] | None
            ) -> str | None:

        """
        Convertit une composante de vitesse en une direction de déplacement
        correspondante.

        Args:
            velocity (Tuple[int]): Un tuple représentant la composante de
            vitesse sous la forme (vx, vy), où vx est la composante
            horizontale et vy est la composante verticale.

        Returns:
            Tuple[int]: La direction de déplacement correspondante à la
            composante de vitesse donnée, parmi 'up', 'right', 'down', 'left'.
        """

        match velocity:
            case (0, 1):
                return 'up'
            case (1, 0):
                return 'right'
            case (0, -1):
                return 'down'
            case (-1, 0):
                return 'left'
            case _:
                return None

    def _rev_maze(self, maze: list[list[int]]) -> list[list[int]]:

        """
        Inverse le labyrinthe pour que les coordonnées soient dans le bon ordre
        pour les ennemis.

        Args:
            maze (list[list[int]]): Le labyrinthe à inverser.

        Returns:
            list[list[int]]: Le labyrinthe inversé.
        """

        rev_maze: list[list[int]] = []
        for i in range(len(maze) - 1, -1, -1):
            rev_maze.append(maze[i])

        return rev_maze

    def _retrieve_enemy_data_from_json(self) -> list[EnemyDataModel]:

        """
        Récupère les données des ennemis à partir d'un fichier JSON et les
        convertit en une liste d'instances de EnemyDataModel.

        Returns:
            list[EnemyDataModel]: Une liste d'instances de EnemyDataModel
            contenant les données des ennemis.
        """

        lst_enemy = []
        try:
            with open(ENEMY_FILE, "r") as file:
                data = json.load(file)
                lst_enemy = [EnemyDataModel(**arg) for arg in data]
        except json.JSONDecodeError as e:
            raise (e)
        except Exception as e:
            raise (e)

        return lst_enemy

    def _get_enemy_data(self, enemy_name: str) -> EnemyDataModel:

        """
        Récupère les données d'un ennemi spécifique à partir du fichier JSON
        en fonction de son nom.

        Args:
            enemy_name (str): Le nom de l'ennemi dont les données doivent être
                récupérées.
        Returns:
            EnemyDataModel: Une instance de EnemyDataModel contenant les
                données de l'ennemi spécifié.
        Raises:
            ValueError: Si l'ennemi spécifié n'est pas trouvé dans le fichier
                JSON.
        """

        enemies_data = self._retrieve_enemy_data_from_json()
        for enemy_data in enemies_data:
            if enemy_data.name == enemy_name:
                return enemy_data
        raise ValueError(f"Enemy {enemy_name} not found in enemy_data.json")

    def _get_offset_y(self) -> int:

        """
        Détermine le décalage vertical pour le positionnement du sprite de
        l'ennemi en fonction de son type.

        Returns:
            int: Le décalage vertical en pixels pour le positionnement du
                sprite de l'ennemi.
        """

        match self.mon:
            case 'Drifloon':
                return 15
            case 'Duskull':
                return 10
            case 'Haunter':
                return 10
            case 'Misdreavus':
                return 10
            case _:
                return 0

    def _get_start_pos(self) -> Tuple[int, int]:

        """
        Détermine la position de départ de l'ennemi en fonction de son type.
        Returns:
            Tuple[int]: Un tuple représentant les coordonnées de la position de
                départ de l'ennemi sous la forme (x, y).
        """

        match self.mon:
            case 'Drifloon':
                return (0, 0)
            case 'Duskull':
                return (0, len(self.maze) - 1)
            case 'Haunter':
                return (len(self.maze[0]) - 1, 0)
            case 'Misdreavus':
                return (len(self.maze[0]) - 1, len(self.maze) - 1)
            case _:
                return (0, 0)

    def die(self) -> None:
        self.is_dead = True
        self.already_dead = True
        self.is_fleeing = False
        self.sprite.color = arcade.color.WHITE
