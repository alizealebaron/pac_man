# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  animated_sprite.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/01 14:38:04 by rruiz           #+#    #+#               #
#  Updated: 2026/06/06 12:00:53 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

class AnimatedSprite(arcade.Sprite):
    def __init__(self, pokemon_name: str, pokemon_width: int, pokemon_height: int, nb_anim: int, is_enemy: bool = None):
        super().__init__()

        self.pokemon_width = pokemon_width
        self.pokemon_height = pokemon_height
        self.pokemon_nb_anim = nb_anim
        if not is_enemy:
            self.sprite_sheet = arcade.SpriteSheet(f'assets/sprite/pokemon/{pokemon_name}/animations/Walk-Anim.png')
        else:
            self.sprite_sheet = arcade.SpriteSheet(f'assets/sprite/enemy/{pokemon_name}/animations/Walk-Anim.png')
        self.all_animations = self._load_walk_anim()
        self.current_direction = 'down'
        self.current_frame = 0
        self.frame_counter = 0
        self.update_texture()

    def _load_walk_anim(self):
        columns = self.pokemon_nb_anim
        all_textures = self.sprite_sheet.get_texture_grid(
            size = (self.pokemon_width, self.pokemon_height),
            columns = self.pokemon_nb_anim,
            count = columns*8
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
        texture = self.all_animations[self.current_direction][self.current_frame]
        self.texture = texture

    def on_update(self, delta_time: float):
        self.frame_counter += 1
        if self.frame_counter >= 5:
            self.current_frame = (self.current_frame + 1) % len(self.all_animations[self.current_direction])
            self.update_texture()
            self.frame_counter = 0
