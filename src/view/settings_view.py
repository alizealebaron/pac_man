# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  settings_view.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/23 13:56:54 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 08:09:09 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+

import arcade
import arcade.gui
from src.pacmanManager import PacmanManager

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/settings_background.png"
MUSIC_PATH = "assets/music/settings_theme.mp3"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class SettingsView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window):

        # Appelle à la fonction d'initialisation parente
        super().__init__(window)

        # Récupération du manager
        self.manager: PacmanManager = self.window.manager

        # Téléchargement des textures avant le draw
        self.background = arcade.load_texture(BACKGROUND_PATH)
        self.retour_sprite = arcade.load_texture("assets/button/retour.png")
        self.settings_sprite = arcade.load_texture("assets/menu/settings.png")

        # Initialisation de la musique
        self.music_player = None

        # Configuration de l'UI Arcade Manager
        self.ui_manager = arcade.gui.UIManager()
        self.init_settings_gui()

    # +---------------------------------------------------------------------+
    # |                            Init Methods                             |
    # +---------------------------------------------------------------------+

    def init_settings_gui(self):

        # Création d'un layout vertical pour ordonner nos éléments
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        # Label pour le volume
        volume_label = arcade.gui.UILabel(
            text="Volume de la musique",
            text_color=arcade.color.WHITE,
            font_size=18
        )
        self.v_box.add(volume_label)

        # Le Slider
        self.volume_slider = arcade.gui.UISlider(
            value=self.manager.settings.volume * 100,
            min_value=0,
            max_value=100,
            width=300
        )
        self.volume_slider.on_change = self.on_volume_change
        self.v_box.add(self.volume_slider)

        # Configuration du clavier
        clavier_label = arcade.gui.UILabel(
            text="Configuration Clavier",
            text_color=arcade.color.WHITE,
            font_size=18
        )
        self.v_box.add(clavier_label)

        # Bouton pour basculer entre les configurations
        self.key_config_button = arcade.gui.UIFlatButton(
            text=self.manager.settings.configuration,
            width=200
        )
        self.key_config_button.on_click = self.on_key_config_click
        self.v_box.add(self.key_config_button)

        # Création du conteneur d'ancrage global
        anchor_layout = arcade.gui.UIAnchorLayout()

        # Ajout de la v_box centrée dans ce conteneur
        anchor_layout.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )

        # Injection du layout dans le manager principal
        self.ui_manager.add(anchor_layout)

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_show_view(self):
        """Appelé quand la vue change"""
        self.ui_manager.enable()
        volume = self.window.manager.settings.volume
        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH,
                                      streaming=True)
            self.music_player = self.music.play(volume=volume, loop=True)

    def on_hide_view(self):
        """Appelé quand la vue change"""
        self.ui_manager.disable()

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
                width=1400,
                height=1000
            )
        )

        # Ajout des settings
        self.ui_manager.draw()

    def on_mouse_press(self, x, y, _, __):

        # Bouton retour
        if (x > 2 and x < 95 and y > 995 and y < 1080):
            self.music.stop(self.music_player)
            self.window.show_view(self.window.start_view)

    # +---------------------------------------------------------------------+
    # |                           Change Methods                            |
    # +---------------------------------------------------------------------+

    def on_volume_change(self, event):
        """Gère le changement de volume via le slider"""
        self.manager.settings.volume = self.volume_slider.value / 100.0

        if self.music_player and self.music_player.playing:
            self.music.set_volume(self.manager.settings.volume,
                                  self.music_player)

    def on_key_config_click(self, event):
        """Gère le changement de configuration de touches"""

        if self.key_config_button.text == "QWERTY":
            self.key_config_button.text = "AZERTY"
            self.manager.settings.configuration = "AZERTY"
        else:
            self.manager.settings.configuration = "QWERTY"
            self.key_config_button.text = "QWERTY"
