# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  configmodel.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/19 11:08:47 by rruiz           #+#    #+#               #
#  Updated: 2026/06/11 09:03:23 by alebaron        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Any, Self
import sys

mandatory_keys: list[str] = ['highscore_filename', 'level', 'lives', 'pacgum',
                             'points_per_pacgum', 'points_per_super_pacgum',
                             'points_per_ghost', 'level_max_time', 'seed']

optional_keys: list[str] = []


class LevelConfig(BaseModel):
    id: int = Field(ge=1)
    width: int = Field(ge=1, le=500, default=10)
    height: int = Field(ge=1, le=500, default=10)


class ConfigModel(BaseModel):
    highscore_filename: Optional[str] = Field(default="highscores.json",
                                              min_length=1)
    level: list[LevelConfig] = Field(min_length=1, default_factory=list)
    lives: int = Field(ge=1, le=1000, default=3)
    pacgum: int = Field(ge=1, le=1000, default=42)
    points_per_pacgum: int = Field(ge=1, le=1000, default=10)
    points_per_super_pacgum: int = Field(ge=1, le=1000, default=50)
    points_per_ghost: int = Field(ge=1, le=1000, default=100)
    level_max_time: int = Field(ge=1, le=3600, default=90)
    seed: Optional[int] = Field(default=42)

    @classmethod
    def build_config(cls, config: dict[str, Any]) -> Self:
        clean: dict[str, Any] = {}

        for field_name, field_info in cls.model_fields.items():
            data = config.get(field_name)

            if not data and field_name in mandatory_keys:
                if field_name != 'level':
                    print(
                        f"Warning: invalid value for '{field_name}': {data}"
                        f"; using default ({field_info.default})",
                        file=sys.stderr
                    )
                else:
                    print(
                        f"Warning: invalid value for '{field_name}': {data}"
                        f"; using default value",file=sys.stderr)
                continue

            try:
                cls.model_validate({field_name: data})
                clean[field_name] = data
            except ValidationError:
                default = field_info.default
                print(
                    f"Warning: invalid value for '{field_name}': {data}"
                    f"; using default ({default})",file=sys.stderr)

        return cls(**clean)
