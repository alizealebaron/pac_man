# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  enemymodel.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 09:21:58 by rruiz           #+#    #+#               #
#  Updated: 2026/06/09 13:25:43 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+

import random
import json
from typing import Tuple
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

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, mon: str, maze: list[list[int]], player: PlayerModel):

        self.mon = mon
        self.maze = self._rev_maze(maze)
        self.start_pos = self._get_start_pos()
        self.x, self.y = self.start_pos
        self.player = player

        enemy_data = self._get_enemy_data(mon)

        self.scale = enemy_data.scale
        self.sprite = AnimatedSprite(mon, enemy_data.width, enemy_data.height, enemy_data.nb_anim, is_enemy=True)
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        self.algo = self._asign_algo()
        self.current_direction = None
        self.last_direction = None
        self.pixel_offset_x = 0
        self.pixel_offset_y = 0
        self.offset_y = self._get_offset_y()

    # +---------------------------------------------------------------------+
    # |                            Reset Method                             |
    # +---------------------------------------------------------------------+

    def reset_pos_and_maze(self, maze: list[list[int]]):

        self.current_direction = None
        self.last_direction = None
        self.maze = self._rev_maze(maze)
        self.start_pos = self._get_start_pos()
        self.reset_pos()

    def reset_pos(self):

        x, y = self.start_pos
        self.x = x
        self.y = y
        self.pixel_offset_x = 0
        self.pixel_offset_y = 0

    # +---------------------------------------------------------------------+
    # |                            View Method                              |
    # +---------------------------------------------------------------------+

    def on_update(self, delta_time):
        if self.pixel_offset_x == 0 and self.pixel_offset_y == 0:
            self.current_direction = self._enemy_move()

        vx, vy = self.current_direction if self.current_direction else (0, 0)

        self.pixel_offset_x += vx * SPEED
        self.pixel_offset_y += vy * SPEED

        if self.pixel_offset_x >= TRANSITION_DISTANCE:
            self.x += 1
            self.pixel_offset_x = 0
            self.last_direction = self._velocity_to_direction(self.current_direction)
            self.current_direction = None
        elif self.pixel_offset_x <= -TRANSITION_DISTANCE:
            self.x -= 1
            self.pixel_offset_x = 0
            self.last_direction = self._velocity_to_direction(self.current_direction)
            self.current_direction = None

        if self.pixel_offset_y >= TRANSITION_DISTANCE:
            self.y += 1
            self.pixel_offset_y = 0
            self.last_direction = self._velocity_to_direction(self.current_direction)
            self.current_direction = None
        elif self.pixel_offset_y <= -TRANSITION_DISTANCE:
            self.y -= 1
            self.pixel_offset_y = 0
            self.last_direction = self._velocity_to_direction(self.current_direction)
            self.current_direction = None

        self.sprite.on_update(delta_time)

    def _asign_algo(self) -> str:
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
        match self.algo:
            case 'random':
                return self._random_move()
            case 'behind':
                return self._behind_move()
            case 'bfs':
                return self._in_front_move()
            case _:
                return (0, 0)

    def _random_move(self) -> Tuple[int]:
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

    def _behind_move(self) -> Tuple[int]:
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

    def _in_front_move(self) -> Tuple[int]:
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

    def _bfs_algo(self, target_x: int, target_y: int):
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

    def _get_behind_player(self) -> Tuple[int, int]:
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

    def _direction_to_velocity(self, direction: str) -> Tuple[int]:
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

    def _velocity_to_direction(self, velocity: Tuple[int]) -> Tuple[int]:
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
                return (0, 0)

    def _rev_maze(self, maze: list[list[int]]) -> list[list[int]]:
        rev_maze: list[list[int]] = []
        for i in range(len(maze) - 1, -1, -1):
            rev_maze.append(maze[i])

        return rev_maze

    def _retrieve_enemy_data_from_json(self) -> list[EnemyDataModel]:
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
        enemies_data = self._retrieve_enemy_data_from_json()
        for enemy_data in enemies_data:
            if enemy_data.name == enemy_name:
                return enemy_data
        raise ValueError(f"Enemy {enemy_name} not found in enemy_data.json")

    def _get_offset_y(self):
        match self.mon:
            case 'Drifloon':
                return 15
            case 'Duskull':
                return 10
            case 'Haunter':
                return 10
            case 'Misdreavus':
                return 10

    def _get_start_pos(self) -> Tuple[int]:
        match self.mon:
            case 'Drifloon':
                return (0, 0)
            case 'Duskull':
                return (0, len(self.maze) - 1)
            case 'Haunter':
                return (len(self.maze[0]) - 1, 0)
            case 'Misdreavus':
                return (len(self.maze[0]) - 1, len(self.maze) - 1)