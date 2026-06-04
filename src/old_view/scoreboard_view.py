# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  scoreboard_view.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/23 10:58:55 by alebaron        #+#    #+#               #
#  Updated: 2026/06/04 12:01:55 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/score_background.png"
MUSIC_PATH = "assets/music/scoreboard_theme.mp3"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class ScoreboardView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window):

        # Initialisation du composant parent
        super().__init__(window)

        # Chargement des textures
        self.background = arcade.load_texture(BACKGROUND_PATH)
        self.retour_sprite = arcade.load_texture("assets/button/retour.png")
        self.score_sprite = arcade.load_texture("assets/menu/scoreboard.png")
        self.rank_0 = arcade.load_texture("assets/rank/rank_0.png")
        self.sprite_frame = arcade.load_texture("assets/sprite/face_frame.png")

        # Récupération du score
        self.lst_score = self.window.manager.scoreboard

        # Initialisation de la musique
        self.music_player = None

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_show_view(self):
        """Appelé quand la vue change"""
        volume =  self.window.manager.settings.volume
        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH,
                                      streaming=True)
            self.music_player = self.music.play(volume=volume, loop=True)

    def on_draw(self):
        """ Draw everything """
        self.clear()

        # Affichage du background
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height
            )
        )

        # Affichage du bouton retour
        height = 90
        width = 170
        arcade.draw_texture_rect(
            texture=self.retour_sprite,
            rect=arcade.XYWH(45,
                             (self.window.height) - (height / 2),
                             width,
                             height)
        )

        # Affichage du fond du scoreboard
        height = 1000
        width = 1400
        arcade.draw_texture_rect(texture=self.score_sprite,
                                 rect=arcade.XYWH(
                                                x=self.window.width / 2 + 20,
                                                y=self.window.height / 2,
                                                width=width,
                                                height=height))

        # Affichage des scores
        self.draw_big_scoreboard()

    def on_mouse_press(self, x, y, _, __):

        # Bouton retour
        if (x > 2 and x < 95 and y > 995 and y < 1080):
            self.music.stop(self.music_player)
            self.window.show_view(self.window.start_view)

    # +---------------------------------------------------------------------+
    # |                            Draw Methods                             |
    # +---------------------------------------------------------------------+

    def draw_big_scoreboard(self):

        # Tri des 3 meilleurs
        scores = sorted(self.lst_score,
                        key=lambda p: p.score,
                        reverse=True)[:30]

        # Configuration des positions
        start_x = 450
        start_y = (self.window.width / 2) - 150
        line_height = 70
        icon_size = 50

        # Joueurs présents au top 3
        for i, player in enumerate(scores):

            if (i % 10 == 0 and i != 0):
                start_x += 400
                start_y = (self.window.width / 2) - 150

            current_y = start_y - ((i % 10) * line_height)

            # Image de rang
            if (i < 12):
                rank_tex = arcade.load_texture(f"assets/rank/rank_{i+1}_64"
                                               ".png")
            else:
                rank_tex = self.rank_0
            arcade.draw_texture_rect(
                texture=rank_tex,
                rect=arcade.XYWH(start_x + (icon_size / 2), current_y,
                                 icon_size, icon_size)
            )

            # Image du pokémon
            pokemon = player.pokemon
            profile_tex = arcade.load_texture(f"assets/sprite/pokemon/"
                                              f"{pokemon}/portraits"
                                              "/Normal.png")
            arcade.draw_texture_rect(
                texture=profile_tex,
                rect=arcade.XYWH(start_x + icon_size + 40, current_y,
                                 icon_size, icon_size)
            )

            arcade.draw_texture_rect(
                texture=self.sprite_frame,
                rect=arcade.XYWH(start_x + icon_size + 40, current_y,
                                 icon_size + 5, icon_size + 5)
            )

            # Nom + Score
            text_content = f"{player.name} ({player.score})"
            player_name = arcade.Text(text_content,
                                      start_x + (icon_size * 2) + 30,
                                      current_y - 8,
                                      color=arcade.color.BLACK,
                                      font_size=12,
                                      font_name="FOT-Humming Pro")
            player_name.draw()
