import pygame
from minigrid.manual_control import ManualControl
from .agent import GridSurvivorAgent
from .env import GridSurvivorEnv, SymbolicObsWrapper
import os


_MAX_HIT_POINTS = 100
_MAX_STEPS = 1200
_ATTACK_HIT_POINTS = 20
_BGM_PATH = os.path.join(os.path.dirname(__file__), 'bgm.ogg')


def _make_grid_survivor(show_screen: bool, with_wrapper: bool):
    env = GridSurvivorEnv(
        render_mode='human' if show_screen else 'rgb_array',
        attack_hit_points=_ATTACK_HIT_POINTS,
        max_hit_points=_MAX_HIT_POINTS,
        max_steps=_MAX_STEPS,
        seed=None,
        screen_size=800
    )
    if with_wrapper:
        env = SymbolicObsWrapper(env)

    if show_screen:
        pygame.mixer.init()
        pygame.mixer.music.load(_BGM_PATH)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)

    return env


def make_grid_survivor(show_screen: bool):
    return _make_grid_survivor(show_screen, with_wrapper=True)


def evaluate(agent: GridSurvivorAgent):
    env = make_grid_survivor(show_screen=True)
    done = False
    observation, _ = env.reset()

    while not done:
        action = agent.act(observation)
        observation, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.close()
                break

            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(int(event.key))
                if key == 'escape':
                    env.close()
                    return


def run_manual():
    env = _make_grid_survivor(show_screen=True, with_wrapper=False)
    env = ManualControl(env)
    env.start()
