# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pause_view.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/05 07:29:23 by alebaron        #+#    #+#               #
#  Updated: 2026/06/05 07:50:59 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade
import arcade.gui

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/pause_background.png"
MUSIC_PATH = "assets/music/pause_theme.mp3"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+


class PauseView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, main_view):

        super().__init__()

        self.background = arcade.load_texture(BACKGROUND_PATH)
        self.menu_manager = arcade.gui.UIManager()

        self.main_view = main_view
        self.music_player = None

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.menu_manager.disable()

    def on_show_view(self):
        """This is run once when we switch to this view"""

        self.menu_manager.enable()

        volume = self.window.manager.settings.volume
        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH,
                                      streaming=True)
            self.music_player = self.music.play(volume=volume, loop=True)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen
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

        self.menu_manager.draw()
