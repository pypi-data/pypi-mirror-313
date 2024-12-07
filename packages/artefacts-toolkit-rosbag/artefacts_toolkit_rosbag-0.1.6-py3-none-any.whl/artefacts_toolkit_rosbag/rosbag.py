from datetime import datetime
from launch.actions import ExecuteProcess


def get_bag_recorder(topic_names, use_sim_time=False):
    """Create a rosbag2 recorder for a given list of topic names and return the node and the filepath"""
    yyyymmddhhmmss = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    rosbag_filepath = "rosbag2_" + yyyymmddhhmmss
    rosbag_cmd = (
        ["ros2", "bag", "record"]
        + topic_names
        + ["-o", rosbag_filepath, "--storage", "mcap"]
    )
    if use_sim_time:
        rosbag_cmd = rosbag_cmd + ["--use-sim-time"]
    bag_recorder = ExecuteProcess(cmd=rosbag_cmd, output="screen")
    return bag_recorder, rosbag_filepath
