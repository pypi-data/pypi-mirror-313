import time

import numpy as np
import robosuite
from robosuite.wrappers import GymWrapper

from pyTRADE.core.wrapper import TRADEWrapper
from ai.thinkingrobots.trade import TRADE
from jpype import JImplements, JOverride
from edu.tufts.hrilab.rl import RobosuiteInterface
from robosuite.controllers import load_controller_config

from pyTRADE.core.java_util import convert_to_java_object


@JImplements(RobosuiteInterface)
class RobosuiteWrapper:
    def __init__(self, env=None):
        self.env = env

    @JOverride
    def makeEnv(self, env_name, robot, render):
        controller_config = load_controller_config(default_controller="JOINT_POSITION")

        self.env = robosuite.make(
            env_name=env_name,
            robots=robot,
            has_renderer=render,
            controller_configs=controller_config
        )

    @JOverride
    def setHighEnv(self, goal):
        print("N/A")

    @JOverride
    def reset(self):
        self.env.reset()

    @JOverride
    def step(self, action):
        return convert_to_java_object(self.env.step(action))

if __name__ == '__main__':
    diarc_wrapper = TRADEWrapper()
    robotsuite_wrapper = RobosuiteWrapper()
    TRADE.registerAllServices(robotsuite_wrapper, "")
    time.sleep(1)
    diarc_wrapper.call_trade("makeEnv", "Lift", "Kinova3", True)
    diarc_wrapper.call_trade("reset")
    env = GymWrapper(robotsuite_wrapper.env)

    for i in range(1000):
        action = np.random.randn(robotsuite_wrapper.env.robots[0].action_dim) # sample random action
        # obs, reward, done, info = robotsuite_wrapper.env.step(action)  # Todo: Get return values from TRADE call
        ret = diarc_wrapper.call_trade("step", action.tolist())
        env.render()  # render on display
