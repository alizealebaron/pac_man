# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  enemydatamodel.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: alebaron, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/06 12:06:51 by rruiz           #+#    #+#               #
#  Updated: 2026/06/06 12:08:10 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field

class EnemyDataModel(BaseModel):
    name: str = Field(min_length=1)
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    nb_anim: int = Field(ge=1)
    scale: float = Field(ge=1)
