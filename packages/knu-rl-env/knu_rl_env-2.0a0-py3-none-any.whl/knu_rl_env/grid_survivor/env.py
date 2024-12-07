import os
from typing import Literal
import numpy as np
import pygame
from itertools import product
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Wall, Ball, WorldObj
from minigrid.minigrid_env import MiniGridEnv
from minigrid.wrappers import FullyObsWrapper
from gymnasium.core import ObservationWrapper
from knu_rl_env.grid_survivor.agent import GridSurvivorAgent


_MISSION_NAME = 'Grid Survivor!'
_BLUEPRINT_PATH = os.path.join(os.path.dirname(__file__), 'grid-survivor.csv')

_SYM_AGENT = 'A'
_SYM_START = 'S'

_SYM_EMTPY = 'E'

_SYM_WALL = 'W'
_SYM_BALL = 'B'
_SYM_HONEY_BEE = 'B'
_SYM_HORNET = 'H'
_SYM_KILLER_BEE = 'K'

_DIR_RIGHT = 'R'
_DIR_DOWN = 'D'
_DIR_LEFT = 'L'
_DIR_UP = 'U'

_OBJ_ID_TO_SYM = {
    1: _SYM_EMTPY,
    2: _SYM_WALL,
    6: _SYM_BALL,
    10: _SYM_AGENT
}

_DIR_ID_TO_SYM = {
    0: _DIR_RIGHT,
    1: _DIR_DOWN,
    2: _DIR_LEFT,
    3: _DIR_UP
}

_COLOR_ID_RED = 0
_COLOR_ID_GREEN = 1
_COLOR_ID_BLUE = 2
_COLOR_ID_PURPLE = 3
_COLOR_ID_YELLOW = 4

_DIR_TO_VEC = [
    np.array((-1, 0)),
    np.array((1, 0)),
    np.array((0, -1)),
    np.array((0, 1)),
    np.array((0, 0)),
]


class HoneyBee(Ball):
    def __init__(self):
        super().__init__(color='yellow')

    def can_overlap(self) -> bool:
        return True


class Hornet(Ball):
    def __init__(self):
        super().__init__(color='blue')

    def can_overlap(self) -> bool:
        return True


class KillerBee(Ball):
    def __init__(self):
        super().__init__(color='purple')

    def can_overlap(self) -> bool:
        return True


