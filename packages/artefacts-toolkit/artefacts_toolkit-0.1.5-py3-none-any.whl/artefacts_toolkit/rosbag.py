from artefacts_toolkit_rosbag.rosbag import get_recorder
from artefacts_toolkit_rosbag.image_topics import get_camera_image, get_video
from artefacts_toolkit_rosbag.message_topics import get_final_topic_message

def get_bag_recorder(topic_names, use_sim_time=False):
    bag_recorder, rosbag_filepath = get_recorder(topic_names, use_sim_time=False)
    return bag_recorder, rosbag_filepath


def extract_video(rosbag_filepath, topic_name, output_filepath, fps=20):
    get_video(rosbag_filepath, topic_name, output_filepath, fps)


def extract_image(flag, rosbag_filepath, camera_topic):
    get_camera_image(flag, rosbag_filepath, camera_topic)


def get_final_message(rosbag_filepath, topic):
    final_message = get_final_topic_message(rosbag_filepath, topic) 
    return final_message