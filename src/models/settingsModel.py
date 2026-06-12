# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : settingsModel.py                                                 #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/06/04 08:07:14 by alebaron                                #
# @update   : 2026/06/04 08:15:00 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import arcade


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class SettingsModel():

    """
    Modèle de données pour les paramètres du jeu.

    Attributes:
        configuration (str): La configuration de touches actuelle
            ("QWERTY" ou "AZERTY").
        volume (float): Le volume actuel du jeu (entre 0.0 et 1.0).
        dict_key (Dict[str, Dict[str, int]]): Un dictionnaire associant les
            configurations de touches à leurs mappings respectifs.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self):

        """
        Initialise les paramètres du jeu avec des valeurs par défaut.
        """

        self.configuration = "QWERTY"
        self.volume = 0.5

        self.dict_key = {
            "QWERTY": {
                    "up": arcade.key.W,
                    "down": arcade.key.S,
                    "left": arcade.key.A,
                    "right": arcade.key.D
            },
            "AZERTY": {
                    "up": arcade.key.Z,
                    "down": arcade.key.S,
                    "left": arcade.key.Q,
                    "right": arcade.key.D
            }
        }
