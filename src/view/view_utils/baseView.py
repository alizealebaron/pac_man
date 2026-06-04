# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  baseView.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/04 13:48:43 by alebaron        #+#    #+#               #
#  Updated: 2026/06/04 15:45:53 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade
from src.pacmanManager import PacmanManager
from src.managers.texture_manager import TextureManager

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/menu_background.png"
MUSIC_PATH = "assets/music/mainMenu_theme.mp3"

MAIN_FONT_PATH = "assets/font/main_font.ttf"
TEXT_FONT_PATH = "assets/font/text_font.otf"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class BaseView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self):

        # Instanciation de la classe mère
        super().__init__()

        # Récupération du manager
        self.manager: PacmanManager = self.window.manager
        self._texture_manager: TextureManager = self.manager.texture_manager

        # Initialisation du background par défaut
        self.background = self.get_texture(BACKGROUND_PATH)

        # Initialisation de la musique
        self.music_player = None
        self.music = None

        # Texture récurrente
        self.sprite_frame = self.get_texture("assets/sprite/face_frame.png")

    # +---------------------------------------------------------------------+
    # |                               Getter                                |
    # +---------------------------------------------------------------------+

    def get_texture(self, path: str) -> arcade.Texture | None:
        return self._texture_manager.get_texture(path)

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_show_view(self):

        # Gestion de la musique
        volume = self.manager.settings.volume
        if not (self.music_player and self.music_player.playing):
            self.music_player = self.music.play(volume=volume, loop=True)

    def on_draw(self):

        # On efface tout ce qu'il y a sur l'écran
        self.clear()

        # Affichage du fond d'écran
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height))
