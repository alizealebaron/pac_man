# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  levelModel.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/19 14:39:15 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 13:45:30 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


from src.mazegenerator.mazegenerator import MazeGenerator


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
        self.maze = MazeGenerator((width, height), seed=(num_level + seed))
