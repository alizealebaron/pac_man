# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  quizz_result_view.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 16:28:27 by alebaron        #+#    #+#               #
#  Updated: 2026/06/02 13:58:48 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade
import random
from typing import Any, Dict

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/personnality_background.png"
MUSIC_PATH = "assets/music/personnality_theme.mp3"

SELECTED_PATH = "assets/quizz/question_selected.png"
UNSELECTED_PATH = "assets/quizz/question_unselected.png"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class ResultQuizzView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window: arcade.Window, music_player: Any, music: Any,
                 dict_caractere: Dict[str, int]):
        super().__init__()

        self.window = window
        self.background = arcade.load_texture(BACKGROUND_PATH)

        # Initialisation de la musique
        self.music_player = music_player
        self.music = music

        self.dict_caracteres = dict_caractere
        self.index_carac = 0

        self.caractere = max(self.dict_caracteres,
                             key=lambda key: self.dict_caracteres[key])
        data_questions = self.window.manager.data_questions
        self.lst_carac = data_questions.caracteres[self.caractere].split("\n")

        # Pokémon généré
        self.random_pokemon = None

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Affichage du background
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height
            )
        )

        # Affichage du bouton retour
        retour_sprite = arcade.load_texture("assets/button/retour.png")
        height = 90
        width = 170
        arcade.draw_texture_rect(
            texture=retour_sprite,
            rect=arcade.XYWH(45,
                             (self.window.height) - (height / 2),
                             width,
                             height)
        )

        # Afficher le texte final
        if ((len(self.lst_carac) > self.index_carac)):
            self.write_end_text()
        else:
            self.draw_pokemon()

    def on_mouse_press(self, x, y, _, __):

        # Bouton retour
        if (x > 2 and x < 95 and y > 995 and y < 1080):
            self.music.stop(self.music_player)
            self.window.show_view(self.window.start_view)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.ENTER or key == arcade.key.SPACE:

            if ((len(self.lst_carac) > self.index_carac)):
                self.index_carac += 1
            else:
                self.window.manager.player.pokemon = self.random_pokemon
                self.window.manager.player.update_pokemon_sprite()
                self.music.stop(self.music_player)
                self.window.show_view(self.window.start_view)

    # +---------------------------------------------------------------------+
    # |                            Draw Methods                             |
    # +---------------------------------------------------------------------+

    def draw_pokemon(self):

        possible_pokemon = [obj for obj in self.window.manager.pokemons
                            if obj.comportement == self.caractere]

        if self.random_pokemon is None:
            self.random_pokemon = random.choice(possible_pokemon)

        sprite = arcade.load_texture(f"assets/sprite/pokemon/"
                                     f"{self.random_pokemon.name}"
                                     "/portraits/Normal.png")
        sprite_size = 150

        arcade.draw_texture_rect(
            texture=sprite,
            rect=arcade.XYWH(self.width / 2,
                             self.height / 2,
                             sprite_size,
                             sprite_size)
        )

        sprite_frame = arcade.load_texture("assets/sprite/face_frame.png")
        arcade.draw_texture_rect(
            texture=sprite_frame,
            rect=arcade.XYWH(self.width / 2,
                             self.height / 2,
                             sprite_size + 15,
                             sprite_size + 15)
        )

        center_x = self.width / 2
        center_y = self.height / 2
        texte = arcade.Text(self.random_pokemon.name,
                            center_x,
                            center_y - sprite_size / 2 - 40,
                            align="center",
                            color=arcade.color.WHITE,
                            font_size=20,
                            font_name="FOT-Humming Pro",
                            anchor_x="center",
                            anchor_y="center")

        texte.draw()

    def write_end_text(self):

        center_x = self.width / 2
        center_y = self.height / 2
        texte = arcade.Text(self.lst_carac[self.index_carac],
                            center_x,
                            center_y,
                            align="center",
                            color=arcade.color.WHITE,
                            font_size=20,
                            font_name="FOT-Humming Pro",
                            anchor_x="center",
                            anchor_y="center")

        texte.draw()
