# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : pacmanManager.py                                                 #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : Invalid date        by -----------                             #
# @update   : 2026/06/04 08:15:40 by alebaron                                #
# ************************************************************************** #


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

# +-------------------------------------------------------------------------+
# |                                  CONST                                  |
# +-------------------------------------------------------------------------+


SCORE_FILE = "data/score.json"
QUESTIONS_FILE = "data/question_data.json"
POKEMONS_FILE = "data/pokemon_data.json"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class PacmanManager():

    # +---------------------------------------------------------------------+
    # |                                Init                                 |
    # +---------------------------------------------------------------------+

    def __init__(self, arg: argparse.Namespace):

        # Récupération de la config
        self.config: ConfigModel = ConfigLoader.load_config(arg.config_file)

        # Récupérations des datas de pokémons
        self.pokemons = self.retrieve_pokemon_data_from_json()

        # Génération aléatoire du joueur
        self.player = PlayerModel(self.config, self.pokemons)

        # Generation des maps et stockage dans une liste
        self.level: list[Level] = self.create_maps(self.config.level)
        self.actual_level = 0

        # Récupération du scoreboard
        self.scoreboard = self.retrieve_score_from_json()

        # Récupération des questions
        self.data_questions = self.retrieve_questions_from_json()

        # Récupération des settings
        self.settings = SettingsModel()

    # +---------------------------------------------------------------------+
    # |                               Setters                               |
    # +---------------------------------------------------------------------+

    def reset_game(self):
        self.actual_level = 0
        self.player.score = 0
        self.player.direction = None
        self.player.next_direction = None
        self.player.sprite.current_direction = "down"

    # +---------------------------------------------------------------------+
    # |                            JSON Methods                             |
    # +---------------------------------------------------------------------+

    def retrieve_score_from_json(self) -> List[Score]:

        lst_score = []

        try:
            with open(SCORE_FILE, "r") as file:
                data = json.load(file)
                lst_score = [Score(**arg) for arg in data]
        except json.JSONDecodeError as e:
            raise (e)
        except Exception:
            pass

        return lst_score

    def update_json_score(self):

        dict_data = [obj.__dict__ for obj in self.scoreboard]

        with open(SCORE_FILE, "w") as f:
            json.dump(dict_data, f, indent=2)

    def create_maps(self, level: list[LevelConfig]) -> list[Level]:
        level_list: list[Level] = []
        for map in level:
            level_list.append(Level(map.id, map.width, map.height))
        return level_list

    def retrieve_questions_from_json(self):

        with open(QUESTIONS_FILE, "r") as file:
            data_dict = json.load(file)

        data = DataQuestionsModel.model_validate(data_dict)

        return data

    def retrieve_pokemon_data_from_json(self):

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
