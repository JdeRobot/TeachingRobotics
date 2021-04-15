---
permalink: /installation/
title: "INSTALLATION INSTRUCTIONS"

sidebar:
  nav: "docs"

toc: true
toc_label: "TOC installation"
toc_icon: "cog"
---

**Robotics-Academy (2.3 release)** supports Linux (Ubuntu 18.04, 20.04 and other distributions), MacOS and Windows. The installation has been greatly simplified, as all the required dependencies are already pre-installed in the Robotics-Academy Docker Image. The users of this release should:

1. Install the [RADI (Robotics-Academy Docker Image)](https://hub.docker.com/r/jderobot/robotics-academy/tags) on their machines
2. Copy the [Robotics-Academy source code repository](https://jderobot.github.io/RoboticsAcademy/installation/#robotics-academy-source-code) on their machines. 

Enjoy :-)

**Robotics-Academy (both 2.1 and 2.0 releases)** currently supports Linux operating system. These installation instructions have been prepared for Ubuntu Linux 18.04 (LTS). Don't install everything listed here, just follow the directions on the Academy exercise you want to perform. For instance, not all the specific infrastructure packages are required for every exercise, and they can be large packages.

1. *Generic infrastucture*
    - Required
    - ROS middleware, Gazebo simulator, JdeRobot-base, JdeRobot-assets

2. *Specific infrastructure*
    - Optional, depends on the exercise
    - Some exercises require also additional software pieces such as OpenCV, MoveIt!, MavROS, PX4, VisualStates, OpenMotionPlanningLibrary, Turtlebot2, etc.

3. *Robotics-Academy source code*
    - Required
    - Robotics-Academy includes templates for the exercises

# Generic infrastructure

## ROS Middleware

Supported release is ROS-Melodic. It can be easily installed from official Debian packages, maintained by OpenRobotics organization.

1. Add the lastest ROS source:

    ```bash
    sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
    ```

    ```bash
 sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
    ```
<!-- sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116 -->


2. Update the repositories
    ```bash
    sudo apt update
    ```

3. Install the official ROS Melodic Debian package

    ```bash
    sudo apt install ros-melodic-desktop-full
    ```
    
4. Environment setup
    ```bash
    echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
    source ~/.bashrc
    ```    
5. Dependencies for building packages
    ```bash  
   sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential  
   sudo rosdep init  
   rosdep update  
    ```
For more information, refer [ros wiki](http://wiki.ros.org/)

## Gazebo simulator

Supported release is Gazebo-9. It can be easily installed from official Debian packages, maintained by OpenRobotics organization. You can safely ignore this step as Gazebo-9 will be automatically installed with ROS Melodic package (described in the [previous step](/RoboticsAcademy/installation/#ros-middleware)).

<!--
1. Add the lastest Gazebo source:

    ```bash
    sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable lsb_release -cs main" > /etc/apt/sources.list.d/gazebo-stable.list'
    ```

    ```bash
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key 67170598AF249743
    ```

2. Install the official Gazebo package:

    ```bash
    sudo apt install gazebo9
    ```
-->

## JdeRobot-base

Supported release is 6.1.0.
It contains ROS drivers not included in the official ROS packages.

1. Add the latest JdeRobot-base source

    ```bash
    sudo sh -c 'echo "deb [arch=amd64] http://wiki.jderobot.org/apt `lsb_release -cs` main" > /etc/apt/sources.list.d/jderobot.list'
    ```

2. Get and add the public key from the JdeRobot repository

    ```bash
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 24E521A4
    ```

3. Update the repositories

    ```bash
    sudo apt update
    ```

4. Install JdeRobot-base

    ```bash
    sudo apt install jderobot
    ```

5. Source the environment variables:
    ```bash
    echo "source /opt/jderobot/setup.bash" >> ~/.bashrc 
    source ~/.bashrc    
    ```

## JdeRobot-assets

Supported release is 6.1.0
It contains Gazebo world files and configuration files required for the Academy exercises.

1. Install jderobot-assets debian package

    ```bash
    sudo apt install jderobot-assets
    ```

2. Install jderobot-assets ROS package

    ```bash
    sudo apt install ros-melodic-jderobot-assets
    ```

3. Source the environment variables:
    ```bash
    echo "source /opt/jderobot/share/jderobot/gazebo/gazebo-setup.sh" >> ~/.bashrc
    echo "source /opt/jderobot/share/jderobot/gazebo/assets-setup.sh" >> ~/.bashrc
    source ~/.bashrc
    ```

# Specific infrastructure

## OpenCV

You can install OpenCV in several ways:

- Installing from the [PyPi repository](https://pypi.org/project/opencv-python/).
- Compiling it from its [source code](https://docs.opencv.org/3.4.1/d2/de6/tutorial_py_setup_in_ubuntu.html).

For more information, visit the [official repository](https://github.com/opencv/opencv).

## JdeRobot-drones

A. Binary installation (recommended)

```bash
sudo apt-get install ros-melodic-jderobot-drones
```

B. Source installation:

1. Install catkin tools

    ```bash
    sudo apt install python-catkin-tools
    ```

2. Set up catkin workspace

    ```bash
    mkdir -p ~/catkin_ws/src
    cd ~/catkin_ws
    catkin init
    echo 'export ROS_WORKSPACE=~/catkin_ws' >> ~/.bashrc # points roscd dir
    source ~/.bashrc
    ```
    
3. Get jderobot-drones ros pkg

    ```bash
    cd ~ && mkdir -p repos && cd repos
    git clone https://github.com/JdeRobot/drones.git
    ```
    
4. Link drone source to catkin_ws

    ```bash
    roscd && cd src
    ln -s ~/repos/drones/drone_wrapper .
    ln -s ~/repos/drones/drone_assets .
    ln -s ~/repos/drones/rqt_drone_teleop .
    ```

5. Update ros dependencies

    ```bash
    roscd
    rosdep init  # needs to be called ONLY once after installation. sudo might be required
    rosdep update && rosdep install --from-paths . --ignore-src --rosdistro melodic -y  #sudo might be required
    ```

6. Build 

    ```bash
    roscd && catkin build
    ```
    
7. Export environment variables

    ```bash
    roscd
    echo 'source '$PWD'/devel/setup.bash' >> ~/.bashrc
    echo 'export GAZEBO_RESOURCE_PATH=${GAZEBO_RESOURCE_PATH}:/usr/share/gazebo-9' >> ~/.bashrc
    echo 'export GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:~/repos/drones/drone_assets/models' >> ~/.bashrc
    source ~/.bashrc
    ```

## MavROS

Binary installation:

1. Install ROS Melodic MAVROS and extras (v1.5.0-1)

    ```bash
    sudo apt install ros-melodic-mavros ros-melodic-mavros-extras
    ```

## PX4

Install previous dependencies:

1. Download and install GeographicLib

    ```bash
    wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
    chmod +x install_geographiclib_datasets.sh
    sudo ./install_geographiclib_datasets.sh
    ```

2. Remove modemmanager

    ```bash
    sudo apt remove modemmanager
    ```

3. Install common dependencies

    ```bash
    sudo apt update -y
    sudo apt-get install git zip qtcreator cmake \
       build-essential genromfs ninja-build exiftool \
       python-pip python-dev -y
    ```

4. Install xxd

    ```bash
    which xxd || sudo apt install xxd -y || sudo apt install vim-common --no-install-recommends -y
    ```

5. Install required python packages

    Install Python 3 pip build dependencies first

    ```bash
    sudo pip3 install wheel setuptools
    ```
    
    Python 3 dependencies installed by pip

    ```bash
    sudo pip3 install argparse argcomplete coverage cerberus empy jinja2 \
                    matplotlib==3.0.* numpy nunavut packaging pkgconfig pyros-genmsg pyulog \
                    pyyaml requests serial six toml psutil pyulog wheel
    ```

    Install everything again for Python 2 because we could not get Firmware to compile using catkin without it.

    ```bash
    sudo pip install --upgrade pip 
    sudo pip install wheel setuptools
    sudo pip install argcomplete argparse catkin_pkg catkin-tools cerberus coverage \
        empy jinja2 matplotlib==2.2.* numpy pkgconfig px4tools pygments pymavlink \
        packaging pyros-genmsg pyulog pyyaml requests rosdep rospkg serial six toml \
        pandas pyserial
    ```

6. Install ninja

    ```bash
    sudo apt install ninja-build -y
    ```

7. Get FastRTPS and FastCDR

    ```bash
    wget https://www.eprosima.com/index.php/component/ars/repository/eprosima-fast-dds/eprosima-fast-rtps-1-7-1/eprosima_fastrtps-1-7-1-linux-tar-gz -O eprosima_fastrtps-1-7-1-linux.tar.gz
    tar -xzf eprosima_fastrtps-1-7-1-linux.tar.gz eProsima_FastRTPS-1.7.1-Linux/
    tar -xzf eprosima_fastrtps-1-7-1-linux.tar.gz requiredcomponents
    tar -xzf requiredcomponents/eProsima_FastCDR-1.0.8-Linux.tar.gz
    ```

8. Build FastRTPS and FastCDR

    ```bash
    (cd eProsima_FastCDR-1.0.8-Linux && ./configure --libdir=/usr/lib && make -j2 && sudo make install)
    cd ..
    (cd eProsima_FastRTPS-1.7.1-Linux && ./configure --libdir=/usr/lib && make -j2 && sudo make install)
    rm -rf requiredcomponents eprosima_fastrtps-1-7-1-linux.tar.gz
    ```

PX4 source installation:
1. Get PX4 source (v1.11.3)

    ```bash
    cd ~ && mkdir -p repos && cd repos
    git clone https://github.com/PX4/Firmware.git
    cd Firmware && git checkout v1.11.3
    git checkout -b v1.11.3
    ```

2. Build PX4

    ```bash
    cd ~/repos/Firmware
    DONT_RUN=1 make px4_sitl_default gazebo
    ```

3. Export environment variables

    ```bash
    echo 'export GAZEBO_PLUGIN_PATH=$GAZEBO_PLUGIN_PATH:~/repos/Firmware/build/px4_sitl_default/build_gazebo' >> ~/.bashrc
    echo 'export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/repos/Firmware/Tools/sitl_gazebo/models' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/repos/Firmware/build/px4_sitl_default/build_gazebo' >> ~/.bashrc
    
    echo 'export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:~/repos/Firmware' >> ~/.bashrc
    echo 'export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:~/repos/Firmware/Tools/sitl_gazebo' >> ~/.bashrc
    
    source ~/.bashrc
    ```

4. Try PX4 (optional)

    ```bash
    roslaunch px4 mavros_posix_sitl.launch
    pxh> commander arm # when launching finishes
    ```

## Real Turtlebot2 on ROS Melodic

0. Prerequisites
- ROS Melodic on Ubuntu 18
- Turtlebot2

1. Build Turtlebot2 Workspace

Firstly, `cd` to your catkin workspace. 

If you don't have one, `cd` to somewhere you want to create it, and then run the following commands to create one
```bash
mkdir -p src
catkin_make
```

Now run the following command (inside the root of catkin workspace) to build up running environment for Turtlebot2
```bash
curl -sLf https://raw.githubusercontent.com/gaunthan/Turtlebot2-On-Melodic/master/install_basic.sh | bash
catkin_make
```

2. Bring Up Turtlebot2
Now connect a turtlebot2 to the computer. After that, run this command to bring up the Turtlebot2
```bash
source ./devel/setup.bash
roslaunch turtlebot_bringup minimal.launch
```

If nothing wrong, you will hear the Turtlebot2 give out a reminder.

3. Test Turtlebot2
If you want to use keyboard to control it, just run the following command
```bash
source ./devel/setup.bash
roslaunch turtlebot_teleop keyboard_teleop.launch
```

And it will output something like this

```bash
ROS_MASTER_URI=http://localhost:11311

process[turtlebot_teleop_keyboard-1]: started with pid [23757]

Control Your Turtlebot!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
space key, k : force stop
anything else : stop smoothly

CTRL-C to quit

currently:	speed 0.2	turn 1 
```

Now you should be able to use keyboard to control your Turtlebot2.

4. Asus Xtion

Install dependencies:
```bash
sudo apt-get install ros-melodic-rgbd-launch ros-melodic-openni2-camera ros-melodic-openni2-launch
sudo apt-get install ros-melodic-rqt ros-melodic-rqt-common-plugins ros-melodic-rqt-robot-plugins
```

Run these commands on three different terminals to test it:
```bash
roscore
```
```bash
roslaunch openni2_launch openni2.launch
```
```bash
rqt
```

In this last application, `rqt`, go to `Plugins` -> `Visualization` -> `Image view` -> `depth/image_raw` to view the camera depth raw data.

5. RPLidar

Just test it! Run these commands on two different terminals:
```bash
roscore
```
```bash
roslaunch rplidar_ros view_rplidar.launch 
```

## MoveIt!

# Robotics-Academy source code

Once you have generic and specific infrastructure installed in your system, you can download and install the JdeRobot Academy software.

1. Clone the Academy software repository.

    ```bash
    git clone https://github.com/JdeRobot/Academy.git
    ```

## Docker installation
1. Clone the [RoboticsAcademy](https://github.com/JdeRobot/RoboticsAcademy) repository.
    ```bash
    git clone https://github.com/JdeRobot/Academy.git
    ```
2. Run the docker container.
    ```bash
    docker run -it --name=docker_academy -p 2303:2303 -p 1905:1905 jderobot/web-templates:follow_line
    ```
3. Once inside de container bash run.
    ```bash
    cd follow_line
    . screen.sh
    ```
4. Then, launch the headless simulation of the exercise (Inside the docker bash).
    ```bash
    roslaunch ./launch/simple_line_follower_ros.launch
    ```
5. The last instruction runs a process that must not be stopped. To carry out the last step we need to open the container bash in another terminal window.
    ```bash
    docker exec -it docker_academy bash
    ```
6. Lastly, to complete the docker setup we must run host.py inside the docker.
    ```bash
    cd follow_line
    python host.py 0.0.0.0
    ```
7. The last instruction will run indefinetly too. Now we go to our local machine (where we have cloned the RoboticsAcademy repository). We need to navigate to RoboticsAcademy/exercises/follow_line/web-templates.

8. Inside assets\websocket_address.js we need to change the variable websocket_address to the IP where our docker container is running. To check the ip:
    ```bash
    docker inspect robotics_academy
    ```
    If you are running Docker Desktop in Windows, the IP will usually be "localhost".
    
9. Launch the index.html web-page with any browser.

10. If while running the exercise you only get a black screen you need to stop the container and start it again (docker container start docker_academy). Instead of carrying out steps 4 and 6 run the following instructions first.
    ```bash
    docker exec -it docker_academy bash
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    apt-get update && sudo apt-get install -y nvidia-container-toolkit
    apt-get install xvfb
    Xvfb :1 -screen 0 1600x1200x16 & export Display=:1.0
    ```
    Then run everything from step 4 to step 9.

<!---

# Installation on Windows(x64)  DEPRECATED

The programming environment is composed of the (a) Docker with Gazebo simulator, (b) JdeRobot middleware for Python and (c) the TeachingRobotics package. All this software is open source so there are alternative ways to install all of them directly from the source code. Currently we use Gazebo-7.4.0, JdeRobot-5.4.1 and TeachingRobotics-0.1.0 releases. JdeRobot Docker includes the Gazebo plugins, models and configuration files to simulate the robot used in the exercises.

### Prerequisites

First check that you have the following dependencies installed. If not, you can install them in the links provided.

- Install checked `env` variables (Is possible that you need restart to run the PATH). You can <a href="https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe" target="_blank">download here</a>.

- Download qt 5.7 <a href="http://download.qt.io/official_releases/qt/5.7/5.7.0/qt-opensource-windows-x86-msvc2015_64-5.7.0.exe" target="_blank">here</a>.
- Download github Desktop <a href="https://desktop.github.com" target="_blank">from here</a>.
- Download Docker:
  - <a href="https://download.docker.com/win/stable/InstallDocker.msi" target="_blank">Windows 10 x64 proffesional or enterprise</a>
  - <a href="http://www.docker.com/products/docker-toolbox" target="_blank"> Other Windows x64</a>



### Installation

Follow the next four steps to have the environment up and running, ready to use.

1. Upgrade pip.

    Open `CMD` or powershell and upgrade pip typing:

    ```bash
    python -m pip install --upgrade pip
    ```

2. Install dependencies.

    Install the following depencencies

    ```bash
    pip3 install numpy zeroc-ice
    pip3 install pyqt5
    pip3 install opencv-python
    ```

3. Install JdeRobot Python.

    Install JdeRobot Python typing:

    ```bash
    pip3 install http://jderobot.org/store/aitormf/uploads/windows/JdeRobot-0.1.0-py3-none-any.whl
    ```

4. Clone Robotics-Academy repository.

    Download the Academy software. With git Shell clone the repository as in Linux and run the exercices with `CMD` o powershell

    ```bash
    git clone https://github.com/jderobot/academy.git
    ```

_Note: Github repositories are located in `Documents\GitHub`_




### Run Exercises

Open Kinematics of Docker and push "Docker cli".

Run the docker passing the world to use (the first time docker image is downloaded):

```bash
docker run -tiP --rm -p 7681:7681 jderobot/jderobot world [world_name]
```

With `CMD` or PowerShell go to practice directory in Academy and run it:

```bash
python [practice_file][config_file]
```

You can watch a video demonstration.


--->
