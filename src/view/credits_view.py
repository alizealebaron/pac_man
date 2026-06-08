# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  credits_view.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/08 13:19:29 by alebaron        #+#    #+#               #
#  Updated: 2026/06/08 21:54:27 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/credits_background.png"
MUSIC_PATH = "assets/music/credits_theme.mp3"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class CreditsView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window):

        # Instanciation de la classe mère
        super().__init__(window)

        self.background = arcade.load_texture(BACKGROUND_PATH)
        self.retour_sprite = arcade.load_texture("assets/button/retour.png")
        self.settings_sprite = arcade.load_texture("assets/menu/credits.png")

        # Instanciation des liste de crédits
        self.lst_artist = ["CHUNSOFT", "Emmuffin", "G〜", "FrivolousAqua",
                           "baronessfaron", "chime", "anomalocaris", "Uni",
                           "Emboarger", "Angels-Snack", "Morei", "ShyStarryRain",
                           "Ichor", "Frostdrop1", "Caitemis", "JFain",
                           "NickOnimura", "NeroIntruder"]

        # Initialisation de la musique
        self.music_player = None

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
            rect=arcade.XYWH(
                45,
                self.window.height - (height / 2),
                width,
                height
            )
        )

        # Affichage du fond des settings
        arcade.draw_texture_rect(
            texture=self.settings_sprite,
            rect=arcade.XYWH(
                x=self.window.width / 2 + 20,
                y=self.window.height / 2,
                width=1500,
                height=1050
            )
        )

        sprite_title = "Sprite & Animations"
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.8,
                                    color=arcade.color.BLACK,
                                    font_size=18,
                                    font_name="FOT-Humming Pro",
                                    bold=True,
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        nb_colonnes = 4
        espacement_x = self.window.width / (nb_colonnes + 1)
        espacement_y = 50
        y_initial = self.window.height * 0.8 - 75

        for index, artist in enumerate(self.lst_artist):
            # Calcul de la colonne et de la ligne
            colonne = index % nb_colonnes
            ligne = index // nb_colonnes

            # Calcul des coordonnées X et Y
            start_x = (colonne + 1) * espacement_x
            start_y = y_initial - (ligne * espacement_y)

            # Affichage du texte
            player_name = arcade.Text(artist,
                                    start_x,
                                    start_y,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
            player_name.draw()

        sprite_title = "Musiques"
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.48,
                                    color=arcade.color.BLACK,
                                    font_size=18,
                                    font_name="FOT-Humming Pro",
                                    bold=True,
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = ("Pokémon Donjon mystère : Équipe de Secours DX"
                        " (Compositeur: Keisuke Ito)")
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.48 - 50,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = "Assets"
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.38,
                                    color=arcade.color.BLACK,
                                    font_size=18,
                                    font_name="FOT-Humming Pro",
                                    bold=True,
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = ("Pokémon Donjon mystère : Équipe de Secours DX"
                        " (Développeur: Spike Chunsoft)")
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.38 - 50,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = ("Pokémon Donjon mystère : Équipe de Secours bleu & rouge"
                        " (Développeur: Chunsoft)")
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.38 - 100,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = "Disclaimer"
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.23,
                                    color=arcade.color.BLACK,
                                    font_size=18,
                                    font_name="FOT-Humming Pro",
                                    bold=True,
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = ("Ce jeu est un fangame crée dans le cadre d'un projet scolaire.")
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.23 - 50,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = ("Pokémon appartient à Nintendo, Game Freak et Creatures.")
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.23 - 100,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = ("Merci de supporter les oeuvres officielles.")
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.23 - 150,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

    def on_mouse_press(self, x, y, _, __):

        # Bouton retour
        if (x > 2 and x < 95 and y > 995 and y < 1080):
            self.music.stop(self.music_player)
            self.window.show_view(self.window.start_view)
