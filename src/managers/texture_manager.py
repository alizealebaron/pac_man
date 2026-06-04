# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  texture_manager.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/04 13:53:14 by alebaron        #+#    #+#               #
#  Updated: 2026/06/04 15:10:50 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import os
import arcade
from typing import Any, Dict


# +-------------------------------------------------------------------------+
# |                                  Class                                  |
# +-------------------------------------------------------------------------+

class TextureManager():

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self):

        self.__dict_texture = self.init_all_textures()

    # +---------------------------------------------------------------------+
    # |                             Accesseur                               |
    # +---------------------------------------------------------------------+

    def get_texture(self, path: str) -> arcade.Texture | None:

        if path in self.__dict_texture:
            return self.__dict_texture[path]
        return None

    # +---------------------------------------------------------------------+
    # |                              Methods                                |
    # +---------------------------------------------------------------------+

    def init_all_textures(self) -> Dict[str, Any]:

        dict_texture = {}

        for root, _, files in os.walk("assets/"):
            for file in files:

                if (file.endswith(".png") and
                   (root.endswith("animations") is False)):

                    texture = arcade.load_texture(f"{root}/{file}")
                    dict_texture[f"{root}/{file}"] = texture

        return dict_texture
