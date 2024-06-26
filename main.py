import roboticstoolbox as rtb
# from roboticstoolbox.backends.swift import Swift
import numpy as np
import spatialgeometry as sg
from spatialmath import SE3, SO3
from point_cloud_manipulability import Point_cloud_Manipulability
from swift import Swift
from tqdm import tqdm
import time

def home_pos(robot):
    # Move to some initial joint position
    # home_q = np.deg2rad([-60, -80, -100, -90, 90, 0])
    home_q = np.deg2rad([-60, -120, -110, -40, 90, 0])
    robot.q = home_q

    env.step()

    T_base_tcp = robot.fkine(robot.q, end="tool0")  # forward kinematics
    # print(T_base_tcp)
    return T_base_tcp


# Instantiate the graphical environment (Swift) and launch
env = Swift()
env.launch()

# # Instantiate a UR5 robot
# robot = rtb.models.URDF.UR5()
# # robot = rtb.models.URDF.UR10()
# T_robot = SE3.Tz(0.3)
# robot.base = T_robot * robot.base # Transform robot base position

# input("Press enter to start robot manipulability check")



# for z in tqdm(np.arange(0.1, 0.5, 0.05), desc="Z Loop", leave = False):
#     robot = rtb.models.URDF.UR5()
#     T_robot = SE3.Tz(z)
#     robot.base = T_robot * robot.base # Transform robot base position

#     for y in tqdm(np.arange(0.3, 0.65, 0.05), desc="Y Loop", leave = False):
#         for x in tqdm(np.arange(-0.1, 0.2, 0.05), desc="X Loop", leave = False):



# for z in tqdm(np.arange(0.3, 0.6, 0.05), desc="Z Loop", leave = False):
#     robot = rtb.models.URDF.UR10()
#     T_robot = SE3.Tz(z)
#     robot.base = T_robot * robot.base # Transform robot base position

#     for y in tqdm(np.arange(0.5, 1.0, 0.05), desc="Y Loop", leave = False):
#         for x in tqdm(np.arange(-0.3, 0.4, 0.05), desc="X Loop", leave = False):


for z in tqdm(np.arange(0.5, 0.52, 0.05), desc="Z Loop", leave = False):
    robot = rtb.models.URDF.UR10()
    T_robot = SE3.Tz(z)
    robot.base = T_robot * robot.base # Transform robot base position

    for y in tqdm(np.arange(0.7, 0.92, 0.05), desc="Y Loop", leave = False):
        for x in tqdm(np.arange(-0.3, -0.28, 0.05), desc="X Loop", leave = False):
            # Create an empty list to store manipulability values
            manipulability_values = []
            success_list = []
            collision_list = []

            # Set the new position of the body
            T_base_belly = SE3(x, y, 0)

            belly = sg.Mesh(filename="belly.stl", scale=[1.0, 1.0, 1.0], base=T_base_belly, collision=True)

            env.add(robot)
            T_base_tcp = home_pos(robot)
            env.add(belly)

            time.sleep(20.0)

            point_cloud = Point_cloud_Manipulability()
            point_cloud.load_from_object_file(stl_file_name="belly.stl", obj_translate=[x, y, 0.0], scale_factor=1, num_points=3500)
            point_cloud.sample_points_above_z(z_threshold=0.15)

            points = np.asarray(point_cloud.filtered_point_cloud.points)
            normals = np.asarray(point_cloud.filtered_point_cloud.normals)

            n = len(points)
            perm = np.random.permutation(n)

            points_shuffeled = points[perm]
            normals_shuffeled = normals[perm]

            points = points_shuffeled[:1000]
            normals = normals_shuffeled[:1000]

            for i in range(len(points)):
                # print("Position: ", points[i])

                # T_point = SE3(points[i][0], points[i][1], points[i][2])
                # point = sg.Sphere(radius=0.01, pose=T_point, collision = False)
                # env.add(point)

                normal = -normals[i] #np.array([0, 1, 0])

                # Compute rotation matrix to align z-axis with surface normal
                z_axis = np.array([0, 0, 1])  # Initial z-axis of the tool frame
                rotation_axis = np.cross(z_axis, normal)
                rotation_angle = np.arccos(np.dot(z_axis, normal))
                rotation_matrix = SO3.AngleAxis(rotation_angle, rotation_axis).A
                
                # Recreate the TCP transformation matrix with the adjusted rotation
                # T_point_tcp = SE3.Rt(T_base_tcp.R, np.array(points[i]))
                # T_point_tcp = SE3.Rt(T_base_tcp.R, [x, y, 0.31])# + 0.15175])
                T_point_tcp = SE3.Rt(rotation_matrix, np.array(points[i]))

                translation = SE3.Tz(-0.15) 
                T_point_tcp = T_point_tcp * translation

                T_point_tcp = SE3.Tz(-z) * T_point_tcp # To account for a different robot base position

                # Inverse Kinematics on robot
                q, success, iter, searches, residual = robot.ik_LM(T_point_tcp, q0=np.deg2rad([-60, -120, -110, -40, 90, 0]), end='tool0')
                robot.q = q

                env.step()

                # Check for collisions
                iscollision = robot.iscollided(q=robot.q, shape=belly) # boolean
                # print("In collision?: ", iscollision)

                # Check Manipulability
                manipulability = robot.manipulability(robot.q)
                # print("Manipulabilty: ", manipulability)

                # Append manipulability value to the list
                manipulability_values.append(manipulability)
                success_list.append(success)
                collision_list.append(iscollision)
                
                #input("Press enter to move to next point")

                # Wait for half a second after each step
                time.sleep(0.5)

            
            #input("Press enter to move to change belly position")
            # Save the NumPy array to a file
            # np.savetxt("data_UR10_v5/manipulability_values_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt", np.array(manipulability_values))
            # np.savetxt("data_UR10_v5/success_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt", np.array(success_list))
            # np.savetxt("data_UR10_v5/collision_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt", np.array(collision_list))
            # env.reset()
