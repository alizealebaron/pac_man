# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_loader.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/19 10:07:49 by rruiz           #+#    #+#               #
#  Updated: 2026/06/12 16:38:59 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import json
from typing import Any
import sys
from src.models.configmodel import ConfigModel


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class ConfigLoader:

    """
    Classe responsable du chargement de la configuration du jeu à partir d'un
    fichier JSON.

    Attributes:
        default_config (dict): La configuration par défaut utilisée en cas de
            problème lors du chargement du fichier de configuration.
    """

    default_config = {
        'highscore_filename': 'highscores.json',
        'level': [
            {'id': 1, 'width': 6, 'height': 6},
            {'id': 2, 'width': 10, 'height': 6},
            {'id': 3, 'width': 8, 'height': 8},
            {'id': 4, 'width': 8, 'height': 10},
            {'id': 5, 'width': 10, 'height': 10},
            {'id': 6, 'width': 12, 'height': 8},
            {'id': 7, 'width': 12, 'height': 12},
            {'id': 8, 'width': 16, 'height': 14},
            {'id': 9, 'width': 16, 'height': 18},
            {'id': 10, 'width': 20, 'height': 20}
        ],
        'lives': 3,
        'points_per_pacgum': 10,
        'points_per_super_pacgum': 50,
        'points_per_ghost': 200,
        'seed': 24,
        'level_max_time': 120
        }

    @staticmethod
    def load_config(config_file_path: str | None) -> ConfigModel:

        """
        Charge la configuration du jeu à partir d'un fichier JSON.
        Args:
            config_file_path (str | None): Le chemin vers le fichier de
                configuration. Si None, la configuration par défaut est
                utilisée.
        Returns:
            ConfigModel: La configuration du jeu.
        """

        if not config_file_path:
            return ConfigModel.build_config(ConfigLoader.default_config)

        config = ConfigLoader._clean_config(config_file_path)

        if not config:
            return ConfigModel.build_config(ConfigLoader.default_config)

        return ConfigModel.build_config(config)

    @staticmethod
    def _clean_config(config_file_path: str) -> dict[str, Any]:

        """
        Lit le fichier de configuration, supprime les commentaires et les
        lignes vides, et retourne un dictionnaire de configuration propre.

        Args:
            config_file_path (str): Le chemin vers le fichier de configuration.
        Returns:
            dict[str, Any]: Un dictionnaire de configuration propre.
        """

        try:
            with open(config_file_path, 'r') as f:
                config = f.read()
        except OSError as e:
            print(f'Warning: cannot open \'{config_file_path}\': {e}'
                  '; using default configuration', file=sys.stderr)
            return {}

        clean_lines = []
        for line in config.splitlines():
            match line:
                case str(x) if '#' in x:
                    no_comment = line.split('#')[0]
                case str(x) if '//' in x:
                    no_comment = line.split('//')[0]
                case str(x) if '/' in x:
                    no_comment = line.split('/')[0]
                case _:
                    no_comment = line
            clean_lines.append(no_comment)

        clean_config = '\n'.join(clean_lines)

        try:
            data: dict[str, Any] = json.loads(clean_config)
        except json.JSONDecodeError as e:
            print(f'Warning: invalid JSON in \'{config_file_path}\': {e}'
                  '; using default configuration', file=sys.stderr)
            return {}

        return data
