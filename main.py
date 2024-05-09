import roboticstoolbox as rtb
# from roboticstoolbox.backends.swift import Swift
import numpy as np
import spatialgeometry as sg
from spatialmath import SE3, SO3
from point_cloud_manipulability import Point_cloud_Manipulability
from swift import Swift


def home_pos(robot):
    # Move to some initial joint position
    home_q = np.deg2rad([-60, -80, -100, -90, 90, 0])
    robot.q = home_q

    env.step()

    T_base_tcp = robot.fkine(robot.q, end="tool0")  # forward kinematics
    # print(T_base_tcp)
    return T_base_tcp


# Instantiate the graphical environment (Swift) and launch
env = Swift()
env.launch()

# Instantiate a UR5 robot
robot = rtb.models.URDF.UR5()
# robot = rtb.models.URDF.UR10()

input("Press enter to start robot manipulability check")

for y in np.arange(0.5, 0.7, 0.1):
    for x in np.arange(-0.2, 0.3, 0.1):
        # Create an empty list to store manipulability values
        manipulability_values = []

        # Set the new position of the body
        T_base_belly = SE3(x, y, 0)
        print(T_base_belly)

        belly = sg.Mesh(filename="belly.stl", scale=[0.6666, 1.0, 1.0], base=T_base_belly, collision=True)

        env.add(robot)
        T_base_tcp = home_pos(robot)
        env.add(belly)

        point_cloud = Point_cloud_Manipulability()
        point_cloud.load_from_object_file(stl_file_name="belly.stl", obj_translate=[x, y, 0.0], scale_factor=0.6666, num_points=500)
        point_cloud.sample_points_above_z(z_threshold=0.1)

        points = np.asarray(point_cloud.filtered_point_cloud.points)[:10]
        normals = np.asarray(point_cloud.filtered_point_cloud.normals)[:10]

        for i in range(len(points)):
            print("Position: ", points[i])

            T_point = SE3(points[i][0], points[i][1], points[i][2])
            point = sg.Sphere(radius=0.01, pose=T_point, collision = False)
            env.add(point)

            normal = -normals[i] #np.array([0, 1, 0])

            # Compute rotation matrix to align z-axis with surface normal
            z_axis = np.array([0, 0, 1])  # Initial z-axis of the tool frame
            rotation_axis = np.cross(z_axis, normal)
            rotation_angle = np.arccos(np.dot(z_axis, normal))
            rotation_matrix = SO3.Exp(rotation_angle * rotation_axis).A
            
            # Recreate the TCP transformation matrix with the adjusted rotation
            # T_point_tcp = SE3.Rt(T_base_tcp.R, np.array(points[i]))
            # T_point_tcp = SE3.Rt(T_base_tcp.R, [x, y, 0.31])# + 0.15175])
            T_point_tcp = SE3.Rt(rotation_matrix, np.array(points[i]))
            print(T_point_tcp)

            # Inverse Kinematics on robot
            q, success, iter, searches, residual = robot.ik_LM(T_point_tcp, q0=robot.q, end='tool0')
            robot.q = q

            env.step()

            # Check for collisions
            iscollision = robot.iscollided(q=robot.q, shape=belly) # boolean
            print("In collision?: ", iscollision)

            # Check Manipulability
            manipulability = robot.manipulability(robot.q)
            print("Manipulabilty: ", manipulability)

            # Append manipulability value to the list
            manipulability_values.append(manipulability)
            
            input("Press enter to move to next point")

        
        input("Press enter to move to change belly position")
        # Save the NumPy array to a file
        np.savetxt("manipulability_values_" + str(x) + "_" + str(y) + ".txt", np.array(manipulability_values))
        env.reset()

