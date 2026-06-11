# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  playerModel.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/21 12:46:42 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 15:40:05 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import random
from typing import List
from src.models.configmodel import ConfigModel
from src.models.pokemonModel import PokemonModel
from src.models.animated_sprite import AnimatedSprite


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class PlayerModel():

    """
    Modèle du joueur.

    Attributes:
        pokemon (PokemonModel): Le pokémon du joueur.
        name (str): Le nom du joueur.
        x (int): La position x du joueur sur la grille.
        y (int): La position y du joueur sur la grille.
        pixel_offset_x (float): Le décalage en pixels sur l'axe x pour
            l'animation.
        pixel_offset_y (float): Le décalage en pixels sur l'axe y pour
            l'animation.
        direction (str): La direction actuelle du joueur ('up', 'down', 'left',
            'right').
        next_direction (str): La prochaine direction du joueur.
        nb_life (int): Le nombre de vies du joueur.
        score (int): Le score du joueur.
        sprite (AnimatedSprite): Le sprite animé du joueur.
        speed (float): La vitesse de déplacement du joueur.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, config: ConfigModel, lst_pokemon: List[PokemonModel]):

        """
        Initialise le modèle du joueur.

        Args:
            config (ConfigModel): La configuration du jeu.
            lst_pokemon (List[PokemonModel]): La liste des pokémons disponibles
                pour le joueur.
        """

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
        self.is_super = False
        self.time_super_max = 10
        self.super_timer = 0.0
        self.sprite = AnimatedSprite(self.pokemon.name, self.pokemon.width,
                                     self.pokemon.height, self.pokemon.nb_anim)
        self.speed = 3.0

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def reset_position(self) -> None:
        """
        Réinitialise la position du joueur au point de départ.
        """

        self.pixel_offset_x = 0.0
        self.pixel_offset_y = 0.0
        self.direction = None
        self.next_direction = None
        self.sprite.current_direction = "down"
        self.is_super = False
        self.super_timer = 0.0

    # +---------------------------------------------------------------------+
    # |                              Methods                                |
    # +---------------------------------------------------------------------+

    def _get_random_pokemon(self,
                            lst_pokemons: List[PokemonModel]) -> PokemonModel:
        """
        Sélectionne un pokémon aléatoire dans la liste des pokémons
        disponibles.

        Args:
            lst_pokemons (List[PokemonModel]): La liste des pokémons
                disponibles.

        Returns:
            PokemonModel: Un pokémon aléatoire sélectionné dans la liste.
        """

        return (lst_pokemons[14])
        # return (random.choice(lst_pokemons.name))

    def _get_random_name(self) -> str:

        """
        Génère un nom aléatoire pour le joueur en combinant un préfixe
        aléatoire avec le nom du pokémon du joueur.

        Returns:
            str: Un nom aléatoire pour le joueur.
        """

        prefixe = ["Bold", "Quirky", "Brave", "Calm", "Quiet", "Docile",
                   "Mild", "Rash", "Gentle", "Hardy", "Jolly", "Lax",
                   "Impish", "Sassy", "Naughty", "Modest", "Naive", "Hasty",
                   "Careful", "Bashful", "Relaxed", "Adamant", "Serious",
                   "Lonely", "Timid", "Chaotic"]

        return random.choice(prefixe) + "_" + self.pokemon.name

    def update_pokemon_sprite(self) -> None:

        """
        Met à jour le sprite du joueur en fonction du pokémon sélectionné.
        """

        self.sprite = AnimatedSprite(self.pokemon.name, self.pokemon.width,
                                     self.pokemon.height, self.pokemon.nb_anim)
