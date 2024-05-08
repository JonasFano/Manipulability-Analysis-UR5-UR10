import roboticstoolbox as rtb
from roboticstoolbox.backends.swift import Swift
import numpy as np
import spatialgeometry as sg
from spatialmath import SE3, SO3
from point_cloud_manipulability import Point_cloud_Manipulability

# Instantiate the graphical environment (Swift) and launch
env = Swift()
env.launch(realtime=True)

# Instantiate a UR5 robot
robot = rtb.models.URDF.UR5()

env.add(robot)

def home_pos(robot):
    # Move to some initial joint position
    home_q = np.deg2rad([-60, -80, -100, -90, 90, 0])
    robot.q = home_q

T_base_tcp = robot.fkine(robot.q, end="tool0")  # forward kinematics
# print(T_base_tcp)

home_pos(robot)
env.step()

input("Press enter to start robot manipulability check")

for y in np.arange(0.6, 0.8, 0.1):
    for x in np.arange(-0.2, 0.3, 0.1):
        # Set the new position of the body
        new_pos = T_base_belly = SE3(x, y, 0.0)

        belly = sg.Mesh(filename="belly.stl", scale=[0.6666, 1.0, 1.0], base=T_base_belly, collision=True)
        env.add(belly)

        point_cloud = Point_cloud_Manipulability()
        point_cloud.load_from_object_file(stl_file_name="belly.stl", obj_translate=[x, y, 0.15175], scale_factor=0.6666, num_points=500)
        point_cloud.sample_points_above_z(z_threshold=0.15)

        points = np.asarray(point_cloud.filtered_point_cloud.points)[:100]
        normals = np.asarray(point_cloud.filtered_point_cloud.normals)[:100]

        for i in range(len(points)):
            print(points[i])
            
            # Recreate the TCP transformation matrix with the adjusted rotation
            T_point_tcp = SE3.Rt(T_base_tcp.R, np.array(points[i]))

            # Inverse Kinematics on robot
            q, success, iter, searches, residual = robot.ik_LM(T_point_tcp, q0=robot.q, end='tool0')
            robot.q = q

            env.step()

            # Check for collisions
            iscollision = robot.iscollided(q=robot.q, shape=belly) # boolean
            print("In collision?: ", iscollision)

            # Check Manipulability
            print("Manipulabilty: ", robot.manipulability(robot.q))

            input("Press enter to move to next point")

        
        input("Press enter to move to change belly position")
        env.remove(belly)



# input("Press enter to move robot into collision")

# T_base_tcp = robot.fkine(robot.q, end="tool0")  # forward kinematics
# T_base_tcp = T_base_tcp @ SE3(0,0,0.1)
# q, success, iter, searches, residual = robot.ik_LM(T_base_tcp, q0=robot.q, end='tool0')
# robot.q = q

# env.step()
# iscollision = robot.iscollided(q=robot.q, shape=belly) # boolean
# print("In collision?: ", iscollision)

# # Check Manipulability
# print("Manipulabilty: ", robot.manipulability(robot.q))