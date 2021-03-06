FROM osrf/ros:melodic-desktop-full
ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}

ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

# Setup NON INTERACTIVE ENVIRONMENT
ENV DEBIAN_FRONTEND noninteractive

# Setup X11 Volume
VOLUME /tmp/.X11-unix:/tmp/.X11-unix:rw

# BASE
RUN apt-get update && apt-get -y --quiet install \
        libjansson-dev \
        libboost-dev \
        imagemagick \
        libtinyxml-dev \
        mercurial \
        build-essential

# PX4
RUN apt remove modemmanager
RUN apt-get update && apt-get -y --quiet --no-install-recommends install \
		bzip2 \
		ca-certificates \
		ccache \
		cmake \
		cppcheck \
		curl \
		dirmngr \
		doxygen \
		exiftool \
		file \
		g++ \
		gcc \
		gdb \
		genromfs \
		git \
		gnupg \
		gosu \
		lcov \
		libfreetype6-dev \
		libgtest-dev \
		libpng-dev \
		libssl-dev \
		lsb-release \
		make \
		ninja-build \
		openjdk-8-jdk \
		openjdk-8-jre \
		openssh-client \
		pkg-config \
		python3-dev \
		python3-pip \
		qtcreator \
		rsync \
		shellcheck \
		tzdata \
		unzip \
		valgrind \
		wget \
		xsltproc \
		zip \
	&& apt-get -y autoremove \
	&& apt-get clean autoclean \
	&& rm -rf /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

RUN which xxd || apt install xxd -y || apt install vim-common --no-install-recommends -y

# gtest
RUN cd /usr/src/gtest \
	&& mkdir build && cd build \
	&& cmake .. && make -j$(nproc) \
	&& cp *.a /usr/lib \
	&& cd .. && rm -rf build

# Install Python 3 pip build dependencies first.
RUN pip3 install wheel setuptools

# Python 3 dependencies installed by pip
RUN pip3 install argparse argcomplete coverage cerberus empy jinja2 \
		matplotlib==3.0.* numpy nunavut packaging pkgconfig pyros-genmsg pyulog \
		pyyaml requests serial six toml psutil pyulog wheel

# manual ccache setup
RUN ln -sf /usr/bin/ccache /usr/lib/ccache/cc \
	&& ln -sf /usr/bin/ccache /usr/lib/ccache/c++

