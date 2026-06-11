# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  arg_parser.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/19 09:22:52 by rruiz           #+#    #+#               #
#  Updated: 2026/06/11 13:52:56 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import argparse


# +-------------------------------------------------------------------------+
# |                                 Methods                                 |
# +-------------------------------------------------------------------------+

def check_argument() -> argparse.Namespace:

    """
    Vérifie les arguments passés en ligne de commande et retourne un objet
    contenant les arguments.

    Returns:
        argparse.Namespace: Un objet contenant les arguments passés en ligne de
        commande.
    """

    parse = argparse.ArgumentParser()

    parse.add_argument(
        'config_file',
        type=str,
        help='Path to the configuration file',
        nargs='?',
        default=None
    )
    arg: argparse.Namespace = parse.parse_args()

    return arg
