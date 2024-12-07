from rosbags.rosbag2 import Reader
from rosbags.typesys import Stores, get_typestore
from artefacts_toolkit_utilities import extract_attribute_data


def get_final_message(rosbag_filepath, topic):
    typestore = get_typestore(Stores.LATEST)
    final_message = None
    topic_attributes = topic.split(".")

    with Reader(rosbag_filepath) as reader:
        for connection, timestamp, rawdata in reader.messages():
            if connection.topic == topic_attributes[0]:
                msg = typestore.deserialize_cdr(rawdata, connection.msgtype)
                final_message = extract_attribute_data(msg, topic_attributes)

    return final_message
