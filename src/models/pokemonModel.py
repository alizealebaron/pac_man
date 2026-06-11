# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pokemonModel.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/26 01:07:26 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 13:48:21 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


from pydantic import BaseModel, Field


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class PokemonModel(BaseModel):
    """
    Modèle de données pour les pokémons du jeu.

    Attributes:
        name (str): Le nom du pokémon.
        width (int): La largeur du sprite du pokémon.
        height (int): La hauteur du sprite du pokémon.
        nb_anim (int): Le nombre d'animations du sprite du pokémon.
        scale (float): L'échelle du sprite du pokémon.
        comportement1 (str): Le premier comportement du pokémon.
        comportement2 (str): Le second comportement du pokémon.
    """

    name: str = Field(min_length=1)
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    nb_anim: int = Field(ge=1)
    scale: float = Field(ge=1)
    comportement1: str
    comportement2: str
