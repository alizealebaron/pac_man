# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_window.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/20 14:35:28 by alebaron        #+#    #+#               #
#  Updated: 2026/05/28 14:20:14 by alebaron        ###   ########.fr        #
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

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, title: str, fullscreen: bool, manager: PacmanManager):

        super().__init__(title=title, fullscreen=fullscreen)
        self.manager = manager

        # Démarrer le jeu
        self.start_view = MenuView()
        self.show_view(self.start_view)
