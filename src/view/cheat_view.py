# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cheat_view.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/09 13:32:00 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 09:51:19 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade
import arcade.gui
from src.pacmanManager import PacmanManager

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/cheat_background.png"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class CheatView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window: arcade.Window, game_view: arcade.View):

        # Initialisation du composant parent
        super().__init__(window)
        self.game_view = game_view
        self.manager: PacmanManager = self.window.manager

        # Chargement des textures
        self.background = arcade.load_texture(BACKGROUND_PATH)
        self.retour_sprite = arcade.load_texture("assets/button/retour.png")
        self.score_sprite = arcade.load_texture("assets/menu/cheat.png")

        # Configuration de l'UI Arcade Manager
        self.ui_manager = arcade.gui.UIManager()
        self.init_settings_gui()

    # +---------------------------------------------------------------------+
    # |                            Init Methods                             |
    # +---------------------------------------------------------------------+

    def init_settings_gui(self):

        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        # === Invincibilité ===
        inv_row = arcade.gui.UIBoxLayout(vertical=False, space_between=20)

        inv_label = arcade.gui.UILabel(
            text="Invincibilité",
            text_color=arcade.color.WHITE,
            font_size=18
        )
        inv_row.add(inv_label)

        self.btn_inv = arcade.gui.UIFlatButton(
            text="Oui" if (self.manager.cheat.invicibility is True) else "Non",
            width=200
        )
        self.btn_inv.on_click = self.manage_invicibility
        inv_row.add(self.btn_inv)
        self.v_box.add(inv_row)

        # === Gelé les fantôme ===

        inv_row = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        inv_label = arcade.gui.UILabel(
            text="Gel des fantômes",
            text_color=arcade.color.WHITE,
            font_size=18
        )
        inv_row.add(inv_label)

        self.btn_ghost = arcade.gui.UIFlatButton(
            text="Oui" if (self.manager.cheat.ghost_freeze is True) else "Non",
            width=200
        )
        self.btn_ghost.on_click = self.manage_ghost
        inv_row.add(self.btn_ghost)
        self.v_box.add(inv_row)

        # === Création des derniers éléments et ajouts au manager ===

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
    # |                             Btn Methods                             |
    # +---------------------------------------------------------------------+

    def manage_invicibility(self, _):

        if self.btn_inv.text == "Oui":
            self.btn_inv.text = "Non"
            self.manager.cheat.invicibility = False
        else:
            self.btn_inv.text = "Oui"
            self.manager.cheat.invicibility = True

    def manage_ghost(self, _):

        if self.btn_ghost.text == "Oui":
            self.btn_ghost.text = "Non"
            self.manager.cheat.ghost_freeze = False
        else:
            self.btn_ghost.text = "Oui"
            self.manager.cheat.ghost_freeze = True

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_show_view(self):
        """Appelé quand la vue change"""
        self.ui_manager.enable()

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
            rect=arcade.XYWH(45,
                             (self.window.height) - (height / 2),
                             width,
                             height)
        )

        # Affichage du fond des settings
        arcade.draw_texture_rect(
            texture=self.score_sprite,
            rect=arcade.XYWH(
                x=self.window.width / 2 + 20,
                y=self.window.height / 2,
                width=1400,
                height=1000
            )
        )

        self.ui_manager.draw()

    def on_mouse_press(self, x, y, _, __):

        # Bouton retour
        if (x > 2 and x < 95 and y > 995 and y < 1080):
            self.window.show_view(self.game_view)
