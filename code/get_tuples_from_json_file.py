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
    'transition_tuples_with_correct_files',
)

t_anomaly_tuple_json = os.path.join(
    latest_dataset_folder,
    'anomaly_tuple.json',
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
    adaptation_reward = 50
    skill_reward = 0
    success_terminal_reward = 1000
    # if action >= 1000:
    #     skill_reward = -(10 +  exec_time)
    # else :
    #     skill_reward = -(10 +  exec_time + adaptation_reward )
    if is_contain_time:
        exec_time = next_state[1]
    skill_reward = -(50 +  exec_time)
    if next_state[1] <= -2000:
        anomaly_reward = -50
    
    total_reward = anomaly_reward + skill_reward
    # terminated_state
    if next_state[0] == 9:
        total_reward += success_terminal_reward
    total_reward = total_reward * 0.001
    return float('%.5f' %total_reward)

def get_ac_name(ac):
    if ac ==0:
        return 'success'
    if ac ==-2000:
        return 'human_collision'
    if ac ==-2001:
        return 'tool_collision'
    if ac ==-2002:
        return 'object_slip'
    if ac ==-2003:
        return 'wall_collision'
    if ac ==-2004:
        return 'no_object'

def get_phase_name(p):
    if p ==0:
        return 'MoveToHomePose'
    if p ==3:
        return 'MoveToPrePickPoseWithEmptyHand'
    if p ==4:
        return 'Pick'
    if p ==5:
        return 'MoveToPrePickPoseWithFullHand'
    if p ==7:
        return 'MoveToPrePlacePoseWithFullHand'
    if p ==8:
        return 'Place'
    if p ==9:
        return 'MoveToPrePlacePoseWithEmptyHand'
    if p ==1000:
        return 'ChangePickPose_1'
    if p ==1001:
        return 'AvoidWallCollision'
    if p ==1002:
        return 'ChangePlacePose_1'
    if p ==1003:
        return 'ChangePickPose_2'

def get_act_name(a):
    if a ==3:
        return 'MoveToPrePickPoseWithEmptyHand'
    if a ==4:
        return 'Pick'
    if a ==5:
        return 'MoveToPrePickPoseWithFullHand'
    if a ==7:
        return 'MoveToPrePlacePoseWithFullHand'
    if a ==8:
        return 'Place'
    if a ==9:
        return 'MoveToPrePlacePoseWithEmptyHand'
    if a ==0:
        return 'ChangePickPose_1'
    if a ==1:
        return 'AvoidWallCollision'
    if a ==2:
        return 'ChangePlacePose_1'
    if a ==6:
        return 'ChangePickPose_2'
# Save the exp tuples
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
        state,act,next_state,exec_t = row_tuple
        if is_contain_time:
            reward = get_reward(state,act,next_state,0,True)    
        else:
            reward = get_reward(state,act,next_state,exec_t,is_contain_time)
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

tuples_with_reward = get_tuples_with_reward(all_episodes_tuples_list,False)

# ===============Compute the rewards, contain the state with execute time, and save as s,a,r,s' tuples.



# ===================Q training
Q = defaultdict(lambda:np.zeros(10))
epoches = 600
GAMMA = 1
ALPHA = 0.01
error_list = []
for epoch in range(epoches) :
    TD_totall_error = 0
    for exp in tuples_with_reward:
        state,act,reward,next_state = exp
        # Change the adaptation act index, otherwise cannot load into dict.
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
        TD_error = target - Q[state][act]
        Q[state][act] = Q[state][act] + (ALPHA * TD_error)
        TD_totall_error += TD_error
    error_list.append(np.mean(TD_totall_error))
    print(epoch)
plt.plot(np.linspace(0,epoches,len(error_list), endpoint = False),np.array(error_list))
plt.xlabel('Episode Number')
plt.ylabel('Average TD_loss over each training Epoch')
plt.show()
print(Q)

# =======================change to Q_table dict for FSM
Q_to_policy = defaultdict(dict)
for state,action_value in Q.items() :
    anomaly_class = state[1]
    ac_n = get_ac_name(anomaly_class)  
  
    phase = state[0]
    phase_n = get_phase_name(phase)

    a_index = np.argmax(action_value)
    act_n = get_act_name(a_index)



    policy_anomaly = {}
    policy_anomaly[ac_n] = act_n
    if phase_n not in Q_to_policy:
        Q_to_policy[phase_n] = []
        Q_to_policy[phase_n].append(policy_anomaly)
    else :
        Q_to_policy[phase_n].append(policy_anomaly)

a =1
