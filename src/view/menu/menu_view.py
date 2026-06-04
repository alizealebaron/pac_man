# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  menu_view.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 10:28:01 by alebaron        #+#    #+#               #
#  Updated: 2026/06/04 15:45:24 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade
from src.view.view_utils.baseView import BaseView
from src.view.game.game_view import GameView
# from src.old_view.scoreboard_view import ScoreboardView
# from src.old_view.settings_view import SettingsView
# from src.old_view.personnality.personnality_view import PersonnalityView

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+

BACKGROUND_PATH = "assets/background/menu_background.png"
BTN_PATH = "assets/button/"
MUSIC_PATH = "assets/music/mainMenu_theme.mp3"

MAIN_FONT_PATH = "assets/font/main_font.ttf"
TEXT_FONT_PATH = "assets/font/text_font.otf"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class MenuView(BaseView):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self):

        super().__init__()

        # Initialisation des textures
        self.player_pokemon = self.manager.player.pokemon

        # Initialisation des fonts
        arcade.load_font(MAIN_FONT_PATH)
        arcade.load_font(TEXT_FONT_PATH)

        # Initialisation des boutons du menu
        self.init_btn_menu()

        # Initialisation de la musique
        self.music_player = None
        self.music = arcade.Sound(MUSIC_PATH, streaming=True)

    # +---------------------------------------------------------------------+
    # |                            Init Methods                             |
    # +---------------------------------------------------------------------+

    def init_btn_menu(self):

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
                "texture": super().get_texture(BTN_PATH + "start.png"),
                "pos": (col_gauche, ligne_haut),
                "action": self.start_game
            },
            "quizz": {
                "texture": super().get_texture(BTN_PATH + "quizz.png"),
                "pos": (col_droite, ligne_haut),
                "action": self.open_quizz
            },
            "settings": {
                "texture": super().get_texture(BTN_PATH + "settings.png"),
                "pos": (col_droite, ligne_milieu),
                "action": self.open_settings
            },
            "scoreboard": {
                "texture": super().get_texture(BTN_PATH + "score.png"),
                "pos": (col_gauche, ligne_milieu),
                "action": self.open_score
            },
            "exit": {
                "texture": super().get_texture(BTN_PATH + "end.png"),
                "pos": (col_centre, ligne_bas),
                "action": self.end_game
            }
        }

    # +---------------------------------------------------------------------+
    # |                            Btn Methods                              |
    # +---------------------------------------------------------------------+

    def start_game(self):
        self.window.show_view(GameView())
        print("1")

    def open_quizz(self):
        # self.window.show_view(PersonnalityView(self.window))
        print("2")

    def open_settings(self):
        # self.window.show_view(SettingsView(self.window))
        print("3")

    def open_score(self):
        # self.window.show_view(ScoreboardView(self.window))
        print("4")

    def end_game(self):
        arcade.exit()

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_draw(self):

        super().on_draw()

        # Affichage des boutons du menu
        for nom, data in self.boutons.items():
            x, y = data["pos"]
            arcade.draw_texture_rect(
                texture=data["texture"],
                rect=arcade.XYWH(x, y, self.btn_width, self.btn_height))

        # Affichage de l'encadré en haut à gauche
        self._draw_player()

        # Affichage de l'encadré en bas à gauche

        sprite_height = 220
        sprite_width = 400

        sprite_board = super().get_texture("assets/menu/leaderboard.png")
        arcade.draw_texture_rect(
            texture=sprite_board,
            rect=arcade.XYWH((sprite_width / 2) + 10,
                             (sprite_height / 2) + 15,
                             sprite_width,
                             sprite_height)
        )

        self._draw_little_scoreboard()

        # Affichage de l'encadré en bas à droite
        if (self.window.manager.settings.configuration == "AZERTY"):
            sprite_keybinds = super().get_texture("assets/menu/keybinds_azerty"
                                                  ".png")
        else:
            sprite_keybinds = super().get_texture("assets/menu/keybinds.png")

        arcade.draw_texture_rect(
            texture=sprite_keybinds,
            rect=arcade.XYWH(self.width - (sprite_width / 2) - 20,
                             (sprite_height / 2) + 20,
                             sprite_width,
                             sprite_height)
        )

    def on_mouse_press(self, x, y, button, modifiers):
        # La détection s'adapte aussi aux dimensions proportionnelles
        for _, data in self.boutons.items():
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
        pokemon_sprite = super().get_texture(f"assets/sprite/pokemon/"
                                             f"{self.player_pokemon.name}"
                                             "/portraits/Normal.png")
        arcade.draw_texture_rect(
            texture=pokemon_sprite,
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

        player_name = arcade.Text(self.manager.player.name,
                                  sprite_size + 25,
                                  (self.hauteur - (sprite_size / 2) - 20),
                                  color=arcade.color.BLACK,
                                  font_size=20,
                                  font_name="FOT-UDKakugoC80 Pro",
                                  bold=True)
        player_name.draw()

    def _draw_little_scoreboard(self):

        # Tri des 3 meilleurs
        scores = sorted(self.manager.scoreboard,
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
            rank_tex = super().get_texture(f"assets/rank/rank_{i+1}_64.png")
            arcade.draw_texture_rect(
                texture=rank_tex,
                rect=arcade.XYWH(start_x + (icon_size / 2), current_y,
                                 icon_size, icon_size)
            )

            # Image du pokémon
            pokemon = player.pokemon
            profile_tex = super().get_texture(f"assets/sprite/pokemon/"
                                              f"{pokemon}/portraits/"
                                              "Normal.png")
            arcade.draw_texture_rect(
                texture=profile_tex,
                rect=arcade.XYWH(start_x + icon_size + 25, current_y,
                                 icon_size, icon_size)
            )

            arcade.draw_texture_rect(
                texture=self.sprite_frame,
                rect=arcade.XYWH(start_x + icon_size + 25, current_y,
                                 icon_size + 5, icon_size + 5)
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
            rank_0 = super().get_texture("assets/rank/rank_0.png")
            arcade.draw_texture_rect(
                texture=rank_0,
                rect=arcade.XYWH(start_x + (icon_size / 2), current_y,
                                 icon_size, icon_size)
            )

            # Image du pokémon
            amogus = super().get_texture("assets/sprite/undefined/Normal.png")
            arcade.draw_texture_rect(
                texture=amogus,
                rect=arcade.XYWH(start_x + icon_size + 25, current_y,
                                 icon_size, icon_size)
            )

            arcade.draw_texture_rect(
                texture=self.sprite_frame,
                rect=arcade.XYWH(start_x + icon_size + 25, current_y,
                                 icon_size + 5, icon_size + 5)
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
