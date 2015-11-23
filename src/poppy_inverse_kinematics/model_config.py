# coding= utf8
from . import robot_utils
import numpy as np


class model_config():
    """Configuration of a model"""
    def __init__(self, joints, representation="euler", model_type="custom", name="robot", motor_config_file=None):
        self.parameters = joints
        self.joints_number = len(joints)
        self.representation = representation
        self.model_type = model_type
        self.name = name
        # motor_config is the path of the pypot-style json robot file
        if motor_config_file is not None:
            self.motor_parameters = robot_utils.get_motor_parameters(json_file=motor_config_file)
            # Generate bounds
            self.bounds = []
            for joint in self.parameters:
                if joint["name"] != "last_joint":
                    offset = self.motor_parameters[joint["name"]]["offset"]
                    if self.motor_parameters[joint["name"]]["orientation"] == "indirect":
                        orientation = "indirect"
                    else:
                        orientation = "direct"

                    # Compute bounds with the right convention
                    new_bounds = tuple([robot_utils.convert_angle_limit(angle, orientation, offset, joint_name=joint["name"]) for angle in self.motor_parameters[joint["name"]]["angle_limit"]])
                else:
                    # If it is the last joint, there is no dof
                    new_bounds = (None, None)

                self.bounds.append(new_bounds)
        else:
            self.motor_parameters = None
            self.motor_bounds = None

    def __repr__(self):
        return("Configuration of robot : {0}".format(self.name))


def from_urdf_file(urdf_file, base_elements=["base_link"], last_link_vector=None, base_elements_type="joint", motor_config_file=None):
    urdf_params = robot_utils.get_urdf_parameters(urdf_file, base_elements=base_elements, last_link_vector=last_link_vector, base_elements_type=base_elements_type)
    return model_config(urdf_params, representation="rpy", model_type="URDF", motor_config_file=motor_config_file)
