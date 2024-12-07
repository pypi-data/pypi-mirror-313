import cv2
import subprocess

from rosbags.rosbag2 import Reader
from rosbags.typesys import Stores, get_typestore
from rosbags.image import message_to_cvimage
from pathlib import Path
from artefacts_toolkit_rosbag_gpl.ros2bag2video import rosbag_to_mp4


def extract_video(rosbag_filepath, topic_name, output_filepath, fps=20):
    rosbag_to_mp4(rosbag_filepath, topic_name, output_filepath, fps)


def _get_last_image_from_rosbag(rosbag_filepath, topic_name, output_dest):
    # Create a typestore and get the string class.
    typestore = get_typestore(Stores.LATEST)

    formatted_name = topic_name.replace("/", "_")
    filename = f"{output_dest}/{formatted_name}.last.png"
    for p in Path(output_dest).glob(f"{formatted_name}.last.png"):
        p.unlink()
    img = None
    # Create reader instance and open for reading.
    with Reader(rosbag_filepath) as reader:
        # Topic and msgtype information is available on .connections list.
        for connection in reader.connections:
            print(connection.topic, connection.msgtype)
        for connection, timestamp, rawdata in reader.messages():
            if connection.topic == topic_name:
                msg = typestore.deserialize_cdr(rawdata, connection.msgtype)
                img = message_to_cvimage(msg, "bgr8")
    if img is not None:
        cv2.imwrite(filename, img)
    return filename


def extract_camera_image(flag, rosbag_filepath, camera_topic):
    if flag:
        output_dir = "output"
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(e)
        try:
            _get_last_image_from_rosbag(rosbag_filepath, camera_topic, output_dir)
        except Exception as e:
            print("error")
            print(e)
