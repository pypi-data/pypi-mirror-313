from abc import ABC
from ..agent import Agent
from gymnasium.envs.toy_text import frozen_lake


class FrozenLakeAgent(Agent, ABC):
    ACTION_LEFT = frozen_lake.LEFT
    ACTION_DOWN = frozen_lake.DOWN
    ACTION_RIGHT = frozen_lake.RIGHT
    ACTION_UP = frozen_lake.UP

    ACTION_SPACE = [ACTION_LEFT, ACTION_RIGHT, ACTION_DOWN, ACTION_UP]
