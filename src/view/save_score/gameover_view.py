# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  gameover_view.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/02 08:06:31 by alebaron        #+#    #+#               #
#  Updated: 2026/06/09 08:27:00 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
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

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window):
        super().__init__(window)

        self.background = arcade.load_texture(BACKGROUND_PATH)

        # Initialisation des infos de la view
        self.title = "Game Over !"
        self.emotion = "Sad"
        pokemon = self.window.manager.player.pokemon.name
        self.profile_tex = arcade.load_texture(f"assets/sprite/pokemon/"
                                               f"{pokemon}/portraits/"
                                               f"{self.emotion}.png")

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_show_view(self):
        """Appelé quand la vue change"""
        self.ui_manager.enable()

        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH)
            self.music_player = self.music.play(volume=1, loop=True)
