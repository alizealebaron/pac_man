# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cheat_view.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/09 13:32:00 by alebaron        #+#    #+#               #
#  Updated: 2026/06/12 16:07:08 by alebaron        ###   ########.fr        #
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

    """
    Vue de triche, permet d'activer des cheats pour faciliter le jeu.

    Attributs:
        game_view (arcade.View): La vue du jeu, pour pouvoir y retourner.
        manager (PacmanManager): Le manager du jeu, pour pouvoir accéder
            aux cheats.
        background (arcade.Texture): Le background de la vue.
        retour_sprite (arcade.Texture): Le sprite du bouton de retour.
        score_sprite (arcade.Texture): Le sprite du fond des settings.
        ui_manager (arcade.gui.UIManager): Le manager de l'UI pour gérer les
            éléments graphiques de la vue.
        v_box (arcade.gui.UIBoxLayout): Le layout vertical pour organiser les
            éléments de la vue.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window: arcade.Window, game_view: arcade.View):

        """
        Initialise la vue de triche.

        Args:
            window (arcade.Window): La fenêtre du jeu.
            game_view (arcade.View): La vue du jeu, pour pouvoir y retourner.
        """

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

    def init_settings_gui(self) -> None:

        """
        Initialise les éléments graphiques de la vue de triche.
        """

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
            text="Intangibilité",
            text_color=arcade.color.WHITE,
            font_size=18
        )
        inv_row.add(inv_label)

        self.btn_ghost = arcade.gui.UIFlatButton(
            text="Oui" if (self.manager.cheat.intagibilite is True) else "Non",
            width=200
        )
        self.btn_ghost.on_click = self.manage_ghost
        inv_row.add(self.btn_ghost)
        self.v_box.add(inv_row)

        # === Augmenter / Réduire la vitesse ===

        inv_row = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        inv_label = arcade.gui.UILabel(
            text="Vitesse du joueur",
            text_color=arcade.color.WHITE,
            font_size=18
        )
        inv_row.add(inv_label)

        self.btn_player_speed = arcade.gui.UIFlatButton(
            text=f"{self.manager.player.speed}",
            width=200
        )
        self.btn_player_speed.on_click = self.manage_player_speed
        inv_row.add(self.btn_player_speed)
        self.v_box.add(inv_row)

        # === Level skip ===

        inv_row = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        inv_label = arcade.gui.UILabel(
            text="Passer le niveau actuel",
            text_color=arcade.color.WHITE,
            font_size=18
        )
        inv_row.add(inv_label)

        if (self.manager.actual_level + 2 > (len(self.manager.level))):
            text = "Fin du jeu"
        else:
            text = f"Passer à l'étage n°{self.manager.actual_level + 2}"

        self.btn_level_skip = arcade.gui.UIFlatButton(
            text=text,
            width=200
        )
        self.btn_level_skip.on_click = self.manage_level_skip
        inv_row.add(self.btn_level_skip)
        self.v_box.add(inv_row)

        # === Le fameux mode dynamax :D ===

        inv_row = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        inv_label = arcade.gui.UILabel(
            text="Mode Dynamax",
            text_color=arcade.color.WHITE,
            font_size=18
        )
        inv_row.add(inv_label)

        self.btn_dyna = arcade.gui.UIFlatButton(
            text="Oui" if (self.manager.cheat.dynamax is True) else "Non",
            width=200
        )
        self.btn_dyna.on_click = self.manage_dynamax
        inv_row.add(self.btn_dyna)
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

    def manage_invicibility(self, _) -> None:

        """Gère le changement d'état de l'invincibilité."""

        if self.btn_inv.text == "Oui":
            self.btn_inv.text = "Non"
            self.manager.cheat.invicibility = False
        else:
            self.btn_inv.text = "Oui"
            self.manager.cheat.invicibility = True

    def manage_ghost(self, _) -> None:

        """Gère le changement d'intagibilite."""

        if self.btn_ghost.text == "Oui":
            self.btn_ghost.text = "Non"
            self.manager.cheat.intagibilite = False
        else:
            self.btn_ghost.text = "Oui"
            self.manager.cheat.intagibilite = True

    def manage_player_speed(self, _) -> None:

        """Gère le changement de vitesse du joueur."""

        new_speed = (self.manager.player.speed % 10) + 1
        self.btn_player_speed.text = f"{new_speed}"
        self.manager.player.speed = new_speed

    def manage_level_skip(self, _) -> None:

        """Passe le niveau au prochain level"""
        self.game_view.is_finished = 1
        self.window.show_view(self.game_view)

    def manage_dynamax(self, _) -> None:

        """Gère le changement d'état du mod dynamax."""

        if self.btn_dyna.text == "Oui":
            self.btn_dyna.text = "Non"
            self.manager.cheat.dynamax = False
            self.manager.player.pokemon.scale /= 3
        else:
            self.btn_dyna.text = "Oui"
            self.manager.cheat.dynamax = True
            self.manager.player.pokemon.scale *= 3

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_show_view(self) -> None:

        """Appelée quand la vue est affichée"""

        self.ui_manager.enable()

    def on_hide_view(self) -> None:

        """Appelée quand la vue est cachée"""

        self.ui_manager.disable()

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

    def on_mouse_press(self, x, y, _, __) -> None:

        """
        Méthode appelée lorsque l'on clique sur la souris.
        """

        # Bouton retour
        if (x > 2 and x < 95 and y > 995 and y < 1080):
            self.window.show_view(self.game_view)

    def on_key_press(self, key, modifiers) -> None:

        """
        Méthode appelée lorsque l'on appuie sur une touche du clavier.
        """

        # Afficher le menu de pause
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
