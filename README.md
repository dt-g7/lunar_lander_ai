# Lunar Lander Reinforcement Learning Environment

A custom implementation of the Lunar Lander environment for reinforcement learning, built with Pygame and Box2D physics engine. This environment provides a realistic simulation of a lunar lander that must learn to safely land on a target platform.
![Image](https://github.com/user-attachments/assets/9b690330-ccd3-431d-9c57-53c3dce18527)

## Features

- Realistic physics simulation using Box2D
- Customizable terrain generation with a designated landing zone
- Visual rendering using Pygame
- Compatible with Stable-Baselines3 reinforcement learning framework
- Configurable reward structure
- Time-limited episodes (15 seconds)
- Detailed state observations and continuous action space

## Requirements

- Python 3.11 (Make sure its 3.11 and not 3.12)
- Pygame
- Box2D
- NumPy
- Stable-Baselines3
- Gymnasium

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd LunarLander
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Project Structure

- `Lunar_Lander_custom_env.py`: Main environment class implementing the Gymnasium interface
- `physics.py`: Box2D physics simulation and world management
- `rendering.py`: Pygame-based visualization
- `custom_run.py`: Training script using Stable-Baselines3 PPO
- `requirements.txt`: Project dependencies

## Environment Details

### Observation Space
The environment provides 6-dimensional observations:
- `dx`: Horizontal distance from landing zone center
- `dy`: Vertical distance from landing zone center
- `x_velocity`: Horizontal velocity
- `y_velocity`: Vertical velocity
- `angle`: Current rotation angle
- `angular_velocity`: Current rotation speed

### Action Space
Continuous 2-dimensional action space:
- `thrust`: Main engine thrust (0 to 50)
- `torque`: Rotation control (-20 to 20)

### Reward Structure
The reward function encourages:
- Staying alive (+5 per step)
- Moving toward landing zone center (-0.31 * distance)
- Maintaining stable vertical velocity (-0.3 * |vertical_velocity|)
- Successful landing (+400)
- Penalties for crashes (-100)

### Termination Conditions
An episode ends when:
- The lander successfully lands on the target platform
- The lander crashes
- The time limit (15 seconds) is reached

## Training

To train a model using PPO:

```bash
python custom_run.py
```

The training script:
- Creates a PPO model with optimized hyperparameters
- Saves the best model to the `custom_lunar` directory
- Evaluates the model every 10,000 timesteps
- Trains for 500,000 timesteps

### PPO Hyperparameters
- Learning rate: 3e-4
- Steps per update: 1024
- Batch size: 128
- Number of epochs: 5
- Gamma: 0.999
- GAE Lambda: 0.98
- Network architecture: Two hidden layers of 128 units each

## Physics Parameters

The environment uses the following physics settings:
- Gravity: -3.0 m/s²
- Thrust scaling: 12.0
- Torque scaling: 0.3
- Lander properties:
  - Density: 0.5
  - Linear damping: 0.2
  - Angular damping: 2.0
  - No bounce (restitution: 0.0)

## Rendering

The environment supports two render modes:
- `human`: Visual display using Pygame
- `none`: No visual output (faster training)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
