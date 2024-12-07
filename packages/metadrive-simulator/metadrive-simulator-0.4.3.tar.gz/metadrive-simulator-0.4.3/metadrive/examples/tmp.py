import cv2
from metadrive.envs.scenario_env import ScenarioEnv
from metadrive.policy.replay_policy import ReplayEgoCarPolicy

if __name__ == "__main__":
    data_directory = "/home/zhenghao/Downloads/scene"
    num_scenarios = 2
    try:
        env = ScenarioEnv(
            {
                "sequential_seed": True,
                "use_render": False,
                "data_directory": data_directory,
                "num_scenarios": num_scenarios,
                "agent_policy": ReplayEgoCarPolicy
            }
        )
        for seed in range(num_scenarios):
            env.reset(seed)
            run = True
            while run:
                o, r, tm, tc, info = env.step([0, 0])
                # o = env.render()
                o = env.render(
                    mode="top_down", target_agent_heading_up=True, text=dict(text="text"), film_size=(20000, 20000)
                )
                print(type(o))
                cv2.imshow("top_down", o[:, :, ::-1])
                cv2.waitKey(1)
                if tm or tc:
                    run = False
    finally:
        env.close()
