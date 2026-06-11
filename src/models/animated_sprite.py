# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  animated_sprite.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/01 14:38:04 by rruiz           #+#    #+#               #
#  Updated: 2026/06/11 11:34:51 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


import arcade


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class AnimatedSprite(arcade.Sprite):

    """
    Classe représentant un sprite animé pour les personnages du jeu.

    Attributes:
        pokemon_width (int): La largeur de chaque frame d'animation.
        pokemon_height (int): La hauteur de chaque frame d'animation.
        pokemon_nb_anim (int): Le nombre de frames d'animation par direction.
        sprite_sheet (arcade.SpriteSheet): La feuille de sprite contenant les
            animations.
        all_animations (dict): Un dictionnaire contenant les animations pour
            chaque direction.
        current_direction (str): La direction actuelle du sprite ('up', 'down',
            'left', 'right').
        current_frame (int): L'index de la frame d'animation actuelle.
        frame_counter (int): Un compteur pour contrôler la vitesse
            de l'animation.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, pokemon_name: str, pokemon_width: int,
                 pokemon_height: int, nb_anim: int, is_enemy: bool = None):

        """
        Initialise le sprite animé pour un personnage donné.

        Args:
            pokemon_name (str): Le nom du Pokémon ou de l'ennemi.
            pokemon_width (int): La largeur de chaque frame d'animation.
            pokemon_height (int): La hauteur de chaque frame d'animation.
            nb_anim (int): Le nombre de frames d'animation par direction.
            is_enemy (bool, optional): Indique si le sprite est un ennemi ou
                un Pokémon. Par défaut, None.
        """

        super().__init__()

        self.pokemon_width = pokemon_width
        self.pokemon_height = pokemon_height
        self.pokemon_nb_anim = nb_anim
        if not is_enemy:
            self.sprite_sheet = arcade.SpriteSheet(f'assets/sprite/pokemon/'
                                                   f'{pokemon_name}/animations'
                                                   f'/Walk-Anim.png')
        else:
            self.sprite_sheet = arcade.SpriteSheet(f'assets/sprite/enemy/'
                                                   f'{pokemon_name}/animations'
                                                   f'/Walk-Anim.png')
        self.all_animations = self._load_walk_anim()
        self.current_direction = 'down'
        self.current_frame = 0
        self.frame_counter = 0
        self.update_texture()

    # +---------------------------------------------------------------------+
    # |                                Method                               |
    # +---------------------------------------------------------------------+

    def _load_walk_anim(self) -> dict:

        """
        Charge les animations de marche à partir de la feuille de sprite.

        Returns:
            dict: Un dictionnaire contenant les animations pour chaque
                direction.
        """

        columns = self.pokemon_nb_anim
        all_textures = self.sprite_sheet.get_texture_grid(
            size=(self.pokemon_width, self.pokemon_height),
            columns=self.pokemon_nb_anim,
            count=columns*8
        )

        anim_south = all_textures[0:columns]
        anim_east = all_textures[columns*2:columns*3]
        anim_north = all_textures[columns*4:columns*5]
        anim_west = all_textures[columns*6:columns*7]

        return {
            'down': anim_south,
            'left': anim_west,
            'up': anim_north,
            'right': anim_east
        }

    def update_texture(self):
        """
        Met à jour la texture du sprite en fonction de la direction et de la
        frame actuelle.
        """

        texture = (self.all_animations[self.current_direction]
                   [self.current_frame])
        self.texture = texture

    def on_update(self, _: float):
        """
        Met à jour l'animation du sprite en fonction de la direction
        actuelle.
        """

        self.frame_counter += 1
        if self.frame_counter >= 5:
            self.current_frame = ((self.current_frame + 1) %
                                  (len(self.all_animations
                                       [self.current_direction])))
            self.update_texture()
            self.frame_counter = 0
