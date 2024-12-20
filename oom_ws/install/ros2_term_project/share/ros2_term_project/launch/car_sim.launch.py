#!/usr/bin/env python3
#
# Copyright 2023. Prof. Jong Min Lee @ Dong-eui University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import json
from launch.substitutions import LaunchConfiguration


print(os.path.realpath(__file__))

ld = LaunchDescription()


def generate_launch_description():
    # configuration
    world = LaunchConfiguration('world')
    print('world =', world)
    world_file_name = 'car_track.world'
    world = os.path.join(get_package_share_directory('ros2_term_project'),
                         'worlds', world_file_name)
    print('world file name = %s' % world)
    # ld = LaunchDescription()
    declare_argument = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true')

    gazebo_run = ExecuteProcess(
        cmd=['gazebo', '-s', 'libgazebo_ros_factory.so', world],
        output='screen')

    cube_mover_node = Node(
        package='ros2_term_project',
        executable='cube_mover',
        name='cube_mover',
        output='screen',
    )
    
    # 차량 spawn 실행 (spawn.py 실행)
    spawn_car_node = ExecuteProcess(
        cmd=['python3', '/home/ros2/Ros2Projects/oom_ws/src/ros2_term_project/test/spawn_car.py'],  # 경로 수정
        output='screen')
    
    line_follower_node = Node(
        package='ros2_term_project',
        executable='follower',
        name='follower',
        output='screen',
    )

    ld.add_action(declare_argument)
    ld.add_action(gazebo_run)
    ld.add_action(cube_mover_node)
    ld.add_action(spawn_car_node)
    ld.add_action(line_follower_node)
    return ld
