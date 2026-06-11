# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  questionModel.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/26 00:33:59 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 13:49:46 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


from typing import List, Dict
from pydantic import BaseModel, Field


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class ReponseModel(BaseModel):

    """
    Modèle de données pour les réponses d'une question.

    Attributes:
        reponse (str): Le texte de la réponse.
        scores (Dict[str, int]): Un dictionnaire associant les personnages à
            leurs scores respectifs pour cette réponse.
    """

    # +---------------------------------------------------------------------+
    # |                             Attributs                               |
    # +---------------------------------------------------------------------+

    reponse: str = Field(min_length=1)
    scores: Dict[str, int]


class QuestionModel(BaseModel):

    """
    Modèle de données pour les questions du jeu.

    Attributes:
        texte (str): Le texte de la question.
        reponses (List[ReponseModel]): La liste des réponses possibles à la
            question.
    """

    # +---------------------------------------------------------------------+
    # |                             Attributs                               |
    # +---------------------------------------------------------------------+

    texte: str = Field(min_length=1)
    reponses: List[ReponseModel]


class DataQuestionsModel(BaseModel):

    """
    Modèle de données pour l'ensemble des questions du jeu.
    Attributes:
        caracteres (Dict[str, str]): Un dictionnaire associant les personnages
            à leurs caractéristiques.
        questions (Dict[str, QuestionModel]): Un dictionnaire associant les
            identifiants de questions à leurs modèles respectifs.
    """

    # +---------------------------------------------------------------------+
    # |                             Attributs                               |
    # +---------------------------------------------------------------------+

    caracteres: Dict[str, str]
    questions: Dict[str, QuestionModel]
