from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, EqualsSubstitution
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from launch.substitutions import Command
import os
from ament_index_python.packages import get_package_share_path

def generate_launch_description():

    urdf_path = os.path.join(get_package_share_path('mh5_description'),
                             'urdf', 'mh5_robot_revH.urdf.xacro')
    rviz_config_path = os.path.join(get_package_share_path('mh5_description'),
                                    'rviz', 'urdf_config.rviz')
    
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    
    return LaunchDescription([
        DeclareLaunchArgument(
            name="use_gui",
            default_value="true",
            description="start joint_state_publisher_gui_node"
        ),

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{'robot_description': robot_description}]
        ),

        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            condition=IfCondition(EqualsSubstitution(LaunchConfiguration("use_gui"), "true"))
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            arguments=['-d', rviz_config_path]
        )
    ])
