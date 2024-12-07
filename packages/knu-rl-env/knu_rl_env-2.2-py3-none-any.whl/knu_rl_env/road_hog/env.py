import numpy as np
import pygame
import gymnasium as gym
from highway_env.envs.common.abstract import AbstractEnv, Observation
from highway_env.envs.common.action import Action, DiscreteAction, action_factory
from highway_env.envs.common.observation import  KinematicObservation
from highway_env.road.lane import LineType, StraightLane, CircularLane, SineLane
from highway_env.road.road import RoadNetwork, Road
from highway_env.vehicle.controller import ControlledVehicle
from highway_env.vehicle.graphics import VehicleGraphics
from highway_env.vehicle.kinematics import Vehicle
from highway_env.vehicle.objects import Landmark, Obstacle, RoadObject
from highway_env.envs.common.graphics import EnvViewer, ObservationGraphics
from highway_env.road.graphics import RoadGraphics, RoadObjectGraphics, WorldSurface


_NAME = 'Road Hog!'
_SCREEN_WIDTH = 1200
_SCREEN_HEIGHT = 900
_N_PARKING_SPOTS_PER_LINE = 25
_N_VEHICLES_PARKED = 40
_N_VEHICLES_ON_ROAD = 9
_N_OBS = 10
_ID_PARKING_SPOT = 40
_FPS_SIM = 15
_FPS_POLICY = 5


class RoadHogVehicle(Vehicle):
    def clip_actions(self) -> None:
        self.action["steering"] = float(self.action["steering"])
        self.action["acceleration"] = float(self.action["acceleration"])
        if self.speed > self.MAX_SPEED:
            self.action["acceleration"] = min(
                self.action["acceleration"], 1.0 * (self.MAX_SPEED - self.speed)
            )
        elif self.speed < self.MIN_SPEED:
            self.action["acceleration"] = max(
                self.action["acceleration"], 1.0 * (self.MIN_SPEED - self.speed)
            )

    def step(self, dt: float) -> None:
        super().step(dt)
        self.crashed = False


class RoadHogControlledVehicle(ControlledVehicle):
    def clip_actions(self) -> None:
        self.action["steering"] = float(self.action["steering"])
        self.action["acceleration"] = float(self.action["acceleration"])

        if self.speed > self.MAX_SPEED:
            self.action["acceleration"] = min(
                self.action["acceleration"], 1.0 * (self.MAX_SPEED - self.speed)
            )
        elif self.speed < self.MIN_SPEED:
            self.action["acceleration"] = max(
                self.action["acceleration"], 1.0 * (self.MIN_SPEED - self.speed)
            )

    def step(self, dt: float) -> None:
        super().step(dt)
        self.crashed = False


class RoadHogRoadGraphics(RoadGraphics):
    @staticmethod
    def display_road_objects(
            road: Road, surface: WorldSurface, offscreen: bool = False
    ) -> None:
         for o in road.objects:
            RoadHogRoadObjectGraphics.display(o, surface, offscreen=offscreen)


class RoadHogRoadObjectGraphics(RoadObjectGraphics):
    @classmethod
    def get_color(cls, object_: RoadObject, transparent: bool = False):
        color = cls.DEFAULT_COLOR

        if isinstance(object_, Obstacle):
            color = cls.YELLOW
        elif isinstance(object_, Landmark):
            if object_.hit:
                color = cls.GREEN
            else:
                color = cls.BLUE

        if transparent:
            color = (color[0], color[1], color[2], 30)

        return color


