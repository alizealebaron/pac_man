# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  quizz_result_view.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 16:28:27 by alebaron        #+#    #+#               #
#  Updated: 2026/06/12 15:42:38 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade
import random
from typing import Any, Dict, List, Optional

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

    """
    Vue pour afficher les résultats du quizz de personnalité.

    Attributes:
        window (arcade.Window): La fenêtre de jeu.
        background (arcade.Texture): La texture de fond de la vue.
        music_player (arcade.SoundPlayer): Le lecteur de musique pour la vue.
        dict_caracteres (Dict[str, int]): Un dictionnaire associant les
            caractères à leurs scores respectifs.
        index_carac (int): L'index du caractère actuellement affiché.
        caractere (str): Le caractère dominant du joueur.
        lst_carac (List[str]): La liste des caractéristiques associées au
            caractère dominant.
        random_pokemon (str): Le nom du pokémon généré aléatoirement.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window: arcade.Window, music_player: Any, music: Any,
                 dict_caractere: Dict[str, int]) -> None:

        """
        Initialise la vue de résultat du quizz.

        Args:
            window (arcade.Window): La fenêtre de jeu.
            music_player (Any): Le lecteur de musique pour la vue.
            music (Any): La musique à jouer dans la vue.
            dict_caractere (Dict[str, int]): Un dictionnaire associant les
                caractères à leurs scores respectifs.
        """

        # Init de la classe parente

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
        self.lst_carac: List[str] = (
            data_questions.caracteres[self.caractere].split("\n"))

        # Pokémon généré
        self.random_pokemon: Optional[Any] = None

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_draw(self) -> None:

        """
        Méthode appelée pour dessiner la vue.
        """

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

    def on_mouse_press(self, x: int, y: int, _: int, __: int) -> None:

        """
        Méthode appelée lorsque l'on clique sur la souris.
        """

        # Bouton retour
        if (x > 2 and x < 95 and y > 995 and y < 1080):
            self.music.stop(self.music_player)
            self.window.show_view(self.window.start_view)

    def on_key_press(self, key: int, _: int) -> None:

        """
        Méthode appelée lorsque l'on appuie sur une touche du clavier.
        """

        if key == arcade.key.ENTER or key == arcade.key.SPACE:

            if ((len(self.lst_carac) > self.index_carac)):
                self.index_carac += 1
            else:
                if self.random_pokemon is not None:
                    self.window.manager.player.pokemon = self.random_pokemon
                    self.window.manager.player.update_pokemon_sprite()
                    if (self.window.manager.cheat.dynamax is True):
                        self.window.manager.player.pokemon.scale *= 3
                self.music.stop(self.music_player)
                self.window.show_view(self.window.start_view)

    # +---------------------------------------------------------------------+
    # |                            Draw Methods                             |
    # +---------------------------------------------------------------------+

    def draw_pokemon(self) -> None:

        """
        Affiche le pokémon correspondant au caractère dominant du joueur.
        """

        possible_pokemon1 = [obj for obj in self.window.manager.pokemons
                             if obj.comportement1 == self.caractere]
        possible_pokemon2 = [obj for obj in self.window.manager.pokemons
                             if obj.comportement2 == self.caractere]

        possible_pokemon = possible_pokemon1 + possible_pokemon2

        if self.random_pokemon is None:
            self.random_pokemon = random.choice(possible_pokemon)

        pokemon = self.random_pokemon
        if pokemon is None:
            return

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

    def write_end_text(self) -> None:

        """
        Affiche le texte final du résultat du quizz, qui correspond à une
        caractéristique du caractère dominant du joueur.
        """

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
