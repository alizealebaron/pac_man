# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  scoreModel.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/21 10:36:34 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 13:49:59 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


from pydantic import BaseModel, Field


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class Score(BaseModel):

    """
    Modèle de données pour les scores des personnages du jeu.

    Attributes:
        name (str): Le nom du personnage.
        score (int): Le score du personnage.
        pokemon (str): Le pokémon associé au personnage.
    """

    # +---------------------------------------------------------------------+
    # |                              Attributs                              |
    # +---------------------------------------------------------------------+

    name: str = Field(min_length=1, max_length=20)
    score: int = Field(ge=0)
    pokemon: str = Field(min_length=1)
