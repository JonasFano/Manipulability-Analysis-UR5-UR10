import roboticstoolbox as rtb
from roboticstoolbox.backends.swift import Swift
import numpy as np
import spatialgeometry as sg
from spatialmath import SE3, SO3


# Instantiate the graphical environment (Swift)
env = Swift()

# Instantiate a UR5 robot
robot = rtb.models.URDF.UR5()
# Move to some initial joint position
q1 = np.deg2rad([-150, 0, -90, 0, 90, 0])
robot.q = q1

# Inverse Kinematics on robot
T_base_tcp = SE3.Rt(SO3.Ry(np.pi), np.array([0.4, 0.1, 0.4]))
q, success, iter, searches, residual = robot.ik_LM(T_base_tcp, q0=robot.q, end='tool0')
robot.q = q

# Create a sphere object to represent the belly
T_base_belly = SE3(0.5, 0, 0.2)
belly = sg.Sphere(radius=0.2, pose=T_base_belly, collision = True)

# Check for collisions
iscollision = robot.iscollided(q=robot.q, shape=belly) # boolean
print("In collision?: ", iscollision)

# Launch the environment (Swift)
env.launch()
env.add(robot)
env.add(belly)

input("Press enter to move robot into collision")

T_base_tcp = robot.fkine(robot.q, end="tool0")  # forward kinematics
T_base_tcp = T_base_tcp @ SE3(0,0,0.1)
q, success, iter, searches, residual = robot.ik_LM(T_base_tcp, q0=robot.q, end='tool0')
robot.q = q

env.step()
iscollision = robot.iscollided(q=robot.q, shape=belly) # boolean
print("In collision?: ", iscollision)

# Check Manipulability
print("Manipulabilty: ", robot.manipulability(robot.q))
