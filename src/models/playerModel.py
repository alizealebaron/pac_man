# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  playerModel.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/21 12:46:42 by alebaron        #+#    #+#               #
#  Updated: 2026/06/02 13:51:45 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import random
import arcade
from typing import List
from src.models.configmodel import ConfigModel
from src.models.pokemonModel import PokemonModel
from src.models.animated_sprite import AnimatedSprite


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class PlayerModel():

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, config: ConfigModel, lst_pokemon: List[PokemonModel]):

        self.pokemon = self._get_random_pokemon(lst_pokemon)
        self.name = self._get_random_name()
        self.x = 0
        self.y = 0
        self.pixel_offset_x = 0.0
        self.pixel_offset_y = 0.0
        self.direction = None
        self.next_direction = None
        self.nb_life = config.lives
        self.score = 0
        self.sprite = AnimatedSprite(self.pokemon.name, self.pokemon.width, self.pokemon.height, self.pokemon.nb_anim)

    # +---------------------------------------------------------------------+
    # |                              Methods                                |
    # +---------------------------------------------------------------------+

    def _get_random_pokemon(self,
                            lst_pokemons: List[PokemonModel]) -> PokemonModel:

        return (random.choice(lst_pokemons))

    def _get_random_name(self):

        prefixe = ["Bold", "Quirky", "Brave", "Calm", "Quiet", "Docile",
                   "Mild", "Rash", "Gentle", "Hardy", "Jolly", "Lax",
                   "Impish", "Sassy", "Naughty", "Modest", "Naive", "Hasty",
                   "Careful", "Bashful", "Relaxed", "Adamant", "Serious",
                   "Lonely", "Timid", "Chaotic"]

        return random.choice(prefixe) + "_" + self.pokemon.name

    def update_pokemon_sprite(self):
        self.sprite = AnimatedSprite(self.pokemon.name, self.pokemon.width,
                                     self.pokemon.height, self.pokemon.nb_anim)
