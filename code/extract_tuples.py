'''
This script saves each topic in a bagfile as a csv.

Accepts a filename as an optional argument. Operates on all bagfiles in current directory if no argument provided

Written by Nick Speal in May 2013 at McGill University's Aerospace Mechatronics Laboratory
www.speal.ca

Supervised by Professor Inna Sharf, Professor Meyer Nahon 

'''

import rosbag, sys, csv
import time
import string
import os #for file management make directory
import shutil #for file management, copy file
import ipdb
import numpy as np
#verify correct input arguments: 1 or 2

with open('anomaly_labels.txt',"r") as f:
	anomaly_labels = f.read()
anomaly_labels_list = string.split(anomaly_labels,'\n')
anomaly_labels_indexes_list = []

for anomaly_label in anomaly_labels_list:
	if anomaly_label == 'human_collision':
		anomaly_label = -2000
	if anomaly_label == 'tool_collision':
		anomaly_label = -2001
	if anomaly_label == 'object_slip':
		anomaly_label = -2002
	if anomaly_label == 'wall_collision':
		anomaly_label = -2003
	anomaly_labels_indexes_list.append(anomaly_label)
anomaly_labels_indexes_list.remove('')
# reverse for pop out
anomaly_labels_indexes_list.reverse()

if (len(sys.argv) > 2):
	print "invalid number of arguments:   " + str(len(sys.argv))
	print "should be 2: 'bag2csv.py' and 'bagName'"
	print "or just 1  : 'bag2csv.py'"
	sys.exit(1)
elif (len(sys.argv) == 2):
	listOfBagFiles = [sys.argv[1]]
	numberOfFiles = "1"
	print "reading only 1 bagfile: " + str(listOfBagFiles[0])
elif (len(sys.argv) == 1):
	listOfBagFiles = []
	fs = os.listdir(".")
	for f in fs :
		if f[-4:] == ".bag":
			listOfBagFiles.append(f)
	# listOfBagFiles = [f for f in os.listdir(".") if f[-4:] == ".bag"]	#get list of only bag files in current dir.
	numberOfFiles = str(len(listOfBagFiles))
	print "reading all " + numberOfFiles + " bagfiles in current directory: \n"
	for f in listOfBagFiles:
		print f
	print "\n press ctrl+c in the next 10 seconds to cancel \n"
	time.sleep(10)
else:
	print "bad argument(s): " + str(sys.argv)	#shouldnt really come up
	sys.exit(1)

count = 0
for bagFile in listOfBagFiles:
	count += 1
	print "reading file " + str(count) + " of  " + numberOfFiles + ": " + bagFile
	#access bag
	bag = rosbag.Bag(bagFile)
	bagContents = bag.read_messages()
	bagName = bag.filename


	#create a new directory
	folder = string.rstrip(bagName, ".bag")
	try:	#else already exists
		os.makedirs(folder)
	except:
		pass
	shutil.copyfile(bagName, folder + '/' + bagName)


	#get list of topics from the bag
	listOfTopics = []
	for topic, msg, t in bagContents:
		if topic not in listOfTopics:
			listOfTopics.append(topic)


	state = np.array((0,0))
	next_state = np.array((0,0))
	tuple_next_phase_recorded = False
	consider_anomaly_tag = False
	norminal = 0
	exp_tuples_list = []
	recordtopic = '/tag_multimodal'


	for topicName in listOfTopics:
		if topicName == recordtopic:
			#Create a new CSV file for each topic
			for subtopic, msg, t in bag.read_messages(topicName):	# for each instant in time that has data for topicName
				#parse data from this instant, which is of the form of multiple lines of "Name: value\n"
				#	- put it in the form of a list of 2-element lists
				msgString = str(msg)
				msgList = string.split(msgString, '\n')
				rowmsg = {}
				for nameValuePair in msgList:
					splitPair = string.split(nameValuePair, ':')
					if splitPair[0] == 'tag':
						splitPair[1] = string.replace(splitPair[1],' ','')
						rowmsg[splitPair[0]] = int(splitPair[1])
					else:
						rowmsg[splitPair[0]] = splitPair[1]

				if rowmsg['tag'] !=0 and next_state[0] != rowmsg['tag']:
					if consider_anomaly_tag==False and rowmsg['tag'] < 0:
						continue
					# record the state.phase
					if rowmsg['tag'] > 0 and tuple_next_phase_recorded == False:
						act = rowmsg['tag']
						next_state = np.array((0,0))
						next_state[0] = rowmsg['tag']
						tuple_next_phase_recorded = True
						consider_anomaly_tag = True
						continue
					else :
						# record the state.anomaly_condition
						if rowmsg['tag'] >0:
							# no anomaly happened when executing
							next_state[1] = norminal
						elif rowmsg['tag'] < 0:
							# Anomaly happened when executing
							next_state[1] =anomaly_labels_indexes_list.pop()
							consider_anomaly_tag = False
						exp_tuple = (state,act,next_state)
						exp_tuples_list.append(exp_tuple)
						state = np.array((0,0))
						state = next_state
						if np.all(next_state == np.array((9,0))):
							# Reset an episode
							state = np.array((0,0))
						tuple_next_phase_recorded = False

			exp_tuple = (state,act,next_state)
			exp_tuples_list.append(exp_tuple)
			print(exp_tuples_list)
	bag.close()
print "Done reading all " + numberOfFiles + " bag files."



