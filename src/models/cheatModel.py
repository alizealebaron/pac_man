# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cheatModel.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/11 08:28:59 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 20:12:53 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class CheatModel():

    """
    Modèle pour les cheats du jeu.

    Attributes:
        invicibility (bool): Indique si le cheat d'invincibilité est activé.
        ghost_freeze (bool): Indique si le cheat de gel des fantômes est
            activé.
        dynamax (bool): Indique si le mode dynamax est activé
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self):
        """
        Initialise le modèle de cheats avec les cheats désactivés par défaut.
        """

        self.invicibility = False
        self.ghost_freeze = False
        self.dynamax = False