# astyle v3.1
RUN wget -q https://downloads.sourceforge.net/project/astyle/astyle/astyle%203.1/astyle_3.1_linux.tar.gz -O /tmp/astyle.tar.gz \
	&& cd /tmp && tar zxf astyle.tar.gz && cd astyle/src \
	&& make -f ../build/gcc/Makefile -j$(nproc) && cp bin/astyle /usr/local/bin \
	&& rm -rf /tmp/*

# Gradle (Required to build Fast-RTPS-Gen)
RUN wget -q "https://services.gradle.org/distributions/gradle-6.3-rc-4-bin.zip" -O /tmp/gradle-6.3-rc-4-bin.zip \
	&& mkdir /opt/gradle \
	&& cd /tmp \
	&& unzip -d /opt/gradle gradle-6.3-rc-4-bin.zip \
	&& rm -rf /tmp/*

ENV PATH "/opt/gradle/gradle-6.3-rc-4/bin:$PATH"

# Fast-RTPS 1.8.2
RUN git clone --recursive https://github.com/eProsima/Fast-DDS.git -b v1.8.2 /tmp/FastRTPS-1.8.2 \
	&& cd /tmp/FastRTPS-1.8.2 \
	&& mkdir build && cd build \
	&& cmake -DTHIRDPARTY=ON -DSECURITY=ON .. \
	&& cmake --build . --target install -- -j $(nproc) \
	&& rm -rf /tmp/*

# Fast-RTPS-Gen 1.0.4
RUN git clone --recursive https://github.com/eProsima/Fast-DDS-Gen.git -b v1.0.4 /tmp/Fast-RTPS-Gen-1.0.4 \
	&& cd /tmp/Fast-RTPS-Gen-1.0.4 \
	&& gradle assemble \
	&& gradle install \
	&& rm -rf /tmp/*

RUN wget --quiet http://packages.osrfoundation.org/gazebo.key -O - | apt-key add - \
	&& sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -sc` main" > /etc/apt/sources.list.d/gazebo-stable.list' \
	&& apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get -y --quiet --no-install-recommends install \
		ant \
		bc \
		gazebo9 \
		gstreamer1.0-plugins-bad \
		gstreamer1.0-plugins-base \
		gstreamer1.0-plugins-good \
		gstreamer1.0-plugins-ugly \
		libeigen3-dev \
		libgazebo9-dev \
		libgstreamer-plugins-base1.0-dev \
		libimage-exiftool-perl \
		libopencv-dev \
		libxml2-utils \
		protobuf-compiler \
	&& apt-get -y autoremove \
	&& apt-get clean autoclean \
	&& rm -rf /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

ENV ROS_DISTRO melodic

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 \
	&& sh -c 'echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-latest.list' \
	&& sh -c 'echo "deb http://packages.ros.org/ros-shadow-fixed/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-shadow.list' \
	&& apt-get update \
	&& apt-get -y --quiet --no-install-recommends install \
		geographiclib-tools \
		libeigen3-dev \
		libgeographic-dev \
		libopencv-dev \
		libyaml-cpp-dev \
		python-pip \
		python-tk \
		ros-$ROS_DISTRO-gazebo-ros-pkgs \
		ros-$ROS_DISTRO-jderobot-drones \
		ros-$ROS_DISTRO-mav-msgs \
		ros-$ROS_DISTRO-mavlink \
		ros-$ROS_DISTRO-mavros \
		ros-$ROS_DISTRO-mavros-extras \
		ros-$ROS_DISTRO-octomap \
		ros-$ROS_DISTRO-octomap-msgs \
		ros-$ROS_DISTRO-pcl-conversions \
		ros-$ROS_DISTRO-pcl-msgs \
		ros-$ROS_DISTRO-pcl-ros \
		ros-$ROS_DISTRO-ros-base \
		ros-$ROS_DISTRO-rostest \
		ros-$ROS_DISTRO-rosunit \
		ros-$ROS_DISTRO-xacro \
		xvfb \
	&& geographiclib-get-geoids egm96-5 \
	&& apt-get -y autoremove \
	&& apt-get clean autoclean \
	&& rm -rf /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

# Install everything again for Python 2 because we could not get Firmware
# to compile using catkin without it.
ENV PIP_DEFAULT_TIMEOUT=1000
RUN pip install wheel setuptools
RUN pip install argcomplete argparse catkin_pkg catkin-tools cerberus coverage 
RUN pip install packaging pyros-genmsg pyulog==0.8.* pyyaml requests rosdep rospkg serial six toml
RUN pip install empy jinja2 matplotlib==2.2.* numpy pkgconfig px4tools pygments 
RUN pip install pymavlink 

# bootstrap rosdep
# RUN rosdep init && rosdep update
RUN rosdep update

## PX4 src
RUN apt-get update
RUN apt upgrade -y --quiet --no-install-recommends libignition-math2
RUN git clone --recursive https://github.com/PX4/Firmware.git -b v1.11.3 \
	&& cd /Firmware \
	&& DONT_RUN=1 make px4_sitl_default gazebo


# Get the Custom Robot Repository
# and set the environment variables
RUN mkdir -p /opt/jderobot && cd /opt/jderobot && git clone https://github.com/JdeRobot/CustomRobots.git \
    && cd CustomRobots && git checkout melodic-devel && git pull origin melodic-devel

## Setting env vars
ENV GAZEBO_RESOURCE_PATH "$GAZEBO_RESOURCE_PATH:/usr/share/gazebo-9:/RoboticsAcademy/exercises/follow_line/web-template/launch"
ENV GAZEBO_PLUGIN_PATH "$GAZEBO_PLUGIN_PATH:/usr/lib/x86_64-linux-gnu/gazebo-9/plugins:/Firmware/build/px4_sitl_default/build_gazebo"
ENV GAZEBO_MODEL_PATH "$GAZEBO_MODEL_PATH:/usr/share/gazebo-9/models:/opt/jderobot/CustomRobots/f1:/opt/jderobot/CustomRobots/roomba_robot:/opt/jderobot/CustomRobots/3d_reconstruction:/opt/jderobot/CustomRobots/Taxi_navigator:/Firmware/Tools/sitl_gazebo/models:/opt/ros/melodic/share/drone_assets/models:/opt/ros/melodic/share/drone_assets/urdf"
ENV LD_LIBRARY_PATH "$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu/gazebo-9/plugins:/Firmware/build/px4_sitl_default/build_gazebo"

# GzWeb
# https://answers.gazebosim.org//question/15807/node-gyp-build-errors-while-trying-to-install-gzweb/
RUN curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
RUN apt-get install -y nodejs
RUN git clone https://github.com/osrf/gzweb.git
RUN cd gzweb && git checkout gzweb_1.4.0 && npm run deploy --- -m local

# VNC
RUN apt-get -y install x11vnc

RUN git clone https://github.com/novnc/noVNC.git &&\
	cd noVNC/utils &&\
	git checkout tags/v1.2.0 &&\ 
	git clone https://github.com/novnc/websockify websockify &&\
	cd websockify &&\
	git checkout tags/v0.9.0

# Console
RUN apt-get -y install xterm

# RoboticsAcademy
RUN git clone https://github.com/JdeRobot/RoboticsAcademy.git && cd RoboticsAcademy && git pull origin master
RUN rsync -a --exclude 'ace-builds' /RoboticsAcademy/exercises/static/exercises/* /RoboticsAcademy/exercises


# Certain Dependencies for Exercises
# Vacuum Cleaner Exercise
RUN apt-get -y --quiet install ros-melodic-kobuki-msgs

# Drone-cat-mouse
RUN apt-get -y --quiet --no-install-recommends install xmlstarlet

# Follow Turtlebot exercise
RUN apt-get update && apt-get -y --quiet --no-install-recommends install \
	ros-$ROS_DISTRO-turtlebot3-description



# Put the other commands in bashrc file
RUN echo 'source /opt/ros/melodic/setup.bash' >> ~/.bashrc
RUN echo 'source /usr/share/gazebo-9/setup.sh' >> ~/.bashrc

# Install and run XDummy XServer
RUN apt-get update && apt-get -y install xserver-xorg-video-dummy x11-apps
RUN wget https://xpra.org/xorg.conf
RUN Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xdummy.log -config ./xorg.conf :0 &
RUN echo 'export DISPLAY=:0' >> ~/.bashrc

RUN echo 'export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/Firmware' >> ~/.bashrc
RUN echo 'export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/Firmware/Tools/sitl_gazebo' >> ~/.bashrc

# websocket server dependency
RUN apt-get update && apt-get install -y python2.7 python-pip
RUN pip install websocket_server posix-ipc
COPY manager.py /manager.py
RUN apt-get install -y python3.8 python3-pip
RUN python3.8 -m pip install websockets asyncio

LABEL com.nvidia.volumes.needed="nvidia_driver"
ENV PATH /usr/local/nvidia/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64:${LD_LIBRARY_PATH}

# django to serve the exercises
RUN pip3 install django

# execute permissions to start.sh
COPY start.sh /start.sh
RUN chmod 755 /start.sh

EXPOSE 2303
EXPOSE 1905
EXPOSE 8080
EXPOSE 7681
EXPOSE 8765
EXPOSE 1108
# Port by WebRtc
EXPOSE 1831
# Port for noVNC
EXPOSE 6080
