from abc import ABC
from ..agent import Agent
from minigrid.core.actions import Actions


class GridSurvivorAgent(Agent, ABC):
    ACTION_LEFT = Actions.left
    ACTION_RIGHT = Actions.right
    ACTION_FORWARD = Actions.forward

    ACTION_SPACE = [ACTION_LEFT, ACTION_RIGHT, ACTION_FORWARD]
