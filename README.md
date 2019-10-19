# SPAIR_with_Reinforcement_Learning
 
This is a repo built on top of [smach_based_introspection_framework](https://github.com/birlrobotics/smach_based_introspection_framework), aiming to endow the robot with the ability of recovery decision making with life-long self-learning.

# Introduction
* Exploiting Dynamic Motion Planning (DMP) method to train the robot with high-level skills (normal kitting skills and recovering skills).
* Gathering and cleaning the multimodal sensery data (tactile sensor, force/torque sensor, camera, joint velocities, joint positions) in the robot kitting task, for learning the patterns of normal and abnormal state with high-level representation, which is built on top of a introspection system.
* Leveraging the high-level representation transitions to bootstrap the recovery decision making policy learning process of robot with Reinforcment Learning algorithm.

# Anomaly Type
In warehouse worker-robot cooperation setting, there are some common anomalies that happen offen.

[image1]: https://github.com/YijiongLin/SPAIR_with_RL/blob/master/hc.gif "human collision"


Youtube: https://youtu.be/aoD8lXBLtK0

