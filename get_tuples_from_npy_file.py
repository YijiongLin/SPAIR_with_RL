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
from smach_based_introspection_framework import ExperimentRecord
from collections import defaultdict, deque
transition_tuples_folders = os.path.join(
    latest_dataset_folder,
    'transition_tuples',
)


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

# output_all_episodes_transitions_path = os.path.join(
#     latest_dataset_folder,
#     'all_episodes_transitions',
# )
# output_all_episodes_transitions_npy = os.path.join(
#     output_all_episodes_transitions_path,
#     'all_episodes_tuples.npy',
# )
# output_all_episodes_transitions_json = os.path.join(
#     output_all_episodes_transitions_path,
#     'all_episodes_tuples.json',
# )

# with open(output_all_episodes_transitions_npy, 'w') as f:
#     np.save(output_all_episodes_transitions_npy,all_episodes_tuples_list)

# with open(output_all_episodes_transitions_json, 'w') as f:
#     json.dump(all_episodes_tuples_list,f)

    
# ===================Q traning
Q = defaultdict(lambda:np.zeros(10))
epoches = 10000
GAMMA = 1
ALPHA = 0.01
for epoch in range(epoches) :
    for exp in all_episodes_tuples_list:
        state,act,reward,next_state = exp
        state = tuple(state)
        next_state = tuple(next_state)
        if act == 1000:
            act = 0
        if act == 1001:
            act = 1
        if act == 1002:
            act = 2
        if act == 1003:
            act = 6
        Q_next = np.max(Q[next_state]) if next_state[0] != 9 else 0
        target = reward + GAMMA * Q_next
        Q[state][act] = Q[state][act] + (ALPHA * (target - Q[state][act]))
    print(epoch)
print(Q)
