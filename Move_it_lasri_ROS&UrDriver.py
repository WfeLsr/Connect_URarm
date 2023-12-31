#!/usr/bin/env python

import time
import roslib; roslib.load_manifest('ur_driver')
import rospy
import actionlib
from control_msgs.msg import *
from trajectory_msgs.msg import *
from sensor_msgs.msg import JointState
from math import pi
import numpy as np
import scipy
import matplotlib.pyplot as plt
from random import *

JOINT_NAMES = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
               'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']

Q_test = [.6,-1.4,2.5,-2.5,-1.6,2.8]    
Q1 = [0.7,0,-1.57,-1.5,0,0]
Q2 = [1.4,0,-1.57,-1.5,0,0]
Q3 = [2,0,-1.57,-1.5,0,0]
Q4 = [2.6,0,-1.57,-1.5,0,0]
Q5 = [3,0,-1.57,-1.5,0,0]
Q6 = [3.4,0,-1.57,-1.5,0,0]
Q7 = [3.6,0,-1.57,-1.5,0,0]
Q8 = [4.5,0,-1.57,-1.5,0,0]
Q9 = [6,0,-1.57,-1.5,0,0]
client = None
N=10#29256
        #Read the Data :
b = np.loadtxt('trajectoire_cercle_angle.txt', dtype=float)
print ('raw angle data size',np.shape(b)) #175536
#print('raw angle data :',b)
print("\n")        
#print "This program makes the robot move between the following three poses:"
#limite real robot constraint
Q=np.copy(b)
for ii in range(0,N):
 for jj in range(0,6) :
  Q[ii][jj]=Q[ii][jj]+0.17
 #Q[ii][5]=1
 if Q[ii][0] >= 3.1:
    Q[ii][0]=Q[ii-1][0]	
 if Q[ii][0] <= -3.1:
    Q[ii][0]=Q[ii-1][0]	
 
 if Q[ii][5] >= 3.1:
    Q[ii][5]=Q[ii][5]-14.5	
 if Q[ii][5] <= -3.1:
    Q[ii][5]=Q[ii][5]+14.5   
print Q


def move1():
    global joints_pos
    g = FollowJointTrajectoryGoal()
    g.trajectory = JointTrajectory()
    g.trajectory.joint_names = JOINT_NAMES
    try:
        joint_states = rospy.wait_for_message("joint_states", JointState)
        joints_pos = joint_states.position
        g.trajectory.points = [
            JointTrajectoryPoint(positions=joints_pos, velocities=[0]*6, time_from_start=rospy.Duration(0.0)),
            JointTrajectoryPoint(positions=Q1, velocities=[0]*6, time_from_start=rospy.Duration(2.0)),
            JointTrajectoryPoint(positions=Q2, velocities=[0]*6, time_from_start=rospy.Duration(3.0)),
            JointTrajectoryPoint(positions=Q3, velocities=[0]*6, time_from_start=rospy.Duration(4.0))]
        client.send_goal(g)
        client.wait_for_result()
    except KeyboardInterrupt:
        client.cancel_goal()
        raise
    except:
        raise

def movecercle():
    global joints_pos
    g = FollowJointTrajectoryGoal()
    g.trajectory = JointTrajectory()
    g.trajectory.joint_names = JOINT_NAMES
    try:
        joint_states = rospy.wait_for_message("joint_states", JointState)
        joints_pos = joint_states.position
        g.trajectory.points = [JointTrajectoryPoint(positions=joints_pos, velocities=[0]*6, time_from_start=rospy.Duration(0.0))]
        d= 2.0

        for i in range(N):
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=Q[i], velocities=[0]*6, time_from_start=rospy.Duration(d)))
            d += 1.
                     
        client.send_goal(g)
        client.wait_for_result()
    except KeyboardInterrupt:
        client.cancel_goal()
        raise
    except:
        raise        

def move_disordered():
    order = [4, 2, 3, 1, 5, 0]
    g = FollowJointTrajectoryGoal()
    g.trajectory = JointTrajectory()
    g.trajectory.joint_names = [JOINT_NAMES[i] for i in order]
    q1 = [Q1[i] for i in order]
    q2 = [Q2[i] for i in order]
    q3 = [Q3[i] for i in order]
    try:
        joint_states = rospy.wait_for_message("joint_states", JointState)
        joints_pos = joint_states.position
        g.trajectory.points = [
            JointTrajectoryPoint(positions=joints_pos, velocities=[0]*6, time_from_start=rospy.Duration(0.0)),
            JointTrajectoryPoint(positions=q1, velocities=[0]*6, time_from_start=rospy.Duration(2.0)),
            JointTrajectoryPoint(positions=q2, velocities=[0]*6, time_from_start=rospy.Duration(3.0)),
            JointTrajectoryPoint(positions=q3, velocities=[0]*6, time_from_start=rospy.Duration(4.0))]
        client.send_goal(g)
        client.wait_for_result()
    except KeyboardInterrupt:
        client.cancel_goal()
        raise
    except:
        raise
    
