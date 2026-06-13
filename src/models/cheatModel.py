# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cheatModel.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/11 08:28:59 by alebaron        #+#    #+#               #
#  Updated: 2026/06/12 14:21:43 by rruiz           ###   ########.fr        #
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
        intagibilite (bool): Indique si le cheat de gel des fantômes est
            activé.
        dynamax (bool): Indique si le mode dynamax est activé
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self) -> None:
        """
        Initialise le modèle de cheats avec les cheats désactivés par défaut.
        """

        self.invicibility = False
        self.intagibilite = False
        self.dynamax = False
