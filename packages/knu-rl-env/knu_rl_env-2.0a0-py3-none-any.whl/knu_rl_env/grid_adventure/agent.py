from abc import ABC
from minigrid.core.actions import Actions
from ..agent import Agent


class GridAdventureAgent(Agent, ABC):
    ACTION_LEFT = Actions.left
    ACTION_RIGHT = Actions.right
    ACTION_FORWARD = Actions.forward
    ACTION_PICKUP = Actions.pickup
    ACTION_DROP = Actions.drop
    ACTION_UNLOCK = Actions.toggle

    ACTION_SPACE = [ACTION_LEFT, ACTION_RIGHT, ACTION_FORWARD, ACTION_PICKUP, ACTION_DROP, ACTION_UNLOCK]
