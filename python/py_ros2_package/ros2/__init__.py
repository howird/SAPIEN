from ..core.pysapien_ros2.ros2 import *
import os

__CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
os.environ["LD_LIBRARY_PATH"] += os.path.abspath(os.path.join(__CURRENT_PATH, "../../sapien_robot.libs"))
print("Current LD_LIBRARY_PATH is: {}".format(os.environ["LD_LIBRARY_PATH"]))


def __init():
    import os
    init_spd_logger()
    set_ros2_logging_level("warning")
    resources_dir = os.path.abspath(os.path.dirname(__file__)).rstrip('/')
    set_resources_directory(resources_dir)
    print(resources_dir)


__init()
