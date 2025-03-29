# 🛸Lunar Lander Reinforcement Learning Environment

<p align="center">
  <img src="https://github.com/user-attachments/assets/9b690330-ccd3-431d-9c57-53c3dce18527" alt="Image" />
</p>
A custom implementation of the Lunar Lander environment for reinforcement learning, built with Pygame and Box2D physics engine. This environment provides a realistic simulation of a lunar lander that must learn to safely land on a target platform.

#### If you haven't played before, I suggest you go download the game I coded from my other repository here to play it and get a feel for it!
https://github.com/dt-g7/lunar_lander_game

## 🚀Features

- Realistic physics simulation using Box2D
- Customizable terrain generation with a designated landing zone
- Visual rendering using Pygame
- Compatible with Stable-Baselines3 reinforcement learning framework
- Configurable reward structure
- Time-limited episodes (15 seconds)
- Detailed state observations and continuous action space

## 📋Requirements

- Python 3.11 (Make sure its 3.11 and not 3.12)
- Pygame
- Box2D
- NumPy
- Stable-Baselines3
- Gymnasium

## 🔧Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd LunarLander
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

### 📁Project Structure

- **`Lunar_Lander_custom_env.py`**: Main environment class implementing the Gymnasium interface  
  *(located in `src/lunar_lander`)*

- **`physics.py`**: Box2D physics simulation and world management  
  *(located in `src/lunar_lander`)*

- **`rendering.py`**: Pygame-based visualization  
  *(located in `src/lunar_lander`)*

- **`custom_run.py`**: Training script using Stable-Baselines3 PPO  
  *(located in `src/lunar_lander`)*

- **`requirements.txt`**: Project dependencies

---

Additional files and folders:

- **`custom_lunar/`**: Contains saved best model for custom env(e.g., `best_model1.zip`) and evaluation outputs (e.g., `evaluations.npz`)
- **`logs/`**: Training logs (e.g., `PPO_0`), needed if you want tensorboard graphs
- **`models/`**: Additional model files 
- **Utility Scripts**:  
  - `load.py`
  - `load_model_not_trained.py`
  - `main.py` *(optional entry-point for interactive testing)*
- **Configuration & Documentation**:  
  - `.gitignore`
  - `README.md`
  - `setup.py`
- **IDE Folder**:  
  - `.idea/`

### Visual Workflow Diagram (click to zoom in)
![Image](https://github.com/user-attachments/assets/1105e419-5c2a-4217-b28b-4de606862896)


### How to load/run models 🤖

Start by making your way into `load.py`

Within any load file you will see:
```bash
model_path = f"{models_dir}/880000.zip"
```
Which specifies which model iteration you will run

In load_model_not_trained.py you will load an untrained model.


### Here is an example of a model BEFORE training:
![Image](https://github.com/user-attachments/assets/bdafc1e0-83de-4418-8dbf-513b9cf976c3)


### Here is an example of a model AFTER training (880000th iteration):
![Image](https://github.com/user-attachments/assets/7278b44f-b1de-41e9-827e-463d802f6941)

### For our own custion environment, this is before:
![Image](https://github.com/user-attachments/assets/3a7eaec6-00a7-40d7-9700-41186b1edea3)
### And this is after:
![Image](https://github.com/user-attachments/assets/b74e0882-c5b1-4cf2-bca8-66333884e375)

### Observation Space 🔭
The environment provides 6-dimensional observations:
- `dx`: Horizontal distance from landing zone center
- `dy`: Vertical distance from landing zone center
- `x_velocity`: Horizontal velocity
- `y_velocity`: Vertical velocity
- `angle`: Current rotation angle
- `angular_velocity`: Current rotation speed

### Action Space 💥
Continuous 2-dimensional action space:
- `thrust`: Main engine thrust (0 to 50)
- `torque`: Rotation control (-20 to 20)

### Reward Structure 🏆 
The reward function encourages:
- Staying alive (+5 per step)
- Moving toward landing zone center (-0.31 * distance)
- Maintaining stable vertical velocity (-0.3 * |vertical_velocity|)
- Successful landing (+400)
- Penalties for crashes (-100)

^ These parameters took a long time to fine tune, but feel free to mess with them to see if you can train a better model!

### Termination Conditions 🔚
An episode ends when:
- The lander successfully lands on the target platform
- The lander crashes
- The time limit (15 seconds) is reached

## Training 🏋🏻‍♀️

To train a model using PPO:

```bash
python custom_run.py
```

The training script:
- Creates a PPO model with optimized hyperparameters
- Saves the best model to the `custom_lunar` directory
- Evaluates the model every 10,000 timesteps
- Trains for 500,000 timesteps

### How will I know if my model is learning? 🧠
While training your model in main.py or custom_run.py SB3 will have the console will print out a few stats for you:
![image](https://github.com/user-attachments/assets/f7611d2e-e44d-4d6c-b23d-48883f64a0a5)

You can also pip install tensorboard and run the command
```bash
tensorboard --logdir logs
```
To show some useful graphs!

![image](https://github.com/user-attachments/assets/03a8dcc9-60c2-4030-9093-7d12c3c7ba1a)


Here we see that over time each episode length becomes shorter as our model learns (ep_len_mean).

#### We also see (ep_rew_mean) go up over time, peaking at about our 900k iteration:
![image](https://github.com/user-attachments/assets/f832f0cf-90a7-4743-a40b-f4cfb02860a1)

(This is how I knew to load the 880,000 model in our directory)

### PPO Hyperparameters 🤖🎨
- Learning rate: 3e-4
- Steps per update: 1024
- Batch size: 128
- Number of epochs: 5
- Gamma: 0.999
- GAE Lambda: 0.98
- Network architecture: Two hidden layers of 128 units each
 
## Physics Parameters 🌌

The environment uses the following physics settings:
- Gravity: -3.0 m/s²
- Thrust scaling: 12.0
- Torque scaling: 0.3
- Lander properties:
  - Density: 0.5
  - Linear damping: 0.2
  - Angular damping: 2.0
  - No bounce (restitution: 0.0)

## Rendering 🖼️

The environment supports two render modes:
- `human`: Visual display using Pygame
- `none`: No visual output (faster training)

## License ⚖️

This project is not licensed, but message me if you intent to use it for something !
