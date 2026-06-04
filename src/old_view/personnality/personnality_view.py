# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  personnality_view.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/26 01:33:59 by alebaron        #+#    #+#               #
#  Updated: 2026/06/04 11:46:32 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade
from src.view.personnality.quizz_view import QuizzView

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

class PersonnalityView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window: arcade.Window):
        super().__init__()

        self.window = window

        self.background = arcade.load_texture(BACKGROUND_PATH)

        # Initialisation de la musique
        self.music_player = None

        # Initalisation des questions
        self.reponses = ["Oui", "Non"]
        self.selected_reponse = 0

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_show_view(self):
        """Appelé quand la vue change"""
        volume = self.window.manager.settings.volume
        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH,
                                      streaming=True)
            self.music_player = self.music.play(volume=volume, loop=True)

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

        # Affichage du premier message
        self.draw_begin_text()

        # Affichage des deux premières réponses

        start_y = self.window.height * 0.5
        space_between = 150

        for reponse in self.reponses:

            if (reponse is self.reponses[self.selected_reponse]):
                question_sprite = arcade.load_texture(SELECTED_PATH)
            else:
                question_sprite = arcade.load_texture(UNSELECTED_PATH)

            sprite_width = self.window.width * 0.5
            sprite_height = self.window.height * 0.09
            center_x = self.width / 2
            center_y = start_y

            arcade.draw_texture_rect(
                texture=question_sprite,
                rect=arcade.XYWH(center_x, center_y, sprite_width,
                                 sprite_height)
            )

            texte = arcade.Text(
                text=reponse,
                x=center_x,
                y=center_y,
                color=arcade.color.WHITE,
                font_size=16,
                anchor_x="center",
                anchor_y="center"
            )
            texte.draw()

            start_y += space_between

    def on_mouse_press(self, x, y, _, __):

        # Bouton retour
        if (x > 2 and x < 95 and y > 995 and y < 1080):
            self.music.stop(self.music_player)
            self.window.show_view(self.window.start_view)

    def on_key_press(self, key, modifiers):

        dict_key = self.window.manager.settings.dict_key
        dict_key = dict_key[self.window.manager.settings.configuration]

        if key == dict_key["up"] or key == arcade.key.UP:
            self.selected_reponse = ((self.selected_reponse - 1) %
                                     len(self.reponses))

        if key == dict_key["down"] or key == arcade.key.DOWN:
            self.selected_reponse = ((self.selected_reponse + 1) %
                                     len(self.reponses))

        if key == arcade.key.ENTER or key == arcade.key.SPACE:
            if self.selected_reponse == 0:
                self.window.show_view(QuizzView(self.window,
                                                self.music_player,
                                                self.music))
            elif self.selected_reponse == 1:
                self.music.stop(self.music_player)
                self.window.show_view(self.window.start_view)

    # +---------------------------------------------------------------------+
    # |                            Draw methods                             |
    # +---------------------------------------------------------------------+

    def draw_begin_text(self):

        text_box_sprite = arcade.load_texture("assets/menu/text_box.png")
        arcade.draw_texture_rect(texture=text_box_sprite,
                                 rect=arcade.XYWH(self.window.width / 2,
                                                  (self.window.height * 0.95
                                                   / 2),
                                                  self.window.width,
                                                  self.window.height))

        text_content = "Vous vous apprêtez à réaliser un test de personnalité"
        text_content += " pour déterminer votre Pokémon."
        texte = arcade.Text(text_content,
                            self.width / 2,
                            150,
                            align="center",
                            color=arcade.color.WHITE,
                            font_size=20,
                            font_name="FOT-Humming Pro",
                            anchor_x="center",
                            anchor_y="center")
        texte.draw()

        text_content = "Cela prendra quelques minutes."
        texte = arcade.Text(text_content,
                            self.width / 2,
                            100,
                            align="center",
                            color=arcade.color.WHITE,
                            font_size=20,
                            font_name="FOT-Humming Pro",
                            anchor_x="center",
                            anchor_y="center")
        texte.draw()

        text_content = "Voulez-vous continuer ?"
        texte = arcade.Text(text_content,
                            self.width / 2,
                            50,
                            align="center",
                            color=arcade.color.WHITE,
                            font_size=20,
                            font_name="FOT-Humming Pro",
                            anchor_x="center",
                            anchor_y="center")
        texte.draw()