class RoadHogEnvViewer(EnvViewer):
    def __init__(self, env: AbstractEnv, config: dict | None = None):
        super().__init__(env, config)
        self.font = pygame.font.SysFont(None, 30)
        pygame.display.set_caption(_NAME)

    def display(self) -> None:
        if not self.enabled:
            return

        self.sim_surface.move_display_window_to(self.window_position())
        RoadHogRoadGraphics.display(self.env.road, self.sim_surface)

        if self.vehicle_trajectory:
            VehicleGraphics.display_trajectory(
                self.vehicle_trajectory, self.sim_surface, offscreen=self.offscreen
            )

        RoadHogRoadGraphics.display_road_objects(
            self.env.road, self.sim_surface, offscreen=self.offscreen
        )

        if EnvViewer.agent_display:
            EnvViewer.agent_display(self.agent_surface, self.sim_surface)
            if not self.offscreen:
                if self.config["screen_width"] > self.config["screen_height"]:
                    self.screen.blit(
                        self.agent_surface, (0, self.config["screen_height"])
                    )
                else:
                    self.screen.blit(
                        self.agent_surface, (self.config["screen_width"], 0)
                    )

        RoadHogRoadGraphics.display_traffic(
            self.env.road,
            self.sim_surface,
            simulation_frequency=self.env.config["simulation_frequency"],
            offscreen=self.offscreen,
        )

        ObservationGraphics.display(self.env.observation_type, self.sim_surface)

        if not self.offscreen:
            self.screen.blit(self.sim_surface, (0, 0))
            bg_rect = pygame.Rect(0, 0, _SCREEN_WIDTH, 40)
            pygame.draw.rect(self.screen, (100, 100, 100), bg_rect)

            text_time = f'Time: {round(self.env.time, 2)} / {round(self.env.timeout, 2)} s'
            font_time = self.font.render(text_time, True, (255, 255, 255))
            self.screen.blit(font_time, (25, 10))

            text_lane_out = f'Lane-out: {round(self.env.time_lane_out, 2)} s (Penalty: {round(self.env.penalty_lane_out_, 2)} s)'
            font_lane_out = self.font.render(text_lane_out, True, (235, 91, 0))
            self.screen.blit(font_lane_out, (25, 40))

            text_crashes = f'Crashes: {self.env.n_crashes} times (Penalty: {round(self.env.penalty_crashes_, 2)} s)'
            font_crashes = self.font.render(text_crashes, True, (217, 22, 86))
            self.screen.blit(font_crashes, (25, 70))

            text_total_time = f'Total: {round(self.env.total_time_, 2)} s'
            font_total_time = self.font.render(text_total_time, True, (255, 178, 0))
            self.screen.blit(font_total_time, (25, 100))

            text_distance = f'Distance: {round(self.env.distance_, 3)} m'
            text_distance = self.font.render(text_distance, True, (255, 255, 255))
            self.screen.blit(text_distance, (300, 10))

            if self.env.config["real_time_rendering"]:
                self.clock.tick(self.env.config["simulation_frequency"])

            pygame.display.flip()

        if self.SAVE_IMAGES and self.directory:
            pygame.image.save(
                self.sim_surface,
                str(self.directory / f"highway-env_{self.frame}.png"),
            )
            self.frame += 1


