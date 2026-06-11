# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_window.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 14:35:28 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 14:51:23 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import arcade
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

    def __init__(self, title: str, fullscreen: bool, manager: PacmanManager):

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

        # Démarrer le jeu
        self.start_view = MenuView()
        self.show_view(self.start_view)
