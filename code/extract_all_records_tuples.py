# bourne

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
#verify correct input arguments: 1 or 2

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

# ==============incorrect files folders path===============================
output_all_incorrect_file_path = os.path.join(
    latest_dataset_folder,
    'all_incorrect_files',
)
# different with 'have_anomaly_tag_without_label', this one has word 'unlabeled' in the anomaly.txt
output_unlabeled_file_path = os.path.join(
    output_all_incorrect_file_path,
    'unlabeled_file_folder',
)

output_no_tag9_file_path = os.path.join(
    output_all_incorrect_file_path,
    'no_tag9_file_folder',
)
output_false_positive_file = os.path.join(
    output_all_incorrect_file_path,
    'false_positive_file_folder',
)
output_no_nominal_tag_is_recorded_file = os.path.join(
    output_all_incorrect_file_path,
    'No_nominal_tag_is_recorded_folder',
)

output_have_anomaly_tag_without_label_file = os.path.join(
    output_all_incorrect_file_path,
    'have_anomaly_tag_without_label',
)

output_unknown_label_file_path = os.path.join(
    output_all_incorrect_file_path,
    'unknown_label',
)


# =============================================

# ==============correct files folder path===============================
output_all_correct_file_path = os.path.join(
    latest_dataset_folder,
    'all_correct_files',
)

if not os.path.isdir(output_all_correct_file_path):
    os.makedirs(output_all_correct_file_path)
    
# =============================================

logger = logging.getLogger()
exp_dirs = [i for i in glob.glob(os.path.join(experiment_record_folder, '*')) if os.path.isdir(i)]
# SORTING IS CRITICAL, 
# we have to process experiments in temporal order
# otherwise recovery tag assignments will crash
exp_dirs.sort() 


# =============================================
# If exist all_episodes_tuples_list file, read it, ortherwise create a new one
output_all_episodes_transitions_path = os.path.join(
    latest_dataset_folder,
    'all_episodes_transitions',
)
output_all_episodes_transitions_npy = os.path.join(
    output_all_episodes_transitions_path,
    'all_episodes_tuples.npy',
)
output_all_episodes_transitions_json = os.path.join(
    output_all_episodes_transitions_path,
    'all_episodes_tuples.json',
)
if not os.path.exists(output_all_episodes_transitions_json):
    if not os.path.isdir(output_all_episodes_transitions_path):
        os.makedirs(output_all_episodes_transitions_path)
    all_episodes_tuples_list = []
else:
    all_episodes_tuples_list = json.load(open(output_all_episodes_transitions_json, 'r'))
# =============================================



