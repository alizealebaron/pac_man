# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 20:04:34 by alebaron        #+#    #+#               #
#  Updated: 2026/06/02 20:04:41 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade
from src.view.maze_renderer import MazeRenderer
from src.managers.collectible_manager import CollectibleManager
from src.view.save_score.win_view import WinView
from src.pacmanManager import PacmanManager

# +-------------------------------------------------------------------------+
# |                                 Global                                  |
# +-------------------------------------------------------------------------+

BACKGROUND_PATH = "assets/background/game_background.png"
MUSIC_PATH = "assets/music/game_theme.mp3"

SPEED = 5.0
TILE_SIZE = 64
TRANSITION_DISTANCE = 64

# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class GameView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, manager: PacmanManager, music_player=None, music=None):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Récupération de la hauteur et de la largeur
        self.largeur = self.window.width
        self.hauteur = self.window.height

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BLACK)

        # Récupération du manager et du labyrinthe
        self.manager = manager
        num_level = self.manager.actual_level
        self.current_maze = self.manager.level[num_level].maze.maze

        # Récupération du labyrinthe à l'envers pour Arcade
        self.rev_maze = self._rev_maze(self.current_maze)

        # Initialiser les renderers
        self.maze_renderer = MazeRenderer(self.rev_maze, self.largeur,
                                          self.hauteur)
        self.scale = self.maze_renderer.scale
        self.offset_x, self.offset_y = (self.maze_renderer.offset_x,
                                        self.maze_renderer.offset_y)

        # Initialisation du gestionnaire de collectibles
        self.collectible_manager = CollectibleManager(self.rev_maze,
                                                      self.scale,
                                                      self.offset_x,
                                                      self.offset_y)

        # Initialisation des coords du player et de ses sprites
        self._player_original_pos()
        self.manager.player.sprite.scale = (self.manager.player.pokemon.scale *
                                            self.scale)
        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.manager.player.sprite)

        # Music
        self.music_player = music_player
        self.music = music

        self.background = arcade.load_texture(BACKGROUND_PATH)

        pokemon = self.manager.player.pokemon.name
        self.pokemon_sprite = arcade.load_texture(f"assets/sprite/pokemon/"
                                                  f"{pokemon}/portraits/"
                                                  "Normal.png")
        self.sprite_frame = arcade.load_texture("assets/sprite/face_frame.png")

        # Détection de la fin d'un level
        self.is_finished = 0  # 0: Play, 1: Win, 2: GameOver

    # +---------------------------------------------------------------------+
    # |                               Methods                               |
    # +---------------------------------------------------------------------+

    def on_draw(self):
        """ Draw everything """
        self.clear()

        # Affichage du background
        self.draw_background()

        # Affichage du labyrinthe et des pacgums
        self.maze_renderer.draw()
        self.collectible_manager.draw()

        # Récupération des coordonnées du joueur en pixel
        pixel_x = self.manager.player.x * TILE_SIZE + 32 + self.manager.player.pixel_offset_x
        pixel_y = self.manager.player.y * TILE_SIZE + 32 + self.manager.player.pixel_offset_y

        # Affichage du joueur au centre du labyrinthe
        self.manager.player.sprite.center_x = pixel_x * self.scale + self.offset_x
        self.manager.player.sprite.center_y = pixel_y * self.scale + self.offset_y - 10
        self.player_sprites.draw()

        # Affichage de l'HUD
        self.draw_UHD()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Vérification que le jeu est toujours en cours
        if (self.is_finished == 1):
            if (self.manager.actual_level == (len(self.manager.level) - 1)):
                self.music.stop(self.music_player)
                self.window.set_mouse_visible(True)
                self.window.show_view(WinView(self.window))
            else:
                self.manager.actual_level += 1
                self.window.show_view(GameView(self.manager, self.music_player,
                                               self.music))


        vx, vy = self._player_move()

        self.manager.player.pixel_offset_x += vx * SPEED
        self.manager.player.pixel_offset_y += vy * SPEED

        if self.manager.player.pixel_offset_x >= TRANSITION_DISTANCE:
            self.manager.player.x += 1
            self.manager.player.pixel_offset_x = 0
            self.get_collectibles()
        elif self.manager.player.pixel_offset_x <= -TRANSITION_DISTANCE:
            self.manager.player.x -= 1
            self.manager.player.pixel_offset_x = 0
            self.get_collectibles()

        if self.manager.player.pixel_offset_y >= TRANSITION_DISTANCE:
            self.manager.player.y += 1
            self.manager.player.pixel_offset_y = 0
            self.get_collectibles()
        elif self.manager.player.pixel_offset_y <= -TRANSITION_DISTANCE:
            self.manager.player.y -= 1
            self.manager.player.pixel_offset_y = 0
            self.get_collectibles()

        self.manager.player.sprite.on_update(delta_time)

    def on_show_view(self):
        """Appelé quand la vue change"""
        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH,
                                      streaming=True)
            self.music_player = self.music.play(volume=1, loop=True)

    # +---------------------------------------------------------------------+
    # |                 Methods for recovering collectibles                 |
    # +---------------------------------------------------------------------+

    def get_collectibles(self):

        x = self.manager.player.x
        y = self.manager.player.y

        p = self.collectible_manager.remove_pacgum(self.player_sprites,
                                                   self.manager.config,
                                                   x,
                                                   y)

        points, self.is_finished = p
        self.manager.player.score += points

    # +---------------------------------------------------------------------+
    # |                            Game Methods                             |
    # +---------------------------------------------------------------------+

    def _rev_maze(self, maze: list[list[int]]) -> list[list[int]]:
        rev_maze: list[list[int]] = []
        for i in range(len(maze) - 1, -1, -1):
            rev_maze.append(maze[i])

        return rev_maze

    def _player_original_pos(self):
        nb_columns = len(self.rev_maze[0])
        nb_lines = len(self.rev_maze)

        grid_x = (nb_columns) // 2 if nb_columns % 2 == 0 else (nb_columns + 1) // 2
        grid_y = (nb_lines) // 2 + 1 if nb_lines % 2 == 0 else (nb_lines + 1) // 2

        self.manager.player.x = grid_x - 1
        self.manager.player.y = grid_y - 1

        self.manager.player.pixel_offset_x = 0.0
        self.manager.player.pixel_offset_y = 0.0

    def on_key_press(self, symbol, modifiers):
        match symbol:
            case arcade.key.UP:
                self.manager.player.next_direction = "up"
            case arcade.key.LEFT:
                self.manager.player.next_direction = "left"
            case arcade.key.DOWN:
                self.manager.player.next_direction = "down"
            case arcade.key.RIGHT:
                self.manager.player.next_direction = "right"

        match symbol:
            case arcade.key.W:
                self.manager.player.next_direction = "up"
            case arcade.key.A:
                self.manager.player.next_direction = "left"
            case arcade.key.S:
                self.manager.player.next_direction = "down"
            case arcade.key.D:
                self.manager.player.next_direction = "right"

    def _player_move(self) -> tuple[float, float]:
        player = self.manager.player

        if player.next_direction and self._is_opposite_direction(player.direction, player.next_direction):
            player.direction = player.next_direction
            player.next_direction = None

        elif player.pixel_offset_x == 0 and player.pixel_offset_y == 0:
            if player.next_direction and self._can_move(player.next_direction):
                player.direction = player.next_direction
                player.next_direction = None

        if player.direction:
            if player.pixel_offset_x != 0 or player.pixel_offset_y != 0:
                match player.direction:
                    case "up":
                        self.manager.player.sprite.current_direction = 'up'
                        return (0, 1)
                    case "right":
                        self.manager.player.sprite.current_direction = 'right'
                        return (1, 0)
                    case "down":
                        self.manager.player.sprite.current_direction = 'down'
                        return (0, -1)
                    case "left":
                        self.manager.player.sprite.current_direction = 'left'
                        return (-1, 0)
                    case _:
                        return (0, 0)

            elif self._can_move(player.direction):
                match player.direction:
                    case "up":
                        self.manager.player.sprite.current_direction = 'up'
                        return (0, 1)
                    case "right":
                        self.manager.player.sprite.current_direction = 'right'
                        return (1, 0)
                    case "down":
                        self.manager.player.sprite.current_direction = 'down'
                        return (0, -1)
                    case "left":
                        self.manager.player.sprite.current_direction = 'left'
                        return (-1, 0)
                    case _:
                        return (0, 0)

        return (0, 0)

    def _can_move(self, direction: str) -> bool:
        grid_x = self.manager.player.x
        grid_y = self.manager.player.y
        if grid_y < 0 or grid_y >= len(self.rev_maze) or grid_x < 0 or grid_x >= len(self.rev_maze[0]):
            return False

        match direction:
            case "up":
                if not (self.rev_maze[grid_y][grid_x] & 1):
                    return True
            case "right":
                if not (self.rev_maze[grid_y][grid_x] & 2):
                    return True
            case "down":
                if not (self.rev_maze[grid_y][grid_x] & 4):
                    return True
            case "left":
                if not (self.rev_maze[grid_y][grid_x] & 8):
                    if self.offset_x != 0:
                        return True
                    return True
            case _:
                return False

    def _is_opposite_direction(self, current: str, next_dir: str) -> bool:
        opposites = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left"
        }
        return opposites.get(current) == next_dir


    # +---------------------------------------------------------------------+
    # |                            Draw Methods                             |
    # +---------------------------------------------------------------------+

    def draw_background(self):

        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height
            )
        )

    def draw_UHD(self):

        pokemon = self.manager.player.pokemon
        sprite = arcade.load_texture(f"assets/sprite/pokemon/{pokemon.name}"
                                     "/portraits/Normal.png")
        sprite_size = 75

        arcade.draw_texture_rect(
            texture=self.pokemon_sprite,
            rect=arcade.XYWH((sprite_size / 2) + 10,
                             (self.hauteur - (sprite_size / 2) - 10),
                             sprite_size,
                             sprite_size)
        )

        arcade.draw_texture_rect(
            texture=self.sprite_frame,
            rect=arcade.XYWH((sprite_size / 2) + 10,
                             (self.hauteur - (sprite_size / 2) - 10),
                             sprite_size + 9,
                             sprite_size + 9)
        )

        sprite_size = 75

        player_life = arcade.Text(f"Live(s): {self.manager.player.nb_life}",
                                  sprite_size + 25,
                                  (self.hauteur - (sprite_size / 2) - 5),
                                  color=arcade.color.WHITE,
                                  font_size=15,
                                  font_name="Comic Sans MS")

        player_score = arcade.Text(f"Score: {self.manager.player.score}",
                                   sprite_size + 25,
                                   (self.hauteur - (sprite_size / 2) - 35),
                                   color=arcade.color.WHITE,
                                   font_size=15,
                                   font_name="Comic Sans MS")

        player_life.draw()
        player_score.draw()
