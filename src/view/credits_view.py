# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  credits_view.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/08 13:19:29 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 14:50:49 by alebaron        ###   ########.fr        #
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

    """
    Vue des crédits, affiche les crédits du jeu.

    Attributs:
        background (arcade.Texture): Le background de la vue.
        retour_sprite (arcade.Texture): Le sprite du bouton de retour.
        settings_sprite (arcade.Texture): Le sprite du fond des settings.
        lst_artist (list): La liste des artistes ayant créer les sprites.
        music_player (arcade.SoundPlayer): Le lecteur de musique pour la
            musique de la vue.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window):

        """
        Initialise la vue des crédits.

        Args:
            window (arcade.Window): La fenêtre de jeu, pour pouvoir y accéder
                depuis la vue.
        """

        # Instanciation de la classe mère
        super().__init__(window)

        self.background = arcade.load_texture(BACKGROUND_PATH)
        self.retour_sprite = arcade.load_texture("assets/button/retour.png")
        self.settings_sprite = arcade.load_texture("assets/menu/credits.png")

        # Instanciation des liste de crédits
        self.lst_artist = ["CHUNSOFT", "Emmuffin", "G~", "FrivolousAqua",
                           "baronessfaron", "chime", "anomalocaris", "Uni",
                           "Emboarger", "Angels-Snack", "Morei",
                           "ShyStarryRain", "Ichor", "Frostdrop1", "Caitemis",
                           "JFain", "NickOnimura", "NeroIntruder"]

        # Initialisation de la musique
        self.music_player = None

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_show_view(self) -> None:
        """Appelé quand la vue est affichée."""
        volume = self.window.manager.settings.volume
        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH,
                                      streaming=True)
            self.music_player = self.music.play(volume=volume, loop=True)

    def on_draw(self) -> None:

        """
        Méthode appelée pour dessiner la vue.
        """

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
                                    self.window.height * 0.49,
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
                                    self.window.height * 0.49 - 50,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = "Assets"
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.39,
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
                                    self.window.height * 0.39 - 50,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = ("Pokémon Donjon mystère : Équipe de Secours bleu "
                        " & rouge (Développeur: Chunsoft)")
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.39 - 100,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = "Disclaimer"
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.24,
                                    color=arcade.color.BLACK,
                                    font_size=18,
                                    font_name="FOT-Humming Pro",
                                    bold=True,
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = ("Ce jeu est un fangame crée dans le cadre d'un projet"
                        " scolaire.")
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.24 - 50,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = ("Pokémon appartient à Nintendo, Game Freak, Creatures "
                        "et The Pokemon Compagny.")
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.24 - 100,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

        sprite_title = ("Merci de supporter les oeuvres officielles.")
        artiste_title = arcade.Text(sprite_title,
                                    self.window.width / 2,
                                    self.window.height * 0.24 - 150,
                                    color=arcade.color.BLACK,
                                    font_size=12,
                                    font_name="FOT-Humming Pro",
                                    anchor_x="center",
                                    anchor_y="center")
        artiste_title.draw()

    def on_mouse_press(self, x, y, _, __) -> None:

        """
        Méthode appelée lorsque l'on clique sur la souris.
        """

        # Bouton retour
        if (x > 2 and x < 95 and y > 995 and y < 1080):
            self.music.stop(self.music_player)
            self.window.show_view(self.window.start_view)
