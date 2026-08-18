# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_window.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: emarette, rruiz, alebaron                 +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 14:35:28 by alebaron        #+#    #+#               #
#  Updated: 2026/08/18 12:49:41 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import arcade
from pyglet.image import load as pyglet_load
from src.view.menu_view import MenuView
from src.pacmanManager import PacmanManager


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class MainWindow(arcade.Window):

    """
    Classe principale de la fenêtre du jeu, gère les différentes vues et le
    manager du jeu.

    Attributs:
        manager (PacmanManager): Le manager du jeu, gère la logique du jeu et
            les données.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, title: str, fullscreen: bool,
                 manager: PacmanManager) -> None:

        """
        Initialise la fenêtre principale du jeu.

        Args:
            title (str): Le titre de la fenêtre.
            fullscreen (bool): Si la fenêtre doit être en plein écran ou non.
            manager (PacmanManager): Le manager du jeu, gère la logique du jeu
                et les données.
        """

        super().__init__(title=title, fullscreen=fullscreen)
        self.manager = manager

        # Charger et appliquer l'icône personnalisée
        icone = pyglet_load("assets/icone.png")
        self.set_icon(icone)

        # Démarrer le jeu
        self.start_view = MenuView()
        self.show_view(self.start_view)
