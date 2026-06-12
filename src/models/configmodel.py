# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  configmodel.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/19 11:08:47 by rruiz           #+#    #+#               #
#  Updated: 2026/06/12 12:13:45 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Any, Self
import sys

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


mandatory_keys: list[str] = ['highscore_filename', 'level', 'lives', 'pacgum',
                             'points_per_pacgum', 'points_per_super_pacgum',
                             'points_per_ghost', 'level_max_time', 'seed']
optional_keys: list[str] = []


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+


class LevelConfig(BaseModel):

    """
    Configuration d'un niveau.

    Attributes:
        id (int): L'identifiant du niveau.
        width (int): La largeur du labyrinthe.
        height (int): La hauteur du labyrinthe.
    """

    # +---------------------------------------------------------------------+
    # |                             Attributs                               |
    # +---------------------------------------------------------------------+

    id: int = Field(ge=1)
    width: int = Field(ge=2, le=500, default=10)
    height: int = Field(ge=2, le=500, default=10)


class ConfigModel(BaseModel):

    """
    Configuration globale du jeu.

    Attributes:
        highscore_filename (str): Le nom du fichier de sauvegarde des
            scores.
        level (list[LevelConfig]): La liste des configurations de niveaux.
        lives (int): Le nombre de vies du joueur.
        pacgum (int): Le nombre de pacgums dans le niveau.
        points_per_pacgum (int): Le nombre de points gagnés par pacgum.
        points_per_super_pacgum (int): Le nombre de points gagnés par super
            pacgum.
        points_per_ghost (int): Le nombre de points gagnés par fantôme
            mangé.
        level_max_time (int): Le temps maximum pour compléter un niveau en
            secondes.
        seed (Optional[int]): La graine pour la génération aléatoire du
            jeu. Si None, une graine aléatoire sera utilisée.
    """

    # +---------------------------------------------------------------------+
    # |                             Attributs                               |
    # +---------------------------------------------------------------------+

    highscore_filename: Optional[str] = Field(default="highscores.json",
                                              min_length=1)
    level: list[LevelConfig] = Field(min_length=1, default_factory=list)
    lives: int = Field(ge=1, le=1000, default=3)
    pacgum: int = Field(ge=1, le=1000, default=42)
    points_per_pacgum: int = Field(ge=1, le=1000, default=10)
    points_per_super_pacgum: int = Field(ge=1, le=1000, default=50)
    points_per_ghost: int = Field(ge=1, le=1000, default=100)
    level_max_time: int = Field(ge=1, le=3600, default=90)
    seed: Optional[int] = Field(default=42)

    # +---------------------------------------------------------------------+
    # |                              Methods                                |
    # +---------------------------------------------------------------------+

    @classmethod
    def build_config(cls, config: dict[str, Any]) -> Self:

        """
        Construit une instance de ConfigModel à partir d'un dictionnaire de
        configuration, en validant les données et en utilisant les valeurs
        par défaut en cas de données invalides.

        Args:
            config (dict[str, Any]): Le dictionnaire de configuration à
                valider.
        """

        clean: dict[str, Any] = {}

        for field_name, field_info in cls.model_fields.items():
            data = config.get(field_name)

            if not data and field_name in mandatory_keys:
                if field_name != 'level':
                    print(
                        f"Warning: invalid value for '{field_name}': {data}"
                        f"; using default ({field_info.default})",
                        file=sys.stderr
                    )
                else:
                    print(
                        f"Warning: invalid value for '{field_name}': {data}"
                        f"; using default value", file=sys.stderr)
                continue

            if field_name == 'level' and isinstance(data, list):
                valid_levels = []
                for item in data:
                    try:
                        valid_levels.append(LevelConfig.model_validate(item))
                    except ValidationError as e:
                        print(
                            f"Warning: invalid level config {item}: {e}; "
                            "skipped", file=sys.stderr
                        )
                if valid_levels:
                    clean[field_name] = valid_levels
                else:
                    print("Warning: no valid levels found; using default",
                          file=sys.stderr)
                continue

            try:
                cls.model_validate({field_name: data})
                clean[field_name] = data
            except ValidationError:
                default = field_info.default
                print(
                    f"Warning: invalid value for '{field_name}': {data}"
                    f"; using default ({default})", file=sys.stderr)

        return cls(**clean)
