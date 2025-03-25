import os
from stable_baselines3 import PPO
from Lunar_Lander_custom_env import LunarLanderEnv

# best model folder maybe I will change the name later
models_dir = "../../custom_lunar"
model_path = os.path.join(models_dir, "best_model1.zip")

env = LunarLanderEnv(render_mode="human")

model = PPO.load(model_path, env=env)

episodes = 5

for episode in range(episodes):
    obs, info = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        env.render()

env.close()
