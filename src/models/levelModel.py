# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  levelModel.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/19 14:39:15 by alebaron        #+#    #+#               #
#  Updated: 2026/06/13 13:56:46 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


from src.mazegenerator.mazegenerator import MazeGenerator
import os
import contextlib


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class Level():
    """
    Classe représentant un niveau du jeu.

    Attributes:
        level (int): Le numéro du niveau.
        maze (MazeGenerator): Le labyrinthe généré pour ce niveau.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, num_level: int, width: int, height: int, seed: int):

        """
        Initialise un niveau avec un numéro, une largeur, une hauteur et une
        graine pour la génération du labyrinthe.
        """

        self.level = num_level
        with open(os.devnull, 'w') as f:
            with contextlib.redirect_stdout(f):
                self.maze = MazeGenerator((width, height), seed=(num_level +
                                                                 seed))
