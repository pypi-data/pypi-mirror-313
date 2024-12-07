import gymnasium
import robosuite
from gymnasium.spaces import Dict, Discrete
from robosuite.wrappers import GymWrapper

from pyTRADE.core.wrapper import TRADEWrapper
from ai.thinkingrobots.trade import TRADE
from jpype import JImplements, JOverride
from edu.tufts.hrilab.rl import RobosuiteInterface
from robosuite.controllers import load_controller_config
from stable_baselines3 import PPO

from pyTRADE.core.java_util import convert_to_java_object


class HierarchicalWrapper(gymnasium.ObservationWrapper):
    def __init__(self, env, goal):
        super().__init__(env)
        if isinstance(goal, str):
            raise Exception("Expecting a list of predicates. Please use [diarc_wrapper.parse_goal(str)].")
        self.observation_space = Dict({
            "low": self.observation_space,
            "high": Discrete(len(goal))
        })

    def observation(self, obs):
        return {
            "low": obs,
            "high": 0
        }


@JImplements(RobosuiteInterface)
class HierarchicalRobosuiteWrapper:
    def __init__(self):
        self._base_env = None
        self.env = None

    @JOverride
    def setHighEnv(self, goal):
        try:
            self.env = HierarchicalWrapper(self._base_env, goal)
        except:
            print(f"Unable to create hierarchical observation space for {goal}.")

    @JOverride
    def makeEnv(self, env_name, robot, render):
        controller_config = load_controller_config(default_controller="JOINT_POSITION")

        self._base_env = GymWrapper(robosuite.make(
            env_name=env_name,
            robots=robot,
            has_renderer=render,
            # has_offscreen_renderer = False,
            # use_camera_obs = False,
            # render_camera="agentview",
            controller_configs=controller_config
        ))

    @JOverride
    def reset(self):
        if self.env is None:
            print("Hierarchical env not set.")
        else:
            return convert_to_java_object(self.env.reset())

    @JOverride
    def step(self, action):
        if self.env is None:
            print("Hierarchical env not set.")
        else:
            return convert_to_java_object(self.env.step(action))


# @JImplements(RLInterface):
#     @JOverride
#     def callPolicy(self, action):
#
#     @JOverride
#     def learnPolicy(self, action):
#
#     @JOverride
#     def updatePolicy(self, failedOperator):

if __name__ == '__main__':
    diarc_wrapper = TRADEWrapper()
    robotsuite_wrapper = HierarchicalRobosuiteWrapper()
    TRADE.registerAllServices(robotsuite_wrapper, "")
    print(TRADE.getAvailableServices())

    diarc_wrapper.call_trade("makeEnv", "Lift", "Panda", True)
    diarc_wrapper.call_trade("setHighEnv", diarc_wrapper.parse_goal("holding(self,physobj_0)"))
    ret = diarc_wrapper.call_trade("reset")

    model = PPO("MultiInputPolicy", robotsuite_wrapper.env, verbose=1)
    model.learn(total_timesteps=int(2e3))
    vec_env = model.get_env()
    obs = vec_env.reset()
    for i in range(1000):
        action, _state = model.predict(obs, deterministic=True)
        vec_env.step(action)
        # ret = diarc_wrapper.call_trade("step", action.flatten().tolist())
        robotsuite_wrapper.env.render()
