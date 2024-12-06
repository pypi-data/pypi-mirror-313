import gymnasium as gym


FROZEN_LAKE_MAZE = [
    "SFFFFFFH",
    "FFHFFFFF",
    "FFFHFFFF",
    "FFFFFHFF",
    "FFFHFFFF",
    "FHHFFFHF",
    "FHFFHFHF",
    "FFFHFFFG",
]



env = gym.make(
    id='FrozenLake-v1',
    max_episode_steps=200,
    render_mode='rgb_array',
    desc=CUSTOM_MAP, # 방금 제작한 맵을 사용
    is_slippery=False, # 타일에서 미끄러지는 여부를 결정
)

CUSTOM_MAP = np.array(CUSTOM_MAP, dtype='c')
CUSTOM_MAP