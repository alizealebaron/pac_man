# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pacmanManager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/21 13:04:41 by alebaron        #+#    #+#               #
#  Updated: 2026/06/11 15:38:35 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


import argparse
import json
from typing import List
from src.parsing.config_loader import ConfigLoader
from src.models.configmodel import ConfigModel, LevelConfig
from src.models.scoreModel import Score
from src.models.playerModel import PlayerModel
from src.models.levelModel import Level
from src.models.questionModel import DataQuestionsModel
from src.models.pokemonModel import PokemonModel
from src.models.settingsModel import SettingsModel
from src.models.cheatModel import CheatModel
from src.managers.enemy_manager import EnemyManager

# +-------------------------------------------------------------------------+
# |                                  CONST                                  |
# +-------------------------------------------------------------------------+


QUESTIONS_FILE = "data/question_data.json"
POKEMONS_FILE = "data/pokemon_data.json"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class PacmanManager():

    """
    Classe principale du manager du jeu, gère la logique du jeu et les
    données.

    Attributs:
        config (ConfigModel): La configuration du jeu, chargée depuis un
            fichier JSON.
        pokemons (List[PokemonModel]): La liste des pokémons, chargée depuis
            un fichier JSON.
        player (PlayerModel): Le joueur, généré aléatoirement à partir de la
            configuration et de la liste des pokémons.
        level (List[Level]): La liste des niveaux du jeu, générée à partir de
            la configuration.
        actual_level (int): Le niveau actuel du jeu.
        current_level (Level): Le niveau actuel du jeu.
        enemy_manager (EnemyManager): Le manager des ennemis, gère la logique
            des ennemis du jeu.
        scoreboard (List[Score]): Le tableau des scores, chargé depuis un
            fichier JSON.
        data_questions (DataQuestionsModel): Les données des questions,
            chargées depuis un fichier JSON.
        settings (SettingsModel): Les paramètres du jeu, gérés par la vue des
            paramètres.
        cheat (CheatModel): Les options de triche du jeu, gérées par la
            vue de triche.
    """

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, arg: argparse.Namespace):

        """
        Initialise le manager du jeu, charge les données depuis les fichiers
        JSON et génère les niveaux et le joueur.

        Args:
            arg (argparse.Namespace): Les arguments de la ligne de commande,
                contenant le chemin du fichier de configuration.
        """

        # Récupération de la config
        self.config: ConfigModel = ConfigLoader.load_config(arg.config_file)

        # Récupérations des datas de pokémons
        self.pokemons = self.retrieve_pokemon_data_from_json()

        # Génération aléatoire du joueur
        self.player = PlayerModel(self.config, self.pokemons)

        # Generation des maps et stockage dans une liste
        self.level: list[Level] = self.create_maps(self.config.level)
        self.actual_level = 0
        self.current_level = self.level[self.actual_level]

        # Génération des ennemies
        self.enemy_manager = EnemyManager(self.config,
                                          self.current_level, self.player)

        # Récupération du scoreboard
        self.scoreboard = self.retrieve_score_from_json()

        # Récupération des questions
        self.data_questions = self.retrieve_questions_from_json()

        # Récupération des settings
        self.settings = SettingsModel()

        # Récupération des options de triche
        self.cheat = CheatModel()

    # +---------------------------------------------------------------------+
    # |                               Setters                               |
    # +---------------------------------------------------------------------+

    def reset_game(self) -> None:

        """
        Réinitialise le jeu, remet le joueur à sa position de départ,
        réinitialise le score et les vies, et remet à jour le niveau actuel.
        """

        self.actual_level = 0
        self.player.score = 0
        self.player.nb_life = self.config.lives
        self.actual_level = 0
        self.current_level = self.level[self.actual_level]
        self.reset_player_position()
        self.enemy_manager.set_current_level(self.current_level)

    def update_new_level(self):

        """
        Passe au niveau suivant, met à jour le niveau actuel et réinitialise
        la position du joueur.
        """

        self.actual_level += 1
        self.current_level = self.level[self.actual_level]

    def reset_player_position(self):

        """
        Réinitialise la position du joueur à sa position de départ, et remet à
        jour sa direction.
        """

        self.player.direction = None
        self.player.next_direction = None
        self.player.sprite.current_direction = "down"

    # +---------------------------------------------------------------------+
    # |                            JSON Methods                             |
    # +---------------------------------------------------------------------+

    def retrieve_score_from_json(self) -> List[Score]:

        """
        Récupère le tableau des scores depuis un fichier JSON, et le
        convertit en une liste d'objets Score.

        Returns:
            List[Score]: La liste des scores récupérée depuis le fichier JSON.
        """

        lst_score = []

        score_file = self.config.highscore_filename
        try:
            with open(score_file, "r") as file:
                data = json.load(file)
                lst_score = [Score(**arg) for arg in data]
        except json.JSONDecodeError as e:
            raise (e)
        except Exception:
            pass

        return lst_score

    def update_json_score(self):

        """
        Met à jour le fichier JSON du tableau des scores avec les scores
        actuels, en convertissant la liste d'objets Score en une liste de
        dictionnaires.
        """

        dict_data = [obj.__dict__ for obj in self.scoreboard]

        score_file = self.config.highscore_filename
        with open(score_file, "w") as f:
            json.dump(dict_data, f, indent=2)

    def create_maps(self, level: list[LevelConfig]) -> list[Level]:
        level_list: list[Level] = []
        for map in level:
            level_list.append(Level(map.id, map.width, map.height,
                                    self.config.seed))
        return level_list

    def retrieve_questions_from_json(self) -> DataQuestionsModel:

        """
        Récupère les données des questions depuis un fichier JSON, et les
        convertit en un objet DataQuestionsModel.

        Returns:
            DataQuestionsModel: Les données des questions récupérées depuis le
            fichier JSON, converties en un objet DataQuestionsModel.
        """

        with open(QUESTIONS_FILE, "r") as file:
            data_dict = json.load(file)

        data = DataQuestionsModel.model_validate(data_dict)

        return data

    def retrieve_pokemon_data_from_json(self) -> List[PokemonModel]:

        """
        Récupère les données des pokémons depuis un fichier JSON, et les
        convertit en une liste d'objets PokemonModel.

        Returns:
            List[PokemonModel]: La liste des pokémons récupérée depuis
                le fichier JSON, convertie en une liste d'objets
                PokemonModel.
        """

        lst_pokemon = []

        try:
            with open(POKEMONS_FILE, "r") as file:
                data = json.load(file)
                lst_pokemon = [PokemonModel(**arg) for arg in data]
        except json.JSONDecodeError as e:
            raise (e)
        except Exception as e:
            raise (e)

        return lst_pokemon
