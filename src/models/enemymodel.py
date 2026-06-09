# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  enemymodel.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 09:21:58 by rruiz           #+#    #+#               #
#  Updated: 2026/06/08 17:41:59 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
import json
from typing import Tuple
from src.models.animated_sprite import AnimatedSprite
from src.models.enemydatamodel import EnemyDataModel
from src.models.playerModel import PlayerModel

SPEED = 1
TRANSITION_DISTANCE = 64
ENEMY_FILE = 'data/enemy_data.json'

OPPOSITES = {
    'up': 'down',
    'right': 'left',
    'down': 'up',
    'left': 'right'
}

class EnemyModel:
    def __init__(self, mon: str, x: int, y: int, maze: list[list[int]], player: PlayerModel):
        self.mon = mon
        self.start_pos = (x, y)
        self.x = x
        self.y = y
        self.player = player

        enemy_data = self._get_enemy_data(mon)

        self.scale = enemy_data.scale
        self.sprite = AnimatedSprite(mon, enemy_data.width, enemy_data.height, enemy_data.nb_anim, is_enemy=True)
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        self.maze = self._rev_maze(maze)
        self.algo = self._asign_algo()
        self.current_direction = None
        self.last_direction = None
        self.pixel_offset_x = 0
        self.pixel_offset_y = 0
        self.offset_y = self._get_offset_y()

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
                return 'behind'
            case 'Haunter':
                return 'random'
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
            case _:
                return (0, 0)

    def _random_move(self) -> Tuple[int]:
        possible_dir = self._get_direction()

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
        possible_dir = self._get_direction()
        min_dist = None

        for direction in possible_dir:
            match direction:
                case 'up':
                    distance = abs(self.x - self.player.x) + abs((self.y + 1) - self.player.y)
                case 'right':
                    distance = abs((self.x + 1) - self.player.x) + abs(self.y - self.player.y)
                case 'down':
                    distance = abs(self.x - self.player.x) + abs((self.y - 1) - self.player.y)
                case 'left':
                    distance = abs((self.x - 1) - self.player.x) + abs(self.y - self.player.y)

            if min_dist is None:
                min_dist = distance
                next_direction = direction

            if distance < min_dist:
                min_dist = distance
                next_direction = direction

        return self._direction_to_velocity(next_direction)

    def _get_direction(self) -> list[str]:
        possible_dir = []
        if not self.maze[self.y][self.x] & 1:
            possible_dir.append('up')
        if not self.maze[self.y][self.x] & 2:
            possible_dir.append('right')
        if not self.maze[self.y][self.x] & 4:
            possible_dir.append('down')
        if not self.maze[self.y][self.x] & 8:
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
