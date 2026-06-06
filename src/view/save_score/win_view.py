# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  win_view.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/28 14:12:22 by alebaron        #+#    #+#               #
#  Updated: 2026/06/05 07:59:24 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import arcade
import arcade.gui
from src.models.scoreModel import Score

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


BACKGROUND_PATH = "assets/background/save_score_background.png"
MUSIC_PATH = "assets/music/save_score_theme.mp3"

SELECTED_PATH = "assets/quizz/question_selected.png"
UNSELECTED_PATH = "assets/quizz/question_unselected.png"
SCROLL_PATH = "assets/menu/scroll.png"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class WinView(arcade.View):

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, window):

        # Instanciation de la classe mère
        super().__init__(window)

        # Initialisation des infos de la view
        self.title = "Thanks you for playing !"
        self.emotion = "Happy"

        # Chargement des textures

        pokemon = self.window.manager.player.pokemon.name

        self.background = arcade.load_texture(BACKGROUND_PATH)
        self.scroll_texture = arcade.load_texture(SCROLL_PATH)
        self.sprite_q_selected = arcade.load_texture(SELECTED_PATH)
        self.sprite_q_unselected = arcade.load_texture(UNSELECTED_PATH)
        self.profile_tex = arcade.load_texture(f"assets/sprite/pokemon/"
                                               f"{pokemon}/portraits/"
                                               f"{self.emotion}.png")
        self.sprite_frame = arcade.load_texture("assets/sprite/face_frame.png")
        self.leader_sprite = arcade.load_texture("assets/menu/"
                                                 "small_leaderboard.png")
        self.rank_0 = arcade.load_texture("assets/rank/rank_0.png")

        # Récupération des scores
        self.lst_score = self.window.manager.scoreboard

        # Initialisation de la musique
        self.music_player = None

        # Initalisation des questions
        self.reponses = ["Retour à l'écran titre",
                         "Enregistrer sous un nouveau nom",
                         "Enregistrer le score"]
        self.selected_reponse = 2

        # Gestion de l'input du pseudo

        self.ui_manager = arcade.gui.UIManager()
        self.input_field = None
        self.show_input_ui = False

    # +---------------------------------------------------------------------+
    # |                            View Methods                             |
    # +---------------------------------------------------------------------+

    def on_show_view(self):
        """Appelé quand la vue change"""
        self.ui_manager.enable()

        volume = self.window.manager.settings.volume
        if not (self.music_player and self.music_player.playing):
            self.music = arcade.Sound(MUSIC_PATH,
                                      streaming=True)
            self.music_player = self.music.play(volume=volume, loop=True)

    def on_hide_view(self):
        """Appelé quand on quitte la vue"""
        self.ui_manager.disable()

    def on_draw(self):
        """ Draw everything """
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

        if self.show_input_ui:
            # Si on saisit le nom, on dessine l'interface par-dessus le fond
            self.draw_input_box()
        else:
            # Sinon, on dessine le menu normal
            self.draw_title()
            self.draw_mid_leaderboard()
            self.draw_profile_icone()
            self.draw_choice()

    def on_key_press(self, key, modifiers):

        dict_key = self.window.manager.settings.dict_key
        dict_key = dict_key[self.window.manager.settings.configuration]

        if key == dict_key["up"] or key == arcade.key.UP:
            self.selected_reponse = ((self.selected_reponse + 1) %
                                     len(self.reponses))

        if key == dict_key["down"] or key == arcade.key.DOWN:
            self.selected_reponse = ((self.selected_reponse - 1) %
                                     len(self.reponses))

        if key == arcade.key.ENTER or key == arcade.key.SPACE:

            if self.selected_reponse == 2:
                self.save_without_name()
            elif self.selected_reponse == 1:
                self.show_name_input()
            elif self.selected_reponse == 0:
                self.window.manager.reset_game()
                self.music.stop(self.music_player)
                self.window.show_view(self.window.start_view)

    # +---------------------------------------------------------------------+
    # |                           Choice Methods                            |
    # +---------------------------------------------------------------------+

    def save_without_name(self):

        score = {
            "name": self.window.manager.player.name,
            "score": self.window.manager.player.score,
            "pokemon": self.window.manager.player.pokemon.name
        }

        score = Score(**score)
        self.window.manager.scoreboard.append(score)
        self.window.manager.update_json_score()
        self.window.manager.reset_game()

        self.music.stop(self.music_player)
        self.window.show_view(self.window.start_view)

    def show_name_input(self):
        """Crée et positionne le champ de saisie du pseudo"""
        self.show_input_ui = True

        # Layout pour ancrer au milieu de l'écran
        self.anchor_layout = arcade.gui.UIAnchorLayout(
            width=self.window.width,
            height=self.window.height
        )

        # Création de la boîte de texte
        self.input_field = arcade.gui.UIInputText(
            text=self.window.manager.player.name,
            width=300,
            height=40,
            text_color=arcade.color.BLACK,
            font_size=20,
            font_name="FOT-Humming Pro",
            border_width=0
        )

        # Interception des touches clavier
        @self.input_field.event("on_event")
        def on_text_event(event):
            if isinstance(event, arcade.gui.events.UIKeyPressEvent):
                if event.symbol in (arcade.key.ENTER, arcade.key.ENTER):
                    new_name = self.input_field.text.strip()
                    if new_name:
                        # On applique le nouveau nom
                        self.window.manager.player.name = new_name
                        self.show_input_ui = False
                        # Nettoyage et suppression de l'UI
                        self.ui_manager.remove(self.anchor_layout)
                        # Lancement de la sauvegarde
                        self.save_without_name()

        # Alignement au centre parfait (sur l'axe X et Y)
        self.anchor_layout.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.input_field
        )

        self.ui_manager.add(self.anchor_layout)

    # +---------------------------------------------------------------------+
    # |                            Draw Methods                             |
    # +---------------------------------------------------------------------+

    def draw_input_box(self):

        arcade.draw_texture_rect(texture=self.scroll_texture,
                                 rect=arcade.XYWH(self.window.width / 2,
                                                  self.window.height / 2,
                                                  self.window.width * 0.5,
                                                  self.window.height * 0.3))

        # Dessin de la ligne noire sous le pseudo
        line_width = 320
        center_x = self.window.width / 2
        center_y = self.window.height / 2

        arcade.draw_line(
            start_x=center_x - (line_width / 2),
            start_y=center_y - 30,
            end_x=center_x + (line_width / 2),
            end_y=center_y - 30,
            color=arcade.color.BLACK,
            line_width=3
        )

        # Dessin des éléments gérés par l'UI Manager (UIInputText au centre)
        self.ui_manager.draw()

        # Dessin du texte explicatif sous le parchemin
        text = arcade.Text(
            text="Appuyez sur entrer pour valider",
            x=self.window.width / 2,
            y=(self.window.height / 2) - (self.window.height * 0.15) - 35,
            color=arcade.color.BLACK,
            font_size=14,
            font_name="FOT-Humming Pro",
            anchor_x="center"
        )

        text.draw()

    def draw_title(self):

        titre = arcade.Text(text=self.title,
                            x=self.window.width / 2,
                            y=self.window.height * 0.9,
                            color=arcade.color.BLACK,
                            bold=True,
                            font_size=30,
                            anchor_x="center",
                            anchor_y="center")

        titre.draw()

    def draw_choice(self):
        start_y = self.window.height * 0.20
        space_between = 150

        # L'axe X central pour tout le bloc de gauche
        align_x = self.window.width * 0.30

        for reponse in self.reponses:
            if (reponse is self.reponses[self.selected_reponse]):
                question_sprite = self.sprite_q_selected
            else:
                question_sprite = self.sprite_q_unselected

            sprite_width = self.window.width * 0.5
            sprite_height = self.window.height * 0.09

            # On utilise l'axe aligné
            center_x = align_x
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

    def draw_profile_icone(self):

        icon_size = 100
        align_x = self.window.width * 0.30

        player_name = arcade.Text(self.window.manager.player.name,
                                  align_x,
                                  self.window.height * 0.67 + icon_size,
                                  color=arcade.color.BLACK,
                                  font_size=22,
                                  font_name="FOT-UDKakugoC80 Pro",
                                  anchor_x="center",
                                  anchor_y="center",
                                  bold=True)
        player_name.draw()

        arcade.draw_texture_rect(
            texture=self.profile_tex,
            rect=arcade.XYWH(align_x,
                             self.window.height * 0.67,
                             icon_size,
                             icon_size)
        )

        arcade.draw_texture_rect(
            texture=self.sprite_frame,
            rect=arcade.XYWH(align_x,
                             self.window.height * 0.67,
                             icon_size + 10,
                             icon_size + 10)
        )

        score = f"Score: {self.window.manager.player.score}"
        player_score = arcade.Text(score,
                                   align_x,
                                   self.window.height * 0.58,
                                   color=arcade.color.BLACK,
                                   font_size=18,
                                   font_name="FOT-UDKakugoC80 Pro",
                                   anchor_x="center",
                                   anchor_y="center")
        player_score.draw()

    def draw_mid_leaderboard(self):

        w = self.window.width * 0.3
        h = self.window.height * 0.7
        arcade.draw_texture_rect(
            texture=self.leader_sprite,
            rect=arcade.XYWH(
                x=self.window.width / 2 + self.window.width / 2 * 0.6,
                y=self.window.height * 0.45,
                width=w,
                height=h
            )
        )

        # Tri des 9 meilleurs
        scores = sorted(self.window.manager.scoreboard,
                        key=lambda p: p.score,
                        reverse=True)[:9]

        # Configuration des positions
        start_x = self.window.height + 225
        start_y = (self.window.width * 0.45) - 135
        line_height = 70
        icon_size = 50

        # Joueurs présents au top 3
        for i, player in enumerate(scores):

            current_y = start_y - (i * line_height)

            # Image de rang
            if (i < 12):
                rank_tex = arcade.load_texture(f"assets/rank/rank_{i+1}_64."
                                               "png")
            else:
                rank_tex = self.rank_0

            arcade.draw_texture_rect(
                texture=rank_tex,
                rect=arcade.XYWH(start_x + (icon_size / 2), current_y,
                                 icon_size, icon_size)
            )

            # Image du pokémon
            pokemon = player.pokemon
            profile_tex = arcade.load_texture(f"assets/sprite/pokemon/{pokemon}"
                                              "/portraits/Normal.png")
            arcade.draw_texture_rect(
                texture=profile_tex,
                rect=arcade.XYWH(start_x + icon_size + 40, current_y,
                                 icon_size, icon_size)
            )

            sprite_frame = arcade.load_texture("assets/sprite/face_frame.png")
            arcade.draw_texture_rect(
                texture=sprite_frame,
                rect=arcade.XYWH(start_x + icon_size + 40, current_y,
                                 icon_size + 5, icon_size + 5)
            )

            # Nom + Score
            text_content = f"{player.name} ({player.score})"
            player_name = arcade.Text(text_content,
                                      start_x + (icon_size * 2) + 30,
                                      current_y - 8,
                                      color=arcade.color.BLACK,
                                      font_size=12,
                                      font_name="FOT-Humming Pro")
            player_name.draw()

        i = len(scores)

        while (i < 3):

            current_y = start_y - (i * line_height)

            # Image de rang
            rank_tex = arcade.load_texture("assets/rank/rank_0.png")
            arcade.draw_texture_rect(
                texture=rank_tex,
                rect=arcade.XYWH(start_x + (icon_size / 2), current_y, icon_size, icon_size)
            )

            # Image du pokémon
            profile_tex = arcade.load_texture(f"assets/sprite/undefined/Normal.png")
            arcade.draw_texture_rect(
                texture=profile_tex,
                rect=arcade.XYWH(start_x + icon_size + 25, current_y, icon_size, icon_size)
            )

            # Nom + Score
            text_content = "..."
            player_name = arcade.Text(text_content,
                                      start_x + (icon_size * 2) + 20,
                                      current_y - 5,
                                      color=arcade.color.BLACK,
                                      font_size=11,
                                      font_name="FOT-Humming Pro")
            player_name.draw()

            i += 1
