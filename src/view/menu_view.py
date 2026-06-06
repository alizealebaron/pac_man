# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  menu_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 10:28:01 by alebaron        #+#    #+#               #
#  Updated: 2026/06/04 12:16:40 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade
from src.view.game_view import GameView
from src.view.scoreboard_view import ScoreboardView
from src.view.settings_view import SettingsView
from src.view.personnality.personnality_view import PersonnalityView

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/menu_background.jpg"
BTN_PATH = "assets/button/"
MUSIC_PATH = "assets/music/mainMenu_theme.mp3"

MAIN_FONT_PATH = "assets/font/main_font.ttf"
TEXT_FONT_PATH = "assets/font/text_font.otf"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class MenuView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self):

        super().__init__()

        # Initialisation des textures
        self.player_pokemon = self.window.manager.player.pokemon

        self.background = arcade.load_texture(BACKGROUND_PATH)
        self.sprite_board = arcade.load_texture("assets/menu/leaderboard.png")
        self.sprite_qwerty = arcade.load_texture("assets/menu/keybinds.png")
        self.sprite_azerty = arcade.load_texture("assets/menu/keybinds_azerty"
                                                 ".png")
        self.sprite_frame = arcade.load_texture("assets/sprite/face_frame.png")
        self.pokemon_sprite = arcade.load_texture(f"assets/sprite/pokemon/"
                                                  f"{self.player_pokemon.name}"
                                                  "/portraits/Normal.png")
        self.sprite_frame = arcade.load_texture("assets/sprite/face_frame.png")
        self.rank_0 = arcade.load_texture("assets/rank/rank_0.png")
        self.amogus = arcade.load_texture("assets/sprite/undefined/Normal.png")

        # Initialisation des fonts
        arcade.load_font(MAIN_FONT_PATH)
        arcade.load_font(TEXT_FONT_PATH)

        # Récupération de la largeur et hauteur de la fenêtre
        self.largeur = self.window.width
        self.hauteur = self.window.height

        # Calcul des dimensions proportionnelles des boutons
        self.btn_width = self.largeur * 0.20
        self.btn_height = self.hauteur * 0.17

        # Calcul des positions (en % de l'écran)
        col_gauche = self.largeur * 0.35
        col_droite = self.largeur * 0.65
        col_centre = self.largeur * 0.50

        ligne_haut = self.hauteur * 0.75
        ligne_milieu = self.hauteur * 0.48
        ligne_bas = self.hauteur * 0.20

        # Initialisation de la box à boutons
        self.boutons = {
            "new_game": {
                "texture": arcade.load_texture(BTN_PATH + "start.png"),
                "pos": (col_gauche, ligne_haut),
                "action": self.start_game
            },
            "quizz": {
                "texture": arcade.load_texture(BTN_PATH + "quizz.png"),
                "pos": (col_droite, ligne_haut),
                "action": self.open_quizz
            },
            "settings": {
                "texture": arcade.load_texture(BTN_PATH + "settings.png"),
                "pos": (col_droite, ligne_milieu),
                "action": self.open_settings
            },
            "scoreboard": {
                "texture": arcade.load_texture(BTN_PATH + "score.png"),
                "pos": (col_gauche, ligne_milieu),
                "action": self.open_score
            },
            "exit": {
                "texture": arcade.load_texture(BTN_PATH + "end.png"),
                "pos": (col_centre, ligne_bas),
                "action": self.end_game
            }
        }

        # Initialisation de la musique
        self.music_player = None

    # +---------------------------------------------------------------------+
    # |                            Btn Methods                              |
    # +---------------------------------------------------------------------+

    def start_game(self):
        self.window.show_view(GameView(self.window.manager))

    def open_quizz(self):
        self.window.show_view(PersonnalityView(self.window))

    def open_settings(self):
        self.window.show_view(SettingsView(self.window))

    def open_score(self):
        self.window.show_view(ScoreboardView(self.window))

    def end_game(self):
        arcade.exit()

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_show_view(self):
        """Appelé quand la vue change"""
        volume = self.window.manager.settings.volume
        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH,
                                      streaming=True)
            self.music_player = self.music.play(volume=volume, loop=True)

        # Reload le nouveau sprite
        self.pokemon_sprite = arcade.load_texture(f"assets/sprite/pokemon/"
                                                  f"{self.player_pokemon.name}"
                                                  "/portraits/Normal.png")

    def on_draw(self):

        self.clear()

        # Affichage du fond d'écran
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height
            )
        )

        # Affichage des boutons du menu
        for nom, data in self.boutons.items():
            x, y = data["pos"]
            arcade.draw_texture_rect(
                texture=data["texture"],
                rect=arcade.XYWH(x, y, self.btn_width, self.btn_height)
            )

        # Affichage de l'encadré en haut à gauche
        self._draw_player()

        # Affichage de l'encadré en bas à gauche

        sprite_height = 220
        sprite_width = 400

        arcade.draw_texture_rect(
            texture=self.sprite_board,
            rect=arcade.XYWH((sprite_width / 2) + 10,
                             (sprite_height / 2) + 15,
                             sprite_width,
                             sprite_height)
        )

        self._draw_little_scoreboard()

        # Affichage de l'encadré en bas à droite
        if (self.window.manager.settings.configuration == "AZERTY"):
            sprite_keybinds = self.sprite_azerty
        else:
            sprite_keybinds = self.sprite_qwerty

        arcade.draw_texture_rect(
            texture=sprite_keybinds,
            rect=arcade.XYWH(self.width - (sprite_width / 2) - 20,
                             (sprite_height / 2) + 20,
                             sprite_width,
                             sprite_height)
        )

    def on_mouse_press(self, x, y, button, modifiers):
        # La détection s'adapte aussi aux dimensions proportionnelles
        for nom, data in self.boutons.items():
            bx, by = data["pos"]

            if (bx - self.btn_width / 2 < x < bx + self.btn_width / 2 and
                by - self.btn_height / 2 < y < by + self.btn_height / 2):
                self.music.stop(self.music_player)
                data["action"]()
                break

        if (x > 1670 and x < 1720 and y > 110 and y < 155):
            self.music.stop(self.music_player)
            self.music = arcade.Sound("assets/music/easter_egg.mp3",
                                      streaming=True)
            self.music_player = self.music.play(volume=1, loop=True)

    # +---------------------------------------------------------------------+
    # |                           Custom Methods                            |
    # +---------------------------------------------------------------------+

    def _draw_player(self):

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

        player_name = arcade.Text(self.window.manager.player.name,
                                  sprite_size + 25,
                                  (self.hauteur - (sprite_size / 2) - 20),
                                  color=arcade.color.BLACK,
                                  font_size=20,
                                  font_name="FOT-UDKakugoC80 Pro",
                                  bold=True)
        player_name.draw()

    def _draw_little_scoreboard(self):

        # Tri des 3 meilleurs
        scores = sorted(self.window.manager.scoreboard,
                        key=lambda p: p.score,
                        reverse=True)[:3]

        # Configuration des positions
        start_x = 30
        start_y = 140
        line_height = 45
        icon_size = 32

        # Joueurs présents au top 3
        for i, player in enumerate(scores):

            current_y = start_y - (i * line_height)

            # Image de rang
            rank_tex = arcade.load_texture(f"assets/rank/rank_{i+1}_64.png")
            arcade.draw_texture_rect(
                texture=rank_tex,
                rect=arcade.XYWH(start_x + (icon_size / 2), current_y, icon_size, icon_size)
            )

            # Image du pokémon
            pokemon = player.pokemon
            profile_tex = arcade.load_texture(f"assets/sprite/pokemon/{pokemon}/portraits/Normal.png") 
            arcade.draw_texture_rect(
                texture=profile_tex,
                rect=arcade.XYWH(start_x + icon_size + 25, current_y, icon_size, icon_size)
            )

            arcade.draw_texture_rect(
                texture=self.sprite_frame,
                rect=arcade.XYWH(start_x + icon_size + 25, current_y, icon_size + 5, icon_size + 5)
            )

            # Nom + Score
            text_content = f"{player.name} ({player.score})"
            player_name = arcade.Text(text_content,
                                      start_x + (icon_size * 2) + 20,
                                      current_y - 5,
                                      color=arcade.color.BLACK,
                                      font_size=11,
                                      font_name="FOT-Humming Pro")
            player_name.draw()

        i = len(scores)

        while (i < 3):

            current_y = start_y - (i * line_height)

            # Image de rang
            arcade.draw_texture_rect(
                texture=self.rank_0,
                rect=arcade.XYWH(start_x + (icon_size / 2), current_y, icon_size, icon_size)
            )

            # Image du pokémon
            arcade.draw_texture_rect(
                texture=self.amogus,
                rect=arcade.XYWH(start_x + icon_size + 25, current_y, icon_size, icon_size)
            )

            arcade.draw_texture_rect(
                texture=self.sprite_frame,
                rect=arcade.XYWH(start_x + icon_size + 25, current_y, icon_size + 5, icon_size + 5)
            )

            # Nom + Score
            text_content = "..."
            player_name = arcade.Text(text_content,
                                      start_x + (icon_size * 2) + 20,
                                      current_y - 5,
                                      color=arcade.color.BLACK,
                                      font_size=11,
                                      font_name="FOT-Humming Pro")
            player_name.draw()

            i += 1
