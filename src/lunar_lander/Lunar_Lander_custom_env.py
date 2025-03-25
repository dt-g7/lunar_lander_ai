"""
Lunar Lander Environment

A custom implementation of the Lunar Lander environment for reinforcement learning.
This environment simulates a lunar lander that must learn to safely land on a target platform.

Author: Dans To
Date: 03/24/2025
"""

import gymnasium as gym
import numpy as np
from gymnasium import spaces
import pygame
from physics import PhysicsWorld
from rendering import Renderer


class LunarLanderEnv(gym.Env):
    """My Custom Lunar Lander Environment for Reinforcement Learning."""

    metadata = {"render_modes": ["human", "none"], "render_fps": 30}
    MAX_STEPS = 1000

    def __init__(self, render_mode=None):
        super().__init__()
        if render_mode is not None and render_mode not in self.metadata["render_modes"]:
            raise ValueError(f"Invalid render mode {render_mode}. Allowed modes are {self.metadata['render_modes']}")
            
        self.render_mode = render_mode
        self.window = None
        self.renderer = None
        self.steps = 0
        
        self.physics = PhysicsWorld()
        if self.render_mode == "human":
            self._init_pygame()

        # Action is a two-element vector: [thrust, torque]
        # Thrust: between 0 and 50; Torque: between -20 and 20.
        self.action_space = spaces.Box(low=np.array([0.0, -20.0]),
                                     high=np.array([50.0, 20.0]),
                                     dtype=np.float32)

        # observation space: [dx, dy, x_velocity, y_velocity, angle, angular_velocity]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32)

    def _init_pygame(self):
        try:
            if not pygame.get_init():
                pygame.init()
            if self.renderer is None:
                self.renderer = Renderer()
        except Exception as e:
            self._cleanup_pygame()
            raise RuntimeError(f"Failed to initialize renderer: {str(e)}")

    def _cleanup_pygame(self):
        try:
            if hasattr(pygame, 'display') and pygame.display.get_init():
                pygame.display.quit()
            if pygame.get_init():
                pygame.quit()
        except Exception:
            pass
        finally:
            self.renderer = None

    def _get_obs(self):
        try:
            state = self.physics.get_lander_state()
            pos = state['position']
            lin_vel = state['linear_velocity']
            angle = state['angle']
            ang_vel = state['angular_velocity']

            landing_zone = self.physics.get_landing_zone()
            landing_center_x = (landing_zone['left'] + landing_zone['right']) / 2.0
            landing_center_y = landing_zone['y']

            dx = pos.x - landing_center_x
            dy = pos.y - landing_center_y

            obs = np.array([dx, dy, lin_vel.x, lin_vel.y, angle, ang_vel], dtype=np.float32)
            return obs
        except Exception as e:
            raise RuntimeError(f"Failed to get observation: {str(e)}")

    def step(self, action):
        """
        Apply the action to the simulation, step forward, compute reward,
        and return observation, reward, done, truncated, and info.
        """
        try:
            self.steps += 1
            
            thrust, torque = action

            prev_state = self._get_obs()

            self.physics.apply_thrust(thrust)
            self.physics.apply_torque(torque)

            self.physics.step()

            obs = self._get_obs()

            timeout = self.steps >= self.MAX_STEPS
            
            reward = 0.0
            
            reward += 5

            landing_zone = self.physics.get_landing_zone()
            landing_center_x = (landing_zone['left'] + landing_zone['right']) / 2.0
            landing_center_y = landing_zone['y']  # Use the landing zone's y (top of ground)
            x_pos = obs[0]
            y_pos = obs[1]
            distance = np.sqrt((x_pos - landing_center_x) ** 2 + (y_pos - landing_center_y) ** 2)
            reward -= 0.31 * distance

            lin_vel_y = obs[3]
            reward -= 0.3 * (abs(lin_vel_y))

            done = self.physics.game_over or timeout
            info = {
                "landed_successfully": self.physics.landed_successfully,
                "timeout": timeout,
                "distance":distance
            }

            if done:
                if self.physics.landed_successfully:
                    reward += 400.0
                else:
                    reward -= 100.0

            if self.render_mode == "human":
                self.render()

            return obs, reward, done, False, info
        except Exception as e:
            raise RuntimeError(f"Error during environment step: {str(e)}")

    def reset(self, seed=None, options=None):
        try:
            self.steps = 0
            
            if seed is not None:
                np.random.seed(seed)
                
            self.physics = PhysicsWorld()
            
            if self.render_mode == "human":
                if self.renderer is None:
                    self._init_pygame()
                else:
                    self.renderer.clear()
                
            obs = self._get_obs()
            
            if self.render_mode == "human":
                self.render()
                
            return obs, {}
        except Exception as e:
            raise RuntimeError(f"Failed to reset environment: {str(e)}")

    def render(self):
        if self.render_mode != "human":
            return
            
        if self.renderer is None:
            self._init_pygame()
            
        try:
            self.renderer.clear()
            for segment in self.physics.ground_segments:
                self.renderer.draw_ground(segment)

            self.renderer.draw_landing_zone(self.physics.get_landing_zone())
            state = self.physics.get_lander_state()
            self.renderer.draw_lander(state['position'], state['angle'])
            if state.get('is_thrusting'):
                self.renderer.draw_thrust_effect(state['position'], state['angle'])
            
            state['time_remaining'] = (self.MAX_STEPS - self.steps) / 60  # Convert to seconds
            
            self.renderer.draw_game_state(state)
            self.renderer.update()
        except Exception as e:
            print(f"Warning: Render failed: {str(e)}")
            self._cleanup_pygame()  # Try to clean up if rendering fails

    def close(self):
        self._cleanup_pygame()
        if hasattr(self, 'physics'):
            self.physics = None
