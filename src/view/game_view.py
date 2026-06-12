# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 20:04:34 by alebaron        #+#    #+#               #
#  Updated: 2026/06/12 11:10:09 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+

import arcade
import arcade.gui
from src.view.maze_renderer import MazeRenderer
from src.managers.collectible_manager import CollectibleManager
from src.view.save_score.win_view import WinView
from src.view.save_score.gameover_view import GameoverView
from src.view.cheat_view import CheatView
from src.view.settings_view import SettingsView
from src.pacmanManager import PacmanManager

# +-------------------------------------------------------------------------+
# |                                 Global                                  |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/game_background.png"
MUSIC_PATH = "assets/music/game_theme.mp3"
SCROLL_PATH = "assets/menu/scroll.png"

TILE_SIZE = 64
TRANSITION_DISTANCE = 64


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class GameView(arcade.View):

    """
    Vue principale du jeu, gère l'affichage du labyrinthe, des ennemis, du
    joueur, des collectibles, de l'UI et du menu de pause.

    Attributs:
        manager (PacmanManager): Le manager du jeu, gère la logique du jeu et
            les données.
        enemy_manager (EnemyManager): Le manager des ennemis, gère la logique
            des ennemis et leurs données.
        collectible_manager (CollectibleManager): Le manager des collectibles,
            gère la logique des collectibles et leurs données.
        maze_renderer (MazeRenderer): Le renderer du labyrinthe,
            gère l'affichage du labyrinthe.
        player_sprites (arcade.SpriteList): La liste des sprites du joueur,
            gère l'affichage du joueur.
        music_player (arcade.SoundPlayer): Le lecteur de musique pour la vue,
            gère la musique de la vue.
        music (arcade.Sound): La musique de la vue, gère la musique de la
            vue.
        background (arcade.Texture): Le background de la vue, gère l'affichage
            du background.
        sprite_frame (arcade.Texture): Le sprite du cadre du portrait du
            joueur, gère l'affichage du cadre du portrait du joueur.
        scroll_texture (arcade.Texture): Le sprite du fond de l'UI, gère
            l'affichage du fond de l'UI.
        cheat_scroll (arcade.Texture): Le sprite du fond de l'UI du menu de
            triche, gère l'affichage du fond de l'UI du menu de triche.
        timer (float): Le timer du niveau, gère le temps restant pour finir le
            niveau.
        is_finished (int): La variable qui indique si le niveau est fini, gère
            l'état du niveau (0: en cours, 1: gagné, 2:
            perdu).
        show_pause_menu (bool): La variable qui indique si le menu de pause est
            affiché, gère l'affichage du menu de pause.
        pause_manager (arcade.gui.UIManager): Le manager de l'UI pour gérer les
            éléments graphiques du menu de pause.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, manager: PacmanManager, music_player=None, music=None):

        """
        Initialise la vue du jeu.

        Args:
            manager (PacmanManager): Le manager du jeu, gère la logique du jeu
                et les données.
            music_player (arcade.SoundPlayer, optional): Le lecteur de musique
                pour la vue, gère la musique de la vue. Defaults to None.
            music (arcade.Sound, optional): La musique de la vue, gère la
                musique de la vue. Defaults to None.
        """

        # === Initialisation de la classe parente ===
        super().__init__()

        # === Initialisation des variables ===

        # Récupération de la largeur et hauteur
        self.largeur = self.window.width
        self.hauteur = self.window.height

        # Détection de la fin d'un level
        self.is_finished = 0  # 0: Play, 1: Win, 2: GameOver

        # Récupération du labyrinthe et du manager
        self.manager = manager
        self.enemy_manager = manager.enemy_manager
        self.enemy_manager.set_current_level(self.manager.current_level)

        num_level = self.manager.actual_level
        self.current_maze = self.manager.level[num_level].maze.maze

        # Récupération du labyrinthe à l'envers pour Arcade
        self.rev_maze = self._rev_maze(self.current_maze)

        # === Mise en place du labyrinthe ===
        self.maze_renderer = MazeRenderer(self.rev_maze, self.largeur,
                                          self.hauteur)
        self.scale = self.maze_renderer.scale
        self.offset_x, self.offset_y = (self.maze_renderer.offset_x,
                                        self.maze_renderer.offset_y)

        # === Initialisation des collectibles ===
        self.collectible_manager = CollectibleManager(self.rev_maze,
                                                      self.scale,
                                                      self.offset_x,
                                                      self.offset_y)

        # === Initialisation des coords du player et de ses sprites ===
        self._player_original_pos()
        self.manager.player.sprite.scale = (self.manager.player.pokemon.scale *
                                            self.scale)
        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.manager.player.sprite)

        for enemy in self.enemy_manager.enemies:
            enemy.sprite.scale = enemy.scale * self.scale

        # === Gestion de la musique ===
        self.music_player = music_player
        self.music = music

        # === Initialisation des textures ===
        self.init_textures()

        # === Initialisation du timer ===
        self.timer = float(self.manager.config.level_max_time) + 1

        # === Cacher le curseur ===
        self.window.set_mouse_visible(False)

        # === GUI manager pour le menu de pause ===

        self.pause_manager = arcade.gui.UIManager()
        self.init_btn_layout()
        self.pause_manager.disable()
        self.show_pause_menu = False

    # +---------------------------------------------------------------------+
    # |                             Init Methods                            |
    # +---------------------------------------------------------------------+

    def init_textures(self) -> None:

        """
        Initialise les textures utilisées dans la vue du jeu.
        """

        self.background = arcade.load_texture(BACKGROUND_PATH)
        pokemon = self.manager.player.pokemon.name
        self.pokemon_sprite = arcade.load_texture(f"assets/sprite/pokemon/"
                                                  f"{pokemon}/portraits/"
                                                  "Normal.png")
        self.sprite_frame = arcade.load_texture("assets/sprite/face_frame.png")
        self.scroll_texture = arcade.load_texture(SCROLL_PATH)
        self.cheat_scroll = arcade.load_texture("assets/menu/small_leader"
                                                "board.png")

    def init_btn_layout(self) -> None:

        """
        Initialise les éléments graphiques du menu de pause.
        """

        btn_resume = arcade.gui.UIFlatButton(text="Retour au jeu", width=150)
        btn_start_new_game = arcade.gui.UIFlatButton(text="Nouvelle partie",
                                                     width=150)
        btn_cheat = arcade.gui.UIFlatButton(text="Triche",
                                            width=150)
        btn_param = arcade.gui.UIFlatButton(text="Paramètres",
                                            width=150)
        btn_exit = arcade.gui.UIFlatButton(text="Retour au menu principal",
                                           width=320)

        self.grid = arcade.gui.UIGridLayout(
            column_count=2, row_count=3, horizontal_spacing=20,
            vertical_spacing=20
        )

        self.grid.add(btn_resume, column=0, row=0)
        self.grid.add(btn_start_new_game, column=1, row=0)
        self.grid.add(btn_cheat, column=0, row=1)
        self.grid.add(btn_param, column=1, row=1)
        self.grid.add(btn_exit, column=0, row=2, column_span=2)

        self.anchor = self.pause_manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

        # Initialisation de l'input des boutons

        @btn_resume.event("on_click")
        def on_click_resume_button(event):
            self.pause_manager.disable()
            self.show_pause_menu = False
            self.window.set_mouse_visible(False)

        @btn_start_new_game.event("on_click")
        def on_click_start_new_game_button(event):
            self.manager.reset_game()
            self.music.stop(self.music_player)
            self.window.show_view(GameView(self.manager))

        @btn_cheat.event("on_click")
        def on_click_cheat(event):
            self.window.show_view(CheatView(self.window, self))

        @btn_param.event("on_click")
        def on_click_param(event):
            self.music.stop(self.music_player)
            self.window.show_view(SettingsView(self.window, self))

        @btn_exit.event("on_click")
        def on_click_exit_button(event):
            self.manager.reset_game()
            self.music.stop(self.music_player)
            self.window.show_view(self.window.start_view)

    # +---------------------------------------------------------------------+
    # |                               Methods                               |
    # +---------------------------------------------------------------------+

    def on_hide_view(self) -> None:

        """
        Méthode appelée lorsque la vue est cachée.
        """

        self.pause_manager.disable()

    def on_draw(self) -> None:

        """
        Méthode appelée pour dessiner la vue.
        """

        self.clear()

        # Affichage du background
        self.draw_background()

        # Affichage du labyrinthe et des pacgums
        self.maze_renderer.draw()
        self.collectible_manager.draw()

        # Récupération des coordonnées du joueur en pixel
        pixel_x = (self.manager.player.x * TILE_SIZE + 32 +
                   self.manager.player.pixel_offset_x)
        pixel_y = (self.manager.player.y * TILE_SIZE + 32 +
                   self.manager.player.pixel_offset_y)

        # Affichage du joueur au centre du labyrinthe
        self.manager.player.sprite.center_x = (pixel_x * self.scale +
                                               self.offset_x)
        self.manager.player.sprite.center_y = (pixel_y * self.scale +
                                               self.offset_y)
        self.player_sprites.draw()

        for enemy in self.enemy_manager.enemies:
            pixel_x = enemy.x * TILE_SIZE + 32 + enemy.pixel_offset_x
            pixel_y = enemy.y * TILE_SIZE + 32 + enemy.pixel_offset_y
            enemy.sprite.center_x = pixel_x * self.scale + self.offset_x
            enemy.sprite.center_y = (pixel_y * self.scale +
                                     self.offset_y - enemy.offset_y)

        for enemy in self.enemy_manager.get_respawning_enemies():
            countdown = enemy.death_timer - int(enemy.respawn_timer)
            arcade.Text(
                str(countdown),
                enemy.sprite.center_x - 13,
                enemy.sprite.center_y - 5,
                arcade.color.RED,
                font_size=30 * self.scale
            ).draw()

        self.enemy_manager.draw()

        # Affichage de l'HUD
        self.draw_UI()

        # Affichage du menu par dessus le jeu en cas de pause
        if (self.show_pause_menu):

            self.window.set_mouse_visible(True)

            ecran_rect = arcade.rect.Rect(
                left=0,
                right=self.window.width,
                bottom=0,
                top=self.window.height,
                x=self.window.width / 2,
                y=self.window.height / 2,
                width=self.window.width,
                height=self.window.height
            )

            arcade.draw_rect_filled(rect=ecran_rect, color=(0, 0, 0, 127))

            # Ecriture du titre de pause
            pause_title = arcade.Text("PAUSE",
                                      self.window.width / 2,
                                      self.height * 0.65,
                                      color=arcade.color.BLACK,
                                      font_size=36,
                                      font_name="FOT-Humming Pro",
                                      anchor_x="center",
                                      anchor_y="center")

            pause_title.draw()
            self.pause_manager.draw()

    def on_update(self, delta_time) -> None:

        """Mise à jour de la vue, appelée 60 fois par seconde."""

        # Mise à jour du timer
        if (self.show_pause_menu is True):
            return

        self.timer -= delta_time

        if (self.timer <= 0 or self.manager.player.nb_life == 0):
            self.is_finished = 2

        # Vérification que le jeu est toujours en cours
        if (self.is_finished == 1):
            if (self.manager.actual_level == (len(self.manager.level) - 1)):
                self.music.stop(self.music_player)
                self.window.set_mouse_visible(True)
                self.window.show_view(WinView(self.window))
            else:
                self.manager.update_new_level()
                self.manager.player.reset_position()
                self.window.show_view(GameView(self.manager, self.music_player,
                                               self.music))
        if (self.is_finished == 2):
            self.music.stop(self.music_player)
            self.window.set_mouse_visible(True)
            self.window.show_view(GameoverView(self.window))

        vx, vy = self._player_move()

        self.manager.player.pixel_offset_x += vx * self.manager.player.speed
        self.manager.player.pixel_offset_y += vy * self.manager.player.speed

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

        if self.manager.player.is_super:
            self.manager.player.super_timer += delta_time

            if not self.manager.enemy_manager.enemies[0].is_fleeing:
                for enemy in self.manager.enemy_manager.enemies:
                    enemy.is_fleeing = True

            if (self.manager.player.super_timer >=
               self.manager.player.time_super_max):

                self.manager.player.is_super = False
                for enemy in self.manager.enemy_manager.enemies:
                    enemy.is_fleeing = False
                    self.manager.player.super_timer = 0.0

        self.manager.player.sprite.on_update(delta_time)

        for enemy in self.enemy_manager.enemies:
            enemy.on_update(delta_time)
            if enemy.just_respawned:
                self.enemy_manager.enemies_sprite.append(enemy.sprite)
                enemy.just_respawned = False
            if enemy.is_dead:
                if enemy.sprite in self.enemy_manager.enemies_sprite:
                    self.enemy_manager.enemies_sprite.remove(enemy.sprite)

        self.enemy_manager.on_update(delta_time)

        if (int(self.timer) != self.manager.config.level_max_time):
            self.check_enemy_collisions()

    def on_show_view(self) -> None:

        """
        Méthode appelée lorsque la vue est affichée. Elle démarre la
        musique de la vue.
        """

        if (self.show_pause_menu is True):
            self.pause_manager.enable()

        self.manager.player.sprite.scale = (self.manager.player.pokemon.scale *
                                            self.scale)
        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.manager.player.sprite)

        volume = self.window.manager.settings.volume
        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH,
                                      streaming=True)
            self.music_player = self.music.play(volume=volume, loop=True)

    # +---------------------------------------------------------------------+
    # |                        Methods for collisions                       |
    # +---------------------------------------------------------------------+

    def check_enemy_collisions(self) -> None:

        """Vérifie les collisions entre le joueur et les ennemis."""

        lst_collisions = []

        for player in self.player_sprites:

            ennemy = self.enemy_manager.enemies_sprite
            lst_collisions += arcade.check_for_collision_with_list(player,
                                                                   ennemy)

        if ((not self.manager.player.is_super) and
           self.manager.cheat.intagibilite is False and
           self.manager.cheat.invicibility is False):

            if (lst_collisions):

                self.manager.player.nb_life -= 1
                if (self.manager.player.nb_life) == 0:
                    return
                self.manager.player.reset_position()
                self._player_original_pos()
                self.enemy_manager.reset_enemy()

        elif ((self.manager.player.is_super and
              self.manager.cheat.intagibilite is False) or
              (self.manager.player.is_super and
              self.manager.cheat.invicibility is True)):

            if (lst_collisions):
                for collision in lst_collisions:
                    enemy = collision.owner
                    shorcut = self.manager.enemy_manager.enemies_sprite
                    shorcut.remove(enemy.sprite)
                    enemy.die()
                    point = self.manager.config.points_per_ghost
                    self.manager.player.score += (point)

    def get_collectibles(self) -> None:

        """
        Vérifie les collisions entre le joueur et les collectibles,
        et met à jour le score et l'état du niveau en conséquence.
        """

        p = self.collectible_manager.remove_pacgum(self.player_sprites,
                                                   self.manager.config,
                                                   self.manager.player)

        points, self.is_finished = p
        self.manager.player.score += points

    # +---------------------------------------------------------------------+
    # |                            Game Methods                             |
    # +---------------------------------------------------------------------+

    def _rev_maze(self, maze: list[list[int]]) -> list[list[int]]:

        """
        Inverse le labyrinthe pour l'adapter au système de coordonnées
        d'Arcade.

        Args:
             maze (list[list[int]]): La matrice représentant le labyrinthe.
        Returns:
             list[list[int]]: La matrice du labyrinthe inversée.
        """

        rev_maze: list[list[int]] = []
        for i in range(len(maze) - 1, -1, -1):
            rev_maze.append(maze[i])

        return rev_maze

    def _player_original_pos(self) -> None:

        """
        Initialise la position du joueur au point de départ défini dans le
        labyrinthe.
        """

        nb_columns = len(self.rev_maze[0])
        nb_lines = len(self.rev_maze)

        grid_x = ((nb_columns) // 2 if nb_columns % 2 == 0 else
                  (nb_columns + 1) // 2)
        grid_y = ((nb_lines) // 2 + 1 if nb_lines % 2 == 0 else
                  (nb_lines + 1) // 2)

        self.manager.player.x = grid_x - 1
        self.manager.player.y = grid_y - 1

        self.manager.player.pixel_offset_x = 0.0
        self.manager.player.pixel_offset_y = 0.0

    def on_key_press(self, key, _) -> None:

        """
        Méthode appelée lorsque l'on appuie sur une touche du clavier.
        """

        if (self.show_pause_menu is False):

            dict_key = self.manager.settings.dict_key
            dict_key = dict_key[self.manager.settings.configuration]

            if key == dict_key["up"] or key == arcade.key.UP:
                self.manager.player.next_direction = "up"
            elif key == dict_key["left"] or key == arcade.key.LEFT:
                self.manager.player.next_direction = "left"
            elif key == dict_key["down"] or key == arcade.key.DOWN:
                self.manager.player.next_direction = "down"
            elif key == dict_key["right"] or key == arcade.key.RIGHT:
                self.manager.player.next_direction = "right"

        # Afficher le menu de pause
        if key == arcade.key.ESCAPE:
            if self.show_pause_menu is False:
                self.pause_manager.enable()
                self.show_pause_menu = True
            else:
                self.pause_manager.disable()
                self.show_pause_menu = False
                self.window.set_mouse_visible(False)

    def _player_move(self) -> tuple[float, float]:

        """
        Calcule le déplacement du joueur en fonction de sa direction actuelle
        et de la configuration du labyrinthe.

        Returns:
            tuple[float, float]: Le déplacement en pixels sur les axes x et y.
        """

        player = self.manager.player

        if (player.next_direction and
            self._is_opposite_direction(player.direction,
                                        player.next_direction)):

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

        """
        Vérifie si le joueur peut se déplacer dans la direction donnée en
        fonction de la configuration du labyrinthe.

        Args:
            direction (str): La direction dans laquelle le joueur souhaite se
                déplacer ('up', 'down', 'left', 'right').
        Returns:
            bool: True si le joueur peut se déplacer dans la direction donnée,
                False sinon.
        """

        grid_x = self.manager.player.x
        grid_y = self.manager.player.y
        if (grid_y < 0 or grid_y >= len(self.rev_maze) or
           grid_x < 0 or grid_x >= len(self.rev_maze[0])):

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
                    return True
            case _:
                return False

    def _is_opposite_direction(self, current: str, next_dir: str) -> bool:

        """
        Vérifie si la prochaine direction est opposée à la direction actuelle
        du joueur.

        Args:
            current (str): La direction actuelle du joueur ('up', 'down',
                'left','right').
            next_dir (str): La prochaine direction du joueur.

        Returns:
            bool: True si la prochaine direction est opposée à la direction
                actuelle, False sinon.
        """

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

    def draw_background(self) -> None:

        """Affiche le background de la vue."""

        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height
            )
        )

    def draw_UI(self) -> None:

        """
        Affiche l'interface utilisateur (UI) de la vue,
        comprenant les informations sur le joueur, le niveau et le
        temps restant.
        """

        # Affichage de la partie haut gauche de l'UI
        sprite_size = 75

        arcade.draw_texture_rect(
            texture=self.pokemon_sprite,
            rect=arcade.XYWH((sprite_size / 2) + 30,
                             (self.hauteur - (sprite_size / 2) - 10) - 20,
                             sprite_size,
                             sprite_size)
        )

        arcade.draw_texture_rect(
            texture=self.sprite_frame,
            rect=arcade.XYWH((sprite_size / 2) + 30,
                             (self.hauteur - (sprite_size / 2) - 10) - 20,
                             sprite_size + 9,
                             sprite_size + 9)
        )

        sprite_size = 75

        player_life = arcade.Text(f"Vie(s): {self.manager.player.nb_life}",
                                  sprite_size + 25 + 20,
                                  (self.hauteur - (sprite_size / 2) - 5) - 20,
                                  color=arcade.color.WHITE,
                                  font_size=15,
                                  font_name="Comic Sans MS")

        player_score = arcade.Text(f"Score: {self.manager.player.score}",
                                   sprite_size + 25 + 20,
                                   ((self.hauteur -
                                     (sprite_size / 2) - 35) - 20),
                                   color=arcade.color.WHITE,
                                   font_size=15,
                                   font_name="Comic Sans MS")

        player_life.draw()
        player_score.draw()

        # Affichage de la partie haut droite de l'UI

        height = self.window.height * 0.12
        width = self.window.width * 0.2

        arcade.draw_texture_rect(
            texture=self.scroll_texture,
            rect=arcade.XYWH(self.window.width - width / 2 - 20,
                             self.window.height - height / 2 - 25,
                             width,
                             height)
        )

        level_text = arcade.Text(f"Étage: {self.manager.actual_level + 1}",
                                 self.window.width - width / 2 - 20,
                                 self.window.height - 70,
                                 color=arcade.color.BLACK,
                                 font_size=18,
                                 font_name="Comic Sans MS",
                                 anchor_x="center",
                                 anchor_y="center")

        time_text = arcade.Text(f"Temps: {int(self.timer)} seconde(s)",
                                self.window.width - width / 2 - 20,
                                self.window.height - 105,
                                color=arcade.color.BLACK,
                                font_size=15,
                                font_name="Comic Sans MS",
                                anchor_x="center",
                                anchor_y="center")

        level_text.draw()
        time_text.draw()
