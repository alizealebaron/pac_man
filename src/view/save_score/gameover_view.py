# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  gameover_view.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 08:06:31 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 14:40:35 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+

import arcade
from src.view.save_score.win_view import WinView

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/gameover_background.png"
MUSIC_PATH = "assets/music/gameover_theme.mp3"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class GameoverView(WinView):

    """
    View affichée lorsque le joueur perd la partie.

    Attributs:
        background (arcade.Texture): Texture de fond de la view.
        title (str): Titre affiché sur la view.
        emotion (str): Emotion affichée sur le portrait du pokemon.
        profile_tex (arcade.Texture): Texture du portrait du pokemon.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window):

        """
        Initialise la view de gameover.
        Args:
            window (arcade.Window): La fenêtre de jeu.
        """

        # Appel du constructeur de la classe parente
        super().__init__(window)

        self.background = arcade.load_texture(BACKGROUND_PATH)

        # Initialisation des infos de la view
        self.title = "Vous avez perdu !"
        self.emotion = "Sad"
        pokemon = self.window.manager.player.pokemon.name
        self.profile_tex = arcade.load_texture(f"assets/sprite/pokemon/"
                                               f"{pokemon}/portraits/"
                                               f"{self.emotion}.png")

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_show_view(self) -> None:

        """
        Méthode appelée lorsque la vue est affichée. Elle démarre la
        musique de la vue.
        """

        self.ui_manager.enable()

        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH)
            self.music_player = self.music.play(volume=1, loop=True)