class GridSurvivorEnv(MiniGridEnv):
    def __init__(self, max_hit_points: int, attack_hit_points: int, max_steps: int, seed: int = None, **kwargs):
        blueprint = np.loadtxt(_BLUEPRINT_PATH, dtype=str, delimiter=',').T
        width, height = blueprint.shape
        start_pos = np.argwhere(blueprint == _SYM_START).flatten()
        assert len(start_pos) == 2, 'Only one start position should be provided.'

        self.agent_start_pos = tuple(start_pos)
        self.agent_start_dir = 0

        self._blueprint = blueprint

        self._honey_bees = []
        self._hornets = []
        self._killer_bees = []
        self._max_hit_points = self._hit_points = max_hit_points
        self._attack_hit_points = attack_hit_points

        self._seed = seed
        self._generator = None

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
            sym = self._blueprint[x, y]
            sym_key = sym[0] if len(sym) > 1 else sym

            if sym_key == _SYM_WALL:
                self.grid.set(x, y, Wall())
            elif sym_key == _SYM_HONEY_BEE:
                obj = HoneyBee()
                self.put_obj(obj, x, y)
                self._honey_bees.append(obj)
            elif sym_key == _SYM_HORNET:
                obj = Hornet()
                self.put_obj(obj, x, y)
                self._hornets.append(obj)
            elif sym_key == _SYM_KILLER_BEE:
                obj = KillerBee()
                self.put_obj(obj, x, y)
                self._killer_bees.append(obj)

        self.agent_pos = self.agent_start_pos
        self.agent_dir = self.agent_start_dir

    def _reward(self) -> float:
        return 0

    def _place_object(self, obj: WorldObj, max_tries: int, positions: np.ndarray, weights: np.ndarray = None):
        if np.array_equal(obj.cur_pos, self.front_pos):
            return

        num_tries = 0
        is_same_pos = False
        probs = weights if weights is not None else np.ones(len(positions))
        probs = probs / np.sum(probs)

        while True:
            if num_tries > max_tries:
                raise RecursionError("rejection sampling failed in place_obj")
            num_tries += 1

            pos = self._generator.choice(positions, p=probs)

            if np.array_equal(obj.cur_pos, pos):
                is_same_pos = True
                break

            if self.grid.get(*pos) is not None:
                continue

            if np.array_equal(pos, self.agent_pos):
                continue

            break

        if not is_same_pos:
            self.grid.set(pos[0], pos[1], obj)
            self.grid.set(obj.cur_pos[0], obj.cur_pos[1], None)
            if obj is not None:
                obj.cur_pos = pos

    def _move_object(self, obj: WorldObj, max_tries: int, mode: Literal['toward', 'random', 'stand']):
        ox, oy = obj.cur_pos
        positions = []

        for i in range(len(_DIR_TO_VEC)):
            dx, dy = _DIR_TO_VEC[i]
            nx, ny = ox + dx, oy + dy
            positions.append((nx, ny))

        positions = np.asarray(positions)
        weights = np.ones(len(positions))

        if mode == 'toward':
            ax, ay = self.agent_pos
            dist = np.array([np.abs(x - ax) + np.abs(y - ay) for x, y in positions])
            min_dist = np.min(dist)
            if min_dist < 10:
                weights[dist == min_dist] = 30
        elif mode == 'stand':
            weights[-1] = 10

        try:
            self._place_object(obj, max_tries, positions, weights)
        except RecursionError:
            pass

    def reset(self, **kwargs):
        self._hit_points = self._max_hit_points
        self._generator = np.random.default_rng(self._seed)
        self._honey_bees.clear()
        self._hornets.clear()
        self._killer_bees.clear()
        obs, info = super().reset(**kwargs)
        obs = {'hit_points': self._hit_points, **obs}
        return obs, info

    def step(self, action):
        is_game_over = False

        if action == GridSurvivorAgent.ACTION_FORWARD:
            for obj in self._hornets:
                self._move_object(obj, 100, 'random')
            for obj in self._killer_bees:
                self._move_object(obj, 100, 'toward')
            for obj in self._honey_bees:
                self._move_object(obj, 100, 'stand')

            front_obj = self.grid.get(*self.front_pos)
            is_saved = front_obj and front_obj.type == 'ball' and front_obj.color == 'yellow'
            is_attacked = front_obj and front_obj.type == 'ball' and front_obj.color == 'blue'
            is_killed = front_obj and front_obj.type == 'ball' and front_obj.color == 'purple'

            if is_saved:
                self.grid.set(front_obj.cur_pos[0], front_obj.cur_pos[1], None)
                self._honey_bees.remove(front_obj)
                is_game_over = len(self._honey_bees) <= 0
            elif is_attacked:
                self.grid.set(front_obj.cur_pos[0], front_obj.cur_pos[1], None)
                self._hornets.remove(front_obj)
                self._hit_points = max(0, self._hit_points - self._attack_hit_points)
                is_game_over = self._hit_points <= 0
            elif is_killed:
                is_game_over = True

        obs, reward, terminated, truncated, info = super().step(action)

        obs = {'hit_points': self._hit_points, **obs}
        if is_game_over:
            return obs, reward, True, truncated, info
        else:
            return obs, reward, terminated, truncated, info

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
            text = f'# Actions: {self.step_count}/{self.max_steps}; Honey Bees Remained: {len(self._honey_bees)}; HP: {self._hit_points}/{self._max_hit_points}; '
            font = pygame.freetype.SysFont(pygame.font.get_default_font(), font_size)
            text_rect = font.get_rect(text, size=font_size)
            text_rect.center = bg.get_rect().center
            text_rect.y = bg.get_height() - font_size * 1.5
            font.render_to(bg, text_rect, text, size=font_size)

            self.window.blit(bg, (0, 0))
            pygame.event.pump()
            self.clock.tick(5)
            pygame.display.flip()

        elif self.render_mode == "rgb_array":
            return img


class SymbolicObsWrapper(ObservationWrapper):
    def __init__(self, env):
        env = FullyObsWrapper(env)
        super().__init__(env)

    def observation(self, obs):
        img = obs['image']
        width, height, _ = img.shape
        grid = np.zeros((width, height)).astype('U3')
        for x, y in product(range(width), range(height)):
            obj, color, state = img[x, y]
            obj = _OBJ_ID_TO_SYM.get(obj, _SYM_EMTPY)
            sym = obj
            if obj == _SYM_BALL:
                if color == _COLOR_ID_YELLOW:
                    sym = _SYM_HONEY_BEE
                elif color == _COLOR_ID_BLUE:
                    sym = _SYM_HORNET
                elif color == _COLOR_ID_PURPLE:
                    sym = _SYM_KILLER_BEE
            elif obj == _SYM_AGENT:
                state = _DIR_ID_TO_SYM.get(state)
                sym = f'{obj}{state}'

            grid[y, x] = sym
        return {'grid': grid, 'hit_points': obs['hit_points']}