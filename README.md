
# SPAIR_with_Reinforcement_Learning
 
This is a repo built on top of [smach_based_introspection_framework](https://github.com/birlrobotics/smach_based_introspection_framework), aiming to endow the robot with the ability of recovery decision making with life-long self-learning.

# Introduction
* Exploiting Dynamic Motion Planning (DMP) method to train the robot with high-level skills (normal kitting skills and recovering skills).
* Gathering and cleaning the multimodal sensory data (tactile sensor, force/torque sensor, camera, joint velocities, joint positions) in the robot kitting task, for learning the patterns of normal and abnormal state with high-level representation, which is built on top of a introspection system.
* Leveraging the high-level representation transitions to bootstrap the recovery decision making policy learning process of robot with Reinforcement Learning algorithm.

# Ktting Anomaly Dataset
The data set [Ktting Anomaly Dataset](https://github.com/birlrobotics/ktting_anomaly_dataset) which this repo is built on top of captures sensory-motor and video data for anomalous events during the Kitting. The dataset consists of 538 rosbags. 85 of those rosbags are paired with RGB video that was captured by an external camera placed directly in front of the robot. The size of the 538 rosbags is of 37GB whilst the size of all videos is of 3.1GB. (For more information please click [here](https://github.com/birlrobotics/ktting_anomaly_dataset))

# Anomaly Type
In warehouse worker-robot cooperation setting, there are some common anomalies that happen often.

## Human Collision 
<img src="https://github.com/YijiongLin/SPAIR_with_RL/blob/master/case/hc.gif" width="700" height="400" />
<img src="https://github.com/YijiongLin/SPAIR_with_RL/blob/master/case/HC2.gif" width="700" height="400" />


## Object Slip 
<img src="https://github.com/YijiongLin/SPAIR_with_RL/blob/master/case/OS.gif" width="700" height="400" />

## Tool Collision
<img src="https://github.com/YijiongLin/SPAIR_with_RL/blob/master/case/TCtag4.gif" width="700" height="400" />
<img src="https://github.com/YijiongLin/SPAIR_with_RL/blob/master/case/TCtag8.gif" width="700" height="400" />


## Wall Collision
<img src="https://github.com/YijiongLin/SPAIR_with_RL/blob/master/case/WC.gif" width="700" height="400" />

## No Object
<img src="https://github.com/YijiongLin/SPAIR_with_RL/blob/master/case/NO.gif" width="700" height="400" />


# Video
Youtube: https://youtu.be/aoD8lXBLtK0

