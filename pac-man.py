# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pac-man.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 16:14:42 by alebaron        #+#    #+#               #
#  Updated: 2026/06/12 11:56:34 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade
import argparse
import sys
from src.parsing.arg_parser import check_argument
from src.view.main_window import MainWindow
from src.pacmanManager import PacmanManager

# +-------------------------------------------------------------------------+
# |                                  CONST                                  |
# +-------------------------------------------------------------------------+


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pacmon Mystery Dungeon"


# +-------------------------------------------------------------------------+
# |                                  Main                                   |
# +-------------------------------------------------------------------------+

def main() -> None:

    """
    Fonction principale du jeu, initialise la fenêtre et le manager, puis
    démarre le jeu.
    """

    try:
        sys.setrecursionlimit(2000)

        # Récupération de la config
        arg: argparse.Namespace = check_argument()

        # Création du manager
        manager = PacmanManager(arg)

        # Affichage de la fenêtre de début de jeu

        _ = MainWindow(title=SCREEN_TITLE, fullscreen=True, manager=manager)
        arcade.run()

    except KeyboardInterrupt:
        print('Program interrupt by user.', file=sys.stderr)

    # except Exception as e:
    #     print(f'Unexpected error: {e}', file=sys.stderr)


if __name__ == '__main__':
    main()
