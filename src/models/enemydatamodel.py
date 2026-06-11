# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  enemydatamodel.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/06 12:06:51 by rruiz           #+#    #+#               #
#  Updated: 2026/06/11 12:08:38 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


from pydantic import BaseModel, Field


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class EnemyDataModel(BaseModel):

    """
    Modèle de données pour les ennemis du jeu.

    Attributes:
        name (str): Le nom de l'ennemi.
        width (int): La largeur du sprite de l'ennemi.
        height (int): La hauteur du sprite de l'ennemi.
        nb_anim (int): Le nombre d'animations du sprite de l'ennemi.
        scale (float): L'échelle du sprite de l'ennemi.
    """

    # +---------------------------------------------------------------------+
    # |                             Attributs                               |
    # +---------------------------------------------------------------------+

    name: str = Field(min_length=1)
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    nb_anim: int = Field(ge=1)
    scale: float = Field(ge=1)
