import os
import numpy as np
import pygame
from itertools import product
from functools import partial
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Lava, Key, Door, Goal, Wall
from minigrid.minigrid_env import MiniGridEnv
from minigrid.wrappers import FullyObsWrapper
from gymnasium.core import ObservationWrapper


_MISSION_NAME = 'Grid Adventure!'
_BLUEPRINT_PATH = os.path.join(os.path.dirname(__file__), 'grid-adventure.csv')

_SYM_AGENT = 'A'
_SYM_START = 'S'
_SYM_GOAL = 'G'

_SYM_WALL = 'W'
_SYM_LAVA = 'L'
_SYM_KEY = 'K'
_SYM_DOOR = 'D'

_SYM_EMTPY = 'E'

_STATE_LOCKED = 'L'
_STATE_OPEN = 'O'
_STATE_CLOSED = 'C'

_COLOR_RED = 'R'
_COLOR_BLUE = 'B'
_COLOR_GREEN = 'G'
_COLOR_YELLOW = 'Y'
_COLOR_PURPLE = 'P'

_DIR_RIGHT = 'R'
_DIR_DOWN = 'D'
_DIR_LEFT = 'L'
_DIR_UP = 'U'

_SYM_TO_INSTANCE = {
    _SYM_WALL: partial(Wall),
    _SYM_LAVA: partial(Lava),
    _SYM_DOOR: partial(Door),
    _SYM_KEY: partial(Key),
}

_COLOR_TO_ARGUMENT = {
    _COLOR_RED: 'red',
    _COLOR_BLUE: 'blue',
    _COLOR_GREEN: 'green',
    _COLOR_YELLOW: 'yellow',
    _COLOR_PURPLE: 'purple',
}

_OBJ_ID_TO_SYM = {
    1: _SYM_EMTPY,
    2: _SYM_WALL,
    4: _SYM_DOOR,
    5: _SYM_KEY,
    8: _SYM_GOAL,
    9: _SYM_LAVA,
    10: _SYM_AGENT
}

_STATE_ID_TO_SYM = {
    0: _STATE_OPEN,
    1: _STATE_CLOSED,
    2: _STATE_LOCKED
}

_COLOR_ID_TO_SYM = {
    0: _COLOR_RED,
    1: _COLOR_GREEN,
    2: _COLOR_BLUE,
    3: _COLOR_PURPLE,
    4: _COLOR_YELLOW
}

_DIR_ID_TO_SYM = {
    0: _DIR_RIGHT,
    1: _DIR_DOWN,
    2: _DIR_LEFT,
    3: _DIR_UP
}


class GridAdventureEnv(MiniGridEnv):
    def __init__(self, max_steps: int, **kwargs):
        blueprint = np.loadtxt(_BLUEPRINT_PATH, dtype=str, delimiter=',').T
        width, height = blueprint.shape
        start_pos = np.argwhere(blueprint == _SYM_START).flatten()
        assert len(start_pos) == 2, 'Only one start position should be provided.'

        goal_pos = np.argwhere(blueprint == _SYM_GOAL).flatten()
        assert len(goal_pos) == 2, 'Only one goal position should be provided.'

        self.blueprint = blueprint
        self.agent_start_pos = tuple(start_pos)
        self.agent_start_dir = 0
        self.goal_pos = tuple(goal_pos)

        super().__init__(
            mission_space=MissionSpace(self._gen_mission),
            width=width,
            height=height,
            max_steps=max_steps,
            **kwargs
        )

    @staticmethod
    def _gen_mission():
        return _MISSION_NAME

    def _gen_grid(self, width, height):
        self.grid = Grid(width, height)

        for x, y in product(range(width), range(height)):
            sym = self.blueprint[x, y]
            sym_key = sym[0] if len(sym) > 1 else sym
            inst = _SYM_TO_INSTANCE.get(sym_key)

            if inst is None:
                continue

            if sym_key == _SYM_WALL or sym == _SYM_LAVA:
                self.put_obj(inst(), x, y)
            elif sym_key == _SYM_KEY:
                color = _COLOR_TO_ARGUMENT[sym[1]] or 'red'
                self.put_obj(inst(color=color), x, y)
            elif sym_key == _SYM_DOOR:
                color = _COLOR_TO_ARGUMENT[sym[1]] or 'red'
                is_open = False
                is_locked = False

                if sym[2] == _STATE_OPEN:
                    is_open = True
                elif sym[2] == _STATE_LOCKED:
                    is_locked = True

                self.put_obj(inst(color=color, is_open=is_open, is_locked=is_locked), x, y)

        self.put_obj(Goal(), self.goal_pos[0], self.goal_pos[1])

        self.agent_pos = self.agent_start_pos
        self.agent_dir = self.agent_start_dir

    def _reward(self) -> float:
        return 0

    def render(self):
        img = self.get_frame(self.highlight, self.tile_size, False)

        if self.render_mode == "human":
            img = np.transpose(img, axes=(1, 0, 2))
            if self.render_size is None:
                self.render_size = img.shape[:2]
            if self.window is None:
                pygame.init()
                pygame.display.init()
                self.window = pygame.display.set_mode(
                    (self.screen_size, self.screen_size)
                )
                pygame.display.set_caption(_MISSION_NAME)
            if self.clock is None:
                self.clock = pygame.time.Clock()
            surf = pygame.surfarray.make_surface(img)

            # Create background with mission description
            offset = surf.get_size()[0] * 0.1
            # offset = 32 if self.agent_pov else 64
            bg = pygame.Surface(
                (int(surf.get_size()[0] + offset), int(surf.get_size()[1] + offset))
            )
            bg.convert()
            bg.fill((255, 255, 255))
            bg.blit(surf, (offset / 2, 0))

            bg = pygame.transform.smoothscale(bg, (self.screen_size, self.screen_size))
            font_size = 22
            action_count = self.step_count
            distance = abs(self.agent_pos[0] - self.goal_pos[0]) + abs(self.agent_pos[1] - self.goal_pos[1])
            text = f'# Actions: {action_count}/{self.max_steps}; Distance: {distance}'
            font = pygame.freetype.SysFont(pygame.font.get_default_font(), font_size)
            text_rect = font.get_rect(text, size=font_size)
            text_rect.center = bg.get_rect().center
            text_rect.y = bg.get_height() - font_size * 1.5
            font.render_to(bg, text_rect, text, size=font_size)

            self.window.blit(bg, (0, 0))
            pygame.event.pump()
            self.clock.tick(self.metadata["render_fps"])
            pygame.display.flip()

        elif self.render_mode == "rgb_array":
            return img


class SymbolicObsWrapper(ObservationWrapper):
    def __init__(self, env):
        env = FullyObsWrapper(env)
        super().__init__(env)

    def observation(self, obs):
        obs = obs['image']
        width, height, _ = obs.shape
        grid = np.zeros((width, height)).astype('U3')
        for x, y in product(range(width), range(height)):
            obj, color, state = obs[x, y]
            obj = _OBJ_ID_TO_SYM.get(obj, _SYM_EMTPY)
            color = _COLOR_ID_TO_SYM.get(color)
            if obj == _SYM_DOOR:
                state = _STATE_ID_TO_SYM.get(state)
                sym = f'{obj}{color}{state}'
            elif obj == _SYM_KEY:
                sym = f'{obj}{color}'
            elif obj == _SYM_AGENT:
                state = _DIR_ID_TO_SYM.get(state)
                sym = f'{obj}{state}'
            else:
                sym = obj
            grid[y, x] = sym

        return grid