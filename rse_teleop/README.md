# RSE Teleoperation Package

`rse_teleop` supplies the configured human-control pipeline used in Robotics
Software Engineering. It keeps each candidate velocity command on a separate
topic and publishes one selected command to `/cmd_vel`.

```text
gamepad -> /joy -> teleop_node -> /cmd_vel/joystick --+
                                                        |
keyboard ----------------------> /cmd_vel/keyboard -----+-> twist_mux -> /cmd_vel
                                                        |
future autonomy ----------------> /cmd_vel/auto --------+
```

The package does not start a simulator. Run the course simulator separately;
any simulator or robot subscribing to `/cmd_vel` can consume the selected
output.

## Install system dependencies

On Ubuntu 24.04 with ROS 2 Jazzy:

```bash
sudo apt update
sudo apt install joystick \
  ros-jazzy-joy \
  ros-jazzy-teleop-twist-joy \
  ros-jazzy-teleop-twist-keyboard \
  ros-jazzy-twist-mux
```

## Build in a workspace

Place this directory under a workspace's `src/` directory, then:

```bash
cd ~/rse_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Source both setup files again in each new terminal.

## Verify the gamepad before using ROS

```bash
lsusb
ls -l /dev/input/js*
jstest /dev/input/js0
```

If `jstest` does not respond to the controller, fix the device or operating-
system problem before debugging ROS topics.

## Inspect raw ROS gamepad input

Start only the joystick input and conversion path:

```bash
ros2 launch rse_teleop joystick.launch.py
```

Inspect the raw device state:

```bash
ros2 topic info /joy
ros2 interface show sensor_msgs/msg/Joy
ros2 topic echo /joy
```

The default configuration uses a common Xbox-style mapping:

- left stick vertical axis (`axes[1]`) controls `linear.x`;
- left stick horizontal axis (`axes[0]`) controls `angular.z`;
- LB (`buttons[4]`) enables normal motion; and
- RB (`buttons[5]`) enables faster motion.

Controller mappings vary. Inspect `/joy` and edit
`config/teleop_twist_joy.yaml` if the indices or directions do not match the
course controller. Do not test an unknown mapping on a physical robot.

## Run the full teleoperation pipeline

Start the gamepad path and multiplexer:

```bash
ros2 launch rse_teleop teleop.launch.py
```

In a separate terminal, start keyboard teleoperation. It stays outside the
launch file because it needs direct terminal input:

```bash
source /opt/ros/jazzy/setup.bash
source ~/rse_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r cmd_vel:=/cmd_vel/keyboard
```

Inspect the candidate and selected commands:

```bash
ros2 topic echo /cmd_vel/joystick
ros2 topic echo /cmd_vel/keyboard
ros2 topic echo /cmd_vel
```

The default priorities are:

| Source | Topic | Priority | Timeout |
| --- | --- | ---: | ---: |
| Gamepad | `/cmd_vel/joystick` | 100 | 0.5 s |
| Keyboard | `/cmd_vel/keyboard` | 50 | 0.5 s |
| Autonomy | `/cmd_vel/auto` | 10 | 0.5 s |

The highest-priority active source controls `/cmd_vel`. After its messages
stop for the configured timeout, the next active source can take control.

## Demonstrate a third command source

This simulation-only command acts as a low-priority autonomous source:

```bash
ros2 topic pub --rate 4 /cmd_vel/auto geometry_msgs/msg/Twist \
  "{linear: {x: 0.1}, angular: {z: 0.0}}"
```

Stop it with `Ctrl+C`. Publish an explicit zero command if no controller is
running through the mux:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

## Emergency-stop lock

The mux listens for a Boolean lock on `/e_stop`. Engage and release it with:

```bash
ros2 topic pub --once /e_stop std_msgs/msg/Bool "{data: true}"
ros2 topic pub --once /e_stop std_msgs/msg/Bool "{data: false}"
```

This is an instructional software lock, not a substitute for a physical
emergency stop on a real robot.

## Record a teleoperation trial

```bash
mkdir -p ~/rse_bags
cd ~/rse_bags
ros2 bag record -o teleop_trial_01 \
  /joy \
  /cmd_vel/joystick \
  /cmd_vel/keyboard \
  /cmd_vel \
  /odom
```

End recording with `Ctrl+C`, then inspect it:

```bash
ros2 bag info teleop_trial_01
```

Before replaying commands, stop live controllers and reset the simulator. Use
`ros2 bag play --help` to confirm the options installed with your ROS release.
To replay only the selected command stream:

```bash
ros2 bag play teleop_trial_01 --topics /cmd_vel
```

Replaying a command topic can move a robot. Use simulation unless a physical
robot has been deliberately prepared for the test.

## Configuration files

- `config/joy.yaml`: device input and filtering
- `config/teleop_twist_joy.yaml`: axes, buttons, and velocity scales
- `config/twist_mux.yaml`: input topics, timeouts, priorities, and lock

These files are intentionally visible for the Week 2 lesson on parameters,
YAML, remapping, and launch files.
