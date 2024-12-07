from abc import ABC
from ..agent import Agent
import numpy as np


class RoadHogAgent(Agent, ABC):
    FORWARD_ACCEL_RIGHT = 0
    FORWARD_ACCEL_NEUTRAL = 1
    FORWARD_ACCEL_LEFT = 2
    NON_ACCEL_LEFT = 3
    NON_ACCEL_NEUTRAL = 4
    NON_ACCEL_RIGHT = 5
    BACKWARD_ACCEL_LEFT = 6
    BACKWARD_ACCEL_NEUTRAL = 7
    BACKWARD_ACCEL_RIGHT = 8

    ACTION_SPACE = [
        FORWARD_ACCEL_RIGHT,
        FORWARD_ACCEL_NEUTRAL,
        FORWARD_ACCEL_LEFT,
        NON_ACCEL_RIGHT,
        NON_ACCEL_NEUTRAL,
        NON_ACCEL_LEFT,
        BACKWARD_ACCEL_LEFT,
        BACKWARD_ACCEL_NEUTRAL,
        BACKWARD_ACCEL_RIGHT
    ]
    