def move_repeated():
    g = FollowJointTrajectoryGoal()
    g.trajectory = JointTrajectory()
    g.trajectory.joint_names = JOINT_NAMES
    try:
        joint_states = rospy.wait_for_message("joint_states", JointState)
        joints_pos = joint_states.position
        d = 2.0
        g.trajectory.points = [JointTrajectoryPoint(positions=joints_pos, velocities=[0]*6, time_from_start=rospy.Duration(0.0))]
        for i in range(10):
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=Q1, velocities=[0]*6, time_from_start=rospy.Duration(d)))
            d += 1
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=Q2, velocities=[0]*6, time_from_start=rospy.Duration(d)))
            d += 1
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=Q3, velocities=[0]*6, time_from_start=rospy.Duration(d)))
            d += 1
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=Q4, velocities=[0]*6, time_from_start=rospy.Duration(d)))
            d += 1
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=Q5, velocities=[0]*6, time_from_start=rospy.Duration(d)))
            d += 1
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=Q6, velocities=[0]*6, time_from_start=rospy.Duration(d)))
            d += 1
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=Q7, velocities=[0]*6, time_from_start=rospy.Duration(d)))            
            d += 1
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=Q8, velocities=[0]*6, time_from_start=rospy.Duration(d)))            
            d += 1
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=Q9, velocities=[0]*6, time_from_start=rospy.Duration(d)))            
            d += 2
        client.send_goal(g)
        client.wait_for_result()
    except KeyboardInterrupt:
        client.cancel_goal() # suddenly stop the robot such as an emrgency stop use client.cancel_goal(g)
        raise
    except:
        raise

def move_interrupt():
    g = FollowJointTrajectoryGoal()
    g.trajectory = JointTrajectory()
    g.trajectory.joint_names = JOINT_NAMES
    try:
        joint_states = rospy.wait_for_message("joint_states", JointState)
        joints_pos = joint_states.position
        g.trajectory.points = [
            JointTrajectoryPoint(positions=joints_pos, velocities=[0]*6, time_from_start=rospy.Duration(0.0)),
            JointTrajectoryPoint(positions=Q1, velocities=[0]*6, time_from_start=rospy.Duration(2.0)),
            JointTrajectoryPoint(positions=Q2, velocities=[0]*6, time_from_start=rospy.Duration(3.0)),
            JointTrajectoryPoint(positions=Q3, velocities=[0]*6, time_from_start=rospy.Duration(4.0))]
    
        client.send_goal(g)
        time.sleep(3.0)
        print "Interrupting"
        joint_states = rospy.wait_for_message("joint_states", JointState)
        joints_pos = joint_states.position
        g.trajectory.points = [
            JointTrajectoryPoint(positions=joints_pos, velocities=[0]*6, time_from_start=rospy.Duration(0.0)),
            JointTrajectoryPoint(positions=Q1, velocities=[0]*6, time_from_start=rospy.Duration(2.0)),
            JointTrajectoryPoint(positions=Q2, velocities=[0]*6, time_from_start=rospy.Duration(3.0)),
            JointTrajectoryPoint(positions=Q3, velocities=[0]*6, time_from_start=rospy.Duration(4.0))]
        client.send_goal(g)
        client.wait_for_result()
    except KeyboardInterrupt:
        client.cancel_goal()
        raise
    except:
        raise
   
def main():
    global client
    try:
        rospy.init_node("test_move", anonymous=True, disable_signals=True)
        client = actionlib.SimpleActionClient('follow_joint_trajectory', FollowJointTrajectoryAction)
        print "Waiting for server..."
        client.wait_for_server()
        print "Connected to server"
        parameters = rospy.get_param(None)
        index = str(parameters).find('prefix')
        if (index > 0):
            prefix = str(parameters)[index+len("prefix': '"):(index+len("prefix': '")+str(parameters)[index+len("prefix': '"):-1].find("'"))]
            for i, name in enumerate(JOINT_NAMES):
                JOINT_NAMES[i] = prefix + name
        
        #Read the Data :
        b = np.loadtxt('trajectoire_cercle_angle.txt', dtype=float)
		print ('raw angle data size',np.shape(b)) #175536
		#print('raw angle data :',b)
		print("\n")
		t = np.loadtxt('trajectoire_cercle_time.txt', dtype=float)
		print ('raw angle data size',np.shape(t))  #4876
		#print('raw angle data :',b)
        print("\n")

		#print('size extract data', np.shape(a1))
        
        print "This program makes the robot move between the following three poses:"

        for ii in range(0,N):
          print Q[ii]
          print('\n')
        
        print "Please make sure that your robot can move freely between these poses before proceeding!"
        inp = raw_input("Continue? y/n: ")[0]
        
        if (inp == 'y'):
            move1()
            #move_repeated()
            #movecercle()
            #move_disordered()
            #move_interrupt()
        else:
            print "Halting program"
    except KeyboardInterrupt:
        rospy.signal_shutdown("KeyboardInterrupt")
        raise

if __name__ == '__main__': main()
