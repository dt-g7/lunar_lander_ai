import os
import sys
import pygame
import traceback
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from Lunar_Lander_custom_env import LunarLanderEnv


def cleanup_pygame():
    try:
        if hasattr(pygame, 'display') and pygame.display.get_init():
            pygame.display.quit()
        if pygame.get_init():
            pygame.quit()
    except Exception:
        pass


def main():
    env = None
    eval_env = None

    try:
        save_path = "../../custom_lunar"
        os.makedirs(save_path, exist_ok=True)

        env = LunarLanderEnv(render_mode="none")
        eval_env = LunarLanderEnv(render_mode="none")

        # eval callback rewrite the saved best model every 10000 iterations
        eval_callback = EvalCallback(eval_env,
                                     best_model_save_path=save_path,
                                     log_path=save_path,
                                     eval_freq=10000,
                                     deterministic=True,
                                     render=False)

        model = PPO("MlpPolicy",  # pretty standard parameters
                    env,
                    verbose=1,
                    learning_rate=3e-4,
                    n_steps=1024,
                    batch_size=128,
                    n_epochs=5,
                    gamma=0.999,
                    gae_lambda=0.98,
                    clip_range=0.2,
                    policy_kwargs=dict(
                        net_arch=[dict(pi=[128, 128], vf=[128, 128])]
                    ))
        model.learn(total_timesteps=500000, callback=eval_callback)

    except KeyboardInterrupt:
        print("\nTraining interrupted by user")
    except Exception as e:
        print(f"\nTraining failed with error: {str(e)}")
        traceback.print_exc()
    finally:
        # Clean up environments
        if env is not None:
            try:
                env.close()
            except Exception:
                pass
        if eval_env is not None:
            try:
                eval_env.close()
            except Exception:
                pass

        cleanup_pygame()


if __name__ == "__main__":
    main()
    sys.exit(0)
