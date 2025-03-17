# Lunar Lander AI

This repository contains a reinforcement learning project that uses the [PPO](https://arxiv.org/abs/1707.06347) (Proximal Policy Optimization) algorithm from [Stable Baselines3](https://stable-baselines3.readthedocs.io/) to train an agent for the [LunarLander-v2](https://gymnasium.farama.org/environments/box2d/lunar_lander/) environment provided by [Gymnasium](https://gymnasium.farama.org/).

The repository includes scripts to:
- Train the agent and periodically save the model.
- Load and run a pre-trained model for demonstration.
- Run a simple baseline using random actions.

---

## Repository Structure

lunar_lander_ai/

├── models/

│   └── PPO/                # Directory where trained PPO models are saved.

├── logs/                   # Directory for tensorboard and training logs.

├── main.py                 # Script for training the PPO agent.

├── load.py                 # Script to load a pre-trained model and run it.

└── ORIGINAL.py             # Basic script that runs the environment with random actions.

---

## Prerequisites

- **Python 3.7+** (recommended Python 3.8 or higher)
- **Gymnasium**  
  Install via pip:
  ```bash
  pip install gymnasium
- **Stable Baselines3**  
  Install via pip:
  ```bash
  pip install gymnasium
Other dependencies such as NumPy and PyTorch are installed automatically with stable-baselines3.

---

## Usage
Training the Agent (main.py)
The main.py script sets up the LunarLander-v2 environment, initializes the PPO model, and trains the agent in iterations. 
Key features include:

Directory Setup:
Ensures that the directories for saving models (models/PPO) and logs (logs) exist.

Environment Setup:
Creates the LunarLander-v2 environment in "rgb_array" render mode.

Model Training:
Trains for a fixed number of timesteps per iteration (default: 10,000 timesteps per iteration) for 100 iterations. The model is saved after each iteration.

---

### Running a Pre-trained Model (load.py)
The load.py script demonstrates how to load a previously trained model and run it in real-time. Key points:

Model Loading:
It loads a model from models/PPO/900000.zip. (Make sure that this file exists or change the path to a saved model.)

Interactive Environment:
The environment is created in "human" render mode, enabling visual feedback.

Continuous Execution:
The script enters an infinite loop where the agent continuously predicts actions and steps through the environment.

- **How to Run:**  
  ```bash
  python load.py

---

### Random Agent Baseline (ORIGINAL.py)
The ORIGINAL.py script is a simple example of interacting with the LunarLander-v2 environment by taking random actions. This can be used as a baseline to compare the performance of the trained agent.

**How to Run:**  
  ```bash
  python ORIGINAL.py
  ```
The script:

Initializes the environment with a fixed seed for reproducibility.
Executes 1,000 steps using randomly sampled actions.
Resets the environment if the episode ends (terminated or truncated).

---

### Customization & Parameters

TIMESTEPS (main.py):
You can modify the constant TIMESTEPS to change how many timesteps the model learns per iteration.

Training Iterations:
The number of iterations (currently 100) can be adjusted based on the desired training duration.

Model Save Frequency:
The model is saved after each iteration. The file naming convention uses the product of TIMESTEPS and the iteration count. Adjust as needed.

Environment Choice:
The scripts use the "LunarLander-v2" environment. For continuous control, you might consider using "LunarLanderContinuous-v2" (especially in load.py where a comment hints at this).

---

## Notes

Logging:
Training logs are saved in the `logs` folder. You can use TensorBoard to monitor training progress:

```bash
tensorboard --logdir logs
```
Model Files:
Ensure that the directory models/PPO is writable. The saved models are in .zip format.

License:
This project isn’t licensed. Feel free to use it, but if you plan to distribute or modify it, reach out to me first if you want!


