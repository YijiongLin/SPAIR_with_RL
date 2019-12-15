# bourne
from smach_based_introspection_framework._constant import (
    SUCCESSULLY_EXECUTED_SKILL,
    UNSUCCESSFULLY_EXECUTED_SKILL,
    ROLLBACK_RECOVERY_TAG,
    RECOVERY_DEMONSTRATED_BY_HUMAN_TAG,
    folder_time_fmt,
    RECOVERY_SKILL_BEGINS_AT,
    experiment_record_folder, 
    dataset_folder,
    latest_dataset_folder,
    anomaly_label_file,
)
import json
import os #for file management make directory
import glob
import rosbag, sys, csv
import time
import string
import os #for file management make directory
import shutil #for file management, copy file
import ipdb
import numpy as np
import logging
import copy
import matplotlib.pyplot as plt
from smach_based_introspection_framework import ExperimentRecord
from collections import defaultdict, deque
transition_tuples_folders = os.path.join(
    latest_dataset_folder,
    'transition_tuples',
)

t_anomaly_tuple_json = os.path.join(
    latest_dataset_folder,
    't_anomaly_tuple.json',
)

with open(t_anomaly_tuple_json, 'r') as f:
    extra_anomaly_tuples = json.load(f)

# t_anomaly_tuple1 = ((7,-2003,),8,-1,(8,-2003,1.0))
# t_anomaly_tuple2 = ((1000,-2001,),5,-1,(5,-2004,2.0))
# t_anomaly_tuple3 = ((4,-2001),5,-1,(5,-2004,2))
# t_anomaly_tuple4 = ((8,-2001,6),9,-1,(9,-2001,2))
# t_anomaly_tuple5 = ((4,-2004,4.0),4,-1,(4,-2004,1.0))
# t_anomaly_tuple6 = ((4,-2004,4.0),3,-0.058,(3,0,3.0))

# t_anomaly_tuple71 = ((3,-2000,1.0),3,-0.058,(3,0,4.0))
# t_anomaly_tuple72 = ((3,-2000,2.0),3,-0.058,(3,0,3.0))
# t_anomaly_tuple72 = ((3,-2000,3.0),3,-0.058,(3,0,3.0))
# t_anomaly_tuple73 = ((3,-2000,4.0),3,-0.058,(3,0,2.0))
# t_anomaly_tuple74 = ((3,-2000,5.0),3,-0.058,(3,0,2.0))
# t_anomaly_tuple75 = ((3,-2000,6.0),4,-0.058,(3,0,2.0))
# t_anomaly_tuple75 = ((3,-2000,7.0),4,-0.058,(4,0,3.0))
# t_anomaly_tuple75 = ((3,-2000,8.0),4,-0.058,(4,0,3.0))
# t_anomaly_tuple8 = ((4,-2004,4.0),3,-0.058,(3,0,3.0))


# extra_anomaly_tuples = []
# extra_anomaly_tuples.append(anomaly_tuple1)
# extra_anomaly_tuples.append(anomaly_tuple2)
# extra_anomaly_tuples.append(anomaly_tuple3)
# extra_anomaly_tuples.append(anomaly_tuple4)
# extra_anomaly_tuples.append(anomaly_tuple5)
# extra_anomaly_tuples.append(anomaly_tuple6)

def get_reward(state,action,next_state,exec_time,is_contain_time):
    anomaly_reward = 0
    skill_reward = 0
    success_terminal_reward = 1000
    if is_contain_time:
        exec_time = next_state[2]
    skill_reward = -(50 +  exec_time)
    if next_state[1] <= -2000:
        anomaly_reward = -50
    
    total_reward = anomaly_reward + skill_reward
    # terminated_state
    if next_state[0] == 9:
        total_reward += success_terminal_reward
    total_reward = total_reward * 0.001
    return float('%.5f' %total_reward)


# Save the exp tuples
output_all_episodes_transitions_path = os.path.join(
    latest_dataset_folder,
    'all_episodes_stime_transitions',
)

if not os.path.exists(output_all_episodes_transitions_path):
    os.makedirs(output_all_episodes_transitions_path)

output_all_episodes_stime_transitions_json = os.path.join(
    output_all_episodes_transitions_path,
    'all_episodes_tuples.json',
)




# ===============Get the row tuples from rosbag.
exp_dirs = [i for i in glob.glob(os.path.join(transition_tuples_folders, '*')) if os.path.isdir(i)]
exp_dirs.sort() 
all_episodes_tuples_list = []
for exp_dir in exp_dirs:
    
        transition_tuples_json = os.path.join(
            exp_dir,
            'episode_tuples.json',
        )
        with open(transition_tuples_json, 'r') as f:
            episode_tuples_list = json.load(f)
            all_episodes_tuples_list.extend(episode_tuples_list)
#===============Compute the rewards, and save as s,a,r,s' tuples. 'is_contain_time' for if consider exec_t as state.
def get_tuples_with_reward(all_episodes_tuples_list,is_contain_time):
    tuples_with_reward = []
    for row_tuple in all_episodes_tuples_list:
        state,act,next_state = row_tuple
        if is_contain_time:
            reward = get_reward(state,act,next_state,0,True)    
        else:
            print('format not right')
            return False
        state = tuple(state)
        next_state = tuple(next_state)
        tuple_with_reward = (state,act,reward,next_state)
        tuples_with_reward.append(tuple_with_reward)
    for _ in range(20):
        for e_a_t in extra_anomaly_tuples:
            state, act,reward, next_state = e_a_t
            state = tuple(state)
            next_state = tuple(next_state)
            tuples_with_reward.append((state, act,reward, next_state))
    return tuples_with_reward

tuples_with_reward = get_tuples_with_reward(all_episodes_tuples_list,True)

with open(output_all_episodes_stime_transitions_json, 'w') as f:
    json.dump(tuples_with_reward,f)