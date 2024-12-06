import os
import pygame
from .agent import RoadHogAgent
from .env import RoadHogEnv


_BGM_PATH = os.path.join(os.path.dirname(__file__), 'bgm.ogg')
_TIMEOUT = 60 * 2
_PENALTY_PER_LANE_OUT = 3.0
_PENALTY_PER_CRASH = 10.0
_COOLDOWN_TIME = 1.5


def _make_road_hog(show_screen: bool, config: dict):
    env = RoadHogEnv(
        config=config,
        timeout=_TIMEOUT,
        penalty_per_lane_out=_PENALTY_PER_LANE_OUT,
        penalty_per_crash=_PENALTY_PER_CRASH,
        crash_cool_time=_COOLDOWN_TIME,
        render_mode='human' if show_screen else 'rgb_array',
    )

    if show_screen:
        pygame.mixer.init()
        pygame.mixer.music.load(_BGM_PATH)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
    return env


def make_road_hog(show_screen: bool):
    return _make_road_hog(show_screen, dict())


def evaluate(agent: RoadHogAgent):
    env = make_road_hog(show_screen=True)
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
    env = _make_road_hog(
        show_screen=True,
        config={
            'manual_control': True,
        }
    )
    done = False
    env.reset()

    while not done:
        _, _, terminated, truncated, _ = env.step(0)
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
