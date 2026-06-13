# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  quizz_view.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/26 04:44:09 by alebaron        #+#    #+#               #
#  Updated: 2026/06/12 15:48:32 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import time
import arcade
import random
from typing import Any, List
from src.models.questionModel import QuestionModel, ReponseModel
from src.view.personnality.quizz_result_view import ResultQuizzView

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

class QuizzView(arcade.View):

    """
    Vue pour le quizz de personnalité.

    Attributes:
        window (arcade.Window): La fenêtre de jeu.
        background (arcade.Texture): La texture de fond de la vue.
        music_player (arcade.SoundPlayer): Le lecteur de musique pour la vue.
        lst_questions (List[QuestionModel]): La liste des questions du quizz.
        index_question (int): L'index de la question actuellement affichée.
        reponses (List[ReponseModel]): La liste des réponses possibles à la
            question actuelle.
        selected_reponse (int): L'index de la réponse actuellement
            sélectionnée.
        dict_caracteres (Dict[str, int]): Un dictionnaire associant les
            caractères à leurs scores respectifs.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window: arcade.Window, music_player: Any,
                 music: Any) -> None:

        """
        Initialise la vue du quizz de personnalité.

        Args:
            window (arcade.Window): La fenêtre de jeu.
            music_player (Any): Le lecteur de musique pour la vue.
            music (Any): La musique à jouer dans la vue.
        """

        # Appelle à la fonction d'initialisation parente

        super().__init__()

        self.window = window

        self.background = arcade.load_texture(BACKGROUND_PATH)

        # Initialisation de la musique
        self.music_player = music_player
        self.music = music

        # Initalisation des questions
        self.lst_questions = self.random_question()
        self.index_question = 0

        # Initialisation des réponses
        self.reponses: List[ReponseModel] = []
        self.selected_reponse = 0

        # Initialisation du caractère
        self.dict_caracteres = self.get_dict_caracteres()

    # +---------------------------------------------------------------------+
    # |                            Init Methods                             |
    # +---------------------------------------------------------------------+

    def get_dict_caracteres(self) -> dict[str, int]:

        """
        Initialise le dictionnaire des caractères avec des scores à 0.

        Returns:
            dict[str, int]: Un dictionnaire associant les caractères à leurs
            scores respectifs, initialisés à 0.
        """

        dict_carac = {}
        lst_carac = self.window.manager.data_questions.caracteres

        for carac in lst_carac:
            dict_carac[carac] = 0

        return dict_carac

    def random_question(self) -> List[QuestionModel]:

        """
        Mélange les questions du quizz et retourne une liste de 10 questions
        aléatoires, avec la dernière question à la fin de la liste.

        Returns:
            List[QuestionModel]: Une liste de 10 questions aléatoires, avec la
                dernière question à la fin de la liste.
        """

        random.seed(int(time.time()))

        questions_dict = self.window.manager.data_questions.questions
        lst_questions: List[QuestionModel] = list(questions_dict.values())

        temp_question = lst_questions.pop(len(lst_questions) - 1)
        result = random.sample(lst_questions, 10)
        result.append(temp_question)

        return result

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

        # Affichage de la question actuelle
        if self.index_question < len(self.lst_questions):
            self.draw_actual_question()

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

        dict_key = self.window.manager.settings.dict_key
        dict_key = dict_key[self.window.manager.settings.configuration]

        if key == dict_key["up"] or key == arcade.key.UP:
            self.selected_reponse = ((self.selected_reponse + 1) %
                                     len(self.reponses))

        if key == dict_key["down"] or key == arcade.key.DOWN:
            self.selected_reponse = ((self.selected_reponse - 1) %
                                     len(self.reponses))

        if key == arcade.key.ENTER or key == arcade.key.SPACE:
            self.selected_reponse = 0
            if self.index_question < len(self.lst_questions):
                self.update_score()
                self.index_question += 1
            elif self.index_question == len(self.lst_questions) and self:
                self.window.show_view(ResultQuizzView(self.window,
                                                      self.music_player,
                                                      self.music,
                                                      self.dict_caracteres))

    # +---------------------------------------------------------------------+
    # |                           Update Methods                            |
    # +---------------------------------------------------------------------+

    def update_score(self) -> None:

        """
        Met à jour le score selon la réponse sélectionnée.
        """

        reponse = self.reponses[self.selected_reponse]

        for score in reponse.scores:
            self.dict_caracteres[score] += reponse.scores[score]

    # +---------------------------------------------------------------------+
    # |                            Draw Methods                             |
    # +---------------------------------------------------------------------+

    def draw_actual_question(self) -> None:

        """
        Affiche la question actuelle et ses réponses.
        """

        # Récupération des données
        act_q = self.lst_questions[self.index_question]
        self.reponses = act_q.reponses[::-1]
        nb_reponses = len(self.reponses)

        # Initialisation des positions initiales
        center_height = self.height * 0.81
        space_between = 150

        sprite_width = self.window.width * 0.6
        sprite_height = self.window.height * 0.09

        # Formule pour la hauteur totale du bloc de réponses
        total_height = ((nb_reponses * sprite_height) +
                        ((nb_reponses - 1) * space_between))

        # Calcul du premier start_y (le sprite du bas)
        start_y = center_height - (total_height / 2) + (sprite_height / 2)

        for reponse in self.reponses:

            if (reponse is self.reponses[self.selected_reponse]):
                question_sprite = arcade.load_texture(SELECTED_PATH)
            else:
                question_sprite = arcade.load_texture(UNSELECTED_PATH)

            center_x = self.width / 2
            center_y = start_y

            arcade.draw_texture_rect(
                texture=question_sprite,
                rect=arcade.XYWH(center_x, center_y, sprite_width,
                                 sprite_height)
            )

            texte = arcade.Text(
                text=reponse.reponse,
                x=center_x,
                y=center_y,
                color=arcade.color.WHITE,
                font_size=16,
                anchor_x="center",
                anchor_y="center"
            )
            texte.draw()

            start_y += space_between

        text_box_sprite = arcade.load_texture("assets/menu/text_box.png")
        arcade.draw_texture_rect(texture=text_box_sprite,
                                 rect=arcade.XYWH(self.window.width / 2,
                                                  (self.window.height * 0.95
                                                   / 2),
                                                  self.window.width,
                                                  self.window.height))

        center_x = self.width / 2
        center_y = 200
        texte = arcade.Text(act_q.texte,
                            center_x,
                            center_y,
                            align="center",
                            color=arcade.color.WHITE,
                            font_size=20,
                            font_name="FOT-Humming Pro",
                            anchor_x="center",
                            anchor_y="center")
        texte.draw()
