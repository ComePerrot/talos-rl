import yaml
from stable_baselines3 import SAC

from .envs.env_talos_deburring import EnvTalosDeburring

training_name = "2023-06-01_test_1"

log_dir = "./logs/"
model_path = log_dir + training_name + "/" + training_name[:-2] + ".zip"
config_path = log_dir + training_name + "/" + training_name[:-2] + ".yaml"

model = SAC.load(model_path)

with open(config_path) as config_file:
    params = yaml.safe_load(config_file)

envDisplay = EnvTalosDeburring(
    params["robot_designer"],
    params["environment"],
    GUI=True,
)
envDisplay.maxTime = 1000
obs = envDisplay.reset()
while True:
    action, _ = model.predict(obs, deterministic=True)
    _, _, done, _ = envDisplay.step(action)
    if done:
        input("Press to any key restart")
        envDisplay.reset()
envDisplay.close()