for count, exp_dir in enumerate(exp_dirs): 
    #=================== Create files for extracted transition tuples from correct record.

    output_transitions_path = os.path.join(
        latest_dataset_folder,
        'transition_tuples',
        '%s'%(os.path.basename(exp_dir)),
    )
    if not os.path.isdir(output_transitions_path):
        os.makedirs(output_transitions_path)
        print("Extracting no.%s rosbag"%count)
        logger.debug("Extracting no.%s rosbag"%count)
    else :
        print("Rosbag in %s had been extracted, and skip this rosbag."%exp_dir)
        logger.debug("Rosbag in %s had been extracted, and skip this rosbag."%exp_dir)
        continue

    er = ExperimentRecord(exp_dir)
    # Extract the tuples
    episode_tuples_list = er.extract_episode_tuples_for_q_table

    #=================== Some error may occur when extracting, due to incorrect record rosbag, and save it to seperate folder
    if episode_tuples_list == 'No_anomaly_label_with_tag_-1':
        output_have_anomaly_tag_without_label_file_folder = os.path.join(
            output_have_anomaly_tag_without_label_file,
            exp_dir[-34:],
        )
        if not os.path.isdir(output_have_anomaly_tag_without_label_file_folder):
            shutil.copytree(exp_dir,output_have_anomaly_tag_without_label_file_folder)
            print("This file have No_anomaly_label_with_tag_-1, and will skip this rosbag:%s"%exp_dir)
            logger.error("This file have No_anomaly_label_with_tag_-1, and will skip this rosbag:%s"%exp_dir)
        continue
        
    elif episode_tuples_list == 'No_nominal_tag_is_recorded':

        output_no_nominal_tag_is_recorded_file_folder = os.path.join(
            output_no_nominal_tag_is_recorded_file,
            exp_dir[-34:],
        )
        if not os.path.isdir(output_no_nominal_tag_is_recorded_file_folder):
            shutil.copytree(exp_dir,output_no_nominal_tag_is_recorded_file_folder)
            print("This file has No nominal tag, and will skip this rosbag:%s"%exp_dir)
            logger.error("This file has No nominal tag, and will skip this rosbag:%s"%exp_dir)
        continue
    elif episode_tuples_list == 'false_positive':

        output_false_positive_file_folder = os.path.join(
            output_false_positive_file,
            exp_dir[-34:],
        )
        if not os.path.isdir(output_false_positive_file_folder):
            shutil.copytree(exp_dir,output_false_positive_file_folder)
            print("This file contains false_positive, and will skip this rosbag:%s"%exp_dir)
            logger.error("This file contains false_positive, and will skip this rosbag:%s"%exp_dir)
        continue
    elif episode_tuples_list=='Unlabeled':
        output_unlabeled_file_path_folder = os.path.join(
            output_unlabeled_file_path,
            exp_dir[-34:],
        )
        if not os.path.isdir(output_unlabeled_file_path_folder):
            shutil.copytree(exp_dir,output_unlabeled_file_path_folder)
            print("This rosbag does not be labeled, and will skip this rosbag:%s"%exp_dir)
            logger.error("This rosbag does not be labeled, and will skip this rosbag:%s"%exp_dir)
        continue
    elif episode_tuples_list=='no_tag_9':
        output_no_tag9_file_path_folder = os.path.join(
            output_no_tag9_file_path,
            exp_dir[-34:],
        )
        if not os.path.isdir(output_no_tag9_file_path_folder):
            shutil.copytree(exp_dir,output_no_tag9_file_path_folder)
            print("This rosbag does not finish, and will skip this rosbag:%s"%exp_dir)
            logger.error("This rosbag does not finish, and will skip this rosbag:%s"%exp_dir)
        continue   
    elif episode_tuples_list=='unknown_label':
        output_unknown_label_file_path_folder = os.path.join(
            output_unknown_label_file_path,
            exp_dir[-34:],
        )
        if not os.path.isdir(output_unknown_label_file_path_folder):
            shutil.copytree(exp_dir,output_unknown_label_file_path_folder)
            print("This rosbag contains unknown lables, and will skip this rosbag:%s"%exp_dir)
            logger.error("This rosbag contains unknown lables, and will skip this rosbag:%s"%exp_dir)
        continue   
    #=====================================


    #==================output the data of correct files===================
    output_transitions_npy = os.path.join(
        output_transitions_path,
        'episode_tuples.npy',
    )
    output_transitions_json = os.path.join(
        output_transitions_path,
        'episode_tuples.json',
    )

    with open(output_transitions_npy, 'w') as f:
        np.save(output_transitions_npy,episode_tuples_list)

    with open(output_transitions_json, 'w') as f:
        json.dump(episode_tuples_list,f)
    
    print("No.%s rosbag done"%count)
    logger.debug("No.%s rosbag done"%count)
    all_episodes_tuples_list.extend(episode_tuples_list)
    # seperate the correct rosbag files 
    output_all_correct_file_path_folder = os.path.join(
        output_all_correct_file_path,
        exp_dir[-34:],
    )

    if not os.path.isdir(output_all_correct_file_path_folder):
        shutil.copytree(exp_dir,output_all_correct_file_path_folder)
        print("copy file to %s"%output_all_correct_file_path_folder)
        logger.debug("copy file to %s"%output_all_correct_file_path_folder)
    # ===============================================


# recording all episodes tuple
with open(output_all_episodes_transitions_npy, 'w') as f:
    np.save(output_all_episodes_transitions_npy,all_episodes_tuples_list)

with open(output_all_episodes_transitions_json, 'w') as f:
    json.dump(all_episodes_tuples_list,f)

print("All episodes finished extracted tuples.")
logger.debug("All episodes finished extracted tuples.")