class RoadHogEnv(AbstractEnv):
    def __init__(self,
                 config: dict,
                 timeout: float,
                 penalty_per_lane_out: float,
                 penalty_per_crash: float,
                 crash_cool_time: float,
                 render_mode: str = None
                 ):
        self.timeout = float(timeout)
        self.penalty_per_lane_out = float(penalty_per_lane_out)
        self.penalty_per_crash = float(penalty_per_crash)
        self.crash_cool_time = float(crash_cool_time)

        self._goal_spot: Landmark | None = None
        self._time_ignore_crash: float | None = None

        self.time_lane_out: float | None = None
        self.n_crashes: int | None = None

        super().__init__(config, render_mode)

    @property
    def distance_(self):
        if self.vehicle is None and self._goal_spot is None:
            return None

        return np.sqrt(
            (self.vehicle.position[0] - self._goal_spot.position[0]) ** 2 +
            (self.vehicle.position[1] - self._goal_spot.position[1]) ** 2
        )

    @property
    def penalty_lane_out_(self):
        if self.time_lane_out is None:
            return 0
        return self.penalty_per_lane_out * self.time_lane_out

    @property
    def penalty_crashes_(self):
        if self.n_crashes is None:
            return 0
        return self.penalty_per_crash * self.n_crashes

    @property
    def total_time_(self):
        return self.time + self.penalty_crashes_ + self.penalty_lane_out_

    @classmethod
    def default_config(cls) -> dict:
        config = super().default_config()
        config.update(
            {
                "steering_range": np.deg2rad(45),
                "simulation_frequency": _FPS_SIM,
                "policy_frequency": _FPS_POLICY,
                "screen_width": 1200,
                "screen_height": 600,
                "centering_position": [0.2, 0.5],
                "scaling": 4,
                "controlled_vehicles": 1,
                "vehicles_count": _N_VEHICLES_ON_ROAD + 1
            }
        )
        return config

    def define_spaces(self) -> None:
        self.observation_type = KinematicObservation(
            self,
            features=["x", "y", "vx", "vy", "cos_h", "sin_h"],
            normalize=False,
            vehicles_count=_N_OBS,
            include_obstacles=True
        )
        if self.config['manual_control']:
            self.action_type = action_factory(
                self,
                {
                    'type': 'ContinuousAction'
                }
            )
        else:
            self.action_type = DiscreteAction(
                self,
                acceleration_range=(-4, 4),
                longitudinal=True,
                lateral=True,
                dynamical=False,
                clip=True,
                actions_per_axis=3,
                speed_range=(-10, 10),
            )
        self.observation_space = self.observation_type.space()
        self.action_space = self.action_type.space()

    def _reward(self, action: Action) -> float:
        return 0

    def _rewards(self, action: Action) -> dict[str, float]:
        return dict()

    def _is_terminated(self) -> bool:
        return self._is_successful()

    def _is_truncated(self) -> bool:
        return self.timeout <= round(self.time, 2)

    def _info(self, obs: Observation, action: Action | None = None) -> dict:
        return dict()

    def _reset(self) -> None:
        self._goal_spot = None
        self._time_ignore_crash = 0

        self.time_lane_out = 0
        self.n_crashes = 0

        self._create_road()
        self._create_vehicles()

    def reset(self,
              *,
            seed: int | None = None,
            options: dict | None = None
        ):
        obs, info = super().reset(seed=seed, options=options)
        obs = self._generate_observation(obs)

        return obs, dict()

    def _generate_observation(self, original_obs):
        is_on_load = self._is_vehicle_on_load()
        if not is_on_load:
            self.time_lane_out += 1 / self.config["policy_frequency"]

        is_crashed = self.vehicle.crashed
        if is_crashed:
            self.vehicle.crashed = False
            if self._time_ignore_crash < self.time:
                self._time_ignore_crash = self.time + self.crash_cool_time
                self.n_crashes += 1

        dict_goal = self._goal_spot.to_dict()
        feat_goal = np.array([
            dict_goal['x'],
            dict_goal['y'],
            dict_goal['vx'],
            dict_goal['vy'],
            dict_goal['cos_h'],
            dict_goal['sin_h']
        ])
        obs = {
            'observation': original_obs,
            'goal_spot': feat_goal,
            'is_on_load': is_on_load,
            'is_crashed': is_crashed,
            'time': round(self.time, 2),
        }
        return obs

    def _create_road(self):
        width = 4.0
        x_offset_1, y_offset_1 = 0, 36
        x_offset_2, y_offset_2 = 0, 16
        length = 8
        spots = _N_PARKING_SPOTS_PER_LINE
        net = RoadNetwork()

        for k in range(spots):
            x = (k + 1 - spots // 2) * (width + x_offset_1) - width / 2
            net.add_lane(
                "parking_a",
                "parking_b",
                StraightLane(
                    [x, y_offset_1],
                    [x, y_offset_1 + length],
                    width=width,
                    line_types=(LineType.CONTINUOUS, LineType.CONTINUOUS)
                ),
            )
            net.add_lane(
                "parking_b",
                "parking_c",
                StraightLane(
                    [x, -y_offset_1],
                    [x, -y_offset_1 - length],
                    width=width,
                    line_types=(LineType.CONTINUOUS, LineType.CONTINUOUS)
                ),
            )

            x = (k + 1 - spots // 2) * (width + x_offset_2) - width / 2
            net.add_lane(
                "parking_d",
                "parking_e",
                StraightLane(
                    [x, y_offset_2],
                    [x, y_offset_2 + length],
                    width=width,
                    line_types=(LineType.CONTINUOUS, LineType.CONTINUOUS)
                ),
            )
            net.add_lane(
                "parking_e",
                "parking_f",
                StraightLane(
                    [x, -y_offset_2],
                    [x, -y_offset_2 - length],
                    width=width,
                    line_types=(LineType.CONTINUOUS, LineType.CONTINUOUS)
                ),
            )

        net.add_lane(
            "exit", "exit_a",
            StraightLane([-70, -2], [-69, -2], width=5, line_types=(LineType.CONTINUOUS, LineType.NONE))
        )
        net.add_lane(
            "exit", "exit_a",
            StraightLane([-70, 3], [-69, 3], width=5, line_types=(LineType.STRIPED, LineType.CONTINUOUS))
        )

        center1 = [-70, 23]
        radii1 = 20

        net.add_lane(
            "exit_a",
            "exit_b",
            CircularLane(
                center1,
                radii1,
                np.deg2rad(270),
                np.deg2rad(181),
                width=5,
                clockwise=False,
                line_types=[LineType.CONTINUOUS, LineType.NONE],
            ),
        )
        net.add_lane(
            "exit_a",
            "exit_b",
            CircularLane(
                center1,
                radii1 + 5,
                np.deg2rad(270),
                np.deg2rad(181),
                width=5,
                clockwise=False,
                line_types=[LineType.STRIPED, LineType.CONTINUOUS],
            ),
        )

        net.add_lane(
            "exit_b",
            "road_a",
            StraightLane(
                [-90, 23],
                [-90, 33],
                line_types=(LineType.CONTINUOUS, LineType.NONE),
                width=5,
            ),
        )

        net.add_lane(
            "exit_b",
            "road_a",
            StraightLane(
                [-95, 23],
                [-95, 33],
                line_types=(LineType.STRIPED, LineType.CONTINUOUS),
                width=5,
            ),
        )

        center2 = [-110, 33]
        radii2 = 15
        net.add_lane(
            "road_a",
            "road_b",
            CircularLane(
                center2,
                radii2,
                np.deg2rad(180),
                np.deg2rad(-1),
                width=5,
                clockwise=False,
                line_types=[LineType.CONTINUOUS, LineType.NONE],
            ),
        )
        net.add_lane(
            "road_a",
            "road_b",
            CircularLane(
                center2,
                radii2 + 5,
                np.deg2rad(180),
                np.deg2rad(-1),
                width=5,
                clockwise=False,
                line_types=[LineType.STRIPED, LineType.CONTINUOUS],
            ),
        )

        net.add_lane(
            "road_b",
            "road_c",
            StraightLane(
                [-130, 32],
                [-130, 22],
                line_types=(LineType.CONTINUOUS, LineType.NONE),
                width=5,
            ),
        )

        net.add_lane(
            "road_b",
            "road_c",
            StraightLane(
                [-125, 32],
                [-125, 22],
                line_types=(LineType.STRIPED, LineType.CONTINUOUS),
                width=5,
            ),
        )

        center3 = [-150, 23]
        radii3 = 20

        net.add_lane(
            "road_c",
            "road_d",
            CircularLane(
                center3,
                radii3,
                np.deg2rad(0),
                np.deg2rad(-91),
                width=5,
                clockwise=False,
                line_types=[LineType.CONTINUOUS, LineType.NONE],
            ),
        )

        net.add_lane(
            "road_c",
            "road_d",
            CircularLane(
                center3,
                radii3 + 5,
                np.deg2rad(0),
                np.deg2rad(-91),
                width=5,
                clockwise=False,
                line_types=[LineType.STRIPED, LineType.CONTINUOUS],
            ),
        )

        dev = 85
        a = 5
        delta_st = 0.2 * dev
        delta_en = dev - delta_st
        w = 2 * np.pi / dev
        x_move = 192

        net.add_lane(
            "road_d",
            "ee",
            SineLane(
                [dev / 2 - x_move, -2 - a],
                [dev / 2 - delta_st - x_move, -2 - a],
                a,
                w,
                -np.pi / 2,
                line_types=[LineType.CONTINUOUS, LineType.NONE],
            ),
        )
        net.add_lane(
            "road_d",
            "ee",
            SineLane(
                [dev / 2 - x_move, -3 - a],
                [dev / 2 - delta_st - x_move, -3 - a],
                a,
                w,
                -np.pi / 2,
                line_types=[LineType.NONE, LineType.CONTINUOUS],
            ),
        )
        net.add_lane(
            "road_d",
            "ex",
            SineLane(
                [-dev / 2 + delta_en - x_move, 2 + a],
                [dev / 2 - x_move, 2 + a],
                a,
                w,
                -np.pi / 2 + w * delta_en,
                line_types=[LineType.CONTINUOUS, LineType.NONE],
            ),
        )
        net.add_lane(
            "road_d",
            "ex",
            SineLane(
                [-dev / 2 + delta_en - x_move, 3 + a],
                [dev / 2 - x_move, 3 + a],
                a,
                w,
                -np.pi / 2 + w * delta_en,
                line_types=[LineType.NONE, LineType.CONTINUOUS],
            ),
        )

        center = [-202, 0]
        radius = 30
        alpha = 24

        radii = [radius, radius + 4]
        n, c, s = LineType.NONE, LineType.CONTINUOUS, LineType.STRIPED
        line = [[c, s], [n, c]]
        for lane in [0, 1]:
            net.add_lane(
                "se",
                "ex",
                CircularLane(
                    center,
                    radii[lane],
                    np.deg2rad(90 - alpha),
                    np.deg2rad(alpha),
                    clockwise=False,
                    line_types=line[lane],
                ),
            )
            net.add_lane(
                "ex",
                "ee",
                CircularLane(
                    center,
                    radii[lane],
                    np.deg2rad(alpha),
                    np.deg2rad(-alpha),
                    clockwise=False,
                    line_types=line[lane],
                ),
            )
            net.add_lane(
                "ee",
                "nx",
                CircularLane(
                    center,
                    radii[lane],
                    np.deg2rad(-alpha),
                    np.deg2rad(-90 + alpha),
                    clockwise=False,
                    line_types=line[lane],
                ),
            )
            net.add_lane(
                "nx",
                "ne",
                CircularLane(
                    center,
                    radii[lane],
                    np.deg2rad(-90 + alpha),
                    np.deg2rad(-90 - alpha),
                    clockwise=False,
                    line_types=line[lane],
                ),
            )
            net.add_lane(
                "ne",
                "wx",
                CircularLane(
                    center,
                    radii[lane],
                    np.deg2rad(-90 - alpha),
                    np.deg2rad(-180 + alpha),
                    clockwise=False,
                    line_types=line[lane],
                ),
            )
            net.add_lane(
                "wx",
                "we",
                CircularLane(
                    center,
                    radii[lane],
                    np.deg2rad(-180 + alpha),
                    np.deg2rad(-180 - alpha),
                    clockwise=False,
                    line_types=line[lane],
                ),
            )
            net.add_lane(
                "we",
                "sx",
                CircularLane(
                    center,
                    radii[lane],
                    np.deg2rad(180 - alpha),
                    np.deg2rad(90 + alpha),
                    clockwise=False,
                    line_types=line[lane],
                ),
            )
            net.add_lane(
                "sx",
                "se",
                CircularLane(
                    center,
                    radii[lane],
                    np.deg2rad(90 + alpha),
                    np.deg2rad(90 - alpha),
                    clockwise=False,
                    line_types=line[lane],
                ),
            )

        self.road = Road(
            network=net,
            np_random=self.np_random,
            record_history=self.config["show_trajectories"],
        )

    def _create_vehicles(self):
        empty_spots = list(self.road.network.lanes_dict().keys())
        parking_spots = empty_spots[0:_N_PARKING_SPOTS_PER_LINE * 4]

        '''
        Player's ego vehicle
        '''
        self.controlled_vehicles = []
        vehicle = RoadHogVehicle.make_on_lane(self.road, ('wx', 'we', 1), np.pi * 1 / 2, 0)
        vehicle.color = VehicleGraphics.EGO_COLOR
        self.road.vehicles.append(vehicle)
        self.controlled_vehicles.append(vehicle)
        empty_spots.remove(vehicle.lane_index)

        '''
        Goal parking spot 
        '''
        lane_index = parking_spots[_ID_PARKING_SPOT]
        lane = self.road.network.get_lane(lane_index)
        self._goal_spot = Landmark(
            self.road, lane.position(lane.length / 2, 0), heading=lane.heading
        )
        self.road.objects.append(self._goal_spot)
        parking_spots.remove(lane_index)

        '''
        Parked vehicles
        '''
        for i in range(_N_VEHICLES_PARKED):
            if not parking_spots:
                continue
            lane_index = parking_spots[self.np_random.choice(np.arange(len(parking_spots)))]
            v = RoadHogVehicle.make_on_lane(self.road, lane_index, 4, speed=0)
            self.road.vehicles.append(v)
            parking_spots.remove(lane_index)

        '''
        Vehicles on the circular lane
        '''
        circle_spots = [('ex', 'ee', 0), ('ex', 'ee', 1), ('ee', 'nx', 0), ('ee', 'nx', 1), ('nx', 'ne', 0),
                        ('nx', 'ne', 1), ('ne', 'wx', 0), ('wx', 'we', 0), ('we', 'sx', 0), ('we', 'sx', 1),
                        ('sx', 'se', 0), ('sx', 'se', 1)]

        for i in range(_N_VEHICLES_ON_ROAD):
            if not circle_spots:
                continue
            lane_index = circle_spots[self.np_random.choice(np.arange(len(circle_spots)))]
            v = RoadHogControlledVehicle.make_on_lane(self.road, lane_index, 4, speed=4)
            v.plan_route_to(lane_index)
            self.road.vehicles.append(v)
            circle_spots.remove(lane_index)

        '''
        Walls
        '''
        width, height = 140, 100
        for y in [-height / 2, height / 2]:
            obstacle = Obstacle(self.road, [0, y])
            obstacle.LENGTH, obstacle.WIDTH = (width, 1)
            obstacle.diagonal = np.sqrt(obstacle.LENGTH ** 2 + obstacle.WIDTH ** 2)
            self.road.objects.append(obstacle)

        for x in [width / 2]:
            obstacle = Obstacle(self.road, [x, 0], heading=np.pi / 2)
            obstacle.LENGTH, obstacle.WIDTH = (height, 1)
            obstacle.diagonal = np.sqrt(obstacle.LENGTH ** 2 + obstacle.WIDTH ** 2)
            self.road.objects.append(obstacle)

        for x in [-width / 2]:
            for y in [-28, 28]:
                obstacle = Obstacle(self.road, [x, y], heading=np.pi / 2)
                obstacle.LENGTH, obstacle.WIDTH = (44, 1)
                obstacle.diagonal = np.sqrt(obstacle.LENGTH ** 2 + obstacle.WIDTH ** 2)
                self.road.objects.append(obstacle)

    def _is_vehicle_on_load(self):
        x, y = self.vehicle.position
        return bool((-70 <= x <= 70 and -50 <= y <= 50) or self.vehicle.on_road)

    def _is_successful(self):
        if self.vehicle is None or self._goal_spot is None:
            return False

        scales = np.array([100, 100, 5, 5, 1, 1])
        dict_vehicle = self.vehicle.to_dict()
        dict_goal = self._goal_spot.to_dict()

        feat_vehicle = np.array([
            dict_vehicle['x'],
            dict_vehicle['y'],
            dict_vehicle['vx'],
            dict_vehicle['vy'],
            dict_vehicle['cos_h'],
            -np.abs(dict_vehicle['sin_h'])
        ]) / scales
        feat_goal = np.array([
            dict_goal['x'],
            dict_goal['y'],
            dict_goal['vx'],
            dict_goal['vy'],
            dict_goal['cos_h'],
            dict_goal['sin_h']
        ]) / scales

        weights = np.array([1, 0.3, 0, 0, 0.02, 0.02])
        p = 0.5
        threshold = 0.12
        norm = np.power(
            np.dot(
                np.abs(feat_vehicle - feat_goal),
                weights
            ),
            p
        )
        return norm < threshold

    def step(self, action):
        if self.road is None or self.vehicle is None:
            raise NotImplementedError(
                "The road and vehicle must be initialized in the environment implementation"
            )

        self.time += 1 / self.config["policy_frequency"]
        self._simulate(action)

        obs = self.observation_type.observe()
        obs = self._generate_observation(obs)
        terminated = self._is_terminated()
        truncated = self._is_truncated()

        if self.render_mode == "human":
            self.render()

        return obs, 0, terminated, truncated, dict()

    def render(self) -> np.ndarray | None:
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
            )
            return
        if self.viewer is None:
            self.viewer = RoadHogEnvViewer(self)

        self.enable_auto_render = True
        self.viewer.display()

        if not self.viewer.offscreen:
            self.viewer.handle_events()
        if self.render_mode == "rgb_array":
            image = self.viewer.get_image()
            return image

